# Financial Analysis Knowledge Base
> Tự học & tổng hợp — cập nhật liên tục trong quá trình sử dụng

---

## 1. PHÂN TÍCH KỸ THUẬT (Technical Analysis)

### 1.1 Momentum Indicators

#### RSI — Relative Strength Index
**Công thức:** RSI = 100 - (100 / (1 + RS)) | RS = Avg Gain / Avg Loss (14 kỳ)

| Vùng | Ý nghĩa | Hành động |
|---|---|---|
| < 30 | Oversold cực mạnh | Xem xét mua, tìm điểm đảo chiều |
| 30–40 | Oversold | Bắt đầu theo dõi, DCA |
| 40–60 | Neutral | Giữ nguyên |
| 60–70 | Overbought nhẹ | Cân nhắc chốt lời một phần |
| > 70 | Overbought mạnh | Không thêm vị thế mới |

**Lesson learned:** RSI oversold KHÔNG đảm bảo giá sẽ tăng ngay — có thể oversold và tiếp tục giảm (bearish momentum). Cần kết hợp EMA200.

**RSI Divergence (quan trọng):**
- **Bullish divergence:** Giá tạo đáy mới thấp hơn, RSI tạo đáy cao hơn → tín hiệu đảo chiều tăng mạnh
- **Bearish divergence:** Giá tạo đỉnh mới cao hơn, RSI tạo đỉnh thấp hơn → tín hiệu đảo chiều giảm

#### MACD — Moving Average Convergence Divergence
**Công thức:** MACD = EMA(12) - EMA(26) | Signal = EMA(9) của MACD

| Tín hiệu | Ý nghĩa |
|---|---|
| MACD > Signal | Bullish momentum |
| MACD < Signal | Bearish momentum |
| MACD cắt lên Signal | Mua (Golden Cross MACD) |
| MACD cắt xuống Signal | Bán (Death Cross MACD) |
| MACD dương & tăng | Uptrend mạnh |
| MACD âm & giảm | Downtrend mạnh |

#### Stochastic Oscillator
**Công thức:** %K = (Close - Lowest Low) / (Highest High - Lowest Low) × 100

| Vùng | Ý nghĩa |
|---|---|
| < 20 | Oversold |
| > 80 | Overbought |
| %K cắt lên %D ở vùng < 20 | Mua mạnh |
| %K cắt xuống %D ở vùng > 80 | Bán mạnh |

---

### 1.2 Trend Indicators

#### EMA — Exponential Moving Average
**EMA nhanh hơn SMA** (ưu tiên giá gần đây hơn)

| EMA | Ý nghĩa | Dùng cho |
|---|---|---|
| EMA20 | Trend ngắn hạn (1 tháng) | Trader |
| EMA50 | Trend trung hạn (2-3 tháng) | Swing trader |
| EMA200 | Trend dài hạn (1 năm) | Investor |

**Quy tắc vàng:**
- Giá > EMA200: Long-term uptrend còn nguyên → **BUY bias**
- Giá < EMA200: Long-term downtrend → **cẩn thận**
- EMA20 cắt lên EMA50 = Golden Cross → tín hiệu tích cực
- EMA20 cắt xuống EMA50 = Death Cross → tín hiệu tiêu cực

**Lesson learned từ thực tế:**
- FPT: RSI 31 (oversold) nhưng giá -21% dưới EMA200 → KHÔNG mua dù RSI oversold
- BAF: RSI 33 + Trên EMA200 → Combo tốt, hội đủ điều kiện mua
- Luôn kiểm tra EMA200 TRƯỚC khi quyết định mua cổ phiếu oversold

#### Bollinger Bands
**Công thức:** Middle = SMA(20) | Upper = SMA(20) + 2σ | Lower = SMA(20) - 2σ

| Tín hiệu | Ý nghĩa |
|---|---|
| Giá chạm BB Lower | Tiềm năng bounce ngắn hạn |
| Giá chạm BB Upper | Tiềm năng điều chỉnh |
| Bands co lại (squeeze) | Sắp có biến động mạnh |
| Bands mở rộng | Trend đang mạnh |

---

### 1.3 Volume Analysis
- **Volume tăng + giá tăng** = Uptrend khỏe mạnh (xác nhận xu hướng)
- **Volume tăng + giá giảm** = Bán mạnh, tránh bắt đáy
- **Volume giảm + giá tăng** = Uptrend yếu, không bền
- **Volume thấp bất thường** = Thiếu thanh khoản, khó thoát lệnh

---

## 2. PHÂN TÍCH CƠ BẢN (Fundamental Analysis)

### 2.1 Valuation Metrics (Định giá)

#### P/E — Price to Earnings Ratio
**Công thức:** P/E = Giá cổ phiếu / EPS (Thu nhập trên mỗi cổ phiếu)

**Cách đọc:**
- P/E = 10x: Nhà đầu tư trả 10đ để mua 1đ lợi nhuận
- P/E thấp = rẻ (tương đối) | P/E cao = đắt hoặc kỳ vọng tăng trưởng cao

**P/E theo ngành VN:**
| Ngành | P/E hợp lý | Ghi chú |
|---|---|---|
| Ngân hàng | 8–12x | Rẻ so với khu vực |
| Công nghệ (FPT) | 18–25x | Premium cho tăng trưởng |
| Thép | 6–12x | Cyclical |
| Tiêu dùng | 15–22x | Ổn định |
| BĐS | 10–20x | Biến động theo chu kỳ |

**⚠️ Bẫy P/E thấp:**
- P/E thấp vì earnings bất thường cao (sắp giảm) → "Value trap"
- Ví dụ: Thép P/E = 5x khi giá thép đỉnh → earnings sẽ giảm → P/E thực cao hơn

**⚠️ Bẫy CAGR lịch sử:**
- MCH CAGR 73.6%/năm từ đáy 2023 → không có nghĩa sẽ tiếp tục từ giá cao hiện tại
- Luôn hỏi: "Nếu mua HÔM NAY, P/E là bao nhiêu?"

#### P/B — Price to Book Value
**Công thức:** P/B = Giá cổ phiếu / Giá trị sổ sách mỗi cổ phiếu

- P/B < 1: Giá thấp hơn tài sản ròng (có thể rẻ hoặc có vấn đề)
- P/B 1–2x: Hợp lý cho ngân hàng
- P/B > 3x: Đắt, cần tăng trưởng cao để justify

#### PEG — Price/Earnings to Growth
**Công thức:** PEG = P/E / EPS Growth Rate

- PEG < 1: Rẻ tương đối (P/E thấp hơn tốc độ tăng trưởng)
- PEG = 1: Fair value
- PEG > 2: Đắt

**Ví dụ:** FPT P/E 22x, EPS growth 20%/năm → PEG = 22/20 = 1.1 → Fair

#### EV/EBITDA
**Công thức:** EV/EBITDA = Enterprise Value / EBITDA

- Tốt hơn P/E vì không bị ảnh hưởng bởi cấu trúc nợ và thuế
- Thép, BĐS thường dùng chỉ số này
- EV/EBITDA < 8x = rẻ (cyclical) | < 15x = hợp lý (growth)

---

### 2.2 Profitability Metrics (Sinh lời)

#### ROE — Return on Equity
**Công thức:** ROE = Net Income / Shareholders' Equity × 100%

| Mức | Đánh giá |
|---|---|
| < 10% | Kém |
| 10–15% | Trung bình |
| 15–20% | Tốt |
| > 20% | Xuất sắc |

**Ngân hàng VN tốt:** VCB ROE ~22%, MBB ROE ~22%, TCB ROE ~18%

**Chú ý:** ROE cao có thể do đòn bẩy cao (vay nhiều) → kiểm tra D/E ratio

#### ROA — Return on Assets
**Công thức:** ROA = Net Income / Total Assets × 100%
- Ngân hàng: ROA > 1.5% = tốt
- Sản xuất: ROA > 5% = tốt

#### EBITDA Margin
**Công thức:** EBITDA / Revenue × 100%
- Thước đo sinh lời hoạt động thuần túy
- Loại bỏ ảnh hưởng của thuế, lãi vay, khấu hao
- > 20% = tốt | > 30% = xuất sắc

#### Gross Margin (Biên lợi nhuận gộp)
**Công thức:** (Revenue - COGS) / Revenue × 100%
- Phản ánh lợi thế cạnh tranh của sản phẩm
- MCH: ~45% (cao → thương hiệu mạnh)
- Thép: ~15% (thấp → commodity)

---

### 2.3 Financial Health (Sức khỏe tài chính)

#### Debt/Equity (D/E)
**Công thức:** D/E = Total Debt / Shareholders' Equity
- D/E < 1: Ít nợ, an toàn
- D/E 1–2x: Bình thường
- D/E > 3x: Nhiều nợ, rủi ro (trừ ngân hàng vì bản chất kinh doanh)

#### Interest Coverage Ratio
**Công thức:** ICR = EBIT / Interest Expense
- ICR > 3x: Tốt (lợi nhuận gấp 3 lần lãi vay)
- ICR < 1.5x: Nguy hiểm

#### Current Ratio (Thanh khoản ngắn hạn)
**Công thức:** Current Assets / Current Liabilities
- > 2x: Tốt | 1–2x: Chấp nhận | < 1x: Rủi ro

#### Free Cash Flow (FCF)
**FCF = Operating Cash Flow - CapEx**
- FCF dương = công ty sinh tiền thực
- FCF âm kéo dài = cẩn thận (đang đốt tiền)
- FCF Yield = FCF / Market Cap → > 5% = hấp dẫn

---

### 2.4 Growth Metrics (Tăng trưởng)

#### Revenue Growth (Tăng trưởng doanh thu)
- > 20%/năm: Tốt (growth stock)
- 10–20%: Khá
- < 10%: Chậm (defensive/mature)

#### EPS CAGR — Compound Annual Growth Rate of EPS
**Công thức:** (EPS_n / EPS_0)^(1/n) - 1

- Đây là driver chính của giá cổ phiếu dài hạn
- P/E × EPS = Giá cổ phiếu
- Nếu EPS tăng 20%/năm và P/E giữ nguyên → giá tăng 20%/năm

---

## 3. RISK METRICS (Đo lường rủi ro)

### 3.1 Volatility (Độ biến động)
**Công thức:** Standard deviation của daily returns × √252 (annualized)

| Mức | Phân loại |
|---|---|
| < 15%/năm | Thấp (ngân hàng lớn, tiện ích) |
| 15–25% | Trung bình |
| 25–40% | Cao (hầu hết cổ phiếu VN) |
| > 40% | Rất cao (penny stocks) |

### 3.2 Sharpe Ratio
**Công thức:** (Return - Risk-free rate) / Volatility
- Risk-free rate VN: ~5.5% (lãi suất ngân hàng)

| Sharpe | Đánh giá |
|---|---|
| < 0 | Tệ (thua gửi ngân hàng) |
| 0–0.5 | Kém |
| 0.5–1.0 | Chấp nhận được |
| 1.0–2.0 | Tốt |
| > 2.0 | Xuất sắc |

**Lesson learned:** Sharpe của MCH là 2.19 từ đáy 2023 — nhưng Sharpe tính BACKWARD từ giá thấp. Người mua ở 161,000 VND hiện tại có Sharpe kỳ vọng thấp hơn nhiều.

### 3.3 Max Drawdown (Mức giảm tối đa từ đỉnh)
**Công thức:** (Trough - Peak) / Peak × 100%

| Mức drawdown | Ý nghĩa |
|---|---|
| -10 đến -20% | Bình thường (correction) |
| -20 đến -40% | Bear market |
| -40 đến -60% | Khủng hoảng nghiêm trọng |
| > -60% | Nguy hiểm (HPG -72%, TCB -64%) |

**Quy tắc:** Max Drawdown càng lớn → cần tâm lý càng vững → phân bổ vốn ít hơn

### 3.4 Beta
**Công thức:** Covariance(Stock, Market) / Variance(Market)

| Beta | Ý nghĩa |
|---|---|
| < 0.5 | Ít biến động hơn thị trường |
| 0.5–1.0 | Ít biến động hơn thị trường |
| = 1.0 | Biến động bằng thị trường |
| > 1.5 | Biến động mạnh hơn thị trường (high risk/reward) |

---

## 4. FRAMEWORK PHÂN TÍCH TỔNG HỢP

### 4.1 Quy trình 5 bước

```
Bước 1: SCREENING
→ Scan RSI < 40, Volume > 500K, Exchange HOSE/HNX
→ Loại bỏ mã dưới EMA200 (trừ khi có catalyst đặc biệt)

Bước 2: VALUATION CHECK
→ P/E hiện tại vs P/E lịch sử vs ngành
→ PEG < 1.5 là hợp lý
→ KHÔNG mua khi P/E > 40x (trừ high-growth với EPS CAGR > 30%)

Bước 3: FUNDAMENTAL QUALITY
→ ROE > 15%
→ D/E hợp lý (theo ngành)
→ FCF dương
→ Revenue/EPS growth trend

Bước 4: CATALYST
→ Điều gì sẽ làm giá tăng trong 1-3 năm tới?
→ Nâng hạng thị trường, expansion, chu kỳ ngành, lãi suất...

Bước 5: SIZING
→ Sharpe > 1.0 → 25-35% danh mục
→ Sharpe 0.5-1.0 → 15-25%
→ Sharpe < 0.5 → < 15%
→ Max Drawdown > 60% → < 10%
```

### 4.2 Scoring System (Áp dụng trong skill)

| Tiêu chí | Điểm | Điều kiện |
|---|---|---|
| RSI < 30 | +3 | Oversold cực mạnh |
| RSI 30-40 | +2 | Oversold |
| Trên EMA200 | +2 | Long-term uptrend intact |
| P/E < Fair P/E | +3 | Định giá hấp dẫn (>20% discount) |
| P/E gần Fair | +2 | Hợp lý (0-20% discount) |
| Dưới BB Lower | +2 | Tiềm năng bounce |
| 52W position < 30% | +2 | Gần đáy 52 tuần |
| MACD bullish | +1 | Momentum cải thiện |
| **Tổng tối đa** | **17** | |

**Khuyến nghị:**
- Score 10+: Mua mạnh
- Score 7-9: Mua tích lũy (DCA)
- Score 4-6: Theo dõi
- Score < 4: Không quan tâm

---

## 5. NGÂN HÀNG TRUNG ƯƠNG & MACRO

### Tác động lãi suất đến chứng khoán
- **Lãi suất giảm** → Chi phí vốn giảm → Doanh nghiệp lợi nhuận tăng → CK tăng
- **Lãi suất tăng** → DCF valuation giảm → P/E hợp lý thấp hơn → CK giảm
- **Quy tắc ngón tay cái:** Lãi suất tăng 1% → P/E hợp lý giảm ~1-2x

### Chỉ số vĩ mô cần theo dõi cho VN
| Chỉ số | Tốt cho CK | Xấu cho CK |
|---|---|---|
| GDP growth | > 6% | < 5% |
| Lạm phát (CPI) | 2-4% | > 6% |
| Tín dụng tăng trưởng | 14-16% | < 10% hoặc > 20% |
| Tỷ giá VND/USD | Ổn định | Mất giá mạnh > 5% |
| FDI | Tăng | Giảm |
| Xuất khẩu | Tăng | Giảm |

---

## 6. LESSONS LEARNED (Từ thực tế phân tích)

### ❌ Sai lầm cần tránh
1. **Mua chỉ vì RSI oversold** — cần kết hợp EMA200 và định giá
2. **Dùng CAGR lịch sử để dự báo tương lai** — MCH CAGR 73%/năm từ đáy không apply cho người mua ở đỉnh
3. **Bỏ qua valuation** — Sharpe cao là lịch sử, không phải tương lai
4. **Overweight 1 mã** — dù MCH/MBB tốt, không nên >40% danh mục
5. **Không có stop loss** — luôn biết mức nào sẽ cut loss

### ✅ Best practices
1. **Kết hợp ít nhất 3 tín hiệu** trước khi quyết định
2. **Luôn hỏi "Tại sao rẻ?"** — có lý do chính đáng hay là "value trap"
3. **DCA theo thời gian** — không all-in một lúc
4. **Review định kỳ** — thị trường thay đổi, thesis có thể sai
5. **So sánh với benchmark** — beat VN-Index mới gọi là tốt

---

*Tài liệu này được cập nhật liên tục trong quá trình phân tích thực tế. Mỗi lần học được điều mới → ghi vào đây.*
