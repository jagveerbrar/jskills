# Technical Analysis Reference Guide & Threshold Rules

A reference manual for interpreting price action indicators, oscillators, moving average regimes, and support/resistance levels.

---

## 1. Moving Averages & Trend Regimes

Moving averages smooth price data to identify the prevailing institutional trend direction and key support/resistance boundaries.

| Metric | Period | Typical Role | Bullish Condition | Bearish Condition |
| :--- | :--- | :--- | :--- | :--- |
| **20-day SMA/EMA** | 20 bars (~1 month) | Short-term momentum floor | Price > 20 SMA | Price < 20 SMA |
| **50-day SMA/EMA** | 50 bars (~10 weeks) | Medium-term institutional trend | Price > 50 SMA | Price < 50 SMA |
| **200-day SMA** | 200 bars (~10 months) | Macro cycle boundary / institutional line in the sand | Price > 200 SMA | Price < 200 SMA |

### Regime Classifications
* **Strong Bullish:** $\text{Price} > \text{SMA}_{50} > \text{SMA}_{200}$. Healthy upward compounding with high institutional sponsorship.
* **Bullish Consolidation:** $\text{Price} \approx \text{SMA}_{50} > \text{SMA}_{200}$. Constructive pullback to support in an ongoing macro bull market.
* **Bearish Relief Rally:** $\text{Price} > \text{SMA}_{50}$ while $\text{SMA}_{50} < \text{SMA}_{200}$. Short-term bounce inside a macro downtrend.
* **Strong Bearish:** $\text{Price} < \text{SMA}_{50} < \text{SMA}_{200}$. Distribution phase and downward momentum.

### Golden & Death Crosses
* **Golden Cross:** 50-day SMA crosses above 200-day SMA. Signals long-term structural momentum shift to the upside.
* **Death Cross:** 50-day SMA crosses below 200-day SMA. Signals potential long-term macro trend breakdown.

---

## 2. Momentum & Oscillators

### Relative Strength Index (RSI - 14 Period)
Measures the speed and change of price movements on a 0 to 100 scale:
* **$\text{RSI} \ge 70$ (Overbought):** Momentum is overheated. Short-term risk of pullback or consolidation is elevated. In strong bull markets, RSI can stay overbought for extended periods.
* **$30 < \text{RSI} < 70$ (Neutral Zone):** Normal price action and trend progression.
* **$\text{RSI} \le 30$ (Oversold):** Selling pressure is exhausted. High probability of mean-reversion bounce. When aligned with a fundamental Margin of Safety, this signals high-conviction value accumulation windows.

### Moving Average Convergence Divergence (MACD)
Calculated as 12-day EMA minus 26-day EMA, with a 9-day EMA signal line:
* **Bullish Crossover:** MACD Line crosses above Signal Line (Histogram turns positive).
* **Bearish Crossover:** MACD Line crosses below Signal Line (Histogram turns negative).
* **Zero-Line Cross:** MACD Line crossing above zero confirms positive absolute medium-term momentum.

---

## 3. Volatility & Channel Bands

### Bollinger Bands (20 Period, 2 Standard Deviations)
* **$\%B = \frac{\text{Price} - \text{Lower Band}}{\text{Upper Band} - \text{Lower Band}}$**
  - $\%B > 1.0$: Price is trading above the upper band (statistical stretch to the upside).
  - $\%B < 0.0$: Price is trading below the lower band (statistical stretch to the downside).
  - $\%B \approx 0.5$: Price is hovering at the 20-day mean.
* **Band Squeeze:** When the upper and lower bands contract significantly, it signals a period of low volatility often preceding an explosive directional expansion.

### Average True Range (ATR - 14 Period)
Measures the absolute volatility of an asset in dollar terms:
* Used to gauge expected normal daily swing ranges.
* Helps determine stop-loss distances or buffer zones (e.g. entering within $1.0 \times \text{ATR}$ of a major moving average).

---

## 4. Support, Resistance & Pivot Points

### Classic Floor Pivots
Calculated from prior period High ($H$), Low ($L$), and Close ($C$):
$$\text{Pivot } (P) = \frac{H + L + C}{3}$$
* $\text{Resistance 1 } (R_1) = 2P - L$
* $\text{Support 1 } (S_1) = 2P - H$
* $\text{Resistance 2 } (R_2) = P + (H - L)$
* $\text{Support 2 } (S_2) = P - (H - L)$

### 52-Week Range Percentile
$$\text{Range Position} = \frac{\text{Current Close} - 52\text{W Low}}{52\text{W High} - 52\text{W Low}} \times 100\%$$
* $< 20\%$: Asset is trading near annual lows. High value-inversion screening territory.
* $> 80\%$: Asset is trading near all-time / 52-week highs. Demands higher fundamental margin of safety.

---

## 5. Integrating Technicals with Value Investing (`Invest`)

In value investing frameworks, technicals must never override intrinsic value calculations or economic moat assessments. Instead, they serve as a **tactical entry filter**:
1. **Rule 1: Don't Buy at Parabolic Tops.** Even if a Tier 1A moat compounder is at Fair Value on normalized owner earnings, avoid entering when RSI > 75 and price is $> 25\%$ extended above its 50-day SMA. Wait for a retest of the 20-day or 50-day moving average.
2. **Rule 2: Maximize DCA Allocation at Oversold Support.** When a verified Tier 1 business experiences macro panic, look for confluence:
   - Price touches the 200-day SMA or major swing low support.
   - 14-day RSI drops below 35.
   - Free Cash Flow multiple is below fair value.
   $\rightarrow$ Deploy maximum accumulation tranches.

---

## 6. Offload & Exit Architecture (Systematic Selling & Trimming Rules)

A holistic execution protocol must define not just where to buy, but exactly when and at what levels to offload, trim, or protect capital:

### 1. Parabolic Exhaustion Trim (Taking Chips Off the Table)
* **Mathematical Trigger:** Confluence of:
  - 14-day RSI $\ge 75.0$ (extreme momentum overheating)
  - Bollinger Band $\%B \ge 1.00$ (trading outside the $+2\sigma$ volatility ceiling)
  - Price extension $\ge 15.0\% - 20.0\%$ above the 20-day SMA
* **Action:** Trim 25% – 33% of the position. Lock in outsized momentum gains before the inevitable mean-reversion pullback occurs.

### 2. Structural Resistance Trim (Target Reached)
* **Trigger:** Price hits a verified 52-week high, upper channel ray, or Fibonacci extension ($1.272\times$ or $1.618\times$) on decelerating volume.
* **Action:** Trim tactical trading tranches. Rebalance capital into safe assets or undervalued watchlist compounders.

### 3. Trailing Profit Stop (Protecting Unrealized Gains)
* **Rule:** For the remaining runner portion of a position, trail an exit stop just beneath the **20-day SMA** or prior swing low.
* **Execution:** If a stock closes below its 20-day SMA on above-average volume, close the remaining tactical position to prevent a winner from turning into a loser.

### 4. Portfolio Asset Tier Differentiation (`Invest` Policy)
* **Tier 1A / 1B Moat Toll-Roads & Platforms (e.g., SPGI, MCO, MSFT, GOOGL, VEEV):**
  - *Rule:* **Systematic Overbought Trims.** While Tier 1A/1B assets are core compounding compounders, do not hold passively through euphoric parabolic run-ups. When an asset becomes heavily overbought (confluence of **RSI $\ge 70–75$**, price extended **$\ge 15\%–20\%$ above 50D SMA** or **$\ge 35\%–50\%$ above 200D SMA**, and Bollinger Band $\%B \ge 1.00$), systematically trim **20% – 33%** to lock in outsized gains into cash equivalents. Re-deploy banked capital when the stock pulls back to test structural 50D/200D SMA support shelves.
* **Tier 2 / Tier 3 Cyclicals & SMB High-Beta (e.g., SHOP, MU, AMD):**
  - *Rule:* **Strictly Enforce Aggressive Technical Offloads.** Cyclicals and high SMB churn businesses experience violent multiple compression. When technical indicators flash parabolic exhaustion (RSI > 75, %B > 1.0) or approach 52-week highs, systematically offload 33–50% to bank cash.
