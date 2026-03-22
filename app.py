import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="QQQ Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📈",
)

# ── Dark terminal CSS — refined ───────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-0: #000000;
    --bg-1: #0d0d0f;
    --bg-2: #1c1c1c;
    --border: #2a2a2e;
    --border-hover: #3a3a3e;
    --text-primary: #d1d4dc;
    --text-secondary: #787b86;
    --text-muted: #555;
    --accent-bull: #26a69a;
    --accent-bear: #ef5350;
    --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
    --radius-sm: 4px;
    --radius-md: 6px;
    --radius-lg: 8px;
    --transition: 180ms ease;
}

* { font-family: var(--font-body) !important; }

html, body, [data-testid="stApp"] {
    background-color: var(--bg-0) !important;
    color: var(--text-primary) !important;
    
}
[data-testid="stMainBlockContainer"] { margin-top: 50px !important; }
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="stColumn"],
.stTabs,
section[data-testid="stSidebar"] > div {
    background-color: var(--bg-0) !important;
}

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--bg-1) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebarContent"] { padding: 12px 14px 16px 14px !important; }
[data-testid="stSidebarContent"] > div:first-child { margin-top: -60px !important; }
[data-testid="stSidebar"] .block-container { padding: 0 !important; }
[data-testid="stSidebar"] hr {
    margin: 8px 0 !important;
    border: none !important;
    border-top: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 4px !important; }
[data-testid="stSidebar"] .stMarkdown { margin: 0 !important; padding: 0 !important; }
[data-testid="stSidebar"] .stTextArea { margin-bottom: 0 !important; }
[data-testid="stSidebar"] [data-testid="stButton"] {
    margin: 2px 0 !important; display: flex !important;
    width: auto !important; align-self: flex-start !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button,
[data-testid="stSidebar"] .stButton > button {
    width: auto !important;
    padding: 2px 10px !important;
    font-size: 10px !important;
    line-height: 1.6 !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] { margin: 0 !important; }
[data-testid="stSidebar"] button[kind="secondary"].cal-nav,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    border: none !important;
    color: var(--text-secondary) !important;
    padding: 0 6px !important;
    font-size: 13px !important;
    min-height: unset !important;
    box-shadow: none !important;
    transition: color var(--transition);
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover:not(:disabled) {
    color: var(--text-primary) !important;
    background: transparent !important;
    border: none !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:disabled {
    color: var(--border) !important;
    cursor: default !important;
    background: transparent !important;
    border: none !important;
}

[data-testid="stHeader"] { background: var(--bg-0) !important; border: none !important; }
.block-container { padding: 0.5rem 1rem 1.5rem 1rem !important; max-width: 100% !important; }

/* ── Topbar ──────────────────────────────────────────── */
.topbar {
    background: linear-gradient(180deg, #141416 0%, #0d0d0f 100%);
    border-bottom: 1px solid var(--border);
    padding: 10px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 11px;
    margin: -1rem -1rem 0 -1rem;
    backdrop-filter: blur(8px);
}
.topbar-div {
    width: 1px; height: 16px; background: var(--border);
    display: inline-block; opacity: 0.6;
}
.topbar-meta { color: var(--text-secondary); letter-spacing: 0.02em; }

/* ── Agent cards ─────────────────────────────────────── */
.agent-card {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px;
    position: relative;
    height: 100%;
    transition: border-color var(--transition), box-shadow var(--transition);
}
.agent-card:hover {
    border-color: var(--border-hover);
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.agent-accent {
    height: 2px; margin: -12px -12px 10px -12px;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
}
.agent-name {
    font-size: 11px; font-weight: 600; color: var(--text-primary);
    margin-bottom: 2px; letter-spacing: 0.01em;
}
.agent-role {
    font-size: 9px; color: var(--text-secondary);
    margin-bottom: 8px; letter-spacing: 0.02em;
}
.agent-dir {
    font-family: var(--font-mono) !important;
    font-size: 12px; font-weight: 600;
}
.agent-dir.bull { color: var(--accent-bull); }
.agent-dir.bear { color: var(--accent-bear); }
.agent-dir.neu  { color: var(--text-secondary); }
.agent-conf {
    font-family: var(--font-mono) !important;
    font-size: 10px; color: var(--text-secondary);
}
.agent-target {
    font-family: var(--font-mono) !important;
    font-size: 10px; color: var(--text-secondary); margin: 4px 0;
}
.agent-target span { color: var(--text-primary); }
.agent-reasoning {
    font-size: 9.5px; color: var(--text-secondary); line-height: 1.5;
    border-left: 2px solid var(--border); padding-left: 8px; margin-top: 6px;
}
.agent-revised {
    font-size: 8px; color: var(--text-secondary);
    border: 1px solid var(--border); background: var(--bg-2);
    border-radius: var(--radius-sm); padding: 2px 5px;
    display: inline-block; margin-top: 4px;
}
.agent-error { font-size: 9px; color: var(--accent-bear); margin-top: 4px; }

/* ── Inputs ──────────────────────────────────────────── */
textarea, .stTextArea textarea {
    background: var(--bg-0) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-size: 12px !important;
    border-radius: var(--radius-sm) !important;
    transition: border-color var(--transition) !important;
}
textarea:focus { border-color: var(--border-hover) !important; }

/* ── Buttons ─────────────────────────────────────────── */
.stButton > button {
    background: var(--border) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-hover) !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    border-radius: var(--radius-sm) !important;
    width: 100%;
    transition: all var(--transition) !important;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    background: var(--border-hover) !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.25) !important;
}

/* ── Predict button — special emphasis ───────────────── */
.predict-btn .stButton > button,
div[data-testid="stVerticalBlock"] > div:has(button:only-child) .stButton > button {
    letter-spacing: 0.04em;
}

/* ── Selectbox ───────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--bg-0) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* ── Metrics ─────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 18px !important;
    color: var(--text-primary) !important;
}
[data-testid="stMetricLabel"] { font-size: 9px !important; color: var(--text-secondary) !important; }

/* ── Section headers ─────────────────────────────────── */
.section-hd {
    font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: var(--text-secondary);
    margin-top: 30px; margin-bottom: 10px;
    overflow: visible; white-space: nowrap; line-height: 1.4;
}
.sidebar-section-hd {
    font-size: 9px; font-weight: 700; letter-spacing: 1.8px;
    text-transform: uppercase; color: var(--text-secondary);
    margin: 10px 0 8px 0; padding: 0; line-height: 1;
    margin-top: 30px !important;
}

/* ── Probability bars ────────────────────────────────── */
.prob-track {
    height: 4px; background: var(--border); border-radius: 2px;
    margin: 2px 0 6px 0; overflow: hidden;
}
.prob-fill {
    height: 100%; border-radius: 2px;
    transition: width 600ms cubic-bezier(0.22, 1, 0.36, 1);
}

/* ── Analogue entries ────────────────────────────────── */
.analogue {
    padding: 8px 0 4px 0; border-bottom: 1px solid var(--border);
    font-size: 10px; line-height: 1;
}
.analogue:last-child { border-bottom: none; }
.analogue-date {
    font-family: var(--font-mono) !important;
    color: var(--text-secondary); display: block; margin-bottom: 4px;
}
.analogue-event { color: var(--text-primary); display: block; margin-bottom: 4px; }
.analogue-ret {
    font-family: var(--font-mono) !important;
    font-weight: 600; display: block;
}

/* ── Indicator pills ─────────────────────────────────── */
.ind-pill {
    font-family: var(--font-mono) !important;
    font-size: 10px; border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 2px 7px; display: inline-block; margin: 2px;
    background: var(--bg-2);
}
.ind-pill.bull { color: var(--accent-bull); }
.ind-pill.bear { color: var(--accent-bear); }
.ind-pill.neu  { color: var(--text-secondary); }

/* ── Stat rows ───────────────────────────────────────── */
.stat-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 5px 0; font-size: 10px; overflow: visible; line-height: 1;
    border-bottom: 1px solid var(--border);
}
.stat-row:last-child { border-bottom: none; }
.stat-key { color: var(--text-secondary); }
.stat-val {
    font-family: var(--font-mono) !important;
    color: var(--text-primary);
}
.stat-val.up { color: var(--accent-bull); }
.stat-val.dn { color: var(--accent-bear); }

/* ── Chat ────────────────────────────────────────────── */
.chat-msg-user {
    background: var(--bg-2); border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 8px 12px; font-size: 10.5px; color: var(--text-secondary);
    margin-bottom: 6px;
}
.chat-msg-agent {
    background: var(--bg-2); border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 8px 12px; font-size: 10.5px; color: var(--text-primary);
    margin-bottom: 6px;
}
.chat-role {
    font-size: 8px; color: var(--text-secondary); font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;
}

/* Revision bubble */
.chat-msg-revision {
    background: rgba(38,166,154,0.06);
    border: 1px solid var(--accent-bull);
    border-radius: var(--radius-md);
    padding: 8px 12px;
    font-size: 10.5px;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.chat-msg-revision .chat-role { color: var(--accent-bull); }

/* ── Progress bar ────────────────────────────────────── */
.stProgress > div > div > div { background: var(--border) !important; }

/* ── Dividers ────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 10px 0 !important; }

/* ── Simulation status ───────────────────────────────── */
.sim-status {
    font-size: 9px; color: var(--text-secondary);
    line-height: 1.8; padding: 4px 0 5px 0;
    overflow: visible; white-space: normal; min-height: 20px;
}

/* ── Spacing resets ──────────────────────────────────── */
[data-testid="stVerticalBlock"] { gap: 4px !important; }
.stMarkdown { margin-bottom: 0 !important; }
.stButton { margin-top: 4px !important; margin-bottom: 0 !important; }
.stRadio { margin-bottom: 0 !important; }
.stTextArea { margin-bottom: 4px !important; }
.stSelectbox { margin-bottom: 4px !important; }
.stTextInput { margin-bottom: 4px !important; }
[data-testid="column"] { padding: 6px 8px !important; min-width: 0; }

/* ── News filter tabs ────────────────────────────────── */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 0 !important; flex-wrap: wrap !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 3px 8px !important; cursor: pointer !important;
    border-radius: var(--radius-sm) !important;
    transition: background var(--transition);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.03) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 10px !important; color: var(--text-secondary) !important;
    font-weight: 400 !important; margin: 0 !important; line-height: 1.6 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has([aria-checked="true"]) {
    background: rgba(255,255,255,0.04) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has([aria-checked="true"]) p {
    color: var(--text-primary) !important; font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] { margin-bottom: 4px !important; }

/* ── Scrollbar ───────────────────────────────────────── */
.tv-news-scroll {
    max-height: 350px; overflow-y: auto;
    scrollbar-width: thin; scrollbar-color: var(--border-hover) transparent;
}
.tv-news-scroll::-webkit-scrollbar { width: 4px; }
.tv-news-scroll::-webkit-scrollbar-track { background: transparent; }
.tv-news-scroll::-webkit-scrollbar-thumb {
    background: var(--border-hover); border-radius: 2px;
}

/* ── Text input ──────────────────────────────────────── */
.stTextInput input {
    background: var(--bg-0) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-size: 12px !important;
    border-radius: var(--radius-sm) !important;
    transition: border-color var(--transition) !important;
}
.stTextInput input:focus { border-color: var(--border-hover) !important; }

/* ── News card hover ─────────────────────────────────── */
.news-card {
    padding: 7px 0; border-bottom: 1px solid var(--border);
    transition: background var(--transition);
}
.news-card:hover { background: rgba(255,255,255,0.015); }
.news-card:last-child { border-bottom: none; }

/* ── Digest card ─────────────────────────────────────── */
.digest-card {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    margin-bottom: 8px;
    transition: border-color var(--transition);
}
.digest-card:hover { border-color: var(--border-hover); }

/* ── Consensus panel ─────────────────────────────────── */
.consensus-panel {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 16px;
}

/* ── Summary strip cards ─────────────────────────────── */
.summary-card {
    flex: 1;
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 8px 10px;
    transition: border-color var(--transition), transform var(--transition);
}
.summary-card:hover {
    border-color: var(--border-hover);
    transform: translateY(-1px);
}

/* ── Regime badge ────────────────────────────────────── */
.regime-badge {
    font-size: 9px; color: var(--text-secondary);
    margin-top: 10px; padding: 7px 10px;
    background: var(--bg-1); border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    font-family: var(--font-mono) !important;
    letter-spacing: 0.02em;
}

/* ── Pipeline label ──────────────────────────────────── */
.pipeline-label {
    font-size: 8px; color: var(--text-muted);
    margin-top: 5px; letter-spacing: 0.4px;
    font-family: var(--font-mono) !important;
}

/* ── Ask-agent stance card ───────────────────────────── */
.stance-card {
    background: var(--bg-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    margin-bottom: 8px;
    transition: border-color var(--transition);
}
.stance-card:hover { border-color: var(--border-hover); }

/* ── Responsive ──────────────────────────────────────── */
@media (max-width: 900px) {
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        width: 100% !important; flex: none !important; min-width: 100% !important;
    }
}

/* ── Subtle load-in animation ────────────────────────── */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeSlideIn 350ms ease both; }
.fade-in-d1 { animation: fadeSlideIn 350ms ease 80ms both; }
.fade-in-d2 { animation: fadeSlideIn 350ms ease 160ms both; }
.fade-in-d3 { animation: fadeSlideIn 350ms ease 240ms both; }
.fade-in-d4 { animation: fadeSlideIn 350ms ease 320ms both; }
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
import news as news_mod
import live_data as ld_mod
from agents import run_simulation, AGENT_PERSONAS, ForecastResult
from consensus import aggregate_forecasts_institutional
from streamlit_autorefresh import st_autorefresh

# ── Session state ──────────────────────────────────────────────────────────────
if "simulation" not in st.session_state:
    st.session_state.simulation = None
if "active_round" not in st.session_state:
    st.session_state.active_round = 2
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "seed" not in st.session_state:
    st.session_state.seed = None
if "news_cache" not in st.session_state:
    st.session_state.news_cache = []
if "last_news_fetch" not in st.session_state:
    st.session_state.last_news_fetch = None
if "digest_cache" not in st.session_state:
    st.session_state.digest_cache = {}
if "key_dates_cache" not in st.session_state:
    st.session_state.key_dates_cache = []
if "consensus_cache" not in st.session_state:
    st.session_state.consensus_cache = []
if "live_quote_cache" not in st.session_state:
    st.session_state.live_quote_cache = {}
if "debate_stances" not in st.session_state:
    st.session_state.debate_stances = {}
if "ask_in_flight" not in st.session_state:
    st.session_state.ask_in_flight = False
if "cal_month" not in st.session_state:
    st.session_state.cal_month = datetime.now().month
if "cal_year" not in st.session_state:
    st.session_state.cal_year = datetime.now().year

hist_mod.seed_demo_history()

# ── Load data ──────────────────────────────────────────────────────────────────
TICKER = "QQQ"
try:
    df = data_mod.fetch_ohlcv(TICKER, period="1y")
    df_5y = data_mod.fetch_ohlcv_5y(TICKER)
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

# ── News + live data — refresh every 5 minutes ────────────────────────────────
st_autorefresh(interval=300_000, limit=None, key="news_autorefresh")
_NEWS_REFRESH_SECS = 300
_now = datetime.now()
_should_refresh = (
    st.session_state.last_news_fetch is None
    or (_now - st.session_state.last_news_fetch).total_seconds() >= _NEWS_REFRESH_SECS
)
if _should_refresh:
    st.session_state.news_cache = news_mod.fetch_all_news()
    st.session_state.last_news_fetch = _now
    st.session_state.live_quote_cache = ld_mod.get_live_quote("QQQ")
    st.session_state.key_dates_cache = ld_mod.get_all_key_dates()
    st.session_state.consensus_cache = ld_mod.get_top_holdings_consensus()

if st.session_state.news_cache:
    st.session_state.digest_cache = news_mod.generate_market_digest(st.session_state.news_cache)

scenario = news_mod.build_scenario_from_news(
    st.session_state.digest_cache, st.session_state.news_cache, regime
)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    _lq = st.session_state.live_quote_cache
    _lq_price = _lq.get("price") or current_price
    _lq_chg = _lq.get("change") or price_change
    _lq_chg_pct = _lq.get("change_pct") or price_change_pct
    _lq_color = "#26a69a" if (_lq_chg or 0) >= 0 else "#ef5350"
    _lq_sign = "+" if (_lq_chg or 0) >= 0 else ""
    vix = macro.get("vix", 0) or 0
    dxy = macro.get("dxy", "N/A")
    y10 = macro.get("yield_10y", "N/A")
    fed = macro.get("fed_rate", "N/A")
    rsi = round(ind.get("rsi", 0) or 0, 2)
    macd_v = round(ind.get("macd", 0) or 0, 2)
    bb = ind.get("bb_position", "mid")

    # ── Panel header ──
    _hdr_col, _ref_col = st.columns([4, 1])
    with _hdr_col:
        st.markdown(
            '<div style="font-size:18px;font-weight:700;color:#d1d4dc;letter-spacing:0.01em;padding:4px 0">'
            'Market Intel</div>',
            unsafe_allow_html=True,
        )
    with _ref_col:
        if st.button("↻", key="news_refresh_btn", help="Refresh market data"):
            st.session_state.news_cache = news_mod.fetch_all_news()
            st.session_state.last_news_fetch = datetime.now()
            st.session_state.digest_cache = news_mod.generate_market_digest(st.session_state.news_cache)
            st.session_state.live_quote_cache = ld_mod.get_live_quote("QQQ")
            st.session_state.key_dates_cache = ld_mod.get_all_key_dates()
            st.session_state.consensus_cache = ld_mod.get_top_holdings_consensus()
            st.rerun()

    # ── Market Pulse ──
    _regime_color = "#ef5350" if "bear" in regime.lower() else "#26a69a" if "bull" in regime.lower() else "#787b86"
    _pulse = f'''<div style="margin-bottom:16px">
<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#787b86;margin-bottom:10px">MARKET PULSE</div>
<div style="display:flex;align-items:baseline;gap:8px;padding-bottom:10px;border-bottom:1px solid #2a2a2e;margin-bottom:8px">
<span style="font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:700;color:#d1d4dc">${_lq_price:.2f}</span>
<span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:{_lq_color}">{_lq_sign}{_lq_chg:.2f} ({_lq_sign}{_lq_chg_pct:.2f}%)</span>
</div>
<div style="font-size:10px">
<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">VIX</span><span style="font-family:'JetBrains Mono',monospace;color:#d1d4dc">{vix}</span></div>
<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">DXY</span><span style="font-family:'JetBrains Mono',monospace;color:#d1d4dc">{dxy}</span></div>
<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">10Y Yield</span><span style="font-family:'JetBrains Mono',monospace;color:#d1d4dc">{y10}%</span></div>
<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">Fed Rate</span><span style="font-family:'JetBrains Mono',monospace;color:#d1d4dc">{fed}%</span></div>
<div style="display:flex;justify-content:space-between;padding:4px 0"><span style="color:#787b86">Regime</span><span style="font-family:'JetBrains Mono',monospace;color:{_regime_color};font-weight:600">{regime}</span></div>
</div>
</div>'''
    st.markdown(_pulse, unsafe_allow_html=True)

    # ── Live news ──
    _total_arts = len(st.session_state.news_cache)
    st.markdown(
        f'<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px">'
        f'<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#787b86;margin-bottom:8px">'
        f'QQQ NEWS <span style="font-weight:400;color:#555;letter-spacing:0">{_total_arts}</span></div></div>',
        unsafe_allow_html=True,
    )

    _filter = st.radio(
        "news_filter",
        ["All", "Fed & Rates", "Earnings", "Tech & AI", "Macro"],
        horizontal=True, label_visibility="collapsed", key="news_category_filter",
    )
    _FILTER_CATS = {
        "All": None, "Fed & Rates": ["Fed & Rates"], "Earnings": ["Earnings"],
        "Tech & AI": ["Tech & AI"], "Macro": ["Economic Data", "Trade & Geopolitics", "Market Structure"],
    }
    _pool = st.session_state.news_cache
    _active_cats = _FILTER_CATS.get(_filter)
    if _active_cats:
        _pool = [a for a in _pool if a.category in _active_cats]

    if not _pool:
        st.markdown(
            '<div style="font-size:10px;color:#787b86;padding:4px 0 12px 0">No articles in this category.</div>',
            unsafe_allow_html=True,
        )
    else:
        _cards = ""
        for _a in _pool[:12]:
            _lb = (
                "border-left:2px solid #26a69a;padding-left:8px;"
                if _a.sentiment > 0.3
                else "border-left:2px solid #ef5350;padding-left:8px;"
                if _a.sentiment < -0.3
                else "padding-left:10px;"
            )
            _pills = "".join(
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:8px;color:#787b86;'
                f'border:1px solid #2a2a2e;border-radius:3px;padding:1px 4px;margin-right:2px">{t}</span>'
                for t in (_a.tickers or [])[:4]
            )
            _ago = news_mod.time_ago(_a.published)
            _link = (
                f'<a href="{_a.url}" target="_blank" style="font-size:9px;color:#555;'
                f'text-decoration:none;margin-top:3px;display:inline-block;'
                f'transition:color 180ms ease">Read more →</a>'
                if _a.url else ""
            )
            _cards += (
                f'<div class="news-card" style="{_lb}">'
                f'<div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;margin-bottom:4px">'
                f'{_pills}<span style="font-size:8px;color:#555">{_ago} · {_a.source or ""}</span></div>'
                f'<div style="font-size:11.5px;color:#d1d4dc;line-height:1.35;font-weight:500;'
                f'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">'
                f'{_a.title}</div>{_link}</div>'
            )
        st.markdown(f'<div class="tv-news-scroll">{_cards}</div>', unsafe_allow_html=True)

    # ── Key dates calendar ──
    _kd = st.session_state.key_dates_cache
    import calendar as _cal_mod
    _today = datetime.now()
    _now_abs = _today.year * 12 + _today.month
    _sel_abs = st.session_state.cal_year * 12 + st.session_state.cal_month
    _at_min = (_now_abs - _sel_abs) >= 12
    _at_max = (_sel_abs - _now_abs) >= 12

    st.markdown(
        '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:4px">'
        '<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;'
        'color:#787b86;margin-bottom:6px">KEY DATES</div></div>',
        unsafe_allow_html=True,
    )

    _cal_left, _cal_title, _cal_right = st.columns([1, 4, 1])
    with _cal_left:
        if st.button("◀", key="cal_prev", disabled=_at_min):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1
            st.rerun()
    with _cal_title:
        _month_name = _cal_mod.month_name[st.session_state.cal_month]
        st.markdown(
            f'<div style="text-align:center;font-size:11px;color:#d1d4dc;font-weight:600;padding-top:4px">'
            f'{_month_name} {st.session_state.cal_year}</div>',
            unsafe_allow_html=True,
        )
    with _cal_right:
        if st.button("▶", key="cal_next", disabled=_at_max):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1
            st.rerun()

    _cal_html = ld_mod.render_calendar_html(
        _kd or [],
        year=st.session_state.cal_year,
        month=st.session_state.cal_month,
    )

    _legend = '<div style="display:flex;gap:10px;margin-top:6px;margin-bottom:6px;flex-wrap:wrap">'
    for _lbl, _lc in [("Earn", "#ef5350"), ("FOMC", "#26a69a"), ("Eco", "#787b86"), ("OpEx", "#d1d4dc")]:
        _legend += f'<span style="font-size:8px;color:{_lc}">● {_lbl}</span>'
    _legend += "</div>"

    _sel_prefix = f"{st.session_state.cal_year:04d}-{st.session_state.cal_month:02d}-"
    _month_events = [e for e in (_kd or []) if (e.get("date") or "").startswith(_sel_prefix)]
    _events_html = ""
    if _month_events:
        for _e in _month_events[:8]:
            _tc = ld_mod._TYPE_COLORS.get(_e["type"], "#787b86")
            _events_html += (
                f'<div style="display:flex;gap:6px;align-items:flex-start;padding:3px 0;'
                f'border-bottom:1px solid #2a2a2e">'
                f'<span style="color:{_tc};font-size:8px;margin-top:2px">●</span>'
                f'<div style="font-size:9px">'
                f'<span style="font-family:\'JetBrains Mono\',monospace;color:#787b86">{_e["date"]}</span> '
                f'<span style="color:#d1d4dc">{_e["event"]}</span>'
                f'<div style="color:#555;font-size:8px">→ {_e["agent"]}</div>'
                f'</div></div>'
            )
    else:
        _events_html = '<div style="font-size:9px;color:#787b86;padding:6px 0">No events this month</div>'

    st.markdown(
        f'{_cal_html}{_legend}'
        f'<div style="margin-bottom:16px">{_events_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Indicators ──
    _ind_data = [
        ("RSI(14)", rsi, "#26a69a" if 30 < rsi < 70 else "#ef5350"),
        ("MACD", f"{macd_v:+.2f}", "#26a69a" if macd_v > 0 else "#ef5350"),
        ("BB Pos", bb, "#26a69a" if bb == "lower" else "#ef5350" if bb == "upper" else "#d1d4dc"),
        ("SMA20", ind.get("sma_20", "N/A"), "#d1d4dc"),
        ("SMA50", ind.get("sma_50", "N/A"), "#d1d4dc"),
        ("SMA200", ind.get("sma_200", "N/A"), "#d1d4dc"),
        ("EMA9", ind.get("ema_9", "N/A"), "#d1d4dc"),
        ("ATR(14)", ind.get("atr", "N/A"), "#d1d4dc"),
    ]
    _ind_html = (
        '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:16px">'
        '<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;'
        'color:#787b86;margin-bottom:8px">INDICATORS</div>'
    )
    for _lbl, _val, _clr in _ind_data:
        _ind_html += (
            f'<div style="display:flex;justify-content:space-between;padding:4px 0;font-size:10px;'
            f'border-bottom:1px solid #2a2a2e">'
            f'<span style="color:#787b86">{_lbl}</span>'
            f'<span style="font-family:\'JetBrains Mono\',monospace;color:{_clr}">{_val}</span></div>'
        )
    _ind_html += '</div>'
    st.markdown(_ind_html, unsafe_allow_html=True)

    # ── Analyst consensus ──
    _cons = st.session_state.consensus_cache
    _cons_block = (
        '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:16px">'
        '<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;'
        'color:#787b86;margin-bottom:8px">ANALYST CONSENSUS</div>'
    )
    if _cons:
        _cons_block += (
            '<table style="width:100%;font-size:10px;border-collapse:collapse;margin:0 auto">'
            '<tr><th style="color:#555;text-align:left;padding:4px 0;font-weight:600">Sym</th>'
            '<th style="color:#26a69a;text-align:right;padding:4px 0;font-weight:600">Buy</th>'
            '<th style="color:#787b86;text-align:right;padding:4px 0;font-weight:600">Hold</th>'
            '<th style="color:#ef5350;text-align:right;padding:4px 0;font-weight:600">Sell</th>'
            '<th style="color:#d1d4dc;text-align:right;padding:4px 0;font-weight:600">PT</th></tr>'
        )
        for _c in _cons:
            _pt = f"${_c['target_mean']:.0f}" if _c.get("target_mean") else "—"
            _cons_block += (
                f'<tr style="border-top:1px solid #2a2a2e">'
                f'<td style="color:#d1d4dc;padding:4px 0;font-weight:500">{_c["symbol"]}</td>'
                f'<td style="font-family:\'JetBrains Mono\',monospace;color:#26a69a;text-align:right;padding:4px 0">{_c["buy"]}</td>'
                f'<td style="font-family:\'JetBrains Mono\',monospace;color:#787b86;text-align:right;padding:4px 0">{_c["hold"]}</td>'
                f'<td style="font-family:\'JetBrains Mono\',monospace;color:#ef5350;text-align:right;padding:4px 0">{_c["sell"]}</td>'
                f'<td style="font-family:\'JetBrains Mono\',monospace;color:#d1d4dc;text-align:right;padding:4px 0">{_pt}</td></tr>'
            )
        _cons_block += '</table>'
    else:
        _cons_block += '<div style="font-size:9px;color:#787b86">Loading analyst data…</div>'
    _cons_block += '</div>'
    st.markdown(_cons_block, unsafe_allow_html=True)

    # ── Historical analogues ──
    analogues = ana_mod.find_analogues(df_5y, scenario, regime)
    _ana_block = (
        '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:16px">'
        '<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;'
        'color:#787b86;margin-bottom:8px">HISTORICAL ANALOGUES</div>'
    )
    if analogues:
        for a in analogues:
            _rc = "#26a69a" if a.return_5d > 0 else "#ef5350"
            _rs = "+" if a.return_5d > 0 else ""
            _ana_block += (
                f'<div style="padding:4px 0;border-bottom:1px solid #2a2a2e">'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#787b86">{a.date}</span> '
                f'<span style="font-size:10px;color:#d1d4dc">— {a.event_label[:45]}</span>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:{_rc};font-weight:600">'
                f'{_rs}{a.return_5d:.1f}% (5d)</div></div>'
            )
    else:
        _ana_block += '<div style="font-size:10px;color:#787b86">No analogues found</div>'
    _ana_block += '</div>'
    st.markdown(_ana_block, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════════════════════════
_tb_color = "#26a69a" if price_change >= 0 else "#ef5350"
st.markdown(
    f"""
<div class="topbar">
  <span style="font-size:14px;font-weight:700;color:#d1d4dc;letter-spacing:0.02em">Oracle<span style="color:#26a69a">QQQ</span></span>
  <span class="topbar-div"></span>
  <span style="font-family:'JetBrains Mono',monospace;font-weight:600;color:#d1d4dc;font-size:11px">{TICKER}</span>
  <span style="font-family:'JetBrains Mono',monospace;font-weight:600;color:{_tb_color};font-size:11px">{current_price:.2f}</span>
  <span style="font-family:'JetBrains Mono',monospace;color:{_tb_color};font-size:10px">{change_sign}{price_change:.2f} ({change_sign}{price_change_pct:.2f}%)</span>
  <span class="topbar-div"></span>
  <span class="topbar-meta">NASDAQ · 1Y daily · Regime: {regime}</span>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
centre, right = st.columns([3, 1], gap="small")

# ── Centre ─────────────────────────────────────────────────────────────────────
with centre:
    st.markdown('<div style="height:50px"></div>', unsafe_allow_html=True)
    fig = charts_mod.build_candlestick(df, ind)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── AI Market Digest ──
    _dg = st.session_state.get("digest_cache", {})
    if _dg.get("digest"):
        _dg_color = (
            "#26a69a" if "bull" in _dg.get("sentiment", "").lower()
            else "#ef5350" if "bear" in _dg.get("sentiment", "").lower()
            else "#787b86"
        )
        _dg_mins = (
            int((datetime.now() - _dg["generated_at"]).total_seconds() / 60)
            if _dg.get("generated_at") else 0
        )
        st.markdown(
            f'<div class="digest-card fade-in">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
            f'<span style="font-size:9px;color:#787b86;text-transform:uppercase;letter-spacing:1.2px;font-weight:600">'
            f'AI Market Digest</span>'
            f'<span style="font-size:8px;color:#555">{_dg_mins}m ago</span></div>'
            f'<div style="font-size:11.5px;color:#d1d4dc;line-height:1.6">{_dg["digest"]}</div>'
            f'<div style="margin-top:10px;display:flex;gap:18px;flex-wrap:wrap;padding-top:8px;border-top:1px solid #2a2a2e">'
            f'<span style="font-size:9px;color:{_dg_color};font-weight:600">● {_dg.get("sentiment","Neutral")}</span>'
            f'<span style="font-size:9px;color:#787b86">KEY RISK: {_dg.get("key_risk","")}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="digest-card">'
            '<div style="font-size:10px;color:#787b86">'
            'Generating AI Market Digest…</div></div>',
            unsafe_allow_html=True,
        )

    predict_clicked = st.button("Predict QQQ Direction", use_container_width=True)

    sim = st.session_state.simulation

    if sim is None or predict_clicked:
        st.markdown(
            '<div style="text-align:center;padding:32px 16px;color:#555;font-size:11px;'
            'border:1px dashed #2a2a2e;border-radius:6px;margin-top:8px">'
            "Review the market digest above, then click <b style='color:#787b86'>Predict QQQ Direction</b>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        valid_count = sum(1 for f in sim.rounds[2] if f.status == "ok")
        scenario_label = st.session_state.seed["scenario"][:55]
        st.markdown(
            f'<div class="sim-status">'
            f'<span style="color:#26a69a">●</span> Simulation complete &nbsp;·&nbsp; '
            f'{valid_count}/5 agents &nbsp;·&nbsp; <span style="color:#d1d4dc">{scenario_label}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

        # Consensus panel
        c = aggregate_forecasts_institutional(
            sim.rounds,
            st.session_state.seed["scenario"],
            regime,
            current_price,
            macro,
        )

        bull_pct = int(c.bull_prob * 100)
        base_pct = int(c.base_prob * 100)
        bear_pct = int(c.bear_prob * 100)
        delta_pct = ((c.consensus_target - current_price) / current_price * 100) if current_price else 0
        delta_sign = "+" if delta_pct >= 0 else ""

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        cons_left, cons_mid, cons_right = st.columns([2, 2, 2], gap="medium")
        with cons_left:
            method_badge = (
                ' <span style="font-family:\'JetBrains Mono\',monospace;color:#d1d4dc;font-size:8px;'
                'background:#2a2a2e;padding:1px 5px;border-radius:3px">BAYESIAN</span>'
                if c.method == "bayesian" else ""
            )
            st.markdown(
                f'<div class="section-hd fade-in" style="margin-top:20px">Scenario Probabilities{method_badge}</div>',
                unsafe_allow_html=True,
            )
            for label, pct, color in [("Bull", bull_pct, "#26a69a"), ("Base", base_pct, "#787b86"), ("Bear", bear_pct, "#ef5350")]:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">'
                    f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;width:30px;color:{color}">{label}</span>'
                    f'<div class="prob-track" style="flex:1"><div class="prob-fill" style="width:{pct}%;background:{color}"></div></div>'
                    f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#787b86;width:28px;text-align:right">{pct}%</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<div style="font-size:9px;color:#555;margin-top:4px">'
                f"{c.agent_count}/5 agents · avg conf {int(c.avg_confidence*100)}%</div>",
                unsafe_allow_html=True,
            )

        with cons_mid:
            st.markdown(
                '<div class="section-hd fade-in-d1" style="margin-top:0">Price Targets (5d)</div>',
                unsafe_allow_html=True,
            )
            for label, val, color in [
                ("Bull", f"${c.bull_target:.2f}", "#26a69a"),
                ("Base", f"${c.base_target:.2f}", "#d1d4dc"),
                ("Bear", f"${c.bear_target:.2f}", "#ef5350"),
            ]:
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0">'
                    f'<span style="color:#787b86">{label}</span>'
                    f'<span style="font-family:\'JetBrains Mono\',monospace;color:{color};font-weight:500">{val}</span></div>',
                    unsafe_allow_html=True,
                )

        with cons_right:
            st.markdown(
                '<div class="section-hd fade-in-d2" style="margin-top:0">Consensus</div>',
                unsafe_allow_html=True,
            )
            target_color = "#26a69a" if delta_pct >= 0 else "#ef5350"
            cv = c.conviction_score
            cv_color = "#26a69a" if cv >= 67 else ("#d29922" if cv >= 34 else "#ef5350")
            cv_tier = "HIGH" if cv >= 67 else ("MOD" if cv >= 34 else "LOW")
            st.markdown(
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:24px;font-weight:700;color:{target_color}">'
                f"${c.consensus_target:.2f}</div>"
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#787b86;margin-top:2px">'
                f'{delta_sign}{delta_pct:.1f}% vs ${current_price:.2f}</div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:{cv_color};margin-top:6px;font-weight:600">'
                f'{cv} <span style="font-size:9px;font-weight:400">{cv_tier}</span></div>',
                unsafe_allow_html=True,
            )
            if c.credible_low:
                entropy_html = (
                    f' <span style="color:#ef5350;font-size:8px">⚠ {c.entropy_label}</span>'
                    if c.entropy_label else ""
                )
                st.markdown(
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:9px;color:#d1d4dc;margin-top:4px">'
                    f"90% CI: ${c.credible_low:.2f} – ${c.credible_high:.2f}{entropy_html}</div>",
                    unsafe_allow_html=True,
                )
            if c.disagreement:
                st.markdown(
                    f'<div style="font-size:9px;color:#787b86;margin-top:4px;'
                    f'border-left:2px solid #787b86;padding-left:6px">'
                    f"⚠ Split: {c.disagreement_detail}</div>",
                    unsafe_allow_html=True,
                )

        # Regime + pipeline
        upw_str = ", ".join(c.upweighted_agents) if c.upweighted_agents else "none"
        regime_display = c.regime_label.replace("_", " ").upper()
        st.markdown(
            f'<div class="regime-badge">'
            f'REGIME: <span style="color:#d1d4dc">{regime_display}</span>'
            f' &nbsp;·&nbsp; Upweighted: <span style="color:#d1d4dc">{upw_str}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="pipeline-label">'
            'BL Prior → Copula Correction → Regime Weights → Entropy Adjustment → Kelly Sizing'
            '</div>',
            unsafe_allow_html=True,
        )

        # Agent config
        agent_names = list(AGENT_PERSONAS.keys())
        agent_roles = {
            "Macro Strategist": "Fed · rates · DXY",
            "Momentum Analyst": "RSI · MACD · trend",
            "Sentiment Analyst": "VIX · fear/greed",
            "Quant Modeler": "Vol · stats",
            "Earnings Analyst": "Tech · DCF",
        }
        accent_colors = {"bullish": "#26a69a", "bearish": "#ef5350", "neutral": "#787b86"}
        dir_symbols = {"bullish": "▲", "bearish": "▼", "neutral": "◆"}
        dir_cls = {"bullish": "bull", "bearish": "bear", "neutral": "neu"}

        # Agent Summary Strip
        st.markdown(
            '<div style="display:flex;justify-content:space-between;align-items:baseline;margin:12px 0 6px">'
            '<span style="font-size:9px;color:#787b86;text-transform:uppercase;letter-spacing:0.8px;font-weight:600">Agent Summary</span>'
            '<span style="font-family:\'JetBrains Mono\',monospace;font-size:8px;color:#555">R3 FINAL</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        _summary_html = '<div style="display:flex;gap:6px;margin-bottom:10px">'
        for i, name in enumerate(agent_names):
            _f = sim.rounds[2][i]
            _delay_cls = f"fade-in-d{i}" if i < 5 else "fade-in"
            if _f.status == "ok":
                _sc = "#26a69a" if _f.direction == "bullish" else "#ef5350" if _f.direction == "bearish" else "#787b86"
                _sym = "▲" if _f.direction == "bullish" else "▼" if _f.direction == "bearish" else "◆"
                _stmt = _f.reasoning.split(". ")[0][:65]
                _summary_html += (
                    f'<div class="summary-card {_delay_cls}" style="border-top:2px solid {_sc}">'
                    f'<div style="font-size:9px;color:#787b86;margin-bottom:3px">{name}</div>'
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:{_sc};font-weight:600;margin-bottom:4px">'
                    f'{_sym} {_f.direction.capitalize()}</div>'
                    f'<div style="font-size:8.5px;color:#555;line-height:1.35">{_stmt}</div>'
                    f'</div>'
                )
            else:
                _summary_html += (
                    f'<div class="summary-card {_delay_cls}" style="border-top:2px solid #555">'
                    f'<div style="font-size:9px;color:#787b86;margin-bottom:3px">{name}</div>'
                    f'<div style="font-size:10px;color:#787b86;font-weight:700;margin-bottom:4px">✕ Error</div>'
                    f'<div style="font-size:8.5px;color:#555;line-height:1.35">&nbsp;</div>'
                    f'</div>'
                )
        _summary_html += '</div>'
        st.markdown(_summary_html, unsafe_allow_html=True)

        # Round selector
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
        cols = st.columns(5, gap="small")
        forecasts = sim.rounds[round_idx]
        for i, (col, name) in enumerate(zip(cols, agent_names)):
            f: ForecastResult = forecasts[i]
            with col:
                accent = accent_colors.get(f.direction, "#787b86") if f.status == "ok" else "#787b86"
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
  <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:4px">
    <span class="agent-dir {dir_c}">{dir_sym} {f.direction.capitalize() if f.status=='ok' else 'Error'}</span>
    <span class="agent-conf">{conf_pct}%</span>
  </div>
  <div style="height:2px;background:#2a2a2e;border-radius:1px;margin-bottom:6px">
    <div style="height:100%;width:{conf_pct}%;background:{accent};border-radius:1px;transition:width 600ms cubic-bezier(0.22,1,0.36,1)"></div>
  </div>
  {target_html}
  <div class="agent-reasoning">{f.reasoning}</div>
  {revised_html}{error_html}
</div>""",
                    unsafe_allow_html=True,
                )


# ── Right column: Ask an Agent ─────────────────────────────────────────────────
with right:
    st.markdown('<div style="height:30px"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-hd" style="margin-top:20px">Ask an Agent</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.simulation is None:
        st.markdown(
            '<div style="font-size:10px;color:#555;padding:16px 0;text-align:center">'
            'Run a prediction to ask agents about their reasoning.</div>',
            unsafe_allow_html=True,
        )
    else:
        _agent_names = list(AGENT_PERSONAS.keys())
        _valid_agents = [
            name for i, name in enumerate(_agent_names)
            if st.session_state.simulation.rounds[2][i].status == "ok"
        ]

        if not _valid_agents:
            st.markdown(
                '<div style="font-size:10px;color:#787b86;padding:12px 0">'
                'No agents available.</div>',
                unsafe_allow_html=True,
            )
        else:
            selected_agent = st.selectbox(
                "Agent", _valid_agents, label_visibility="collapsed", key="ask_agent_select"
            )
            agent_idx = _agent_names.index(selected_agent)
            r3 = st.session_state.simulation.rounds[2][agent_idx]

            _stance = st.session_state.debate_stances.get(selected_agent)
            if _stance:
                _dir = _stance["direction"]
                _conf = _stance["confidence"]
                _tl = _stance["target_low"]
                _th = _stance["target_high"]
                _reason = _stance["reasoning"]
                _rev = _stance.get("revision_count", 0)
            else:
                _dir = r3.direction
                _conf = r3.confidence
                _tl = r3.target_low
                _th = r3.target_high
                _reason = r3.reasoning
                _rev = 0

            _stance_color = "#26a69a" if _dir == "bullish" else "#ef5350" if _dir == "bearish" else "#787b86"
            _stance_sym = "▲" if _dir == "bullish" else "▼" if _dir == "bearish" else "◆"
            _conf_pct = int(_conf * 100)
            _rev_badge = (
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:8px;color:#d1d4dc;'
                f'background:#2a2a2e;border-radius:3px;padding:1px 6px;margin-left:8px">REVISED ×{_rev}</span>'
            ) if _rev > 0 else ''

            st.markdown(
                f'<div class="stance-card">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
                f'<div style="display:flex;align-items:center;gap:6px">'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;font-weight:600;color:{_stance_color}">'
                f'{_stance_sym} {_dir.capitalize()}</span>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:9px;color:#787b86">{_conf_pct}%</span>'
                f'{_rev_badge}'
                f'</div>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:9px;color:#d1d4dc">${_tl:.0f}–${_th:.0f}</span>'
                f'</div>'
                f'<div style="height:3px;background:#2a2a2e;border-radius:2px;margin-bottom:8px">'
                f'<div style="height:100%;width:{_conf_pct}%;background:{_stance_color};border-radius:2px;'
                f'transition:width 600ms cubic-bezier(0.22,1,0.36,1)"></div></div>'
                f'<div style="font-size:10px;color:#8b949e;line-height:1.5;'
                f'border-left:2px solid {_stance_color};padding-left:8px">{_reason}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            chat_key = f"ask_{selected_agent}"
            if chat_key not in st.session_state.chat_history:
                st.session_state.chat_history[chat_key] = []

            if st.session_state.chat_history[chat_key]:
                _thread = ""
                for msg in st.session_state.chat_history[chat_key]:
                    if msg["role"] == "user":
                        _thread += (
                            f'<div class="chat-msg-user">'
                            f'<div class="chat-role">You</div>{msg["content"]}</div>'
                        )
                    elif msg["role"] == "revision":
                        _old = msg.get("old_direction", "").capitalize()
                        _new = msg.get("new_direction", "").capitalize()
                        _new_color = (
                            "#26a69a" if msg.get("new_direction") == "bullish"
                            else "#ef5350" if msg.get("new_direction") == "bearish"
                            else "#787b86"
                        )
                        _thread += (
                            f'<div class="chat-msg-revision">'
                            f'<div class="chat-role">↻ STANCE REVISED</div>'
                            f'<span style="color:#787b86">{_old}</span>'
                            f' → <span style="color:{_new_color};font-weight:700">{_new}</span>'
                            f'  <span style="font-family:\'JetBrains Mono\',monospace;color:#8b949e">'
                            f'{int(msg.get("confidence", 0)*100)}%</span>'
                            f'  <span style="font-family:\'JetBrains Mono\',monospace;color:#d1d4dc">'
                            f'${msg.get("target_low", 0):.0f}–${msg.get("target_high", 0):.0f}</span>'
                            f'</div>'
                        )
                    else:
                        _thread += (
                            f'<div class="chat-msg-agent">'
                            f'<div class="chat-role">{selected_agent}</div>{msg["content"]}</div>'
                        )
                st.markdown(
                    f'<div class="tv-news-scroll" style="max-height:300px">{_thread}</div>',
                    unsafe_allow_html=True,
                )

            question = st.text_input(
                "Ask", placeholder="Ask about this agent's reasoning…",
                label_visibility="collapsed", key="ask_input"
            )
            _ask_disabled = st.session_state.ask_in_flight
            if st.button("Ask", key="ask_btn", disabled=_ask_disabled) and question.strip():
                import json as _json
                from anthropic import Anthropic
                from agents import AGENT_PERSONAS as personas

                st.session_state.ask_in_flight = True

                _base_system = personas[selected_agent]["system"]
                _ask_system = _base_system + """

A human trader wants to understand your forecast in more depth.
Explain your reasoning clearly and specifically. Reference the data, indicators,
and market conditions that informed your view.

If the human presents a compelling counter-argument with evidence that genuinely
changes your analysis, you may update your stance — but only if warranted.

At the END of every response, you MUST include a JSON block in this exact format:
```json
{"stance_update": {"changed": false}}
```
If your view has genuinely changed based on new reasoning, use:
```json
{"stance_update": {"changed": true, "direction": "bullish|bearish|neutral", "confidence": 0.0, "target_low": 0, "target_high": 0, "reasoning": "Brief updated reasoning"}}
```
Keep responses concise and specific (2-3 sentences max before the JSON block)."""

                prior_forecast = (
                    f"Your current forecast: direction={_dir}, "
                    f"confidence={_conf:.0%}, target=${_tl:.0f}–${_th:.0f}, "
                    f'reasoning="{_reason}"'
                )
                messages = [
                    {"role": "user", "content": prior_forecast},
                    {"role": "assistant", "content": "Understood. I stand by this forecast based on my analysis."},
                ]
                for msg in st.session_state.chat_history[chat_key]:
                    if msg["role"] in ("user", "assistant"):
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"],
                        })
                messages.append({"role": "user", "content": question})

                try:
                    aclient = Anthropic()
                    with st.spinner("…"):
                        resp = aclient.messages.create(
                            model="claude-sonnet-4-6",
                            max_tokens=400,
                            system=_ask_system,
                            messages=messages,
                        )
                    answer = resp.content[0].text
                except Exception:
                    answer = None

                st.session_state.ask_in_flight = False

                if answer is None:
                    st.session_state.chat_history[chat_key].append({"role": "user", "content": question})
                    st.session_state.chat_history[chat_key].append({
                        "role": "assistant",
                        "content": "⚠ Agent unavailable — try again.",
                    })
                else:
                    _display_answer = answer
                    _revision_event = None
                    try:
                        _json_start = answer.rfind("```json")
                        if _json_start != -1:
                            _json_end = answer.find("```", _json_start + 7)
                            _json_str = answer[_json_start + 7:_json_end].strip()
                            _display_answer = answer[:_json_start].strip()
                            _update = _json.loads(_json_str)
                            if _update.get("stance_update", {}).get("changed"):
                                _su = _update["stance_update"]
                                _prev_rev = st.session_state.debate_stances.get(
                                    selected_agent, {}
                                ).get("revision_count", 0)
                                st.session_state.debate_stances[selected_agent] = {
                                    "direction": _su["direction"],
                                    "confidence": _su["confidence"],
                                    "target_low": _su["target_low"],
                                    "target_high": _su["target_high"],
                                    "reasoning": _su["reasoning"],
                                    "revision_count": _prev_rev + 1,
                                }
                                _revision_event = {
                                    "role": "revision",
                                    "old_direction": _dir,
                                    "new_direction": _su["direction"],
                                    "confidence": _su["confidence"],
                                    "target_low": _su["target_low"],
                                    "target_high": _su["target_high"],
                                }
                    except Exception:
                        pass

                    st.session_state.chat_history[chat_key].append({"role": "user", "content": question})
                    st.session_state.chat_history[chat_key].append({"role": "assistant", "content": _display_answer})
                    if _revision_event:
                        st.session_state.chat_history[chat_key].append(_revision_event)

                st.rerun()


# ── Simulation runner ──
if predict_clicked:
    _auto_scenario = news_mod.build_scenario_from_news(
        st.session_state.get("digest_cache", {}),
        st.session_state.news_cache,
        regime,
    )
    seed = {
        "ticker": TICKER,
        "scenario": _auto_scenario,
        "price_history": df,
        "current_price": current_price,
        "current_indicators": ind,
        "macro_context": macro,
        "regime": regime,
        "analogues": ana_mod.find_analogues(df_5y, _auto_scenario, regime),
        "live_news": st.session_state.news_cache,
        "live_news_text": news_mod.format_for_agents(st.session_state.news_cache),
        "live_quote": st.session_state.live_quote_cache,
        "earnings_calendar": st.session_state.key_dates_cache
            and [e for e in st.session_state.key_dates_cache if e["type"] == "earnings"],
        "economic_calendar": st.session_state.key_dates_cache
            and [e for e in st.session_state.key_dates_cache if e["type"] in ("economic", "fomc")],
        "analyst_consensus": st.session_state.consensus_cache,
        "key_dates": st.session_state.key_dates_cache,
    }
    st.session_state.seed = seed
    st.session_state.chat_history = {}
    st.session_state.debate_stances = {}
    st.session_state.active_round = 2
    with st.spinner("Running prediction — 3 rounds × 5 agents…"):
        result = run_simulation(seed)
    st.session_state.simulation = result
    hist_mod.save_prediction(seed, result)
    st.rerun()


