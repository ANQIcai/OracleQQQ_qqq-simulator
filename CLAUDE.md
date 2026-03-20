# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

QQQ multi-agent price analysis tool. Fetches historical OHLCV data, computes technical indicators, runs 4 Claude-powered analyst personas in parallel, and renders an interactive Streamlit dashboard.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run with a specific date range
streamlit run app.py -- --start 2023-01-01 --end 2024-01-01
```

## Architecture

```
app.py              # Streamlit entry point — layout, chart rendering, agent panel
agents.py           # 4 analyst personas (macro, momentum, sentiment, quant) via Anthropic SDK
indicators.py       # RSI, MACD, Bollinger Bands computed on top of yfinance OHLCV data
data.py             # QQQ data fetching + caching via yfinance
```

### Agent design

Each agent in `agents.py` receives a structured context dict (price snapshot, indicator values, recent news summary) and returns a `ForecastResult` dataclass with: `direction` (bullish/bearish/neutral), `confidence` (0–1), `target_price`, `reasoning`, and `timeframe`. Agents run concurrently via `asyncio.gather`. A consensus function aggregates results into a weighted prediction shown in the UI.

### Data flow

`data.py` → `indicators.py` → `agents.py` → `app.py`

The Streamlit app calls `data.py` with `@st.cache_data` to avoid redundant API calls. Indicators are computed in-memory on each refresh. Agent calls are async and streamed where possible.

## Environment

Requires `ANTHROPIC_API_KEY` in environment or `.env` file.
