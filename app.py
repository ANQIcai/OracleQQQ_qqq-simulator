import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="QQQ Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📈",
)

# ── Dark terminal CSS ──────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [data-testid="stApp"] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d !important;
    padding-top: 1.5rem !important;
}
[data-testid="stSidebarContent"] {
    padding: 0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1rem !important;
}
[data-testid="stSidebar"] hr {
    margin: 0.75rem 0 !important;
    border-color: #30363d !important;
}
/* Sidebar vertical block gap: let section spacing be explicit via HTML, not Streamlit gap */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 10px !important; }
[data-testid="stSidebar"] .stMarkdown { margin-bottom: 0 !important; }
[data-testid="stSidebar"] .stTextArea { margin-bottom: 0 !important; }
[data-testid="stSidebar"] .stButton { margin-top: 0 !important; margin-bottom: 0 !important; }

[data-testid="stHeader"] { background: #161b22; border-bottom: 1px solid #30363d; }
.block-container { padding: 1rem 1rem 1.5rem 1rem !important; max-width: 100% !important; }

/* Topbar */
.topbar {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 6px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}
.topbar-logo { font-weight: 700; letter-spacing: 0.08em; color: #e6edf3; }
.topbar-div { width: 1px; height: 14px; background: #30363d; display: inline-block; }
.topbar-price { color: #22c55e; font-weight: 600; }
.topbar-change { color: #22c55e; }
.topbar-meta { color: #8b949e; }

/* Agent cards */
.agent-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 3px;
    padding: 10px;
    position: relative;
    height: 100%;
}
.agent-accent { height: 2px; margin: -10px -10px 8px -10px; border-radius: 3px 3px 0 0; }
.agent-name { font-size: 11px; font-weight: 700; color: #e6edf3; margin-bottom: 1px; }
.agent-role { font-size: 9px; color: #8b949e; margin-bottom: 6px; }
.agent-dir { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; }
.agent-dir.bull { color: #22c55e; }
.agent-dir.bear { color: #ef4444; }
.agent-dir.neu  { color: #d29922; }
.agent-conf { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #8b949e; }
.agent-target { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #8b949e; margin: 3px 0; }
.agent-target span { color: #e6edf3; }
.agent-reasoning {
    font-size: 9px; color: #8b949e; line-height: 1.45;
    border-left: 2px solid #30363d; padding-left: 6px; margin-top: 5px;
}
.agent-revised {
    font-family: 'JetBrains Mono', monospace; font-size: 8px;
    color: #d29922; border: 1px solid #3a2e12; background: #1a1408;
    border-radius: 2px; padding: 1px 4px; display: inline-block; margin-top: 3px;
}
.agent-error { font-size: 9px; color: #ef4444; margin-top: 4px; }

/* Scenario input */
textarea, .stTextArea textarea {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    font-family: -apple-system, 'Segoe UI', sans-serif !important;
    font-size: 12px !important;
    border-radius: 3px !important;
}
textarea:focus { border-color: #58a6ff !important; }

/* Run button */
.stButton > button {
    background: #58a6ff !important;
    color: #0d1117 !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    border-radius: 3px !important;
    width: 100%;
}
.stButton > button:hover { background: #79bcff !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #0d1117 !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
}

/* Metric overrides */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 3px;
    padding: 8px 10px;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 18px !important;
    color: #e6edf3 !important;
}
[data-testid="stMetricLabel"] { font-size: 9px !important; color: #8b949e !important; }

/* Section headers */
.section-hd {
    font-size: 11px; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; color: #8b949e;
    margin-top: 0; margin-bottom: 8px;
    overflow: visible; white-space: nowrap;
    line-height: 1.4;
}
.sidebar-section-hd {
    font-size: 10px; font-weight: 600; letter-spacing: 1.5px;
    text-transform: uppercase; color: #8b949e;
    margin: 0 0 6px 0; padding: 0;
}

/* Probability bars */
.prob-track {
    height: 3px; background: #30363d; border-radius: 2px;
    margin: 2px 0 6px 0; overflow: hidden;
}
.prob-fill { height: 100%; border-radius: 2px; }

/* Analogue entries — date/event/return each own line, 4px between lines */
.analogue { padding: 8px 0 4px 0; border-bottom: 1px solid #21262d; font-size: 10px; line-height: 1; }
.analogue:last-child { border-bottom: none; }
.analogue-date { font-family: 'JetBrains Mono', monospace; color: #8b949e; display: block; margin-bottom: 4px; }
.analogue-event { color: #e6edf3; display: block; margin-bottom: 4px; }
.analogue-ret { font-family: 'JetBrains Mono', monospace; font-weight: 600; display: block; }

/* Indicator pills */
.ind-pill {
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    border: 1px solid #30363d; border-radius: 2px; padding: 2px 7px;
    display: inline-block; margin: 2px;
}
.ind-pill.bull { color: #22c55e; border-color: #1a3a28; background: #0d1f16; }
.ind-pill.bear { color: #ef4444; border-color: #3a1a1a; background: #1f0d0d; }
.ind-pill.neu  { color: #d29922; border-color: #3a2e12; background: #1a1408; }

/* Stat rows — 8px vertical spacing per spec */
.stat-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 0 0 0;
    font-size: 10px; overflow: visible; line-height: 1.4;
}
.stat-row + .stat-row { border-top: 1px solid #21262d; }
.stat-key { color: #8b949e; }
.stat-val { font-family: 'JetBrains Mono', monospace; color: #e6edf3; }
.stat-val.up { color: #22c55e; }
.stat-val.dn { color: #ef4444; }

/* Chat */
.chat-msg-user { background: #161b22; border: 1px solid #58a6ff; border-radius: 3px; padding: 7px 10px; font-size: 10px; color: #8b949e; margin-bottom: 6px; }
.chat-msg-agent { background: #161b22; border: 1px solid #30363d; border-radius: 3px; padding: 7px 10px; font-size: 10px; color: #e6edf3; margin-bottom: 6px; }
.chat-role { font-size: 9px; color: #8b949e; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; }

/* Progress bar */
.stProgress > div > div > div { background: #58a6ff !important; }

/* Dividers */
hr { border-color: #30363d !important; margin: 10px 0 !important; }

/* Simulation status line — Bug 2: full height, never clipped */
.sim-status {
    font-size: 9px; color: #8b949e;
    line-height: 1.8; padding: 4px 0 5px 0;
    overflow: visible; white-space: normal;
    min-height: 20px;
}

/* Reduce default Streamlit element gaps */
[data-testid="stVerticalBlock"] { gap: 4px !important; }
.stMarkdown { margin-bottom: 0 !important; }
.stButton { margin-top: 4px !important; margin-bottom: 0 !important; }
.stRadio { margin-bottom: 0 !important; }
.stTextArea { margin-bottom: 4px !important; }
.stSelectbox { margin-bottom: 4px !important; }
.stTextInput { margin-bottom: 4px !important; }

/* Column padding — no overflow clipping on x or y (Bug 2) */
[data-testid="column"] {
    padding: 6px 8px !important;
    min-width: 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Imports ────────────────────────────────────────────────────────────────────
import data as data_mod
import indicators as ind_mod
import analogues as ana_mod
import charts as charts_mod
import history as hist_mod
from agents import run_simulation, AGENT_PERSONAS, ForecastResult
from consensus import aggregate_forecasts_bayesian

# ── Session state ──────────────────────────────────────────────────────────────
if "simulation" not in st.session_state:
    st.session_state.simulation = None
if "active_round" not in st.session_state:
    st.session_state.active_round = 2
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "seed" not in st.session_state:
    st.session_state.seed = None

hist_mod.seed_demo_history()

# ── Load data ──────────────────────────────────────────────────────────────────
TICKER = "QQQ"
try:
    df = data_mod.fetch_ohlcv(TICKER, period="1y")
    macro = data_mod.fetch_macro_context()
    current_price = data_mod.get_current_price(df)
    ind = ind_mod.compute_all(df)
    regime = ana_mod.detect_regime(df, vix=macro.get("vix"))
except Exception as e:
    st.error(f"Data fetch failed: {e}")
    st.stop()

price_change = float(df["Close"].iloc[-1]) - float(df["Close"].iloc[-2])
price_change_pct = price_change / float(df["Close"].iloc[-2]) * 100
change_sign = "+" if price_change >= 0 else ""

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Bug 1 fix: ALL left-panel content lives exclusively here
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-section-hd">SCENARIO</div>', unsafe_allow_html=True)
    scenario = st.text_area("", value="Fed cuts rates 50bps unexpectedly", height=80, label_visibility="collapsed")
    run_clicked = st.button("▶ Run Simulation", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="sidebar-section-hd">INDICATORS</div>', unsafe_allow_html=True)
    rsi = round(ind.get("rsi", 0) or 0, 2)
    macd_v = round(ind.get("macd", 0) or 0, 2)
    bb = ind.get("bb_position", "mid")
    vix = macro.get("vix", 0) or 0
    st.markdown(f'`RSI {rsi}` `MACD {macd_v:+.2f}` `BB {bb}` `VIX {vix}`')

    st.markdown("---")
    st.markdown('<div class="sidebar-section-hd">MACRO DATA</div>', unsafe_allow_html=True)
    dxy = macro.get("dxy", "N/A")
    y10 = macro.get("yield_10y", "N/A")
    fed = macro.get("fed_rate", "N/A")
    for label, val in [
        ("DXY", dxy),
        ("10Y Yield", f"{y10}%" if y10 else "N/A"),
        ("Fed Rate", f"{fed}%" if fed else "N/A"),
        ("SMA50", ind.get("sma_50", "N/A")),
        ("SMA200", ind.get("sma_200", "N/A")),
    ]:
        st.markdown(f"**{label}** <span style='float:right'>{val}</span>", unsafe_allow_html=True)
    st.markdown(f"**Regime** <span style='float:right;color:#ef4444'>{regime}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sidebar-section-hd">HISTORICAL ANALOGUES</div>', unsafe_allow_html=True)
    analogues = ana_mod.find_analogues(df, scenario, regime)
    if analogues:
        for a in analogues:
            ret_color = "#22c55e" if a.return_5d > 0 else "#ef4444"
            sign = "+" if a.return_5d > 0 else ""
            st.markdown(f"**{a.date}** — {a.event_label[:45]}")
            st.markdown(f"<span style='color:{ret_color}'>{sign}{a.return_5d:.1f}% (5d)</span>", unsafe_allow_html=True)
    else:
        st.markdown("_No analogues found_")

# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR — rendered once in main area only
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f"""
<div class="topbar">
  <span class="topbar-logo">QQQ SIM</span>
  <span class="topbar-div"></span>
  <span style="font-weight:700">{TICKER}</span>
  <span class="topbar-price">{current_price:.2f}</span>
  <span class="topbar-change">{change_sign}{price_change:.2f} ({change_sign}{price_change_pct:.2f}%)</span>
  <span class="topbar-div"></span>
  <span class="topbar-meta">NASDAQ · 1Y daily · Regime: {regime}</span>
</div>
""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
# RUN SIMULATION — runs in main area, clean rerun after
# ══════════════════════════════════════════════════════════════════════════════
if run_clicked:
    seed = {
        "ticker": TICKER,
        "scenario": scenario,
        "price_history": df,
        "current_price": current_price,
        "current_indicators": ind,
        "macro_context": macro,
        "regime": regime,
        "analogues": ana_mod.find_analogues(df, scenario, regime),
    }
    st.session_state.seed = seed
    st.session_state.chat_history = {}
    st.session_state.active_round = 2
    with st.spinner("Running simulation — 3 rounds × 5 agents…"):
        result = run_simulation(seed)
    st.session_state.simulation = result
    hist_mod.save_prediction(seed, result)
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN COLUMNS — centre (chart + agents) | right (accuracy + chat)
# ══════════════════════════════════════════════════════════════════════════════
centre, right = st.columns([3, 1], gap="small")

# ── Centre ─────────────────────────────────────────────────────────────────────
with centre:
    fig = charts_mod.build_candlestick(df, ind)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    sim = st.session_state.simulation

    if sim is None:
        st.markdown(
            '<div style="text-align:center;padding:32px;color:#8b949e;font-size:11px">'
            "Enter a scenario in the sidebar and click ▶ Run Simulation"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        # Status + round selector (Bug 2: sim-status class ensures visible height)
        valid_count = sum(1 for f in sim.rounds[2] if f.status == "ok")
        scenario_label = st.session_state.seed["scenario"][:55]
        st.markdown(
            f'<div class="sim-status">'
            f'<span style="color:#22c55e">●</span> Simulation complete &nbsp;·&nbsp; '
            f'{valid_count}/5 agents &nbsp;·&nbsp; <span style="color:#e6edf3">{scenario_label}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
        round_choice = st.radio(
            "Round",
            options=["R1 — Independent", "R2 — Challenge", "R3 — Final"],
            index=st.session_state.active_round,
            horizontal=True,
            label_visibility="collapsed",
        )
        round_idx = {"R1 — Independent": 0, "R2 — Challenge": 1, "R3 — Final": 2}[round_choice]
        st.session_state.active_round = round_idx

        # Agent cards
        agent_names = list(AGENT_PERSONAS.keys())
        agent_roles = {
            "Macro Strategist": "Fed · rates · DXY",
            "Momentum Analyst": "RSI · MACD · trend",
            "Sentiment Analyst": "VIX · fear/greed",
            "Quant Modeler": "Vol · stats",
            "Earnings Analyst": "Tech · DCF",
        }
        accent_colors = {"bullish": "#22c55e", "bearish": "#ef4444", "neutral": "#d29922"}
        dir_symbols = {"bullish": "▲", "bearish": "▼", "neutral": "◆"}
        dir_cls = {"bullish": "bull", "bearish": "bear", "neutral": "neu"}

        cols = st.columns(5, gap="small")
        forecasts = sim.rounds[round_idx]
        for i, (col, name) in enumerate(zip(cols, agent_names)):
            f: ForecastResult = forecasts[i]
            with col:
                accent = accent_colors.get(f.direction, "#8b949e") if f.status == "ok" else "#8b949e"
                dir_sym = dir_symbols.get(f.direction, "◆") if f.status == "ok" else "✕"
                dir_c = dir_cls.get(f.direction, "neu") if f.status == "ok" else "bear"
                revised_html = ""
                if f.revised_from and f.revised_from != f.direction:
                    revised_html = f'<div class="agent-revised">↕ Revised from {f.revised_from}</div>'
                target_html = ""
                if f.status == "ok" and f.target_low > 0:
                    target_html = (
                        f'<div class="agent-target">Target '
                        f'<span>${f.target_low:.0f}–${f.target_high:.0f}</span></div>'
                    )
                conf_pct = int(f.confidence * 100)
                error_html = f'<div class="agent-error">⚠ {f.reasoning[:60]}</div>' if f.status == "error" else ""
                st.markdown(
                    f"""<div class="agent-card">
  <div class="agent-accent" style="background:{accent}"></div>
  <div class="agent-name">{name}</div>
  <div class="agent-role">{agent_roles[name]}</div>
  <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:3px">
    <span class="agent-dir {dir_c}">{dir_sym} {f.direction.capitalize() if f.status=='ok' else 'Error'}</span>
    <span class="agent-conf">{conf_pct}%</span>
  </div>
  <div style="height:2px;background:#30363d;border-radius:1px;margin-bottom:5px">
    <div style="height:100%;width:{conf_pct}%;background:{accent};border-radius:1px"></div>
  </div>
  {target_html}
  <div class="agent-reasoning">{f.reasoning}</div>
  {revised_html}{error_html}
</div>""",
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # Consensus panel — method toggle
        method_col, _ = st.columns([3, 3])
        with method_col:
            consensus_method = st.radio(
                "Consensus method",
                ["Simple", "Bayesian Ensemble"],
                horizontal=True,
                label_visibility="collapsed",
                key="consensus_method_radio",
            )

        if consensus_method == "Bayesian Ensemble":
            c = aggregate_forecasts_bayesian(sim.rounds, st.session_state.seed["scenario"])
        else:
            c = sim.consensus

        bull_pct = int(c.bull_prob * 100)
        base_pct = int(c.base_prob * 100)
        bear_pct = int(c.bear_prob * 100)
        delta_pct = ((c.consensus_target - current_price) / current_price * 100) if current_price else 0
        delta_sign = "+" if delta_pct >= 0 else ""

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        cons_left, cons_mid, cons_right = st.columns([2, 2, 2], gap="medium")
        with cons_left:
            method_badge = ' <span style="color:#58a6ff;font-size:9px">BAYESIAN</span>' if c.method == "bayesian" else ""
            st.markdown(f'<div class="section-hd" style="margin-top:0">Scenario Probabilities{method_badge}</div>', unsafe_allow_html=True)
            for label, pct, color in [("Bull", bull_pct, "#22c55e"), ("Base", base_pct, "#8b949e"), ("Bear", bear_pct, "#ef4444")]:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">'
                    f'<span style="font-size:10px;font-family:monospace;width:30px;color:{color}">{label}</span>'
                    f'<div class="prob-track" style="flex:1"><div class="prob-fill" style="width:{pct}%;background:{color}"></div></div>'
                    f'<span style="font-family:monospace;font-size:10px;color:#8b949e;width:28px;text-align:right">{pct}%</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<div style="font-size:9px;color:#8b949e;margin-top:4px">'
                f"{c.agent_count}/5 agents · avg conf {int(c.avg_confidence*100)}%</div>",
                unsafe_allow_html=True,
            )

        with cons_mid:
            st.markdown('<div class="section-hd" style="margin-top:0">Price Targets (5d)</div>', unsafe_allow_html=True)
            for label, val, color in [("Bull", f"${c.bull_target:.2f}", "#22c55e"), ("Base", f"${c.base_target:.2f}", "#e6edf3"), ("Bear", f"${c.bear_target:.2f}", "#ef4444")]:
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;font-size:10px;padding:3px 0">'
                    f'<span style="color:#8b949e">{label}</span>'
                    f'<span style="font-family:monospace;color:{color}">{val}</span></div>',
                    unsafe_allow_html=True,
                )

        with cons_right:
            st.markdown('<div class="section-hd" style="margin-top:0">Consensus</div>', unsafe_allow_html=True)
            target_color = "#22c55e" if delta_pct >= 0 else "#ef4444"
            st.markdown(
                f'<div style="font-family:monospace;font-size:22px;font-weight:700;color:{target_color}">'
                f"${c.consensus_target:.2f}</div>"
                f'<div style="font-size:10px;color:#8b949e">{delta_sign}{delta_pct:.1f}% vs ${current_price:.2f}</div>',
                unsafe_allow_html=True,
            )
            if c.method == "bayesian" and c.credible_low:
                st.markdown(
                    f'<div style="font-size:9px;color:#58a6ff;margin-top:4px">'
                    f"90% CI: ${c.credible_low:.2f} – ${c.credible_high:.2f}</div>",
                    unsafe_allow_html=True,
                )
            if c.disagreement:
                st.markdown(
                    f'<div style="font-size:9px;color:#d29922;margin-top:4px;border-left:2px solid #d29922;padding-left:5px">'
                    f"⚠ Split: {c.disagreement_detail}</div>",
                    unsafe_allow_html=True,
                )

# ── Right panel ────────────────────────────────────────────────────────────────
with right:
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-hd" style="margin-top:0">Accuracy Replay</div>', unsafe_allow_html=True)
    sc = hist_mod.get_scorecard()
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Correct", sc["correct"])
        st.metric("Total", sc["total"])
    with m2:
        st.metric("Wrong", sc["wrong"])
        st.metric("Accuracy", f"{sc['accuracy']}%")

    if st.button("Score Past", key="score_btn"):
        n = hist_mod.score_past_predictions()
        st.success(f"Scored {n} predictions")

    st.markdown("---")

    # Agent chat — restored below accuracy panel
    if st.session_state.simulation is not None:
        st.markdown('<div class="section-hd" style="margin-top:16px">Ask an Agent</div>', unsafe_allow_html=True)
        agent_options = list(AGENT_PERSONAS.keys())
        selected_agent = st.selectbox("Agent", agent_options, label_visibility="collapsed")

        chat_key = selected_agent
        if chat_key not in st.session_state.chat_history:
            st.session_state.chat_history[chat_key] = []

        for msg in st.session_state.chat_history[chat_key]:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-msg-user"><div class="chat-role">You</div>{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="chat-msg-agent"><div class="chat-role">{selected_agent}</div>{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

        question = st.text_input("Ask", placeholder="Follow-up question…", label_visibility="collapsed")
        if st.button("Ask", key="ask_btn") and question.strip():
            agent_names = list(AGENT_PERSONAS.keys())
            agent_idx = agent_names.index(selected_agent)
            r3 = st.session_state.simulation.rounds[2][agent_idx]

            from anthropic import Anthropic
            from agents import AGENT_PERSONAS as personas

            aclient = Anthropic()
            prior_forecast = (
                f"Your Round 3 forecast: direction={r3.direction}, "
                f"confidence={r3.confidence:.0%}, target=${r3.target_low:.0f}–${r3.target_high:.0f}, "
                f'reasoning="{r3.reasoning}"'
            )
            messages = [
                {"role": "user", "content": prior_forecast},
                {"role": "assistant", "content": "Understood. I stand by this forecast based on my analysis."},
                {"role": "user", "content": question},
            ]
            with st.spinner("…"):
                resp = aclient.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=300,
                    system=personas[selected_agent]["system"],
                    messages=messages,
                )
                answer = resp.content[0].text

            st.session_state.chat_history[chat_key].append({"role": "user", "content": question})
            st.session_state.chat_history[chat_key].append({"role": "assistant", "content": answer})
            st.rerun()
