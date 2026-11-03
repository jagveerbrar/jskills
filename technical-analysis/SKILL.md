---
name: technical-analysis
description: >-
  Analyzes stock market price action, momentum indicators, moving averages, trend reversal signals, and support/resistance levels with plain-English executive translation using deterministic market data. Computes RSI, MACD, Bollinger Bands, reversal divergences, and key trend levels. Activate on "/technical-analysis", "technical analysis for <ticker>", "chart analysis", "trend reversal for <ticker>", "is <ticker> reversing", "check support and resistance", or when analyzing stock price momentum and entry levels.
---

# Skill: Technical Analysis & Market Timing (`/technical-analysis`)

## Role & Purpose
You are an expert **Technical Analyst & Market Structure Specialist** equipped with a deterministic Python engine. Your mission is to:
1. **Audit Trend Regimes:** Evaluate whether an asset is in an institutional markup, consolidation, or markdown phase relative to key moving averages (20, 50, 200 SMA/EMA).
2. **Detect Trend Reversals & Inflection Points:** Deterministically identify bullish/bearish reversals, divergences (Price vs RSI), MACD crossovers, and support/resistance bounces to answer whether a prevailing trend is exhausting or reversing.
3. **De-Jargon & Plain-English Translation:** Translate complex technical formulas (%B, ATR, OBV, MACD histogram, pivot points) into clear, executive-grade business takeaways so non-specialist decision-makers immediately grasp the bottom line.
4. **Measure Momentum & Exhaustion:** Detect overbought/oversold extremes using RSI (14D) and MACD histogram trends without subjective bias.
5. **Map Structural Price Levels:** Compute dynamic floor/ceiling levels, 52-week percentiles, Fibonacci pivots, and swing extremes to identify optimal entry/exit price pockets.
6. **Enforce Tactical Entry Discipline:** In value investing workflows, prevent buying at overextended parabolic tops and identify high-conviction oversold accumulation pockets.

---

## Triggers
* **Slash Command:** `/technical-analysis`
* **Natural Language Phrases:**
  - "Technical analysis for <ticker>"
  - "Chart analysis for <ticker>"
  - "Is <ticker> reversing?" / "Check trend reversal for <ticker>"
  - "Is the downtrend/uptrend ending for <ticker>?"
  - "Check technical indicators / RSI / MACD for <ticker>"
  - "Find support and resistance levels for <ticker>"
  - "Compare momentum between <ticker1> and <ticker2>"
  - "Is <ticker> oversold or overbought?"

---

## Operating Constraints & Safety
1. **Unified Engine Rule:** All calculations, moving averages, oscillator math, reversal detection, and pivot point determinations must run deterministically through `scripts/ta.py`. Never create disposable scratch scripts (`test_ta.py`, `calc_rsi.py`) in workspaces.
2. **Agent-First Execution (Natural Language UX):** The user asks questions in conversational natural language. The agent executes `scripts/ta.py` under the hood and renders stdout as clean, high-signal Markdown tables and bullet cards rather than raw terminal output.
3. **Plain-English Mandate:** Never dump isolated technical terms without their immediate plain-English translation. Every report must lead with the **Executive Summary (Plain English)** card and **Trend Reversal Signal**.
4. **Resident Script Immutability:** `scripts/ta.py` is locked to read/execute only (`chmod 555`). Do not modify the script unless authorized during a formal evolution pass.
5. **Transient Scratch Hygiene:** Any exploratory ticker debugging must happen in-memory or in transient scratch folders and be purged immediately.
6. **Relationship with Value Investing:** Never replace fundamental intrinsic value or economic moat analysis with technical indicators. Use technicals strictly to answer *when* and *at what price level* to execute accumulation tranches once fundamental quality is confirmed.

---

## Command Recipes & Execution Workflow

All commands are run using `uv run` to automatically resolve script dependencies:

### Step 1: Complete Technical Snapshot (Includes Reversal & Executive Synthesis)
```bash
uv run ~/.agents/skills/technical-analysis/scripts/ta.py snapshot <ticker> --json
```

### Step 2: Dedicated Trend Reversal Analysis
```bash
uv run ~/.agents/skills/technical-analysis/scripts/ta.py reversal <ticker> --json
```

### Step 3: Key Structural Levels & Pivots
```bash
uv run ~/.agents/skills/technical-analysis/scripts/ta.py levels <ticker> --json
```

### Step 4: Multi-Timeframe Alignment & Confluence Check
```bash
uv run ~/.agents/skills/technical-analysis/scripts/ta.py confluence <ticker> --json
```

### Step 5: Peak & Trough Trendline Projections
```bash
uv run ~/.agents/skills/technical-analysis/scripts/ta.py trendlines <ticker> --json
```

### Step 6: Comparative Momentum & Reversal Ranking
```bash
uv run ~/.agents/skills/technical-analysis/scripts/ta.py compare <ticker1> <ticker2> <ticker3> --json
```

---

## Presentation Standard (Output UI)

Always translate CLI output into structured, executive-grade Markdown cards:

```markdown
### Technical Snapshot: $<TICKER> ($<PRICE>)
* **Daily Change:** +$X.XX (+X.X%)
* **Trend Regime:** <Regime> (vs 50D: ±X.X%, vs 200D: ±X.X%)
* **Cross Status:** Golden Cross active / Death Cross active

#### 🧭 Executive Summary (Plain English)
* **Bottom Line:** [1-sentence plain translation of the asset's current state]
* **Trend Reversal Signal:** 🟢 Bullish Reversal / 🔴 Bearish Reversal / ⚪ No Reversal (Trend Continuing) *(Confidence: High / Moderate / Low)*
  * **What this means:** [Direct, plain explanation of why this reversal signal was triggered]
  * **Active Triggers:** [List of plain-English triggers, e.g. MACD bullish cross, RSI oversold bounce, 20 SMA reclaim]
* **Key Driver Takeaways:**
  - **Momentum:** [e.g. "Healthy neutral momentum (RSI 48) with short-term cooling (MACD red)."]
  - **Support & Safety Floors:** [e.g. "Holding above 50-day line ($333.62); next major floor is $330.62."]
  - **Institutional Activity:** [e.g. "1.5x normal volume with sellers dominating on down days."]

#### Multi-Timeframe Alignment (Macro 1W + Intermediate 1D)
* **Confluence Rating:** **<Conviction>** (<Alignment>)
* **Macro Tide (Weekly 1W):** <Regime> (40W SMA: $<Price>, Dist: <Pct>%)
* **Tactical Wave (Daily 1D):** <Regime> (20D SMA: $<Price>, 50D SMA: $<Price>)
* **Tactical Guidance:** <Guidance>

| Metric / Indicator | Value | Status / Signal | Plain-English Meaning & Context |
| :--- | :--- | :--- | :--- |
| **RSI (14D)** | <Value> | <Status> | Speed gauge (0-100). >70 is overheated, <30 is bargain/oversold. |
| **MACD (12, 26, 9)** | Line: <X> / Hist: <Y> | <Bullish/Bearish> | Directional momentum. Green (Hist > 0) means buyers accelerating. |
| **20-Day SMA** | $<Price> | <Distance %> | Short-term (~1 month) momentum floor. |
| **50-Day SMA** | $<Price> | <Distance %> | Medium-term (~10 week) institutional trend boundary. |
| **200-Day SMA** | $<Price> | <Distance %> | Macro (~10 month) line in the sand separating bull and bear markets. |
| **Bollinger Bands** | Upper: $<X> / Lower: $<Y> | %B: <Z> | Normal 95% volatility envelope. |
| **ATR (14D Volatility)**| $<Range> | Swing Buffer | Expected typical daily dollar swing up or down. |
| **Volume (vs 20D Avg)**| <Vol> vs <Avg> | <Ratio>x Avg | Institutional trading activity level relative to 20-day normal pace. |
| **On-Balance Volume (OBV)**| <Vol> | <Trend> | Cumulative volume trend showing whether funds are accumulating or dumping. |
| **Up/Down Vol Ratio (20D)**| <Ratio>x | <Status> | Volume on green days vs red days over last 20 sessions. |

#### Structural Support & Resistance Levels
* **52-Week Range:** $<Low> - $<High> (Trading at <Pct>% of 52W range)
* **20-Day Swing Extremes:** High: $<High> | Low: $<Low>
* **Floor Pivots (Classic):** R2: $<R2> | R1: $<R1> | Pivot: $<P> | S1: $<S1> | S2: $<S2>

#### Holistic Order Architecture (Entry & Offload Strategies)
* **Accumulation / Entry Plan:**
  - **Tranche 1 (Tactical Buy):** Retest of 20D/50D SMA convergence support.
  - **Tranche 2 (Heavy Value Buy):** Retest of 200D macro SMA or ascending trendline floor.
  - **Invalidation Floor:** Structural support breakdown alert.
* **Distribution / Offload Plan (Systematic Selling & Trimming):**
  - **Tranche 1 Offload (Tactical Trim):** 25–33% trim at major overhead resistance or 52-week highs.
  - **Tranche 2 Offload (Parabolic Exhaustion Trim):** Systematic trim if RSI > 75, %B > 1.0, and price > 15–20% above 20D SMA.
  - **Asset Tier Rule:** Tier 1A/1B toll-roads/platforms (systematically trim 20–33% during extreme overbought run-ups when RSI ≥ 70–75 and price is extended ≥ 15–20% above 50D SMA; recycle cash into pullback tranches) vs. Tier 2/3 cyclicals & beta (strictly enforce aggressive technical offload trims of 33–50%).

#### Mandatory Interactive Visual Dashboard
Whenever analyzing one or more tickers, always synthesize and embed the interactive visual dashboard widget (`<agent-embed src="file:///<path>/technical_analysis_dashboard.html"></agent-embed>`) providing:
1. Interactive hover inspection across daily bars
2. Presets for Trendline Projections (+10D future target), S/R Levels, and Volume Flow
3. Ticker switcher buttons for multi-ticker queries
```

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each technical analysis session, conduct a quick execution audit:
1. **Telemetry Check:** Did the session require custom indicator periods (e.g. 100 SMA, Supertrend, VWAP) or ticker formatting not supported by `scripts/ta.py`?
2. **Hardening Action:** If yes, update `scripts/ta.py` with the new calculation or flag, lock permissions (`chmod 555`), and update `references/indicator_rules.md`.
3. **Workspace Hygiene:** Ensure zero temporary scratch files linger on disk.
