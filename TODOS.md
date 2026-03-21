# TODOS

## Design System

### Create DESIGN.md
**What:** Codify the TradingView-dark design system as a proper design document — color tokens, font stack, spacing scale, component patterns (agent-card, stat-row, ind-pill, etc.).
**Why:** The design system exists implicitly in app.py CSS but isn't documented. Every new feature requires reverse-engineering conventions from the stylesheet, risking drift.
**Pros:** Enables /design-review to validate against it. New contributors can onboard faster. Prevents accidental color/spacing inconsistencies.
**Cons:** Minor upfront effort (~15 min with CC).
**Context:** Flagged during plan-design-review of "Ask an Agent" panel (2026-03-21). Run /design-consultation to generate.
**Depends on / blocked by:** Nothing.

## UX Improvements

### Calendar nav button accessibility
**What:** The ◀ ▶ month navigation buttons announce as symbol names to screen readers, not "previous month" / "next month".
**Why:** Streamlit's `st.button()` has no `aria-label` parameter. Screen readers read the raw Unicode character name.
**Pros:** Fixing it properly means a custom Streamlit component — correct signal for any future a11y audit.
**Cons:** Requires a custom component; high effort for low current impact.
**Context:** Flagged during plan-design-review of calendar widget redesign (2026-03-21). Known Streamlit platform limitation, not an app bug.
**Depends on / blocked by:** Nothing — but fix requires a custom Streamlit component.

### Enter key submission for Ask an Agent input
**What:** Allow pressing Enter to submit a question in the "Ask an Agent" chat input, instead of requiring a mouse click on "Ask".
**Why:** Standard UX expectation for chat-style interfaces. Click-only input adds friction for keyboard users.
**Pros:** Faster interaction. Feels native to a chat UX.
**Cons:** Requires wrapping the input + button in `st.form()`, which slightly changes the Streamlit widget rendering model.
**Context:** Flagged during plan-design-review of "Ask an Agent" panel (2026-03-21). Streamlit's text_input doesn't natively fire on Enter without st.form().
**Depends on / blocked by:** "Ask an Agent" panel implementation.

## News & Data Pipeline

### ~~Historical Analogues: use 5-year dataset~~ ✓ Done 2026-03-21
Added `fetch_ohlcv_5y()` in data.py (cached 1h). Both `find_analogues()` calls in app.py now use `df_5y`.

### ~~Replace debug prints with logging.debug in news.py~~ ✓ Done 2026-03-21
All 8 `print(f"[news] ...")` calls replaced with `log.debug(...)`. Logger configured via `logging.getLogger(__name__)`.

## Consensus Engine

### Calibrate Conviction Score against historical accuracy
**What:** Track the Conviction Score computed at prediction time in history.json, then measure how often high-conviction predictions (67+) outperform low-conviction ones over time.
**Why:** The Kelly-based Conviction Score is theoretically grounded but empirically unvalidated. Without calibration data, users can't tell if 72 HIGH actually predicts better outcomes than 31 LOW.
**Pros:** Turns the Conviction Score into a self-improving signal. Enables future tuning of the Kelly fraction multiplier (currently 0.35).
**Cons:** Requires enough prediction history to be statistically meaningful (~20-30 predictions minimum).
**Context:** Flagged during plan-design-review of 5-Layer Consensus Engine (2026-03-21). Conviction Score introduced via fractional Kelly.
**Depends on / blocked by:** 5-Layer Consensus Engine implementation.

### Empirical copula correlation matrix
**What:** Replace the hardcoded agent correlation matrix (Macro↔Earnings: 0.4, Momentum↔Quant: 0.6, etc.) with values computed from actual agent output history in history.json.
**Why:** Fixed correlations are analytical estimates. If two agents consistently agree or diverge in practice, the copula layer should reflect that — currently it can't.
**Pros:** Self-calibrating system. Copula layer becomes more accurate as prediction history grows.
**Cons:** Requires ~20+ predictions with diverse outcomes to be statistically meaningful. Adds complexity to history.py.
**Context:** Flagged during plan-eng-review of 5-Layer Consensus Engine (2026-03-21). Current matrix is hardcoded in consensus.py AGENT_CORRELATION_MATRIX.
**Depends on / blocked by:** 5-Layer Consensus Engine implementation; sufficient prediction history.
