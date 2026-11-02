# Grounded Fermi Market Sizing & Unit Economics Rubric

This reference defines the mathematical formulas, validation criteria, and unit economics hurdles applied in Stage 5 of `/industry-analysis`.

---

## 1. Bottom-Up Market Sizing Formulas

Never rely on generic top-down industry reports (e.g., "$50B global agtech market"). Build market size from empirical ground-level counts:

```
[ Total Operator Universe (Census / Directory Data) ]
                       │
                       ▼  × % Matching ICP Criteria
               [ SAM (Target Segment) ]
                       │
                       ▼  × % Reachable in Initial Geography
            [ Beachhead Addressable Market ]
                       │
                       ▼  × Realistic Annual Contract Value (ACV)
            [ Beachhead SOM (Annual Market Potential) ]
```

### Mathematical Breakdown:
* **Total Universe ($N_{\text{total}}$):** Exact count from national statistics (e.g., CBS, Eurostat, Chamber of Commerce / KvK).
* **Segment Filter ($f_{\text{ICP}}$):** Percentage of operators experiencing the acute regulatory/labor pain (e.g., dairy farms $>80\text{ cows}$ facing manure export penalties $= 65\%$).
* **Beachhead Pool ($N_{\text{beachhead}}$):** Operators in the initial dense territory (e.g., 3 specific provinces).
* **Annual Contract Value ($\text{ACV}$):** Value-share pricing or SaaS seat fees.
* **Beachhead SOM:**
  $$\text{SOM}_{\text{beachhead}} = N_{\text{beachhead}} \times \text{ACV}$$

---

## 2. Unit Economics & Hurdle Thresholds

Every concept must clear these four economic hurdles before passing Gate 3:

| Metric | Minimum Venture Hurdle | Rationale & Failure Mode |
| :--- | :--- | :--- |
| **Payback Period** | **$<6\text{ months}$** (Ideally immediate cash-positive) | If payback exceeds 1 season / 12 months, conservative SMB operators will postpone purchasing indefinitely. |
| **Value-to-Price Ratio** | **$\ge 5:1$** (Startup captures $\le 20\%$ of value) | Customer must keep $\ge 80\%$ of the cash saved or revenue unlocked to make the adoption decision frictionless. |
| **Gross Margin** | **$\ge 80\%$** | Software cannot have human-in-the-loop engineering or consulting drag scaling linearly with customers. |
| **Breakeven Scale** | **$<50\text{ Enterprise / Channel Accounts}$** | The business must reach operating breakeven without requiring unrealistic mass-market consumer penetration. |

---

## 3. Fermi Estimation Example Template

When reporting in Stage 5, format the business case strictly using this block:

```markdown
### Grounded Fermi Sizing Block

* **Operator Baseline:** [Target Sector] in [Target Region].
* **Total Addressable Population:** [N] total operators (Source: [CBS / Registry]).
* **Target Beachhead ICP:** [N_beachhead] operators ([Specific criteria]).
* **Customer Economic Impact:**
  * Direct Cash Bleed Avoided / Revenue Unlocked: €[X] / year per operator.
  * Proposed Startup Pricing: €[Y] / year (Value share: [Z]%).
  * Customer Payback Period: [M] months ([Immediate ROI justification]).
* **Beachhead Market Potential (SOM):**
  * 100% Beachhead SOM: €[Total SOM] / year.
  * 15% Penetration Scenario: €[Realistic ARR] / year across [N_clients] operators.
* **Channel Multiplier (B2B2C):**
  * Target Channel Intermediaries: [N_advisors] consultants managing [Avg_farms] operators each.
  * Accounts Needed for €500k ARR: [N_accounts] advisory firms.
```
