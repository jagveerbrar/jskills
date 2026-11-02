---
name: deep-research
description: >-
  Autonomous deep research engine using Google's Gemini Interactions API. Initiates recursive background research, polls execution state, and compiles cited markdown intelligence reports. Activate on "/deep-research", "/gdr", "run deep research on...", "deep research", or when conducting autonomous multi-source market or technical research.
---

# Skill: Deep Research (`/deep-research`)

## Role & Purpose
You are an autonomous intelligence researcher and research orchestrator. You leverage Google's official **Gemini Interactions API** (`google-genai` SDK) via a unified resident CLI engine (`scripts/research.py`) to execute recursive, multi-step web research, cross-reference diverse sources, and compile cited, venture-grade markdown briefing documents.

---

## Triggers
* **Command:** `/deep-research`, `/gdr`
* **Natural Language:** "Run deep research on...", "Deep research market dynamics for...", "Investigate post-mortems of...", "Autonomous research on..."

---

## Operating Constraints & Safety
1. **Unified Engine Rule:** All research execution and status polling must run through `scripts/research.py`. Never author ad-hoc scratch scripts or fragmented scrapers in project folders.
2. **Asynchronous Background Execution:** Deep research runs take 3–15 minutes. The agent MUST launch long-running executions using background execution so the chat session remains responsive.
3. **Agent as Natural Language Orchestrator:** The human communicates in high-level intent. The agent crafts inversion-driven research briefs (consulting [`references/prompting_guide.md`](references/prompting_guide.md)), invokes the CLI under the hood, and presents structured progress digests in Markdown.
4. **Resident Script Immutability:** `scripts/research.py` is permanently locked with `chmod 555` to prevent tampering.
5. **Output Destination Contract:** Default reports are saved to `<cwd>/research/<slug>_<timestamp>.md`.

---

## Execution Workflow

### Step 1: Prompt Inversion & Framing
Before calling the CLI, frame the research prompt to avoid generic marketing fluff. Incorporate principles from [`references/prompting_guide.md`](references/prompting_guide.md):
- **Post-mortems & Bottlenecks:** What failed previously?
- **Bottom-Up Economics:** What are the actual pricing tiers, gross margins, and COGS?
- **Unserved Friction:** What are recurring complaints on forums and reviews?
- **Regulatory Hurdles:** What specific compliance risks exist?

### Step 2: Launching the Research Run

Launch the unified CLI tool in the background:

```bash
uv run ~/.agents/skills/deep-research/scripts/research.py run "<structured-research-prompt>" --output "<destination-path>.md"
```

*For multi-step or manual polling, use the `start` and `poll` subcommands:*
```bash
# Start background interaction and get ID
uv run ~/.agents/skills/deep-research/scripts/research.py start "<prompt>" --json

# Poll status
uv run ~/.agents/skills/deep-research/scripts/research.py poll <interaction-id> --json
```

### Step 3: Notification & Ingestion
When notified that the background task has completed:
1. Confirm the generated markdown file exists on disk.
2. Provide a 3-bullet executive digest in the chat highlighting:
   - Core non-obvious findings.
   - Primary bottlenecks or failure modes discovered.
   - Top 3 cited sources.
3. Link directly to the generated report file: `[Report](file:///path/to/report.md)`.

### Step 4: Downstream Handoff (The Action Flywheel)
Do not stop at research. Offer immediate downstream actions:
- **Concept Stress-Testing:** Feed the report into `/spar` to challenge assumptions.
- **Venture Prototyping:** Feed findings into `/prototype-generator` to draft a smoke test or PRD.

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each deep research session, conduct a quick execution audit:
1. **Telemetry Check:** Did the run require custom polling intervals, unsupported agent model tags, or novel prompt schemas not covered in `references/prompting_guide.md`?
2. **Hardening Action:** Consolidate any necessary subcommands or parameter adjustments directly into `scripts/research.py` and update this `SKILL.md`.
3. **Workspace Hygiene:** Ensure no intermediate scratch files or orphan polling logs remain in the working directory.
