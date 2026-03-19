---
name: vn-stock-analyst
description: "Phân tích cổ phiếu thị trường chứng khoán Việt Nam (HOSE/HNX/UPCOM). Kết hợp phân tích kỹ thuật real-time (RSI, MACD, EMA, Bollinger Bands) từ TradingView với phân tích cơ bản (P/E, ROE, tăng trưởng ngành). Use when: (1) user asks about Vietnamese stock prices or analysis, (2) user wants to know which stocks to buy, (3) user asks about a specific stock ticker, (4) user wants sector/industry analysis for Vietnam market, (5) user asks about VN-Index trend."
---

# VN Stock Analyst Skill

Analyze Vietnamese stocks (HOSE/HNX/UPCOM) using real-time technical data from TradingView combined with fundamental sector analysis.

---

## Step 1: Real-time Price Fetch (TradingView Scanner API)

The TradingView scanner endpoint works **WITHOUT authentication**:

```
POST https://scanner.tradingview.com/vietnam/scan
Content-Type: application/json
```

### Fetch specific tickers:

```python
import urllib.request, json

payload = {
    "symbols": {"tickers": ["HOSE:FPT", "HOSE:VCB"]},
    "columns": ["name","close","change","change_abs","volume","high","low","open",
                "RSI","EMA20","EMA50","EMA200","MACD.macd","MACD.signal",
                "BB.upper","BB.lower","ATR","Stoch.K","Stoch.D",
                "price_52_week_high","price_52_week_low"]
}

req = urllib.request.Request(
    "https://scanner.tradingview.com/vietnam/scan",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.loads(r.read())
```

### Scan full market for oversold stocks:

```python
payload = {
    "filter": [
        {"left": "RSI", "operation": "less", "right": 40},
        {"left": "exchange", "operation": "in_range", "right": ["HOSE", "HNX"]}
    ],
    "columns": ["name","close","change","volume","RSI","EMA20","EMA50"],
    "sort": {"sortBy": "RSI", "sortOrder": "asc"},
    "range": [0, 20]
}
```

### Use scripts (preferred):

For **market scan** (oversold opportunities):
```bash
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/scan_market.py [--rsi 40] [--exchange HOSE] [--limit 20]
```

For **single stock deep analysis**:
```bash
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/analyze_stock.py FPT [HOSE]
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/analyze_stock.py VCB HOSE
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/analyze_stock.py HPG HOSE
```

For **return estimation** (CAGR, scenarios, comparison):
```bash
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py FPT
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py VCB --capital 100
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py HPG --capital 50 --years 3
```

Run these via `exec` tool. The scripts handle all API calls and signal computation.

---

## Step 2: Technical Signal Interpretation

For each stock, compute and interpret these signals:

### RSI (Relative Strength Index)
- `RSI < 35` → 🟢 **Oversold** — potential buy
- `RSI > 65` → 🔴 **Overbought** — consider taking profit
- `35 ≤ RSI ≤ 65` → 🟡 **Neutral**

### EMA Trend
Compare `close` vs `EMA20`, `EMA50`, `EMA200`:
- Above all 3 EMA → **Strong uptrend** ▲▲▲
- Above EMA200 only → Long-term uptrend, short-term correction (accumulation zone)
- Below all 3 EMA → **Strong downtrend** ▼▼▼

### MACD
- `macd > signal` → 🟢 **Bullish crossover**
- `macd < signal` → 🔴 **Bearish crossover**

### Bollinger Bands
- `close ≤ BB.lower` → Price at lower band = **potential reversal** 🟢
- `close ≥ BB.upper` → Price at upper band = **overbought zone** 🔴

### Stochastic
- `K < 20` → Oversold
- `K > 80` → Overbought

### 52-Week Position
```
position = (close - low52w) / (high52w - low52w) * 100
```
- < 30% → Near 52W low (potential value zone)
- > 70% → Near 52W high (momentum or resistance)

### 🎯 Buy Zone Criteria (all 3 should be true)
1. `RSI < 40` — Oversold
2. `close > EMA200` — Long-term uptrend intact
3. `close ≤ BB.lower × 1.03` — Near or below Bollinger lower band

---

## Step 3: Fundamental Analysis Framework

Reference `references/sector-fundamentals.md` for sector-specific data.

### Key metrics to discuss:
| Metric | Good | Excellent |
|--------|------|-----------|
| **ROE** | > 15% | > 20% |
| **P/E** | Compare to sector avg | Compare to historical |
| **Revenue growth** | > 10% YoY | > 20% YoY |
| **Debt/Equity** | < 1.0 | < 0.5 |
| **Dividend yield** | > 3% | > 5% |

Always contextualize P/E against sector average (see `references/sector-fundamentals.md`).

---

## Step 4: Return Estimation (Ước tính Lợi nhuận)

Reference `references/return-estimation.md` for full methodology. Use `scripts/estimate_returns.py` to automate.

### Quick run:
```bash
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py FPT
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py VCB --capital 100
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py HPG --capital 50 --years 3
```

### What the script computes:
1. **Fetches 5 years daily price history** from VNDirect dChart API (no auth required)
2. **Historical metrics**: 3M/6M/1Y return, 3Y/5Y CAGR, annual volatility, max drawdown, Sharpe Ratio
3. **Three scenarios** based on historical CAGR ± volatility:
   - 🐻 **Bear**: `max(5.5%, CAGR₃ᵧ − 1σ)` — pessimistic
   - 📊 **Base**: `CAGR₃ᵧ` — mean reversion
   - 🐂 **Bull**: `CAGR₃ᵧ + 0.5σ` — optimistic
4. **Comparison table**: vs. bank deposit (5.5%/yr) and VN-Index (~11%/yr)
5. **Risk label** based on Sharpe Ratio

### When fetching fails (VNDirect down):
Use manual estimation based on sector CAGR from `references/sector-fundamentals.md`:
- Banking blue chips: ~12–15%/năm (Base)
- Technology (FPT): ~20%/năm (Base)
- Steel (HPG): ~10–18%/năm cyclical, high volatility
- Consumer (VNM): ~8–12%/năm, lower risk

---

## Step 5: Output Format

Always structure your analysis as:

```
## 📊 [TICKER] — [Company Name]
Giá: X,XXX VND | Hôm nay: +/-X.XX%
Volume: XM cổ phiếu

### Kỹ thuật
RSI: XX.X [signal emoji]
Trend: EMA20 [▲/▼] | EMA50 [▲/▼] | EMA200 [▲/▼]
MACD: [🟢 Bullish / 🔴 Bearish]
Bollinger: [position relative to bands]
52W: High X,XXX | Low X,XXX | Vị trí: XX%

### Cơ bản
Ngành: [sector name]
P/E: XX.Xx (ngành: XX-XXx)
ROE: XX%
[Other relevant fundamentals]
Tiềm năng: [key growth drivers]
Rủi ro: [key risks]

### Kết luận
[🟢 VÙNG MUA TỐT / 🟡 THEO DÕI / ⏳ CHỜ THÊM / 🔴 TRÁNH]
[1-2 sentence reasoning]
```

---

## Tips & Notes

- **Exchange prefixes**: HOSE (Ho Chi Minh), HNX (Hanoi), UPCOM
- **Ticker format for API**: `HOSE:FPT`, `HNX:SHB`, etc.
- **VN-Index**: Use ticker `VNINDEX` on HOSE exchange
- **Market hours**: 9:00–11:30 and 13:00–15:00 ICT (UTC+7), Mon–Fri
- **Always mention**: This is analysis assistance, not financial advice. Do your own research (DYOR).
- For sector-specific insights, always reference `references/sector-fundamentals.md`
