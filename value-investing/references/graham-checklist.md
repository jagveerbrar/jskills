# Benjamin Graham Value Investing Checklist & Formulas

A rigorous reference manual for classical security analysis based on Benjamin Graham's *The Intelligent Investor* and *Security Analysis*.

---

## 1. The Defensive Investor's 7-Point Selection Checklist

Graham formulated these seven strict quantitative filters to minimize risk of permanent capital impairment for defensive (passive) investors. A stock failing any single criterion is rejected.

| # | Criterion | Graham's Standard | Underlying Rationale |
| :--- | :--- | :--- | :--- |
| **1** | **Adequate Size** | Substantial enterprise (e.g. Fortune 500 / top tier) | Exclude small, fragile, highly volatile micro-caps. |
| **2** | **Strong Financial Condition** | Current Ratio $\ge 2.0$; Long-Term Debt $\le$ Net Current Assets | Ensure liquidity to survive acute macro or sector shocks. |
| **3** | **Earnings Stability** | Positive net earnings every year for 10 straight years | Reject cyclical or turnaround gambles with negative years. |
| **4** | **Dividend Record** | Uninterrupted dividend payouts for $\ge 20$ consecutive years | Proof of real, cash-generative operations across full economic cycles. |
| **5** | **Earnings Growth** | Minimum 33% total EPS growth over the past 10 years (~2.9% CAGR) | Ensure business is not slowly eroding against inflation. |
| **6** | **Moderate P/E Ratio** | Current Price $\le 15\times$ average 3-year earnings | Establish a baseline price cushion against valuation compression. |
| **7** | **Moderate Price-to-Book** | Price-to-Book (P/B) $\le 1.5\times$ (or $\text{P/E} \times \text{P/B} \le 22.5$) | Prevent paying massive premiums over tangible liquidation equity. |

---

## 2. Core Quantitative Formulas

### A. The Graham Number (Maximum Defensive Intrinsic Price)
Caps valuation by bounding both earnings and physical book value:
$$\text{Graham Number} = \sqrt{22.5 \times \text{EPS} \times \text{BVPS}}$$
- **Rule:** If $\text{Market Price} < \text{Graham Number}$, a Margin of Safety exists.
- **Fail-Safe Zero:** If $\text{EPS} \le 0$, $\text{Graham Number} = 0$, immediately rejecting asset-rich "value traps" that generate no profit.

### B. Graham Growth Formula (Growth-Adjusted Intrinsic Value)
Formulated by Graham to evaluate expanding enterprises without penalizing earnings growth:
$$\text{Acceptable P/E} = 8.5 + 2g$$
Where:
- $8.5$: Baseline P/E assigned to a stagnant company with zero growth.
- $g$: Conservative estimated annual earnings growth rate over the next 7 to 10 years (as a percentage, e.g. 10 for 10%).

### C. The Inverted Market-Implied Growth Hurdle
To discover what future performance the current market price demands:
$$g_{\text{implied}} = \frac{\text{Current P/E} - 8.5}{2}$$
- **Interpretation:** If a company trades at a 50 P/E, $g_{\text{implied}} = \frac{50 - 8.5}{2} = 20.75\%$.
- Compounding at 20.75% annually for 10 years requires multiplying earnings by $\approx 6.6\times$. Very few large enterprises can sustain this due to competition and the Law of Large Numbers.

### D. Margin of Safety Calculation
$$\text{Margin of Safety (\%)} = \frac{\text{Intrinsic Fair Value} - \text{Market Price}}{\text{Intrinsic Fair Value}} \times 100\%$$
- Classical Graham Standard: Demands a $\ge 30\%$ discount.
- Buffett Modern Moat Standard: A 15%–25% discount may be accepted *only* if protected by an exceptionally durable economic moat and highly predictable cash flows.

---

## 3. Portfolio Allocation & Temperament Rules

1. **The 50/50 Baseline Rule:**
   - 50% in conservative, high-quality common stocks (inflation hedge + cash-flow growth).
   - 50% in high-grade bonds or guaranteed cash equivalents (deflation hedge + liquidity buffer).
2. **The 25/75 Guardrails:**
   - Equities must never fall below 25% (eroded by inflation).
   - Equities must never exceed 75% (exposed to panic sell-offs).
3. **Mechanical Rebalancing:**
   - When market euphoria elevates equities to 70%–75%, mechanically trim equities and buy safe assets.
   - When panic crashes depress equities toward 25%–30%, mechanically deploy safe assets into equities.
4. **Dollar-Cost Averaging (DCA):**
   - Automatically buys more units at cheaper prices and fewer units at elevated prices, eliminating emotional market timing.
