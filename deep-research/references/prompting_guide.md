# Deep Research Prompting Guide & Inversion Heuristics

Google Deep Research (GDR) runs recursive multi-query crawls and synthesizes citations across dozens of sources. To avoid generic high-level marketing fluff, prompts must be engineered with explicit **inversion, boundary constraints, and structured output schemas**.

---

## 1. Core Inversion Archetypes

### Archetype A: The Post-Mortem & Bottleneck Audit
* **Purpose:** Uncover why past attempts at this product, venture, or business model failed.
* **Prompt Template:**
  ```text
  Conduct a rigorous post-mortem audit of companies, startups, or open-source projects that attempted [SPECIFIC CONCEPT / MARKET] between [YEAR RANGE, e.g. 2018-2025]. 
  Identify:
  1. Names and shutdown/pivot dates of at least 3-5 notable attempts.
  2. The primary failure mode for each: distribution friction, customer acquisition cost (CAC) vs lifetime value (LTV), regulatory barriers, or technical infeasibility.
  3. The structural bottlenecks they could not overcome.
  Provide direct citations and links to founder post-mortems, news reports, or investor memos.
  ```

### Archetype B: Bottom-Up Unit Economics & Pricing Benchmark
* **Purpose:** Bypass inflated top-down TAM and find real transactional data.
* **Prompt Template:**
  ```text
  Analyze the commercial unit economics and pricing models in the [DOMAIN / ICP, e.g. European SME accounting automation] market.
  Research and provide:
  1. Actual public or leaked pricing tiers of current market players (per seat, per usage, % of GMV).
  2. Average sales cycle length and buyer persona title.
  3. Estimated gross margins and major COGS drivers (e.g. LLM inference cost, third-party API costs, human-in-the-loop review).
  4. Bottom-up TAM estimate based on verifiable business counts and average contract value (ACV).
  Cite sources for all pricing points and financial metrics.
  ```

### Archetype C: Unserved Customer Pain & Complaint Synthesis
* **Purpose:** Find high-intent dissatisfaction with current market leaders.
* **Prompt Template:**
  ```text
  Investigate user reviews, forum discussions (Reddit, Hacker News, G2, Trustpilot, industry-specific forums) concerning [LEADING PRODUCTS / INCUMBENTS in DOMAIN].
  Synthesize:
  1. The top 3-5 recurring complaints and friction points that existing solutions fail to resolve.
  2. Features or workflows users frequently build workarounds for (e.g. custom spreadsheets, Zapier hacks).
  3. Switching barriers: What prevents users from churning even when dissatisfied?
  Include verbatim excerpts and source links where possible.
  ```

### Archetype D: Regulatory, Legal & Compliance Hurdles
* **Purpose:** Audit compliance risk (EU AI Act, GDPR, local jurisdictions, API TOS).
* **Prompt Template:**
  ```text
  Perform a regulatory and compliance feasibility analysis for an AI service operating in [JURISDICTION, e.g. Netherlands / EU] that handles [SPECIFIC DATA / TASK, e.g. automated HR performance evaluations or SME invoice factoring].
  Detail:
  1. Relevant legal frameworks (e.g. EU AI Act high-risk classification, GDPR Article 22 on automated decision-making).
  2. Mandatory certification, reporting, or human-oversight prerequisites.
  3. Recent enforcement actions or regulatory warnings issued in this domain.
  Cite official regulatory texts, legal commentary, and case law.
  ```

---

## 2. Framing Rules for High-Signal Output
1. **Never ask open-ended questions like "Tell me about the market for X".** Always force structured comparative analysis.
2. **Specify the time window:** Restrict research to the last 2-3 years to eliminate outdated pre-LLM architectures.
3. **Require direct source attribution:** Request links to primary filings, technical docs, or real reviews rather than analyst blogs.
