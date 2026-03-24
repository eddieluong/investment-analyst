#!/usr/bin/env python3
"""
Portfolio Screener — Scan thị trường → đề xuất danh mục mới tối ưu.

Scan TradingView tìm top assets theo score, phân bổ theo risk profile.

Usage:
  python3 portfolio_screener.py --capital 500000000 --risk balanced --markets vn,us,crypto,gold --horizon medium
  python3 portfolio_screener.py --capital 200000000 --risk conservative --markets vn,gold --horizon long
  python3 portfolio_screener.py --capital 1000000000 --risk aggressive --markets vn,us,crypto,gold --horizon short
"""

import urllib.request, json, sys, argparse, math
from datetime import datetime

RF_RATE = 0.055  # risk-free VN

# ── Risk Profile Allocation Templates ──

ALLOCATION_TEMPLATES = {
    "conservative": {
        "label": "🛡️ Bảo thủ (Conservative)",
        "description": "Ưu tiên bảo toàn vốn, tăng trưởng ổn định",
        "allocation": {
            "bonds_cash": 0.50,    # Trái phiếu / tiền gửi
            "blue_chip": 0.30,     # Blue chip ổn định
            "gold": 0.15,          # Vàng phòng hộ
            "crypto": 0.05,        # Crypto nhỏ
        },
        "expected_return": {"bear": 0.04, "base": 0.08, "bull": 0.12},
        "max_single": 0.15,
    },
    "balanced": {
        "label": "⚖️ Cân bằng (Balanced)",
        "description": "Cân bằng tăng trưởng và ổn định",
        "allocation": {
            "blue_chip": 0.30,     # Blue chip
            "growth": 0.25,        # Growth stocks
            "gold": 0.20,          # Vàng
            "etf": 0.15,           # ETF
            "crypto": 0.10,        # Crypto
        },
        "expected_return": {"bear": 0.06, "base": 0.14, "bull": 0.22},
        "max_single": 0.20,
    },
    "aggressive": {
        "label": "🔥 Tích cực (Aggressive)",
        "description": "Tối đa tăng trưởng, chấp nhận rủi ro cao",
        "allocation": {
            "growth": 0.35,        # Growth stocks
            "crypto": 0.25,        # Crypto
            "midcap": 0.20,        # Midcap tiềm năng
            "forex_commodities": 0.15,  # Forex & Commodities
            "commodities": 0.05,   # Commodities khác
        },
        "expected_return": {"bear": -0.05, "base": 0.20, "bull": 0.40},
        "max_single": 0.25,
    },
}

# ── Horizon configs ──

HORIZON_CONFIGS = {
    "short": {"label": "Ngắn hạn (< 3 tháng)", "prefer_liquid": True, "dca_months": 1,
              "weight_momentum": 0.6, "weight_value": 0.2, "weight_trend": 0.2},
    "medium": {"label": "Trung hạn (3-12 tháng)", "prefer_liquid": False, "dca_months": 3,
               "weight_momentum": 0.3, "weight_value": 0.4, "weight_trend": 0.3},
    "long": {"label": "Dài hạn (> 1 năm)", "prefer_liquid": False, "dca_months": 6,
             "weight_momentum": 0.1, "weight_value": 0.5, "weight_trend": 0.4},
}

# ── Market Scanner Configs ──

MARKET_SCANNERS = {
    "vn": {
        "url": "https://scanner.tradingview.com/vietnam/scan",
        "label": "🇻🇳 Cổ phiếu Việt Nam",
        "categories": ["blue_chip", "growth", "midcap"],
        "filter_blue_chip": {
            "filter": [
                {"left": "exchange", "operation": "in_range", "right": ["HOSE"]},
                {"left": "market_cap_basic", "operation": "greater", "right": 30_000_000_000_000},
                {"left": "volume", "operation": "greater", "right": 500_000},
            ],
        },
        "filter_growth": {
            "filter": [
                {"left": "exchange", "operation": "in_range", "right": ["HOSE", "HNX"]},
                {"left": "market_cap_basic", "operation": "in_range", "right": [10_000_000_000_000, 50_000_000_000_000]},
                {"left": "volume", "operation": "greater", "right": 300_000},
            ],
        },
        "filter_midcap": {
            "filter": [
                {"left": "exchange", "operation": "in_range", "right": ["HOSE", "HNX"]},
                {"left": "market_cap_basic", "operation": "in_range", "right": [3_000_000_000_000, 15_000_000_000_000]},
                {"left": "volume", "operation": "greater", "right": 200_000},
            ],
        },
        "columns": ["name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "BB.upper",
                    "price_52_week_high", "price_52_week_low",
                    "Perf.W", "Perf.1M", "Perf.3M", "Perf.6M", "Perf.Y",
                    "Volatility.D", "price_earnings_ttm", "market_cap_basic"],
        "currency": "VND",
    },
    "us": {
        "url": "https://scanner.tradingview.com/america/scan",
        "label": "🇺🇸 US Equities & ETF",
        "categories": ["blue_chip", "growth", "etf"],
        "filter_blue_chip": {
            "filter": [
                {"left": "exchange", "operation": "in_range", "right": ["NASDAQ", "NYSE"]},
                {"left": "market_cap_basic", "operation": "greater", "right": 100_000_000_000},
                {"left": "volume", "operation": "greater", "right": 2_000_000},
            ],
        },
        "filter_growth": {
            "filter": [
                {"left": "exchange", "operation": "in_range", "right": ["NASDAQ", "NYSE"]},
                {"left": "market_cap_basic", "operation": "in_range", "right": [10_000_000_000, 200_000_000_000]},
                {"left": "volume", "operation": "greater", "right": 1_000_000},
            ],
        },
        "filter_etf": {
            "filter": [
                {"left": "exchange", "operation": "in_range", "right": ["AMEX", "NASDAQ"]},
                {"left": "is_primary", "operation": "equal", "right": True},
                {"left": "volume", "operation": "greater", "right": 1_000_000},
            ],
            "symbols": {"tickers": [
                "AMEX:VOO", "AMEX:SPY", "NASDAQ:QQQ", "AMEX:VTI", "AMEX:IVV",
                "AMEX:VT", "NASDAQ:BND", "AMEX:GLD", "AMEX:XLE", "NASDAQ:SOXX",
                "AMEX:VWO", "AMEX:ARKK", "AMEX:IEMG", "AMEX:VNM",
            ]},
        },
        "columns": ["name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "BB.upper",
                    "price_52_week_high", "price_52_week_low",
                    "Perf.W", "Perf.1M", "Perf.3M", "Perf.6M", "Perf.Y",
                    "Volatility.D", "price_earnings_ttm", "market_cap_basic"],
        "currency": "USD",
    },
    "crypto": {
        "url": "https://scanner.tradingview.com/crypto/scan",
        "label": "🪙 Crypto",
        "categories": ["crypto"],
        "filter_crypto": {
            "filter": [
                {"left": "exchange", "operation": "in_range", "right": ["BINANCE"]},
                {"left": "volume", "operation": "greater", "right": 50_000_000},
            ],
        },
        "columns": ["name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "BB.upper",
                    "price_52_week_high", "price_52_week_low",
                    "Perf.W", "Perf.1M", "Perf.3M", "Perf.6M", "Perf.Y",
                    "Volatility.D"],
        "currency": "USD",
    },
    "gold": {
        "url": "https://scanner.tradingview.com/cfd/scan",
        "label": "🥇 Vàng & Kim loại quý",
        "categories": ["gold"],
        "filter_gold": {
            "symbols": {"tickers": ["TVC:GOLD", "TVC:SILVER", "AMEX:GLD", "AMEX:IAU", "AMEX:SLV"]},
        },
        "columns": ["name", "close", "change", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "BB.upper",
                    "price_52_week_high", "price_52_week_low",
                    "Perf.W", "Perf.1M", "Perf.3M", "Perf.6M", "Perf.Y",
                    "Volatility.D"],
        "currency": "USD",
    },
}


def fetch_scanner(url, payload, timeout=15):
    """Fetch TradingView scanner API."""
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  ⚠️ Lỗi kết nối: {e}")
        return {"data": []}


def score_asset(d, columns, horizon_config):
    """Score an asset 0-15 dựa trên technical indicators."""
    col_map = {c: i for i, c in enumerate(columns)}

    def get(name):
        idx = col_map.get(name)
        return d[idx] if idx is not None and idx < len(d) else None

    close = get("close")
    rsi = get("RSI")
    ema200 = get("EMA200")
    macd = get("MACD.macd")
    macd_sig = get("MACD.signal")
    bb_lower = get("BB.lower")
    h52 = get("price_52_week_high")
    l52 = get("price_52_week_low")
    pe = get("price_earnings_ttm")
    perf_3m = get("Perf.3M")
    perf_1y = get("Perf.Y")
    vol_d = get("Volatility.D")

    if close is None:
        return 0, []

    score = 0
    reasons = []

    # RSI score
    if rsi is not None:
        if rsi < 30:
            score += 3; reasons.append(f"RSI cực oversold ({rsi:.0f})")
        elif rsi < 40:
            score += 2; reasons.append(f"RSI oversold ({rsi:.0f})")
        elif rsi > 70:
            score -= 1; reasons.append(f"RSI overbought ({rsi:.0f})")

    # EMA200 trend
    if close and ema200:
        if close > ema200:
            score += 2; reasons.append("Trên EMA200 ✓")
        else:
            score -= 1; reasons.append("Dưới EMA200 ✗")

    # MACD
    if macd is not None and macd_sig is not None:
        if macd > macd_sig:
            score += 1; reasons.append("MACD bullish")

    # Bollinger
    if close and bb_lower and close <= bb_lower * 1.02:
        score += 2; reasons.append("Gần BB Lower")

    # 52W position
    if h52 and l52 and h52 != l52:
        pos52 = (close - l52) / (h52 - l52) * 100
        if pos52 < 20:
            score += 2; reasons.append(f"Gần đáy 52W ({pos52:.0f}%)")
        elif pos52 < 40:
            score += 1

    # P/E value (for stocks)
    if pe is not None and pe > 0:
        if pe < 10:
            score += 2; reasons.append(f"P/E rất rẻ ({pe:.1f})")
        elif pe < 15:
            score += 1; reasons.append(f"P/E hợp lý ({pe:.1f})")
        elif pe > 40:
            score -= 1

    # Momentum (weighted by horizon)
    wm = horizon_config["weight_momentum"]
    if perf_3m is not None:
        if perf_3m > 10:
            score += int(2 * wm)
        elif perf_3m < -20:
            score += int(1 * wm)  # potential bounce

    # Estimate Sharpe-like ratio
    ann_return = (perf_1y / 100.0) if perf_1y else ((perf_3m / 100.0 * 4) if perf_3m else 0)
    ann_vol = (vol_d * math.sqrt(252) / 100.0) if vol_d and vol_d > 0 else 0.3
    sharpe = (ann_return - RF_RATE) / ann_vol if ann_vol > 0 else 0

    return max(score, 0), reasons


def scan_market(market_key, category, limit=15):
    """Scan một market category."""
    config = MARKET_SCANNERS[market_key]
    url = config["url"]
    columns = config["columns"]

    filter_key = f"filter_{category}"
    if filter_key not in config:
        return []

    filter_config = config[filter_key]

    payload = {
        "columns": columns,
        "sort": {"sortBy": "volume", "sortOrder": "desc"},
        "range": [0, limit],
    }

    # Merge filter or symbols
    if "symbols" in filter_config:
        payload["symbols"] = filter_config["symbols"]
    if "filter" in filter_config:
        payload["filter"] = filter_config["filter"]

    data = fetch_scanner(url, payload)
    return data.get("data", []), columns


def estimate_metrics(d, columns):
    """Extract key metrics from scanner data."""
    col_map = {c: i for i, c in enumerate(columns)}

    def get(name):
        idx = col_map.get(name)
        return d[idx] if idx is not None and idx < len(d) else None

    close = get("close")
    perf_1y = get("Perf.Y")
    perf_6m = get("Perf.6M")
    perf_3m = get("Perf.3M")
    vol_d = get("Volatility.D")

    # Annual return estimate
    if perf_1y is not None:
        ann_return = perf_1y / 100.0
    elif perf_6m is not None:
        ann_return = (1 + perf_6m / 100.0) ** 2 - 1
    elif perf_3m is not None:
        ann_return = (1 + perf_3m / 100.0) ** 4 - 1
    else:
        ann_return = 0

    # Volatility estimate
    if vol_d and vol_d > 0:
        ann_vol = vol_d * math.sqrt(252) / 100.0
    else:
        ann_vol = 0.25

    sharpe = (ann_return - RF_RATE) / ann_vol if ann_vol > 0 else 0

    return {
        "close": close,
        "rsi": get("RSI"),
        "ema200": get("EMA200"),
        "pe": get("price_earnings_ttm"),
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "name": get("name"),
        "mcap": get("market_cap_basic"),
    }


def fmt_vnd(value):
    if abs(value) >= 1e9:
        return f"{value/1e9:.2f} tỷ"
    if abs(value) >= 1e6:
        return f"{value/1e6:.1f} triệu"
    return f"{value:,.0f}"


def fmt_price(value, currency="VND"):
    if value is None:
        return "N/A"
    if currency == "VND":
        return f"{value:,.0f}"
    return f"${value:,.2f}"


def main():
    parser = argparse.ArgumentParser(description="Portfolio Screener — Scan & Đề xuất danh mục mới")
    parser.add_argument("--capital", "-c", type=float, required=True, help="Tổng vốn (VND)")
    parser.add_argument("--risk", "-r", choices=["conservative", "balanced", "aggressive"],
                        default="balanced", help="Khẩu vị rủi ro (mặc định: balanced)")
    parser.add_argument("--markets", "-m", default="vn,us,crypto,gold",
                        help="Thị trường: vn,us,crypto,gold (mặc định: tất cả)")
    parser.add_argument("--horizon", "-t", choices=["short", "medium", "long"],
                        default="medium", help="Thời gian đầu tư (mặc định: medium)")
    parser.add_argument("--limit", "-l", type=int, default=10,
                        help="Số mã tối đa mỗi category (mặc định: 10)")
    args = parser.parse_args()

    capital = args.capital
    risk = args.risk
    markets = [m.strip().lower() for m in args.markets.split(",")]
    horizon = args.horizon
    limit = args.limit

    template = ALLOCATION_TEMPLATES[risk]
    horizon_cfg = HORIZON_CONFIGS[horizon]

    print(f"\n{'='*80}")
    print(f"  🔍 PORTFOLIO SCREENER — Scan Thị Trường & Đề Xuất Danh Mục Mới")
    print(f"  Vốn: {fmt_vnd(capital)} | Risk: {template['label']}")
    print(f"  Thị trường: {', '.join(markets)} | Horizon: {horizon_cfg['label']}")
    print(f"  Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*80}")

    print(f"\n  📝 {template['description']}")
    print(f"\n  Phân bổ mục tiêu:")
    for cat, pct in template["allocation"].items():
        cat_labels = {
            "bonds_cash": "📦 Trái phiếu/Tiền gửi",
            "blue_chip": "🏛️ Blue Chip",
            "growth": "🚀 Growth Stocks",
            "gold": "🥇 Vàng",
            "crypto": "🪙 Crypto",
            "etf": "📈 ETF",
            "midcap": "📊 Midcap tiềm năng",
            "forex_commodities": "💱 Forex & Commodities",
            "commodities": "🛢️ Commodities",
        }
        label = cat_labels.get(cat, cat)
        print(f"     {label}: {pct*100:.0f}% (~{fmt_vnd(capital * pct)})")

    # ── Scan each market ──
    all_candidates = {}  # category → [(symbol, score, reasons, metrics)]

    for market in markets:
        if market not in MARKET_SCANNERS:
            print(f"\n  ⚠️ Thị trường '{market}' không hỗ trợ. Bỏ qua.")
            continue

        mkt_config = MARKET_SCANNERS[market]
        print(f"\n{'─'*80}")
        print(f"  ⏳ Đang scan {mkt_config['label']}...")

        for category in mkt_config["categories"]:
            results, columns = scan_market(market, category, limit)

            if not results:
                print(f"     {category}: không có kết quả")
                continue

            scored = []
            for item in results:
                sym = item["s"].split(":")[-1]
                d = item["d"]
                score, reasons = score_asset(d, columns, horizon_cfg)
                metrics = estimate_metrics(d, columns)
                scored.append((sym, score, reasons, metrics, market))

            scored.sort(key=lambda x: x[1], reverse=True)
            top = scored[:5]  # top 5 per category

            if category not in all_candidates:
                all_candidates[category] = []
            all_candidates[category].extend(top)

            # Print scan results
            currency = mkt_config["currency"]
            print(f"\n     📊 Top {category.upper()} ({len(results)} scanned → {len(top)} selected):")
            print(f"     {'Mã':<10} {'Giá':>12} {'RSI':>6} {'Score':>6} {'P/E':>7} {'Sharpe':>7} Lý do")
            print(f"     {'─'*75}")

            for sym, sc, reasons, met, _ in top:
                price_str = fmt_price(met["close"], currency)
                rsi_str = f"{met['rsi']:.0f}" if met.get("rsi") else "—"
                pe_str = f"{met['pe']:.1f}" if met.get("pe") and met["pe"] > 0 else "—"
                sharpe_str = f"{met['sharpe']:.2f}"
                reason_str = ", ".join(reasons[:2]) if reasons else "—"
                print(f"     {sym:<10} {price_str:>12} {rsi_str:>6} {sc:>6} {pe_str:>7} {sharpe_str:>7} {reason_str}")

    # ── Build recommended portfolio ──
    print(f"\n{'='*80}")
    print(f"  🎯 DANH MỤC ĐỀ XUẤT")
    print(f"{'='*80}")

    portfolio = []  # [(ticker, weight_pct, category, reason, metrics, market)]

    allocation = template["allocation"]
    max_single = template["max_single"]

    # Map allocation categories to scanned categories
    category_mapping = {
        "bonds_cash": {"source": None, "fixed": [
            ("BOND_VN", "Trái phiếu/Tiền gửi VN 6-7%/năm"),
        ]},
        "blue_chip": {"source": "blue_chip"},
        "growth": {"source": "growth"},
        "gold": {"source": "gold", "fixed": [
            ("XAUUSD", "Vàng phòng hộ lạm phát & rủi ro"),
        ]},
        "crypto": {"source": "crypto"},
        "etf": {"source": "etf", "fallback_fixed": [
            ("VOO", "S&P 500 ETF — core US exposure"),
            ("QQQ", "NASDAQ 100 — tech/AI exposure"),
        ]},
        "midcap": {"source": "midcap"},
        "forex_commodities": {"source": None, "fixed": [
            ("XAUUSD", "Vàng — safe haven"),
            ("WTI", "Dầu — hưởng lợi Iran tensions"),
        ]},
        "commodities": {"source": None, "fixed": [
            ("WTI", "Dầu WTI — commodity exposure"),
        ]},
    }

    for cat, target_pct in allocation.items():
        if target_pct <= 0:
            continue

        mapping = category_mapping.get(cat, {})
        source = mapping.get("source")

        if source and source in all_candidates and all_candidates[source]:
            # Pick from scanned results
            candidates = all_candidates[source]
            # How many assets for this category
            n_pick = max(1, min(3, int(target_pct / max_single) + 1))
            picked = candidates[:n_pick]

            # Distribute weight
            per_asset = target_pct / n_pick

            for sym, sc, reasons, met, mkt in picked:
                reason = reasons[0] if reasons else f"Top {cat}"
                portfolio.append((sym, per_asset * 100, cat, reason, met, mkt))

        elif "fixed" in mapping:
            # Use fixed allocation
            fixed = mapping["fixed"]
            per_asset = target_pct / len(fixed)
            for ticker, reason in fixed:
                portfolio.append((ticker, per_asset * 100, cat, reason, {}, ""))

        elif "fallback_fixed" in mapping:
            fixed = mapping["fallback_fixed"]
            per_asset = target_pct / len(fixed)
            for ticker, reason in fixed:
                portfolio.append((ticker, per_asset * 100, cat, reason, {}, ""))

    # Normalize weights to 100%
    total_w = sum(w for _, w, *_ in portfolio)
    if total_w > 0 and abs(total_w - 100) > 1:
        portfolio = [(t, w / total_w * 100, *rest) for t, w, *rest in portfolio]

    # Print portfolio
    print(f"\n  {'#':<3} {'Mã':<10} {'Tỷ trọng':>9} {'Giá trị':>14} {'Loại':<15} {'Lý do'}")
    print(f"  {'─'*85}")

    cat_labels = {
        "bonds_cash": "📦 Trái phiếu", "blue_chip": "🏛️ Blue Chip",
        "growth": "🚀 Growth", "gold": "🥇 Vàng", "crypto": "🪙 Crypto",
        "etf": "📈 ETF", "midcap": "📊 Midcap",
        "forex_commodities": "💱 Forex/Comm", "commodities": "🛢️ Commodities",
    }

    total_est_return = 0
    total_est_vol = 0

    for i, (ticker, weight, cat, reason, met, mkt) in enumerate(portfolio, 1):
        value = capital * weight / 100
        cat_str = cat_labels.get(cat, cat)
        print(f"  {i:<3} {ticker:<10} {weight:>8.1f}% {fmt_vnd(value):>14} {cat_str:<15} {reason}")

        # Accumulate portfolio metrics
        ret = met.get("ann_return", 0.06) if met else 0.06
        vol = met.get("ann_vol", 0.15) if met else 0.15
        total_est_return += ret * weight / 100
        total_est_vol += (vol * weight / 100) ** 2

    total_est_vol = math.sqrt(total_est_vol)
    est_sharpe = (total_est_return - RF_RATE) / total_est_vol if total_est_vol > 0 else 0

    # ── Expected Returns ──
    print(f"\n{'─'*80}")
    print(f"  📈 EXPECTED RETURN (ước tính)")
    print(f"{'─'*80}")

    exp = template["expected_return"]

    print(f"\n  Danh mục tổng hợp:")
    print(f"     Expected Return:  {total_est_return*100:+.1f}%/năm")
    print(f"     Volatility (est): {total_est_vol*100:.1f}%/năm")
    print(f"     Sharpe Ratio:     {est_sharpe:.2f}")

    print(f"\n  Kịch bản lợi nhuận:")
    for years in [1, 3, 5]:
        bear_v = capital * (1 + exp["bear"]) ** years
        base_v = capital * (1 + exp["base"]) ** years
        bull_v = capital * (1 + exp["bull"]) ** years
        print(f"\n  📅 {years} năm:")
        print(f"     🐻 Bear:  {fmt_vnd(bear_v)} ({(bear_v/capital-1)*100:+.1f}%)")
        print(f"     📊 Base:  {fmt_vnd(base_v)} ({(base_v/capital-1)*100:+.1f}%)")
        print(f"     🐂 Bull:  {fmt_vnd(bull_v)} ({(bull_v/capital-1)*100:+.1f}%)")

    # ── DCA Schedule ──
    print(f"\n{'─'*80}")
    print(f"  📅 LỊCH DCA GỢI Ý")
    print(f"{'─'*80}")

    dca_months = horizon_cfg["dca_months"]
    n_batches = max(2, min(6, int(dca_months * 2)))
    batch_amount = capital / n_batches

    print(f"\n  Chia {n_batches} đợt mua, mỗi đợt ~{fmt_vnd(batch_amount)}")
    print(f"  Horizon: {horizon_cfg['label']}")
    print()

    if horizon == "short":
        print(f"  📌 Đợt 1 (Tuần 1):  Mua 50% — ưu tiên mã có RSI < 40")
        print(f"  📌 Đợt 2 (Tuần 2):  Mua 50% còn lại")
        print(f"\n  ⚡ Ngắn hạn: vào nhanh, cut loss nhanh (SL -5%)")
    elif horizon == "medium":
        for batch in range(1, n_batches + 1):
            week = batch * 2
            pct = 100 / n_batches
            if batch == 1:
                note = "Blue chip + Gold trước"
            elif batch == n_batches:
                note = "Growth + Crypto cuối"
            else:
                note = "Chia đều các mã"
            print(f"  📌 Đợt {batch} (Tuần {week}):  ~{fmt_vnd(batch_amount)} ({pct:.0f}%) — {note}")
        print(f"\n  💡 Mua thêm khi RSI giảm < 35. Tránh mua khi RSI > 65.")
    else:  # long
        months = ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6"]
        priorities = [
            "Blue chip VN + US ETF",
            "Thêm Growth stocks",
            "Vàng + Bonds",
            "Crypto (nếu RSI < 40)",
            "Midcap tiềm năng",
            "Cân bằng lại, mua thêm mã yếu",
        ]
        for i in range(min(n_batches, 6)):
            print(f"  📌 {months[i]}:  ~{fmt_vnd(batch_amount)} — {priorities[i]}")
        print(f"\n  💡 Dài hạn: kiên nhẫn, mua đều đặn, review mỗi quý.")

    # ── Risk warnings ──
    print(f"\n{'─'*80}")
    print(f"  ⚠️ LƯU Ý QUAN TRỌNG")
    print(f"{'─'*80}")
    print(f"""
  1. Phân bổ trên là GỢI Ý dựa trên dữ liệu kỹ thuật real-time
  2. CAGR lịch sử ≠ kỳ vọng tương lai (đặc biệt ở giá hiện tại)
  3. Nên research thêm fundamentals trước khi mua
  4. Luôn có stop loss cho mỗi vị thế
  5. Review danh mục mỗi tháng, rebalance mỗi quý
  6. Không all-in — DCA là bạn tốt nhất
""")

    print(f"{'='*80}")
    print(f"  ⚠️ Phân tích mang tính tham khảo, không phải khuyến nghị đầu tư. DYOR.")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
