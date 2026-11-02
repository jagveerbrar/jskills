# jskills: Compounding Agent Skills & Evolution Harness

> A provider-neutral, production-grade AI agent skills harness featuring autonomous evaluation, self-hardening loops, and first-principles venture prototyping engines.

[![Ecosystem](https://img.shields.io/badge/Ecosystem-Agentic%20AI-blue)](https://github.com/jagveerbrar)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Standards](https://img.shields.io/badge/Standards-.agents%20%2F%20AGENTS.md-orange)](https://github.com/anthropics/skills)

---

## 🏗️ Architecture & Philosophy

`jskills` is designed around three architectural invariants:

1. **Provider-Neutral Runtime Discovery:** All skills conform to the canonical `.agents/skills` standard. A single global symlink hub (`scripts/sync-skills.sh`) projects skills into `~/.agents/skills/`, making them natively interoperable across Google Antigravity, Claude Code, and custom agent harnesses.
2. **Unified Single-Binary Tooling:** Tool-based skills encapsulate domain logic inside a single, modular CLI runner (`scripts/<tool>.py`) with structured `--json` subcommands. Throwaway scratch scripts are forbidden.
3. **The Self-Evolution Flywheel:** Every skill includes test assertion suites (`evals/evals.json`) and post-execution audit hooks. When friction occurs, the autonomous meta-tooling diagnoses failure boundaries, extracts test cases, and surgical patches the skill definition.

---

## 📦 Public Skill Catalog

### 🚀 Venture & Strategy Engines
* **[`dare`](dare/SKILL.md):** Decompose, Audit assumptions, Recombine facts, and Experiment against reality. A first-principles reasoning engine for complex product and business strategy.
* **[`spar`](spar/SKILL.md):** Dialectical sparring partner delivering sharp pushback paired with non-obvious generative angles to stress-test entrepreneurial hypotheses.
* **[`prototype-generator`](prototype-generator/SKILL.md):** Autonomous venture prototyping pipeline coordinating isolated subagents for adversarial sparring, anti-bias synthetic customer discovery (30% non-consumption rule), and smoke tests.
* **[`industry-analysis`](industry-analysis/SKILL.md):** Deconstructs unfamiliar industries, maps hourglass value chains, identifies high-margin bottlenecks, and sizes opportunities with Fermi business cases.

### 📈 Quantitative Finance & Valuation
* **[`value-investing`](value-investing/SKILL.md):** Benjamin Graham value investing framework, economic moat scoring, and SaaS liquidity / market-implied growth hurdle adjustments.
* **[`technical-analysis`](technical-analysis/SKILL.md):** Deterministic momentum indicators, multi-timeframe moving average alignments, Bollinger Bands, and support/resistance confluence levels via `scripts/ta.py`.

### 🔬 Research & Prompt Architecture
* **[`deep-research`](deep-research/SKILL.md):** Autonomous multi-source recursive research engine utilizing the Gemini Interactions API.
* **[`generate-prompt`](generate-prompt/SKILL.md):** High-performance prompt generator utilizing Andrew Ng structured prompting principles and few-shot conditioning.
* **[`prompt-library.md`](prompt-library.md):** Curated, battle-tested prompt blocks for progressive context management across agent conversations.

### 🔄 The Meta-Skills Harness
* **[`create-skill`](create-skill/SKILL.md):** Forward authoring and retrospective session distillation scaffolder.
* **[`eval-skill`](eval-skill/SKILL.md):** Mines live conversation history to extract positive/negative behavioral assertions into Anthropics-compatible eval suites.
* **[`evolve-skill`](evolve-skill/SKILL.md):** Closed-loop evolution orchestrator that diagnoses failures, patches `SKILL.md`, and runs CSO security audits.
* **[`run-evals`](run-evals/SKILL.md):** Provider-neutral automated eval replay runner with LLM-as-judge scoring.

---

## ⚡ Quick Start

```bash
# 1. Clone repository
git clone git@github.com:jagveerbrar/jskills.git ~/Projects/jskills

# 2. Synchronize skills to global agent hub
./scripts/sync-skills.sh

# 3. Check for external upstream updates
./scripts/sync-skills.sh --check
```

---

## 🛡️ Security & Script Immutability
All resident CLI tools enforce strict read/execute immutable permissions (`chmod 555`). Workflows modifying tool code require an automated security audit before re-locking permissions.
