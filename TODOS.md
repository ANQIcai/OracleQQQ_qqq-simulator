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

### Enter key submission for Ask an Agent input
**What:** Allow pressing Enter to submit a question in the "Ask an Agent" chat input, instead of requiring a mouse click on "Ask".
**Why:** Standard UX expectation for chat-style interfaces. Click-only input adds friction for keyboard users.
**Pros:** Faster interaction. Feels native to a chat UX.
**Cons:** Requires wrapping the input + button in `st.form()`, which slightly changes the Streamlit widget rendering model.
**Context:** Flagged during plan-design-review of "Ask an Agent" panel (2026-03-21). Streamlit's text_input doesn't natively fire on Enter without st.form().
**Depends on / blocked by:** "Ask an Agent" panel implementation.

## News & Data Pipeline

### Historical Analogues: use 5-year dataset
**What:** Pass a 5-year OHLCV dataframe to `find_analogues()` instead of the 1-year main df.
**Why:** The HISTORICAL_EVENTS library spans 2018–2025, but with the 1y df only 2025+ events have enough pre-event data (30-day window). Everything else is skipped (`idx=0 → empty window → continue`). Currently produces at most 1 result.
**Pros:** Full 16-event library becomes usable. Analogues section shows meaningful historical parallels. Much richer context for predictions.
**Cons:** Requires a second yfinance fetch (5y period) — can be cached separately in data.py with `@st.cache_data`. Adds ~200ms on first load.
**Context:** Flagged during plan-eng-review of sidebar data pipeline (2026-03-21). The bug is in `find_analogues()`: `window_df = df.iloc[max(0, idx-30):idx]` where idx=0 for all pre-2025 events → empty window → skipped. Fix is to load a longer df, not to change the analogue logic.
**Depends on / blocked by:** Nothing.

### Replace debug prints with logging.debug in news.py
**What:** Replace `print(f"[news] ...")` calls in `fetch_all_news()`, `fetch_finnhub_news()`, and `fetch_alphavantage_news()` with `logging.debug(...)` and configure a logger.
**Why:** Debug prints added during the 2026-03-21 news pipeline fix will clutter production console output. They're useful for diagnosis but shouldn't be on by default.
**Pros:** Clean production output. Still diagnostic when `LOG_LEVEL=DEBUG` is set.
**Cons:** Minimal — just swapping print for logging.debug.
**Context:** Flagged during plan-eng-review of sidebar data pipeline (2026-03-21). The prints are currently `[news] raw: 0 AV + 180 FH = 148 after dedup` etc.
**Depends on / blocked by:** Nothing.

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
