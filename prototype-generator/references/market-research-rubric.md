# Market Research & Intelligence Rubric (Phase 0)

This rubric guides the dedicated `research` subagent to conduct exhaustive internet research before sparring begins.

---

## 1. The 4 Research Pillars

### Pillar 1: Market Demand & Willingness-to-Pay (WTP)
* **Goal:** Determine if real businesses or consumers spend money to solve this problem, what price points exist, and the total addressable urgency.
* **Search Query Archetypes:**
  - `"<problem keyword>" cost OR pricing OR "per month" OR subscription`
  - `"willing to pay" "<problem keyword>"`
  - `"<industry> software" pricing comparison`

### Pillar 2: Pain-Point Proof & Raw User Sentiment
* **Goal:** Extract unfiltered complaints, frustrations, and horror stories directly from operator communities.
* **Search Query Archetypes:**
  - `site:reddit.com/r/<relevant_subreddit> "<pain keyword>" OR "hate" OR "nightmare"`
  - `site:reddit.com/r/AirBnBHosts OR site:reddit.com/r/realestateinvesting "<pain keyword>"`
  - `site:reddit.com/r/smallbusiness "<pain keyword>" "how do you handle"`
  - `"app store" "<competitor>" reviews "terrible" OR "broken" OR "missing"`

### Pillar 3: Clumsy Manual Workarounds
* **Goal:** Uncover how people currently patch the problem without dedicated software (spreadsheets, manual texting, physical checklists, jury-rigged hardware).
* **Search Query Archetypes:**
  - `"how do you track" OR "spreadsheet template" "<problem keyword>"`
  - `"workaround for" "<industry problem>"`
  - `"manual process" "<workflow keyword>"`

### Pillar 4: Direct Competitors & Upstream Platform Extinction Risk
* **Goal:** Identify existing software, but crucially assess whether upstream platforms (OpenAI, Google, Apple, Shopify) will roll this out natively within 6–12 months.
* **Search Query Archetypes:**
  - `"<keyword>" alternatives OR competitors`
  - `"vs" "<top_competitor>" software`
  - `"OpenAI" OR "Google" OR "ChatGPT" native feature "<problem keyword>"`
  - `"<competitor>" complaints OR "why I switched"`

### Pillar 5: "Why Now?" Inflection Catalyst
* **Goal:** Identify the exact technological, regulatory, or protocol shift (e.g. UCP adoption, vision LLM cost collapse, new EU compliance mandates) that makes this possible today when it wasn't 12 months ago.
* **Search Query Archetypes:**
  - `"<problem keyword>" API OR protocol OR regulation "2025" OR "2026"`
  - `"new standard" OR "new protocol" "<industry keyword>"`

---

## 2. Structure of `market_intelligence.md` Output Dossier

The research subagent must synthesize all findings into this exact Markdown format:

```markdown
# Market Intelligence Dossier: [Idea Title]

## 1. Executive Summary & Demand Signals
* **Market Urgency Rating:** (High / Moderate / Low)
* **Observed Price Anchors:** ($X/mo, $Y/transaction, or $0 free expectation)
* **Target ICP Proof:** (Who actually cares most and has budget authority)
* **"Why Now?" Inflection Catalyst:** (Recent technical, regulatory, or protocol enabler)

## 2. Real-World Pain Point Proof (Quotes & Forum Evidence)
* **Evidence Point 1:** [Quote / summary + source URL/subreddit]
* **Evidence Point 2:** [Quote / summary + source URL/subreddit]
* **Evidence Point 3:** [Quote / summary + source URL/subreddit]

## 3. Current Clumsy Workarounds
* **Workaround A:** [Description of manual spreadsheet/process and why it fails at scale]
* **Workaround B:** [Description of jury-rigged hardware or consumer tools]

## 4. Competitive Landscape & Platform Extinction Risk
| Competitor / Platform | Type | Pricing Model | Threat Level | Vulnerability / Defensible Moat |
| :--- | :--- | :--- | :--- | :--- |
| **Competitor A** | Incumbent | ... | ... | ... |
| **Google / OpenAI / Big Tech** | Upstream Platform | Free/Native | High/Med/Low | ... |

## 5. Strategic Wedge Opportunities for Sparring
* **Wedge 1 (High-Margin Niche):** ...
* **Wedge 2 (Counter-Positioning / Protocol Leverage):** ...
```

---

## 3. Phase 2: Targeted Empirical Ground-Truthing Rubric

After the initial debate, the ground-truthing research subagent takes the specific contested assumptions and validates them against live empirical data.

### Structure of `empirical_validation.md` Output:

```markdown
# Empirical Ground-Truthing Dossier: [Idea Title]

## 1. Statutory & Regulatory Audit
* **Question / Assumption:** [e.g. Can return rights or liability be waived?]
* **Statutory Baseline:** [Citations of relevant law, directives, or court precedent]
* **Real-World Enforcement:** [How operators actually handle it: waivers, deposits, B2B limits]
* **Verdict:** (Enforceable / Illegal / Grey Area)

## 2. Real-World Ecosystem & Standard Adoption Audit
* **Question / Assumption:** [e.g. Is protocol/standard X actually deployed by target merchants?]
* **Actual Market Penetration:** [Empirical stats, live deployments, who is live vs who is holding back]
* **Incumbent Resistance:** [Why incumbents adopt or resist]
* **Verdict:** (Widely Live / Early Niche / Vaporware / PR-only)

## 3. Financial Downside & Failure Liability
* **Failure Mechanism:** [What happens when the product makes an error or fails?]
* **Customer P&L Impact:** [Concrete financial loss: return shipping, write-downs, downtime]
* **Mitigation Requirement:** [Insurance, strict schema, disclaimer, or human-in-the-loop]
```
