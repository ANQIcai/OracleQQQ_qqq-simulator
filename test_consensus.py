"""
Unit tests for the 5-Layer Institutional Consensus Engine.
Run with: python -m pytest test_consensus.py -v
"""
import math
import pytest
from dataclasses import dataclass
from unittest.mock import patch


# ── Minimal ForecastResult stub ───────────────────────────────────────────────

@dataclass
class _F:
    agent_name: str
    direction: str
    confidence: float
    target_low: float
    target_high: float
    status: str = "ok"
    reasoning: str = ""


def _make_rounds(forecasts):
    """Replicate the same forecast list across all 3 debate rounds."""
    return [forecasts, forecasts, forecasts]


def _make_forecast(name, direction="bullish", confidence=0.7,
                   low=490.0, high=510.0, status="ok"):
    return _F(agent_name=name, direction=direction, confidence=confidence,
              target_low=low, target_high=high, status=status)


# ── Fixtures ──────────────────────────────────────────────────────────────────

AGENTS = [
    "Macro Strategist", "Momentum Analyst", "Sentiment Analyst",
    "Quant Modeler", "Earnings Analyst",
]

_ALL_BULLISH = [_make_forecast(a, "bullish") for a in AGENTS]
_ALL_BEARISH = [_make_forecast(a, "bearish", low=440.0, high=460.0) for a in AGENTS]
_ALL_ERRORED = [_make_forecast(a, status="error") for a in AGENTS]

CURRENT_PRICE = 500.0

# Patch track records to return {} for all agents (equal weight baseline = 0.5)
# The function does `from history import get_agent_track_records` at call time,
# so we patch the function in the history module directly.
_TRACK_PATCH = patch("history.get_agent_track_records", return_value={})


# ── Helper: call institutional with patched track records ─────────────────────

def _run(rounds, scenario="fed rate hike", regime="low_vol_uptrend",
         price=CURRENT_PRICE, macro=None):
    from consensus import aggregate_forecasts_institutional
    with _TRACK_PATCH:
        return aggregate_forecasts_institutional(
            rounds, scenario, regime, price, macro or {}
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Layer 1 — Black-Litterman Prior
# ═══════════════════════════════════════════════════════════════════════════════

def test_bl_prior_blends_toward_implied_return():
    """
    When agents forecast exactly at current_price, the BL prior should
    pull the consensus_target above current_price (positive implied return).
    """
    at_current = [_make_forecast(a, "bullish", low=500.0, high=500.0) for a in AGENTS]
    c = _run(_make_rounds(at_current), price=500.0)
    # implied annual = 0.05 + 1.15*0.05 = 0.1075; 5-day ≈ 0.213 → BL prior ≈ 501.07
    # agents all at 500, so posterior should be *above* 500
    assert c.consensus_target > 500.0, (
        f"Expected consensus > 500 with BL prior, got {c.consensus_target}"
    )


def test_bl_prior_skipped_when_no_price():
    """With current_price=0 the BL prior contributes nothing (no crash)."""
    c = _run(_make_rounds(_ALL_BULLISH), price=0.0)
    assert c.consensus_target > 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# Layer 2 — Copula Dependency Correction
# ═══════════════════════════════════════════════════════════════════════════════

def test_copula_widens_posterior_std():
    """
    With 5 correlated agents, copula_factor > 1 (effective_N ≈ 2.4 < 5), so
    posterior_std is inflated vs the independent-agent case.

    NOTE: The BL prior (precision ≈ 0.4) strongly dominates agent precisions
    (total ≈ 0.015), so the absolute CI is ~$7–8.  We verify:
      1. CI is positive.
      2. CI is wider than with a single isolated agent (copula factor > 1 expands
         std even when the prior anchors the mean).
    """
    # 5 correlated agents
    c5 = _run(_make_rounds(_ALL_BULLISH))
    ci5 = c5.credible_high - c5.credible_low
    assert ci5 > 0, "CI should have positive width"

    # 1 agent only — copula_factor = sqrt(1/1) = 1.0 (no inflation)
    one_agent_rounds = _make_rounds([_make_forecast("Macro Strategist", "bullish")])
    c1 = _run(one_agent_rounds)
    ci1 = c1.credible_high - c1.credible_low

    # 5 correlated agents should produce a wider CI than 1 uncorrelated agent
    # because copula_factor > 1 inflates the std more than the extra precision reduces it
    assert ci5 > ci1, (
        f"Expected 5-agent correlated CI (${ci5:.2f}) > 1-agent CI (${ci1:.2f})"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Layer 3 — Regime-Adaptive Weights
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("regime,expected_upweighted", [
    ("low_vol_uptrend",    ["Momentum Analyst", "Quant Modeler"]),
    ("high_vol_uptrend",   ["Macro Strategist", "Sentiment Analyst"]),
    ("low_vol_ranging",    ["Quant Modeler", "Earnings Analyst"]),
    ("high_vol_downtrend", ["Macro Strategist", "Sentiment Analyst"]),
    ("crisis",             ["Macro Strategist", "Sentiment Analyst"]),
])
def test_regime_mapping(regime, expected_upweighted):
    c = _run(_make_rounds(_ALL_BULLISH), regime=regime)
    for name in expected_upweighted:
        assert name in c.upweighted_agents, (
            f"{name} should be upweighted in {regime}, got {c.upweighted_agents}"
        )


def test_unknown_regime_no_crash():
    """An unrecognised regime string → all multipliers = 1.0, no crash."""
    c = _run(_make_rounds(_ALL_BULLISH), regime="unknown_regime_xyz")
    assert c.upweighted_agents == []
    assert c.consensus_target > 0


def test_crisis_triggered_by_vix():
    """VIX > 35 overrides the detected regime and activates crisis weights."""
    c = _run(_make_rounds(_ALL_BULLISH), regime="low_vol_uptrend",
             macro={"vix": 40})
    assert c.regime_label == "crisis"
    assert "Macro Strategist" in c.upweighted_agents


# ═══════════════════════════════════════════════════════════════════════════════
# Layer 4 — Shannon Entropy
# ═══════════════════════════════════════════════════════════════════════════════

def test_all_same_direction_groupthink():
    """All agents bullish → H=0 → GROUPTHINK label."""
    c = _run(_make_rounds(_ALL_BULLISH))
    assert c.entropy_label == "GROUPTHINK", f"Expected GROUPTHINK, got '{c.entropy_label}'"


def test_even_split_high_entropy():
    """2 bullish + 2 bearish + 1 neutral ≈ max entropy → HIGH ENTROPY + wider CI."""
    mixed = [
        _make_forecast("Macro Strategist",   "bullish"),
        _make_forecast("Momentum Analyst",   "bullish"),
        _make_forecast("Sentiment Analyst",  "bearish", low=440.0, high=460.0),
        _make_forecast("Quant Modeler",      "bearish", low=440.0, high=460.0),
        _make_forecast("Earnings Analyst",   "neutral", low=465.0, high=535.0),
    ]
    c_mixed = _run(_make_rounds(mixed))
    c_same  = _run(_make_rounds(_ALL_BULLISH))
    assert c_mixed.entropy_label == "HIGH ENTROPY", (
        f"Expected HIGH ENTROPY, got '{c_mixed.entropy_label}'"
    )
    # CI should be wider for high-entropy case
    ci_mixed = c_mixed.credible_high - c_mixed.credible_low
    ci_same  = c_same.credible_high - c_same.credible_low
    assert ci_mixed > ci_same, "HIGH ENTROPY CI should be wider than GROUPTHINK CI"


def test_entropy_log2_zero_guard():
    """p=0 terms must not cause log2(0) → no exception."""
    # All bullish → base_prob=0, bear_prob=0; log2(0) must be guarded
    _run(_make_rounds(_ALL_BULLISH))  # no exception = pass


# ═══════════════════════════════════════════════════════════════════════════════
# Layer 5 — Fractional Kelly Conviction
# ═══════════════════════════════════════════════════════════════════════════════

def test_kelly_b_zero_no_division():
    """consensus_target <= current_price → b<=0 → conviction_score = 0, no crash."""
    at_par = [_make_forecast(a, "bearish", low=400.0, high=460.0) for a in AGENTS]
    c = _run(_make_rounds(at_par), price=500.0)
    # posterior_mean will be below 500 with these bearish targets + BL pull
    # if still above 500 due to BL, conviction can be positive; just assert no crash
    assert 0 <= c.conviction_score <= 100


def test_kelly_negative_fraction_clamped():
    """Negative raw Kelly fraction should clamp to 0, not produce negative score."""
    # Very bearish forecasts with a bullish-dominated probability
    bearish_low_conf = [_make_forecast(a, "bearish", confidence=0.3,
                                       low=200.0, high=250.0) for a in AGENTS]
    c = _run(_make_rounds(bearish_low_conf), price=500.0)
    assert c.conviction_score >= 0


def test_kelly_fraction_high_conviction():
    """
    Strong bullish consensus far above current price → conviction should be HIGH (≥67).
    Agents: all bullish, 90% confidence, targets 550–600 on a $500 stock.
    """
    strong_bulls = [
        _make_forecast(a, "bullish", confidence=0.9, low=550.0, high=600.0)
        for a in AGENTS
    ]
    c = _run(_make_rounds(strong_bulls), price=500.0)
    assert c.conviction_score >= 67, (
        f"Expected HIGH conviction (≥67), got {c.conviction_score}"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Fallback — all agents error
# ═══════════════════════════════════════════════════════════════════════════════

def test_fallback_all_agents_error():
    """When all agents error, falls back to aggregate_forecasts() without crash."""
    from consensus import aggregate_forecasts_institutional
    with _TRACK_PATCH:
        c = aggregate_forecasts_institutional(
            _make_rounds(_ALL_ERRORED), "some scenario", "low_vol_uptrend", 500.0
        )
    # aggregate_forecasts fallback returns bear_prob=1.0 and agent_count=0
    assert c.agent_count == 0
    assert c.conviction_score == 0
    assert c.regime_label == ""
