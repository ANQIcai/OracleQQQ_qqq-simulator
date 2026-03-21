"""
live_data.py — Real-time market data for OracleQQQ.
Uses Finnhub free-tier endpoints with module-level TTL caching.
"""
import os
import time
import calendar
from datetime import datetime, timedelta, date
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

FINNHUB_KEY = os.getenv("FINNHUB_API_KEY", "")

_BASE = "https://finnhub.io/api/v1"
_HEADERS = {"X-Finnhub-Token": FINNHUB_KEY}

_TOP10 = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "AVGO", "TSLA", "COST", "NFLX"]
_CONSENSUS_SYMBOLS = ["NVDA", "MSFT", "AAPL", "AMZN", "META"]

# ── TTL cache ─────────────────────────────────────────────────────────────────
_cache: dict = {}


def _get(key: str) -> Optional[object]:
    entry = _cache.get(key)
    if entry and time.time() < entry["expires"]:
        return entry["data"]
    return None


def _set(key: str, data, ttl_seconds: int) -> None:
    _cache[key] = {"data": data, "expires": time.time() + ttl_seconds}


def _finnhub_get(path: str, params: dict = None) -> Optional[dict]:
    if not FINNHUB_KEY:
        return None
    try:
        resp = requests.get(
            f"{_BASE}{path}", headers=_HEADERS, params=params or {}, timeout=8
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None


# ── Live quote ────────────────────────────────────────────────────────────────

def get_live_quote(symbol: str = "QQQ") -> dict:
    """Real-time price, change, and change% for any symbol. Cached 1 min."""
    key = f"quote:{symbol}"
    cached = _get(key)
    if cached is not None:
        return cached
    data = _finnhub_get("/quote", {"symbol": symbol})
    if not data:
        return {}
    result = {
        "symbol": symbol,
        "price": data.get("c"),       # current price
        "change": data.get("d"),       # change vs prev close
        "change_pct": data.get("dp"),  # change %
        "high": data.get("h"),
        "low": data.get("l"),
        "open": data.get("o"),
        "prev_close": data.get("pc"),
        "timestamp": data.get("t"),
    }
    _set(key, result, ttl_seconds=60)
    return result


# ── Earnings calendar ─────────────────────────────────────────────────────────

def get_earnings_calendar() -> list:
    """Upcoming earnings for QQQ top 10 holdings. Cached 1 hour."""
    key = "earnings_calendar"
    cached = _get(key)
    if cached is not None:
        return cached
    today = datetime.now().strftime("%Y-%m-%d")
    end = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
    data = _finnhub_get("/calendar/earnings", {"from": today, "to": end})
    if not data or "earningsCalendar" not in data:
        _set(key, [], ttl_seconds=3600)
        return []
    results = []
    for item in data["earningsCalendar"]:
        if item.get("symbol") in _TOP10:
            results.append({
                "symbol": item.get("symbol"),
                "date": item.get("date"),
                "eps_estimate": item.get("epsEstimate"),
                "eps_actual": item.get("epsActual"),
                "revenue_estimate": item.get("revenueEstimate"),
                "quarter": item.get("quarter"),
                "year": item.get("year"),
            })
    results.sort(key=lambda x: x.get("date") or "")
    _set(key, results, ttl_seconds=3600)
    return results


# ── Economic calendar ─────────────────────────────────────────────────────────

_HIGH_IMPACT_EVENTS = {
    "cpi", "consumer price", "nonfarm", "nfp", "fomc", "federal reserve",
    "gdp", "unemployment", "payroll", "pce", "retail sales", "pmi", "ism",
    "rate decision", "interest rate decision",
}


def get_economic_calendar() -> list:
    """Upcoming high-impact US economic events for the next 30 days. Cached 1 hour."""
    key = "economic_calendar"
    cached = _get(key)
    if cached is not None:
        return cached
    today = datetime.now().strftime("%Y-%m-%d")
    end = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    data = _finnhub_get("/calendar/economic", {"from": today, "to": end})
    if not data or "economicCalendar" not in data:
        _set(key, [], ttl_seconds=3600)
        return []
    results = []
    for item in data["economicCalendar"]:
        event_name = (item.get("event") or "").lower()
        country = (item.get("country") or "").upper()
        if country != "US":
            continue
        if not any(kw in event_name for kw in _HIGH_IMPACT_EVENTS):
            continue
        results.append({
            "date": (item.get("time") or "")[:10],
            "time": item.get("time", ""),
            "event": item.get("event"),
            "impact": item.get("impact", ""),
            "actual": item.get("actual"),
            "estimate": item.get("estimate"),
            "previous": item.get("prev"),
        })
    results.sort(key=lambda x: x.get("time") or "")
    _set(key, results, ttl_seconds=3600)
    return results


# ── Analyst recommendations ───────────────────────────────────────────────────

def get_analyst_recommendations(symbol: str) -> dict:
    """Latest buy/hold/sell counts for a symbol. Cached 6 hours."""
    key = f"recs:{symbol}"
    cached = _get(key)
    if cached is not None:
        return cached
    data = _finnhub_get("/stock/recommendation", {"symbol": symbol})
    if not data or not isinstance(data, list) or len(data) == 0:
        return {}
    latest = data[0]
    result = {
        "symbol": symbol,
        "buy": latest.get("buy", 0) or 0,
        "hold": latest.get("hold", 0) or 0,
        "sell": latest.get("sell", 0) or 0,
        "strong_buy": latest.get("strongBuy", 0) or 0,
        "strong_sell": latest.get("strongSell", 0) or 0,
        "period": latest.get("period", ""),
    }
    result["total"] = (
        result["buy"] + result["hold"] + result["sell"]
        + result["strong_buy"] + result["strong_sell"]
    )
    _set(key, result, ttl_seconds=21600)
    return result


# ── Price targets ─────────────────────────────────────────────────────────────

def get_price_targets(symbol: str) -> dict:
    """Analyst price target consensus (high, low, mean, median). Cached 6 hours."""
    key = f"targets:{symbol}"
    cached = _get(key)
    if cached is not None:
        return cached
    data = _finnhub_get("/stock/price-target", {"symbol": symbol})
    if not data:
        return {}
    result = {
        "symbol": symbol,
        "high": data.get("targetHigh"),
        "low": data.get("targetLow"),
        "mean": data.get("targetMean"),
        "median": data.get("targetMedian"),
        "analyst_count": data.get("numberOfAnalysts"),
        "last_updated": data.get("lastUpdated"),
    }
    _set(key, result, ttl_seconds=21600)
    return result


# ── Insider activity ──────────────────────────────────────────────────────────

def get_insider_activity(symbol: str) -> list:
    """Recent insider buys/sells (last 30 days). Cached 6 hours."""
    key = f"insider:{symbol}"
    cached = _get(key)
    if cached is not None:
        return cached
    data = _finnhub_get("/stock/insider-transactions", {"symbol": symbol})
    if not data or "data" not in data:
        _set(key, [], ttl_seconds=21600)
        return []
    results = []
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    for item in (data["data"] or [])[:20]:
        if (item.get("transactionDate") or "") >= cutoff:
            results.append({
                "name": item.get("name"),
                "date": item.get("transactionDate"),
                "type": item.get("transactionCode"),  # P=purchase, S=sale
                "shares": item.get("share"),
                "price": item.get("transactionPrice"),
            })
    _set(key, results, ttl_seconds=21600)
    return results


# ── Key dates ─────────────────────────────────────────────────────────────────

# Known FOMC meeting decision days (second day of each 2-day meeting)
_FOMC_DATES = [
    # 2025
    "2025-01-29", "2025-03-19", "2025-05-07", "2025-06-18",
    "2025-07-30", "2025-09-17", "2025-10-29", "2025-12-10",
    # 2026 — Mar 18-19, May 6-7, Jun 17-18, Jul 29-30, Sep 16-17, Oct 28-29, Dec 9-10
    "2026-01-28", "2026-03-19", "2026-05-07", "2026-06-18",
    "2026-07-30", "2026-09-17", "2026-10-29", "2026-12-10",
]

# Estimated earnings dates (fallback when Finnhub returns nothing).
# Based on typical Q1 reporting windows; shown with "(est.)" suffix.
_EARNINGS_FALLBACK = [
    {"symbol": "TSLA", "date_template": "{year}-04-22", "event": "TSLA Earnings (est.)"},
    {"symbol": "GOOGL", "date_template": "{year}-04-24", "event": "GOOGL Earnings (est.)"},
    {"symbol": "META",  "date_template": "{year}-04-25", "event": "META Earnings (est.)"},
    {"symbol": "MSFT",  "date_template": "{year}-04-28", "event": "MSFT Earnings (est.)"},
    {"symbol": "AAPL",  "date_template": "{year}-04-29", "event": "AAPL Earnings (est.)"},
    {"symbol": "AMZN",  "date_template": "{year}-04-30", "event": "AMZN Earnings (est.)"},
    {"symbol": "NVDA",  "date_template": "{year}-05-21", "event": "NVDA Earnings (est.)"},
]


def _options_expiry_dates(months_ahead: int = 2) -> list:
    """Monthly options expiry = 3rd Friday of each month."""
    dates = []
    now = datetime.now()
    for m_offset in range(months_ahead + 1):
        year = now.year + (now.month - 1 + m_offset) // 12
        month = (now.month - 1 + m_offset) % 12 + 1
        first_day = date(year, month, 1)
        first_friday = first_day + timedelta(days=(4 - first_day.weekday()) % 7)
        third_friday = first_friday + timedelta(weeks=2)
        dates.append(third_friday.strftime("%Y-%m-%d"))
    return dates


def get_all_key_dates() -> list:
    """
    Combine earnings, economic events, FOMC dates, and options expiry into
    a sorted list of upcoming events covering current + next month. Cached 1 hour.
    """
    key = "key_dates"
    cached = _get(key)
    if cached is not None:
        return cached

    today = datetime.now().strftime("%Y-%m-%d")
    # Cover current month + full next month (62 days is always sufficient)
    end = (datetime.now() + timedelta(days=62)).strftime("%Y-%m-%d")
    events = []

    # Earnings — try API first, fall back to estimated dates
    api_earnings = get_earnings_calendar()
    if api_earnings:
        for e in api_earnings:
            d = e.get("date") or ""
            if today <= d <= end:
                eps_str = f"EPS est: {e['eps_estimate']}" if e.get("eps_estimate") else ""
                events.append({
                    "date": d,
                    "event": f"{e['symbol']} Earnings",
                    "type": "earnings",
                    "symbol": e.get("symbol"),
                    "agent": "Earnings Analyst",
                    "detail": eps_str,
                })
    else:
        # Fallback: estimated dates for current year
        year = datetime.now().year
        for fb in _EARNINGS_FALLBACK:
            d = fb["date_template"].format(year=year)
            if today <= d <= end:
                events.append({
                    "date": d,
                    "event": fb["event"],
                    "type": "earnings",
                    "symbol": fb["symbol"],
                    "agent": "Earnings Analyst",
                    "detail": "Estimated date",
                })

    # Economic data
    for e in get_economic_calendar():
        d = e.get("date") or ""
        if today <= d <= end:
            detail = f"Est: {e.get('estimate', 'N/A')} | Prev: {e.get('previous', 'N/A')}"
            events.append({
                "date": d,
                "event": e.get("event", "Economic Release"),
                "type": "economic",
                "agent": "Macro Strategist",
                "detail": detail,
            })

    # FOMC meetings
    for d in _FOMC_DATES:
        if today <= d <= end:
            events.append({
                "date": d,
                "event": "FOMC Decision",
                "type": "fomc",
                "agent": "Macro Strategist",
                "detail": "Federal Reserve rate decision",
            })

    # Options expiry (current + next month)
    for d in _options_expiry_dates(months_ahead=1):
        if today <= d <= end:
            events.append({
                "date": d,
                "event": "Options Expiry",
                "type": "opex",
                "agent": "Quant Modeler",
                "detail": "Monthly options expiration",
            })

    events.sort(key=lambda x: x["date"])
    _set(key, events, ttl_seconds=3600)
    return events


# ── Multi-symbol consensus ────────────────────────────────────────────────────

def get_top_holdings_consensus() -> list:
    """Fetch analyst recs + price targets for top 5 holdings. Cached 6 hours."""
    key = "top_consensus"
    cached = _get(key)
    if cached is not None:
        return cached
    results = []
    for sym in _CONSENSUS_SYMBOLS:
        recs = get_analyst_recommendations(sym)
        targets = get_price_targets(sym)
        quote = get_live_quote(sym)
        if recs or targets:
            results.append({
                "symbol": sym,
                "buy": (recs.get("buy", 0) or 0) + (recs.get("strong_buy", 0) or 0),
                "hold": recs.get("hold", 0) or 0,
                "sell": (recs.get("sell", 0) or 0) + (recs.get("strong_sell", 0) or 0),
                "target_mean": targets.get("mean"),
                "current_price": quote.get("price"),
            })
    _set(key, results, ttl_seconds=21600)
    return results


# ── Calendar HTML renderer ────────────────────────────────────────────────────

_TYPE_COLORS = {
    "earnings": "#ef5350",  # TradingView red
    "fomc": "#26a69a",      # TradingView green
    "economic": "#787b86",  # secondary text
    "opex": "#d1d4dc",      # primary text
}

_TYPE_AGENT = {
    "earnings": "Earnings Analyst",
    "fomc": "Macro Strategist",
    "economic": "Macro Strategist",
    "opex": "Quant Modeler",
}


def _render_month_grid(year: int, month: int, event_map: dict, today_str: str) -> str:
    """Render a single month grid table."""
    first_weekday = date(year, month, 1).weekday()  # 0=Monday
    _, days_in_month = calendar.monthrange(year, month)

    html = (
        f'<div style="color:#787b86;font-size:9px;font-weight:600;letter-spacing:0.5px;'
        f'margin-bottom:4px">{calendar.month_name[month]} {year}</div>'
        '<table style="width:100%;border-collapse:collapse">'
        '<tr>'
    )
    for day_abbr in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        html += f'<th style="color:#787b86;text-align:center;padding:1px 0;font-size:8px">{day_abbr}</th>'
    html += "</tr><tr>"

    col = first_weekday
    for _ in range(first_weekday):
        html += "<td></td>"

    for day_num in range(1, days_in_month + 1):
        date_str = f"{year:04d}-{month:02d}-{day_num:02d}"
        is_today = date_str == today_str
        is_past = date_str < today_str

        num_color = "#3a3a3a" if is_past else "#d1d4dc"
        cell_bg = "background:#2a2a2e;border-radius:3px;" if is_today else ""

        dot_html = ""
        for etype in event_map.get(date_str, []):
            c = _TYPE_COLORS.get(etype, "#787b86")
            dot_html += f'<span style="color:{c};font-size:5px;line-height:1">●</span>'

        html += (
            f'<td style="text-align:center;padding:1px 0;{cell_bg}">'
            f'<div style="color:{num_color};font-size:9px">{day_num}</div>'
        )
        if dot_html:
            html += f'<div style="line-height:1.2">{dot_html}</div>'
        html += "</td>"

        col += 1
        if col == 7:
            html += "</tr><tr>"
            col = 0

    html += "</tr></table>"
    return html


def render_calendar_html(key_dates: list) -> str:
    """Render two month grids (current + next) with colored event dots as an HTML string."""
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    # Build event map for both months
    event_map: dict = {}
    for e in key_dates:
        d = (e.get("date") or "")[:10]
        if d:
            event_map.setdefault(d, []).append(e.get("type", ""))

    # Current month
    cur_year, cur_month = today.year, today.month
    # Next month (handle year rollover)
    if cur_month == 12:
        nxt_year, nxt_month = cur_year + 1, 1
    else:
        nxt_year, nxt_month = cur_year, cur_month + 1

    html = '<div style="font-size:10px">'
    html += _render_month_grid(cur_year, cur_month, event_map, today_str)
    html += '<div style="margin-top:12px">'
    html += _render_month_grid(nxt_year, nxt_month, event_map, today_str)
    html += '</div>'

    # Legend
    html += '<div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">'
    for label, color in [
        ("Earn", "#ef5350"), ("FOMC", "#26a69a"),
        ("Eco", "#787b86"), ("OpEx", "#d1d4dc"),
    ]:
        html += f'<span style="font-size:8px;color:{color}">● {label}</span>'
    html += "</div></div>"

    return html
