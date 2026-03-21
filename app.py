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

# ── Dark terminal CSS ──────────────────────────────────────────────────────────
st.markdown(
    """
<style>
* {
    font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif !important;
}
html, body, [data-testid="stApp"] {
    background-color: #000000 !important;
    color: #d1d4dc !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif !important;
}
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="stColumn"],
.stTabs,
section[data-testid="stSidebar"] > div {
    background-color: #000000 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
    border-right: 1px solid #2a2a2e !important;
    padding-top: 0 !important;
}
[data-testid="stSidebarContent"] { padding: 10px 12px 16px 12px !important; }
[data-testid="stSidebarContent"] > div:first-child { margin-top: -60px !important; }
[data-testid="stSidebar"] .block-container { padding: 0 !important; }
[data-testid="stSidebar"] hr {
    margin: 8px 0 !important;
    border: none !important;
    border-top: 1px solid #2a2a2e !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 4px !important; }
[data-testid="stSidebar"] .stMarkdown { margin: 0 !important; padding: 0 !important; }
[data-testid="stSidebar"] .stTextArea { margin-bottom: 0 !important; }
[data-testid="stSidebar"] [data-testid="stButton"] { margin: 2px 0 !important; display: flex !important; width: auto !important; align-self: flex-start !important; }
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
/* Calendar nav buttons — transparent, icon-only style */
[data-testid="stSidebar"] button[kind="secondary"].cal-nav,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    border: none !important;
    color: #787b86 !important;
    padding: 0 6px !important;
    font-size: 13px !important;
    min-height: unset !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover:not(:disabled) {
    color: #d1d4dc !important;
    background: transparent !important;
    border: none !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:disabled {
    color: #2a2a2e !important;
    cursor: default !important;
    background: transparent !important;
    border: none !important;
}

[data-testid="stHeader"] { background: #000000 !important; border: none !important; }
.block-container { padding: 0.5rem 1rem 1.5rem 1rem !important; max-width: 100% !important; }

/* Topbar */
.topbar {
    background: #1c1c1c;
    border-bottom: 1px solid #2a2a2e;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    font-size: 11px;
    margin: -1rem -1rem 0 -1rem;
}
.topbar-logo { font-weight: 700; letter-spacing: 0.08em; color: #d1d4dc; }
.topbar-div { width: 1px; height: 14px; background: #2a2a2e; display: inline-block; }
.topbar-meta { color: #787b86; }

/* Agent cards */
.agent-card {
    background: #1c1c1c;
    border: 1px solid #2a2a2e;
    border-radius: 3px;
    padding: 10px;
    position: relative;
    height: 100%;
}
.agent-accent { height: 2px; margin: -10px -10px 8px -10px; border-radius: 3px 3px 0 0; }
.agent-name { font-size: 11px; font-weight: 700; color: #d1d4dc; margin-bottom: 1px; }
.agent-role { font-size: 9px; color: #787b86; margin-bottom: 6px; }
.agent-dir {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    font-size: 12px; font-weight: 700;
}
.agent-dir.bull { color: #26a69a; }
.agent-dir.bear { color: #ef5350; }
.agent-dir.neu  { color: #787b86; }
.agent-conf {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    font-size: 10px; color: #787b86;
}
.agent-target {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    font-size: 10px; color: #787b86; margin: 3px 0;
}
.agent-target span { color: #d1d4dc; }
.agent-reasoning {
    font-size: 9px; color: #787b86; line-height: 1.45;
    border-left: 2px solid #2a2a2e; padding-left: 6px; margin-top: 5px;
}
.agent-revised {
    font-size: 8px; color: #787b86;
    border: 1px solid #2a2a2e; background: #1c1c1c;
    border-radius: 2px; padding: 1px 4px; display: inline-block; margin-top: 3px;
}
.agent-error { font-size: 9px; color: #ef5350; margin-top: 4px; }

/* Inputs */
textarea, .stTextArea textarea {
    background: #000000 !important;
    border: 1px solid #2a2a2e !important;
    color: #d1d4dc !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif !important;
    font-size: 12px !important;
    border-radius: 3px !important;
}
textarea:focus { border-color: #3a3a3e !important; }

/* All buttons — grey style, no blue */
.stButton > button {
    background: #2a2a2e !important;
    color: #d1d4dc !important;
    border: 1px solid #3a3a3e !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    border-radius: 3px !important;
    width: 100%;
}
.stButton > button:hover { background: #3a3a3e !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #000000 !important;
    border-color: #2a2a2e !important;
    color: #d1d4dc !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #1c1c1c;
    border: 1px solid #2a2a2e;
    border-radius: 3px;
    padding: 8px 10px;
}
[data-testid="stMetricValue"] {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif !important;
    font-size: 18px !important;
    color: #d1d4dc !important;
}
[data-testid="stMetricLabel"] { font-size: 9px !important; color: #787b86 !important; }

/* Section headers */
.section-hd {
    font-size: 11px; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; color: #787b86;
    margin-top: 0; margin-bottom: 8px;
    overflow: visible; white-space: nowrap; line-height: 1.4;
}
.sidebar-section-hd {
    font-size: 9px; font-weight: 700; letter-spacing: 1.8px;
    text-transform: uppercase; color: #787b86;
    margin: 10px 0 8px 0; padding: 0; line-height: 1;
}

/* Probability bars */
.prob-track {
    height: 3px; background: #2a2a2e; border-radius: 2px;
    margin: 2px 0 6px 0; overflow: hidden;
}
.prob-fill { height: 100%; border-radius: 2px; }

/* Analogue entries */
.analogue { padding: 8px 0 4px 0; border-bottom: 1px solid #2a2a2e; font-size: 10px; line-height: 1; }
.analogue:last-child { border-bottom: none; }
.analogue-date {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    color: #787b86; display: block; margin-bottom: 4px;
}
.analogue-event { color: #d1d4dc; display: block; margin-bottom: 4px; }
.analogue-ret {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    font-weight: 600; display: block;
}

/* Indicator pills */
.ind-pill {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    font-size: 10px; border: 1px solid #2a2a2e; border-radius: 2px;
    padding: 2px 7px; display: inline-block; margin: 2px; background: #1c1c1c;
}
.ind-pill.bull { color: #26a69a; }
.ind-pill.bear { color: #ef5350; }
.ind-pill.neu  { color: #787b86; }

/* Stat rows */
.stat-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 4px 0; font-size: 10px; overflow: visible; line-height: 1;
    border-bottom: 1px solid #2a2a2e;
}
.stat-row:last-child { border-bottom: none; }
.stat-key { color: #787b86; }
.stat-val {
    font-family: 'Trebuchet MS', -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif;
    color: #d1d4dc;
}
.stat-val.up { color: #26a69a; }
.stat-val.dn { color: #ef5350; }

/* Chat */
.chat-msg-user {
    background: #1c1c1c; border: 1px solid #2a2a2e; border-radius: 3px;
    padding: 7px 10px; font-size: 10px; color: #787b86; margin-bottom: 6px;
}
.chat-msg-agent {
    background: #1c1c1c; border: 1px solid #2a2a2e; border-radius: 3px;
    padding: 7px 10px; font-size: 10px; color: #d1d4dc; margin-bottom: 6px;
}
.chat-role {
    font-size: 9px; color: #787b86; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px;
}

/* Progress bar */
.stProgress > div > div > div { background: #2a2a2e !important; }

/* Dividers */
hr { border-color: #2a2a2e !important; margin: 10px 0 !important; }

/* Simulation status */
.sim-status {
    font-size: 9px; color: #787b86;
    line-height: 1.8; padding: 4px 0 5px 0;
    overflow: visible; white-space: normal; min-height: 20px;
}

/* Reduce default Streamlit element gaps */
[data-testid="stVerticalBlock"] { gap: 4px !important; }
.stMarkdown { margin-bottom: 0 !important; }
.stButton { margin-top: 4px !important; margin-bottom: 0 !important; }
.stRadio { margin-bottom: 0 !important; }
.stTextArea { margin-bottom: 4px !important; }
.stSelectbox { margin-bottom: 4px !important; }
.stTextInput { margin-bottom: 4px !important; }

/* Column padding */
[data-testid="column"] { padding: 6px 8px !important; min-width: 0; }

/* News filter: hide radio circles, style as TradingView text tabs */
[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap: 0 !important; flex-wrap: wrap !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 2px 6px !important; cursor: pointer !important; border-radius: 2px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child { display: none !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 10px !important; color: #787b86 !important;
    font-weight: 400 !important; margin: 0 !important; line-height: 1.6 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has([aria-checked="true"]) p {
    color: #d1d4dc !important; font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] { margin-bottom: 4px !important; }

/* Read-more link */
.tv-rm:hover { color: #d1d4dc !important; }

/* Scrollbar */
.tv-news-scroll {
    max-height: 350px; overflow-y: auto;
    scrollbar-width: thin; scrollbar-color: #3a3a3e transparent;
}
.tv-news-scroll::-webkit-scrollbar { width: 4px; }
.tv-news-scroll::-webkit-scrollbar-track { background: transparent; }
.tv-news-scroll::-webkit-scrollbar-thumb { background: #3a3a3e; border-radius: 2px; }

/* Text input (Ask an Agent) */
.stTextInput input {
    background: #000000 !important;
    border: 1px solid #2a2a2e !important;
    color: #d1d4dc !important;
    font-size: 12px !important;
    border-radius: 3px !important;
}
.stTextInput input:focus { border-color: #3a3a3e !important; }

/* Revision system bubble */
.chat-msg-revision {
    background: #0d1f1e;
    border: 1px solid #26a69a;
    border-radius: 3px;
    padding: 7px 10px;
    font-size: 10px;
    color: #d1d4dc;
    margin-bottom: 6px;
}
.chat-msg-revision .chat-role {
    color: #26a69a;
}

/* Responsive: stack right column below centre on narrow screens */
@media (max-width: 900px) {
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        width: 100% !important;
        flex: none !important;
        min-width: 100% !important;
    }
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

# ── News + live data — refresh every 5 minutes, triggered by st_autorefresh ───
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

# Update AI digest (10-min cache handled inside generate_market_digest)
if st.session_state.news_cache:
    st.session_state.digest_cache = news_mod.generate_market_digest(st.session_state.news_cache)

# Auto-build scenario from live news (replaces manual text input)
scenario = news_mod.build_scenario_from_news(
    st.session_state.digest_cache, st.session_state.news_cache, regime
)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Build all sidebar data first
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

    # ── PANEL HEADER — Market Intel title + refresh button ──
    _hdr_col, _ref_col = st.columns([4, 1])
    with _hdr_col:
        st.markdown(
            '<div style="font-size:20px;font-weight:700;color:#d1d4dc;letter-spacing:0.3px;padding:4px 0">'
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

    # ── MARKET PULSE as single HTML block ──
    _pulse = f'''<div style="margin-bottom:16px">
<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#d1d4dc;margin-bottom:8px">MARKET PULSE</div>
<div style="display:flex;align-items:baseline;gap:6px;padding-bottom:8px;border-bottom:1px solid #2a2a2e;margin-bottom:6px">
<span style="font-size:15px;font-weight:700;color:#d1d4dc">${_lq_price:.2f}</span>
<span style="font-size:10px;color:{_lq_color}">{_lq_sign}{_lq_chg:.2f} ({_lq_sign}{_lq_chg_pct:.2f}%)</span>
</div>
<div style="font-size:10px">
<div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">VIX</span><span style="color:#d1d4dc">{vix}</span></div>
<div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">DXY</span><span style="color:#d1d4dc">{dxy}</span></div>
<div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">10Y Yield</span><span style="color:#d1d4dc">{y10}%</span></div>
<div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">Fed Rate</span><span style="color:#d1d4dc">{fed}%</span></div>
<div style="display:flex;justify-content:space-between;padding:3px 0"><span style="color:#787b86">Regime</span><span style="color:#ef5350">{regime}</span></div>
</div>
</div>'''
    st.markdown(_pulse, unsafe_allow_html=True)

    # ── LIVE NEWS ──
    _total_arts = len(st.session_state.news_cache)

    st.markdown(
        f'<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px">'
        f'<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#d1d4dc;margin-bottom:8px">'
        f'QQQ NEWS <span style="font-weight:400;color:#787b86;letter-spacing:0">{_total_arts}</span></div></div>',
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
        st.markdown('<div style="font-size:10px;color:#787b86;padding:4px 0 12px 0">No articles in this category.</div>', unsafe_allow_html=True)
    else:
        _cards = ""
        for _a in _pool[:12]:
            _lb = "border-left:2px solid #26a69a;padding-left:7px;" if _a.sentiment > 0.3 else "border-left:2px solid #ef5350;padding-left:7px;" if _a.sentiment < -0.3 else ""
            _pills = "".join(f'<span style="font-size:8px;color:#787b86;border:1px solid #2a2a2e;border-radius:2px;padding:1px 3px;margin-right:2px">{t}</span>' for t in (_a.tickers or [])[:4])
            _ago = news_mod.time_ago(_a.published)
            _link = f'<a href="{_a.url}" target="_blank" style="font-size:9px;color:#787b86;text-decoration:none;margin-top:3px;display:inline-block">Read more →</a>' if _a.url else ""
            _cards += f'<div style="padding:6px 0;border-bottom:1px solid #2a2a2e;{_lb}"><div style="display:flex;align-items:center;gap:3px;flex-wrap:wrap;margin-bottom:4px">{_pills}<span style="font-size:8px;color:#787b86">{_ago} · {_a.source or ""}</span></div><div style="font-size:12px;color:#d1d4dc;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">{_a.title}</div>{_link}</div>'
        st.markdown(f'<div class="tv-news-scroll">{_cards}</div>', unsafe_allow_html=True)

    # ── KEY DATES — single-month calendar with nav ──
    _kd = st.session_state.key_dates_cache
    import calendar as _cal_mod
    _today = datetime.now()
    _min_year = _today.year - 1 if _today.month > 1 else _today.year - 2
    _min_month = (_today.month - 1) or 12  # one month back but we allow 12 months back total
    # Compute absolute month counts for bound check (months since year 0)
    _now_abs = _today.year * 12 + _today.month
    _sel_abs = st.session_state.cal_year * 12 + st.session_state.cal_month
    _at_min = (_now_abs - _sel_abs) >= 12
    _at_max = (_sel_abs - _now_abs) >= 12

    st.markdown(
        '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:4px">'
        '<div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;'
        'color:#d1d4dc;margin-bottom:6px">KEY DATES</div></div>',
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

    # Legend + event list
    _legend = (
        '<div style="display:flex;gap:8px;margin-top:6px;margin-bottom:6px;flex-wrap:wrap">'
    )
    for _lbl, _lc in [("Earn", "#ef5350"), ("FOMC", "#26a69a"), ("Eco", "#787b86"), ("OpEx", "#d1d4dc")]:
        _legend += f'<span style="font-size:8px;color:{_lc}">● {_lbl}</span>'
    _legend += "</div>"

    # Events filtered to selected month
    _sel_prefix = f"{st.session_state.cal_year:04d}-{st.session_state.cal_month:02d}-"
    _month_events = [e for e in (_kd or []) if (e.get("date") or "").startswith(_sel_prefix)]
    _events_html = ""
    if _month_events:
        for _e in _month_events[:8]:
            _tc = ld_mod._TYPE_COLORS.get(_e["type"], "#787b86")
            _events_html += (
                f'<div style="display:flex;gap:5px;align-items:flex-start;padding:2px 0;'
                f'border-bottom:1px solid #2a2a2e">'
                f'<span style="color:{_tc};font-size:8px;margin-top:2px">●</span>'
                f'<div style="font-size:9px">'
                f'<span style="color:#787b86">{_e["date"]}</span> '
                f'<span style="color:#d1d4dc">{_e["event"]}</span>'
                f'<div style="color:#787b86;font-size:8px">→ {_e["agent"]}</div>'
                f'</div></div>'
            )
    else:
        _events_html = '<div style="font-size:9px;color:#787b86;padding:6px 0">No events this month</div>'

    st.markdown(
        f'{_cal_html}{_legend}'
        f'<div style="margin-bottom:16px">{_events_html}</div>',
        unsafe_allow_html=True,
    )

    # ── INDICATORS as single HTML block ──
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
    _ind_html = '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:16px"><div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#d1d4dc;margin-bottom:8px">INDICATORS</div>'
    for _lbl, _val, _clr in _ind_data:
        _ind_html += f'<div style="display:flex;justify-content:space-between;padding:3px 0;font-size:10px;border-bottom:1px solid #2a2a2e"><span style="color:#787b86">{_lbl}</span><span style="color:{_clr}">{_val}</span></div>'
    _ind_html += '</div>'
    st.markdown(_ind_html, unsafe_allow_html=True)

    # ── ANALYST CONSENSUS as single HTML block ──
    _cons = st.session_state.consensus_cache
    _cons_block = '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:16px"><div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#d1d4dc;margin-bottom:8px">ANALYST CONSENSUS</div>'
    if _cons:
        _cons_block += '<table style="width:100%;font-size:10px;border-collapse:collapse;margin:0 auto"><tr><th style="color:#787b86;text-align:left;padding:3px 0">Sym</th><th style="color:#26a69a;text-align:right;padding:3px 0">Buy</th><th style="color:#787b86;text-align:right;padding:3px 0">Hold</th><th style="color:#ef5350;text-align:right;padding:3px 0">Sell</th><th style="color:#d1d4dc;text-align:right;padding:3px 0">PT</th></tr>'
        for _c in _cons:
            _pt = f"${_c['target_mean']:.0f}" if _c.get("target_mean") else "—"
            _cons_block += f'<tr style="border-top:1px solid #2a2a2e"><td style="color:#d1d4dc;padding:3px 0">{_c["symbol"]}</td><td style="color:#26a69a;text-align:right;padding:3px 0">{_c["buy"]}</td><td style="color:#787b86;text-align:right;padding:3px 0">{_c["hold"]}</td><td style="color:#ef5350;text-align:right;padding:3px 0">{_c["sell"]}</td><td style="color:#d1d4dc;text-align:right;padding:3px 0">{_pt}</td></tr>'
        _cons_block += '</table>'
    else:
        _cons_block += '<div style="font-size:9px;color:#787b86">Loading analyst data…</div>'
    _cons_block += '</div>'
    st.markdown(_cons_block, unsafe_allow_html=True)

    # ── HISTORICAL ANALOGUES as single HTML block ──
    analogues = ana_mod.find_analogues(df_5y, scenario, regime)
    _ana_block = '<div style="border-top:1px solid #2a2a2e;padding-top:12px;margin-top:8px;margin-bottom:16px"><div style="font-size:9px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#d1d4dc;margin-bottom:8px">HISTORICAL ANALOGUES</div>'
    if analogues:
        for a in analogues:
            _rc = "#26a69a" if a.return_5d > 0 else "#ef5350"
            _rs = "+" if a.return_5d > 0 else ""
            _ana_block += f'<div style="padding:3px 0;border-bottom:1px solid #2a2a2e"><span style="font-size:10px;color:#787b86">{a.date}</span> <span style="font-size:10px;color:#d1d4dc">— {a.event_label[:45]}</span><div style="font-size:10px;color:{_rc}">{_rs}{a.return_5d:.1f}% (5d)</div></div>'
    else:
        _ana_block += '<div style="font-size:10px;color:#787b86">No analogues found</div>'
    _ana_block += '</div>'
    st.markdown(_ana_block, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR — rendered once in main area only
# ══════════════════════════════════════════════════════════════════════════════
_tb_color = "#26a69a" if price_change >= 0 else "#ef5350"
st.markdown(
    f"""
<div class="topbar">
  <span style="font-size:13px;font-weight:700;color:#d1d4dc;letter-spacing:0.5px">Oracle<span style="color:#26a69a">QQQ</span></span>
  <span class="topbar-div"></span>
  <span style="font-weight:700;color:#d1d4dc">{TICKER}</span>
  <span style="font-weight:600;color:{_tb_color}">{current_price:.2f}</span>
  <span style="color:{_tb_color}">{change_sign}{price_change:.2f} ({change_sign}{price_change_pct:.2f}%)</span>
  <span class="topbar-div"></span>
  <span class="topbar-meta">NASDAQ · 1Y daily · Regime: {regime}</span>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN COLUMNS — centre (chart + agents) | right (accuracy + chat)
# ══════════════════════════════════════════════════════════════════════════════
centre, right = st.columns([3, 1], gap="small")

# ── Centre ─────────────────────────────────────────────────────────────────────
with centre:
    fig = charts_mod.build_candlestick(df, ind)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── AI Market Digest ──────────────────────────────────────────────────
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
            f'<div style="background:#1c1c1c;border:1px solid #2a2a2e;border-radius:4px;padding:12px;margin-bottom:8px">'
            f'<div style="font-size:9px;color:#787b86;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">'
            f'AI Market Digest &nbsp;·&nbsp; {_dg_mins}m ago</div>'
            f'<div style="font-size:11px;color:#d1d4dc;line-height:1.55">{_dg["digest"]}</div>'
            f'<div style="margin-top:8px;display:flex;gap:16px;flex-wrap:wrap">'
            f'<span style="font-size:9px;color:{_dg_color}">● {_dg.get("sentiment","Neutral")}</span>'
            f'<span style="font-size:9px;color:#787b86">KEY RISK: {_dg.get("key_risk","")}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="background:#1c1c1c;border:1px solid #2a2a2e;border-radius:4px;'
            'padding:12px;margin-bottom:8px;font-size:10px;color:#787b86">'
            'Generating AI Market Digest…</div>',
            unsafe_allow_html=True,
        )

    predict_clicked = st.button("Predict QQQ Direction", use_container_width=True)

    sim = st.session_state.simulation

    if sim is None or predict_clicked:
        st.markdown(
            '<div style="text-align:center;padding:24px;color:#787b86;font-size:11px">'
            "Review the market digest above, then click Predict QQQ Direction"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        # Status line
        valid_count = sum(1 for f in sim.rounds[2] if f.status == "ok")
        scenario_label = st.session_state.seed["scenario"][:55]
        st.markdown(
            f'<div class="sim-status">'
            f'<span style="color:#26a69a">●</span> Simulation complete &nbsp;·&nbsp; '
            f'{valid_count}/5 agents &nbsp;·&nbsp; <span style="color:#d1d4dc">{scenario_label}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

        # Consensus panel — 5-Layer Institutional Engine
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
            method_badge = ' <span style="color:#d1d4dc;font-size:9px">BAYESIAN</span>' if c.method == "bayesian" else ""
            st.markdown(f'<div class="section-hd" style="margin-top:0">Scenario Probabilities{method_badge}</div>', unsafe_allow_html=True)
            for label, pct, color in [("Bull", bull_pct, "#26a69a"), ("Base", base_pct, "#787b86"), ("Bear", bear_pct, "#ef5350")]:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">'
                    f'<span style="font-size:10px;font-family:Trebuchet MS,-apple-system,BlinkMacSystemFont,Roboto,Ubuntu,sans-serif;width:30px;color:{color}">{label}</span>'
                    f'<div class="prob-track" style="flex:1"><div class="prob-fill" style="width:{pct}%;background:{color}"></div></div>'
                    f'<span style="font-family:Trebuchet MS,-apple-system,BlinkMacSystemFont,Roboto,Ubuntu,sans-serif;font-size:10px;color:#787b86;width:28px;text-align:right">{pct}%</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<div style="font-size:9px;color:#787b86;margin-top:4px">'
                f"{c.agent_count}/5 agents · avg conf {int(c.avg_confidence*100)}%</div>",
                unsafe_allow_html=True,
            )

        with cons_mid:
            st.markdown('<div class="section-hd" style="margin-top:0">Price Targets (5d)</div>', unsafe_allow_html=True)
            for label, val, color in [("Bull", f"${c.bull_target:.2f}", "#26a69a"), ("Base", f"${c.base_target:.2f}", "#d1d4dc"), ("Bear", f"${c.bear_target:.2f}", "#ef5350")]:
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;font-size:10px;padding:3px 0">'
                    f'<span style="color:#787b86">{label}</span>'
                    f'<span style="font-family:Trebuchet MS,-apple-system,BlinkMacSystemFont,Roboto,Ubuntu,sans-serif;color:{color}">{val}</span></div>',
                    unsafe_allow_html=True,
                )

        with cons_right:
            st.markdown('<div class="section-hd" style="margin-top:0">Consensus</div>', unsafe_allow_html=True)
            target_color = "#26a69a" if delta_pct >= 0 else "#ef5350"
            # Conviction Score label
            cv = c.conviction_score
            cv_color = "#26a69a" if cv >= 67 else ("#d29922" if cv >= 34 else "#ef5350")
            cv_tier  = "HIGH" if cv >= 67 else ("MOD" if cv >= 34 else "LOW")
            st.markdown(
                f'<div style="font-family:Trebuchet MS,-apple-system,BlinkMacSystemFont,Roboto,Ubuntu,sans-serif;font-size:22px;font-weight:700;color:{target_color}">'
                f"${c.consensus_target:.2f}</div>"
                f'<div style="font-size:10px;color:#787b86">{delta_sign}{delta_pct:.1f}% vs ${current_price:.2f}</div>'
                f'<div style="font-size:10px;color:{cv_color};margin-top:4px;font-weight:600">'
                f'{cv} <span style="font-size:9px">{cv_tier}</span></div>',
                unsafe_allow_html=True,
            )
            # 90% CI + entropy label
            if c.credible_low:
                entropy_html = (
                    f' <span style="color:#ef5350;font-size:8px">⚠ {c.entropy_label}</span>'
                    if c.entropy_label else ""
                )
                st.markdown(
                    f'<div style="font-size:9px;color:#d1d4dc;margin-top:4px">'
                    f"90% CI: ${c.credible_low:.2f} – ${c.credible_high:.2f}{entropy_html}</div>",
                    unsafe_allow_html=True,
                )
            if c.disagreement:
                st.markdown(
                    f'<div style="font-size:9px;color:#787b86;margin-top:4px;border-left:2px solid #787b86;padding-left:5px">'
                    f"⚠ Split: {c.disagreement_detail}</div>",
                    unsafe_allow_html=True,
                )

        # Full-width regime row + 5-layer liner
        upw_str = ", ".join(c.upweighted_agents) if c.upweighted_agents else "none"
        regime_display = c.regime_label.replace("_", " ").upper()
        st.markdown(
            f'<div style="font-size:9px;color:#787b86;margin-top:10px;padding:6px 8px;'
            f'background:#161b22;border-radius:3px;border:1px solid #2a2a2e">'
            f'REGIME: <span style="color:#d1d4dc">{regime_display}</span>'
            f' &nbsp;·&nbsp; Upweighted: <span style="color:#d1d4dc">{upw_str}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:8px;color:#555;margin-top:5px;letter-spacing:0.3px">'
            'BL Prior → Copula Correction → Regime Weights → Entropy Adjustment → Kelly Sizing'
            '</div>',
            unsafe_allow_html=True,
        )

        # Agent names + config (used by summary strip and agent cards below)
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

        # Agent Summary Strip — always shows R3 Final
        st.markdown(
            '<div style="display:flex;justify-content:space-between;align-items:baseline;margin:10px 0 4px">'
            '<span style="font-size:9px;color:#787b86;text-transform:uppercase;letter-spacing:0.5px">Agent Summary</span>'
            '<span style="font-size:8px;color:#555">R3 FINAL</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        _summary_html = '<div style="display:flex;gap:6px;margin-bottom:10px">'
        for i, name in enumerate(agent_names):
            _f = sim.rounds[2][i]
            if _f.status == "ok":
                _sc = "#26a69a" if _f.direction == "bullish" else "#ef5350" if _f.direction == "bearish" else "#787b86"
                _sym = "▲" if _f.direction == "bullish" else "▼" if _f.direction == "bearish" else "◆"
                _stmt = _f.reasoning.split(". ")[0][:65]
                _summary_html += (
                    f'<div style="flex:1;background:#1c1c1c;border:1px solid #2a2a2e;border-top:2px solid {_sc};'
                    f'border-radius:3px;padding:6px 8px">'
                    f'<div style="font-size:9px;color:#787b86;margin-bottom:2px">{name}</div>'
                    f'<div style="font-size:10px;color:{_sc};font-weight:700;margin-bottom:3px">{_sym} {_f.direction.capitalize()}</div>'
                    f'<div style="font-size:8px;color:#787b86;line-height:1.3">{_stmt}</div>'
                    f'</div>'
                )
            else:
                _summary_html += (
                    f'<div style="flex:1;background:#161b22;border:1px solid #2a2a2e;border-top:2px solid #555;'
                    f'border-radius:3px;padding:6px 8px">'
                    f'<div style="font-size:9px;color:#787b86;margin-bottom:2px">{name}</div>'
                    f'<div style="font-size:10px;color:#787b86;font-weight:700;margin-bottom:3px">✕ Error</div>'
                    f'<div style="font-size:8px;color:#555;line-height:1.3">&nbsp;</div>'
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
  <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:3px">
    <span class="agent-dir {dir_c}">{dir_sym} {f.direction.capitalize() if f.status=='ok' else 'Error'}</span>
    <span class="agent-conf">{conf_pct}%</span>
  </div>
  <div style="height:2px;background:#2a2a2e;border-radius:1px;margin-bottom:5px">
    <div style="height:100%;width:{conf_pct}%;background:{accent};border-radius:1px"></div>
  </div>
  {target_html}
  <div class="agent-reasoning">{f.reasoning}</div>
  {revised_html}{error_html}
</div>""",
                    unsafe_allow_html=True,
                )


# ── Right column: Ask an Agent ─────────────────────────────────────────────────
with right:
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-hd" style="margin-top:0">Ask an Agent</div>', unsafe_allow_html=True)

    if st.session_state.simulation is None:
        st.markdown(
            '<div style="font-size:10px;color:#787b86;padding:12px 0">'
            'Run a prediction to ask agents about their reasoning.</div>',
            unsafe_allow_html=True,
        )
    else:
        # Build list of agents with valid forecasts only
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

            # Use debated stance if available, otherwise use round 3 forecast
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
                f'<span style="font-size:8px;color:#d1d4dc;background:#2a2a2e;border-radius:2px;'
                f'padding:1px 5px;margin-left:8px">REVISED ×{_rev}</span>'
            ) if _rev > 0 else ''

            st.markdown(
                f'<div style="background:#1c1c1c;border:1px solid #2a2a2e;border-radius:3px;'
                f'padding:10px;margin-bottom:8px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
                f'<div style="display:flex;align-items:center;gap:6px">'
                f'<span style="font-size:11px;font-weight:700;color:{_stance_color}">'
                f'{_stance_sym} {_dir.capitalize()}</span>'
                f'<span style="font-size:9px;color:#787b86">{_conf_pct}%</span>'
                f'{_rev_badge}'
                f'</div>'
                f'<span style="font-size:9px;color:#d1d4dc">${_tl:.0f}–${_th:.0f}</span>'
                f'</div>'
                f'<div style="height:2px;background:#2a2a2e;border-radius:1px;margin-bottom:6px">'
                f'<div style="height:100%;width:{_conf_pct}%;background:{_stance_color};border-radius:1px">'
                f'</div></div>'
                f'<div style="font-size:10px;color:#8b949e;line-height:1.45;'
                f'border-left:2px solid {_stance_color};padding-left:6px">{_reason}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            chat_key = f"ask_{selected_agent}"
            if chat_key not in st.session_state.chat_history:
                st.session_state.chat_history[chat_key] = []

            # Render chat thread
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
                        _new_color = "#26a69a" if msg.get("new_direction") == "bullish" else "#ef5350" if msg.get("new_direction") == "bearish" else "#787b86"
                        _thread += (
                            f'<div class="chat-msg-revision">'
                            f'<div class="chat-role">↻ STANCE REVISED</div>'
                            f'<span style="color:#787b86">{_old}</span>'
                            f' → <span style="color:{_new_color};font-weight:700">{_new}</span>'
                            f'  <span style="color:#8b949e">{int(msg.get("confidence", 0)*100)}%</span>'
                            f'  <span style="color:#d1d4dc">'
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

            # Ask input + button (button disabled while in-flight)
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
                    # Error state: styled chat bubble
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


# ── Simulation runner (outside container to prevent double-render on rerun) ──
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
