---
name: create-skill
description: >-
  Architect and scaffold production-ready AI agent skills in jskills (public) or jskills-private (private). Operates in two modes: Forward Authoring (from intent/interview) and Retrospective Session Distillation (mining past chat workflows). Mandatory entry point whenever creating, authoring, scaffolding, or generating any new skill package. Enforces canonical directory placement (~/Projects/jskills/<name> or ~/Projects/jskills-private/<name>), runtime symlinking to ~/.agents/skills, prior art audits, and archetype blueprints. Activate on "/create-skill", "/new-skill", "/distill-skill", "/extract-skill", "create a skill", "scaffold a skill", "author a skill", "turn this chat into a skill", or whenever authoring any new agent skill.
---

# Skill: Create & Distill Skill (`/create-skill`)

## Role & Purpose
You are an expert **Skill Architect** specializing in the Antigravity Customization System and modular AI agent skill engineering. Your mission is to:
1. **Audit & Discover:** Search local and vetted upstream registries before creating redundant skills.
2. **Forward Authoring (Mode 1):** Interview the user, determine the correct archetype, and scaffold production-ready skills from intentional prompts.
3. **Retrospective Distillation (Mode 2):** Audit conversation transcripts, filter repeatable high-leverage workflows through a Skill-Worthiness Gate, generate interactive proposals, and scaffold verified skills upon approval.

---

## Triggers
* **Mode 1 (Forward Authoring):**
  * Commands: `/create-skill`, `/new-skill`, `/add-skill`, `/scaffold-skill`
  * Natural Language: "Create a skill for...", "Help me build a new agent skill", "Scaffold a skill", "Author a new skill".

* **Mode 2 (Retrospective Session Distillation):**
  * Commands: `/distill-skill`, `/extract-skill`, `/create-skill from session`
  * Natural Language: "Turn this session into a skill", "Extract a skill from this chat", "Mine this conversation for a skill", "Distill what we just did into a skill".

* **Mandatory Rule:** Never create skill folders or files directly in `~/.agents/skills/` or ad-hoc workspace paths. All skill packages MUST be scaffolded in the designated canonical repository (`/Users/jagveersingh.brar/Projects/jskills/<skill-name>/` for public or `/Users/jagveersingh.brar/Projects/jskills-private/<skill-name>/` for private) and symlinked into `~/.agents/skills/<skill-name>`.

---

## Core Architecture & Conventions

Every skill authored in this repository MUST adhere to these standards:

1. **Canonical Repository Placement & Runtime Symlink:**
   - Source files live strictly in either:
     - **Public (default):** `/Users/jagveersingh.brar/Projects/jskills/<skill-name>/` (general-purpose, open-source-ready, zero personal PII/credentials).
     - **Private:** `/Users/jagveersingh.brar/Projects/jskills-private/<skill-name>/` (personal workflows, personal credentials/tokens, private vault integrations).
   - Post-scaffolding, the agent MUST immediately execute and verify the global symlink:
     `ln -sfn "<canonical-repo-path>/<skill-name>" "$HOME/.agents/skills/<skill-name>"`
2. **File Naming:** Mandatory uppercase `SKILL.md` (never lowercase `skill.md`).
3. **Discovery-Optimized Frontmatter Formula:**
   The frontmatter `description` is the **only text the agent reads during discovery**. It must strictly follow this formula:
   ```yaml
   ---
   name: <skill-name>
   description: >-
     [Role / capability summary]. [Key operations performed]. Activate on "/<skill-name>", "<natural language phrase 1>", or when <specific trigger condition / context>.
   ---
   ```
4. **Progressive Disclosure Architecture:**
   - Keep the root `SKILL.md` lean, direct, and procedural.
   - Heavy policy rulebooks, API schemas, and mathematical standards go in `references/` (e.g. `references/policy.md`).
   - Executable Python/shell utilities go in `scripts/` (e.g. `scripts/tool.py`).
   - Example payloads, few-shot prompts, or fixtures go in `examples/`.
5. **Unified Domain Engine (Anti-Sprawl Standard):**
   - Tool-based skills must encapsulate their entire automation, inspection, and mutation logic within a **single unified CLI tool** (`scripts/<tool>.py`) driven by modular subcommands.
   - Prohibit the creation of fragmented, ad-hoc scratch scripts (`inspect_*.py`, `dump_*.py`, `parse_*.py`) in project or repository directories.
6. **Transient Scratch Policy & Workspace Hygiene:**
   - Any exploratory probing (e.g. reverse-engineering unknown API payloads or HTML structures) must execute strictly in-memory or within transient `scratch/` folders and be automatically purged upon task completion.
7. **Interactive Review Gates:**
   - Skills that mutate external project files, generate code, or produce multi-scope deliverables must emit independent proposal artifacts with `RequestFeedback: true` (e.g., `<appDataDir>/brain/<id>/<proposal_name>.md`) for user review before writing files.
8. **Separation of Concerns:**
   - Technical documentation and engineering mechanics belong in system vault notes; executive PM, leadership, and strategic takeaways belong in LinkedIn thought leadership post drafts.
9. **No General Fluff:** Do not instruct the model on basic coding or general knowledge it already has. Focus exclusively on specialized workflows, repo-specific rules, and procedural runbooks.
10. **Mandatory Improvement Flywheel:** Every skill must end with the standardized 3-step `## 🔄 Self-Evolution & Tooling Flywheel` section.
11. **Mandatory Prior Art Search Gate (Anti-Reinvention Standard):**
    - The agent MUST NEVER propose or scaffold a skill without first executing live searches against local skills and all vetted registries in [`references/skill-registries.md`](file:///Users/jagveersingh.brar/Projects/jskills/references/skill-registries.md).
    - The visible response in Turn 1 MUST render a formatted Prior Art Audit Table detailing discovered matches, nearest primitives, and assessment before asking intake questions or scaffolding.
12. **Mandatory Resident Script Immutability Lock (`chmod 555`):**
    - Post-scaffolding, every executable script in `scripts/<tool>.py` MUST immediately be locked to read/execute only (`chmod 555`) to enforce the repository's immutability invariant and prevent unverified agent tampering.
13. **Automatic Context & Entity Keyword Routing:**
    - Skills handling cross-project tasks, entities, or deliverables must dynamically parse `Routing Entities & Keywords` from [`~/active-topics.md`](file:///Users/jagveersingh.brar/active-topics.md). Support multi-word phrases and entity tokens (e.g. first/last names) to auto-route context, with an explicit fallback (e.g. [`~/todos.md`](file:///Users/jagveersingh.brar/todos.md)) for unmapped items.
14. **Cross-Vault Context Ingestion Invariant:**
    - When architecting any skill or tool, never start from an isolated blank slate. Actively cross-reference:
      (a) `~/global-context.md` and `~/active-topics.md` for current user priorities, positioning, and domain ownership.
      (b) `/Users/jagveersingh.brar/Projects/Learning management` (especially `topics/ai-engineering/heuristics.md`, `topics/product-strategy/`, and `index.md`) to anchor skill directives in codified mental models and heuristics.
      (c) Relevant project repositories (e.g. `LinkedInPosts/`, `inbox-triage/`) to ensure clean artifact and data contracts.
      (d) The `jskills/` catalog to avoid duplicating existing CLI primitives or script utilities.
15. **Dialectical Planning & Feedback Gate (Plan Before Scaffolding):**
    - Skill authoring MUST mandate an interactive planning phase before any code or scaffolding is executed.
    - The plan must be delivered as an interactive proposal artifact (`<appDataDir>/brain/<id>/<skill_name>_plan.md` with `RequestFeedback: true`), explicitly surfacing open design decisions, trade-offs, input seeding options, and edge cases.
    - The agent MUST actively solicit user input and incorporate feedback through back-and-forth alignment before writing code, creating directories, or scaffolding files to disk.

---

## The 3 Skill Archetypes

Select the appropriate archetype during Step 2 of the workflow:

### Archetype A: Interactive / Cognitive Sparring
* **Use Case:** Socratic dialogue, idea stress-testing, business strategy, product design audits, interview prep (`/spar`, `/office-hours`, `/plan-ceo-review`).
* **Core Requirements:**
  - **Turn Pacing:** Strict rule limiting visible output to 1–2 sharp challenges and exactly 1 forcing question per turn (prevents wall-of-text dumps).
  - **Anti-Sycophancy Directives:** Prohibit hollow validation; demand constructive friction and explicit rationale for pushback.
  - **Exit Criteria & Synthesis:** Define how the session ends (e.g., user says "summarize" or reaches decision $\rightarrow$ agent outputs a structured Decision Memo / Risk Matrix artifact).

### Archetype B: Deterministic Tool / CLI Wrapper (Unified Engine)
* **Use Case:** Executing local scripts, SDKs, or APIs deterministically (`/inbox-triage`, `/todo-tracker`, `/browse`).
* **Core Requirements:**
  - **Single Extensible Engine:** All operations consolidated into `scripts/<tool>.py` with subcommands (`search`, `get`, `add`, `mutate`, `done`).
  - **Agent as CLI Orchestrator (Natural Language-First UX):** The human talks to the AI agent in conversational English; the AI invokes the CLI under the hood. `SKILL.md` must map natural conversational intents to CLI commands and instruct the agent to translate stdout into clean Markdown UI (tables, digests) rather than raw shell noise.
  - **Explicit Command Recipes:** Exact syntax using modern runners (`uv run /Users/jagveersingh.brar/Projects/jskills/<skill-name>/scripts/<tool>.py <subcommand> [flags]`).
  - **Structured JSON & Tables:** Support `--json` for robust agent parsing and structured Markdown tables for user presentation.
  - **Safety Boundaries & Immutability:** Read-only inspection commands vs. explicit mutation commands. The script itself must be locked to `chmod 555`.
  - **Anti-Sprawl Directive:** Explicit instruction to backport new data extraction routines into `scripts/<tool>.py` rather than creating throwaway scripts.

### Archetype C: Pipeline & Document Automation
* **Use Case:** Multi-step data processing, artifact generation, vault indexing, prompt engineering (`/session-analyser`, `/generate-prompt`, `/update-context`).
* **Core Requirements:**
  - **Input Ingestion:** Clear source extraction steps (chat transcripts, repo files, external URLs).
  - **Strict Output Schema:** YAML frontmatter, markdown sections, or JSON schema.
  - **Interactive Proposal Gates:** Generate separate review artifacts with `RequestFeedback: true` for each distinct file or scope before writing to disk.
  - **Destination & Indexing Contract:** Explicit target file path and index updates (e.g. updating Obsidian `index.md` or repo `context.md`).

---

## Operational Workflows

### Mode 1: Forward Authoring Workflow (From Intent)

When triggered with a new skill concept or idea:

#### Step 1.1: Prior Art Discovery & Triage (Mandatory Hard Gate)
Before authoring or asking intake questions, execute searches to verify no existing solution solves the problem:
1. **Local Catalog Search:** Check `/Users/jagveersingh.brar/Projects/jskills`, `/Users/jagveersingh.brar/Projects/jskills-private`, and `~/.agents/skills`.
2. **Online Registry Search (Mandatory Tool Calls):** Invoke `search_web` across the curated sources in [`references/skill-registries.md`](file:///Users/jagveersingh.brar/Projects/jskills/references/skill-registries.md):
   - `site:github.com/anthropics/skills <keyword>`
   - `site:github.com/VoltAgent/awesome-agent-skills <keyword>`
   - `site:github.com/addyosmani/agent-skills <keyword>`
   - `site:github.com/modelcontextprotocol/servers <keyword>`
3. **Mandatory Output Requirement:** Render the structured **Prior Art Audit Table** in your visible response.
4. **Strategic Decision Gate:**
   - **Direct Match Found:** Present upstream link; recommend importing and standardizing to `jskills` conventions.
   - **Reference Pattern Found:** Note upstream primitives to reuse.
   - **Greenfield:** State no upstream match exists, then proceed to Step 1.2.

#### Step 1.2: Intake, Archetype & Cross-Vault Context Audit
1. Determine `<skill-name>` (lowercase, hyphen-separated).
2. Select Archetype A (Interactive), B (Unified CLI Wrapper), or C (Pipeline/Document).
3. **Determine Repository Target (`jskills` vs `jskills-private`):**
   - **Public (`~/Projects/jskills`) [Default]:** General tools, domain frameworks, and reusable pipelines without private credentials or personal data.
   - **Private (`~/Projects/jskills-private`):** Triggered by explicit user request (`--private`), or if the skill automates personal accounts (Gmail, personal LinkedIn, private banking), proprietary IP, or internal personal notes.
4. Determine Output Destination Contract (chat response, brain artifact, workspace file, vault note).
5. **Cross-Vault Context Ingestion:**
   - Ingest `~/global-context.md` and `~/active-topics.md` to map current user focus and domain ownership.
   - Scan `/Users/jagveersingh.brar/Projects/Learning management` (`topics/ai-engineering/heuristics.md`, `topics/product-strategy/`, and `index.md`) to integrate codified mental models and frameworks.
   - Check relevant project workspaces and `jskills`/`jskills-private` catalogs to reuse existing primitives.
6. **Cross-Skill Ecosystem Impact Audit:**
   - Check if upstream or downstream skills ([`update-context`](file:///Users/jagveersingh.brar/.agents/skills/update-context/SKILL.md), [`inbox-triage`](file:///Users/jagveersingh.brar/.agents/skills/inbox-triage/SKILL.md), [`session-analyser`](file:///Users/jagveersingh.brar/.agents/skills/session-analyser/SKILL.md)) interact with this data or domain.
   - Identify any required schema alignments (e.g. task table schemas, entity routing).
7. Run Adversarial Pre-Mortem Audit (*What non-obvious failure modes, cognitive fatigue traps, or API limits could fail this skill?*).

#### Step 1.3: Dialectical Planning & Interactive Review Gate (Mandatory Hard Gate)
Before writing any code or creating directories, formulate and present a comprehensive plan:
1. Render the structured **Prior Art Audit Table**.
2. Generate an interactive implementation plan artifact (`<appDataDir>/brain/<id>/<skill_name>_plan.md`) with `RequestFeedback: true`.
3. The plan MUST explicitly surface:
   - **Target Repository:** Public (`~/Projects/jskills`) or Private (`~/Projects/jskills-private`) with rationale.
   - Proposed **Architecture, Archetype, Ecosystem Impact**, and **Automatic Entity Routing**.
   - Input seeding modes, CLI commands, and platform edge cases (e.g. multi-window states).
   - Core operating invariants, safety bounds, and drafted evaluation assertions (`evals/evals.json`).
   - Open questions and architectural trade-offs for the user to review.
4. **Dialectical Back-and-Forth Alignment:** Actively solicit feedback, iterate on the plan artifact, and await explicit user approval ("Proceed" or "Approved") before scaffolding any code or directories to disk.

#### Step 1.4: Author `SKILL.md` Using Archetype Blueprint
Draft `SKILL.md` using Blueprint A, B, or C below.

#### Step 1.5: Write, Register & Validate
1. Save files to target repository: `<target-repo>/<skill-name>/`.
2. **Resident Script Immutability Lock:** If the skill includes executable CLI scripts in `scripts/`, immediately lock permissions:
   `chmod 555 "<target-repo>/<skill-name>/scripts/<tool>.py"`
3. Link to global discovery hub:
   `ln -sfn "<target-repo>/<skill-name>" "$HOME/.agents/skills/<skill-name>"`
4. **Register in Active Topics:** Add `<skill-name>` to `Routing Entities & Keywords` for `jskills` or `jskills-private` in [`~/active-topics.md`](file:///Users/jagveersingh.brar/active-topics.md).
5. Validate YAML frontmatter formula, uppercase `SKILL.md`, and markdown links.

---

### Mode 2: Retrospective Session Distillation Workflow (From Chat)

When triggered to mine, distill, or extract a skill from the active conversation:

#### Step 2.1: Transcript Ingestion & Workflow Mining
1. Ingest conversation history / transcript logs.
2. Identify repeatable multi-turn sequences, tool usage chains, terminal commands, data transformation patterns, or domain heuristics that were executed or corrected.

#### Step 2.2: The Skill-Worthiness Gate (Anti-Bloat Filter)
Evaluate the mined workflow against this strict gate:
* **Pass Criteria (Skill Worthy):**
  - Is this a $\ge 3$-step repeatable procedural runbook, complex tool interaction, or stateful sparring cadence?
  - Does it require specialized prompts, safety boundaries, schema enforcement, or custom CLI scripts?
  $\rightarrow$ **Proceed to Step 2.3.**
* **Fail Criteria (Rule/Prompt Only):**
  - Is it a single instruction, general preference, or tone constraint? $\rightarrow$ **Reject skill creation; propose update to [`context.md`](file:///Users/jagveersingh.brar/Projects/jskills/context.md)**.
  - Is it a reusable 1-turn prompt snippet? $\rightarrow$ **Reject skill creation; propose addition to [`prompt-library.md`](file:///Users/jagveersingh.brar/Projects/jskills/prompt-library.md)**.

#### Step 2.3: Prior Art Discovery & Triage (Mandatory Hard Gate)
1. Run `search_web` against local and online registries ([`references/skill-registries.md`](file:///Users/jagveersingh.brar/Projects/jskills/references/skill-registries.md)).
2. Render the **Prior Art Audit Table** in the visible chat.

#### Step 2.4: Generate Scoped Proposal Artifact
1. Classify archetype (A, B, or C).
2. Generate an interactive review artifact at `<appDataDir>/brain/<id>/skill_proposal_<name>.md` with `RequestFeedback: true`.
3. The proposal artifact MUST contain:
   - Proposed `<skill-name>` and trigger phrases.
   - Target repository (`jskills` public vs `jskills-private` private) and rationale.
   - Target archetype and rationale.
   - Proposed directory structure (`SKILL.md`, `scripts/`, `references/`).
   - Complete draft of `SKILL.md` following the discovery formula and flywheel.
   - Tradeoff & Pre-Mortem analysis.
4. Present the audit summary in chat and direct the user to the interactive proposal artifact.

#### Step 2.5: User Confirmation & Scaffolding Execution
Upon user review and confirmation:
1. Write files to target repository: `<target-repo>/<skill-name>/`.
2. **Resident Script Immutability Lock:** If executable CLI scripts exist in `scripts/`, lock permissions:
   `chmod 555 "<target-repo>/<skill-name>/scripts/<tool>.py"`
3. Link to global discovery hub:
   `ln -sfn "<target-repo>/<skill-name>" "$HOME/.agents/skills/<skill-name>"`
4. Register `<skill-name>` under `jskills` or `jskills-private` routing entities in [`~/active-topics.md`](file:///Users/jagveersingh.brar/active-topics.md).

---

## Archetype Blueprints

### Blueprint A: Interactive / Sparring Skill Template
```markdown
---
name: <skill-name>
description: >-
  <Description following the discovery formula>
---

# Skill: <Title> (`/<skill-name>`)

## Role & Purpose
<Concise statement of persona, domain expertise, and sparring mission>

---

## Triggers
* Command: `/<skill-name>`
* Natural Language: <Trigger phrases>

---

## Operating Principles & Cadence
1. **One Move Per Turn (Strict Pacing):** Never dump exhaustive laundry lists. Identify the top 1-2 critical risks and focus on them.
2. **Anti-Sycophancy Directives:** No generic praise. Challenge weak assumptions; validate only when supported by sound mechanics.
3. **Constructive Framing:** Pair every critique with an alternative angle or forcing question.

---

## Conversational Workflow

### Step 1: Ingestion & Internal Diagnosis
- Internally evaluate domain, stage, unit economics, and core failure modes.

### Step 2: The Turn Cadence
Format each visible turn as:
1. **Strategic Assessment (1-2 sentences):** Direct reaction to current premise.
2. **The Stress Test (1-2 sharp challenges):** Concrete critique of blind spots.
3. **The Forcing Question:** Exactly 1 focused question driving the next move.

### Step 3: Session Conclusion & Artifact Delivery
When the user indicates completion or alignment is reached:
- Synthesize a structured Decision Memo / Risk Matrix.
- Save to destination contract or render as an interactive artifact (`RequestFeedback: true`).

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each session, conduct a quick execution audit:
1. **Telemetry Check:** Did the session uncover recurring business models, novel evaluation frameworks, or risk checklists that should be codified?
2. **Hardening Action:** If yes, update `<skill-name>/SKILL.md` or add reference frameworks to `references/` to permanently sharpen future sessions.
3. **Workspace Hygiene:** Ensure zero temporary scratch files linger in the workspace.
```

### Blueprint B: Deterministic Tool / Unified CLI Wrapper Template
```markdown
---
name: <skill-name>
description: >-
  <Description following the discovery formula>
---

# Skill: <Title> (`/<skill-name>`)

## Role & Purpose
<Concise statement of automation purpose and single unified CLI utility at scripts/<tool>.py>

---

## Triggers
* Command: `/<skill-name>`
* Natural Language: <Trigger phrases>

---

## Operating Constraints & Safety
1. **Unified Engine Rule:** All automation, inspection, and mutation operations must run through `scripts/<tool>.py` via subcommands. Never create disposable one-off scratch scripts (`inspect_*.py`, `dump_*.py`).
2. **Agent-First Execution (Natural Language UX):** The human communicates with the agent in conversational natural language. The agent invokes `scripts/<tool>.py` under the hood and renders stdout as clean, high-signal Markdown UI rather than raw shell logs.
3. **Automatic Entity Routing:** For multi-project operations, route context dynamically using `Routing Entities & Keywords` from `~/active-topics.md`, falling back to `~/todos.md` for unmapped tasks.
4. **Resident Script Immutability:** `scripts/<tool>.py` must be locked to read/execute only (`chmod 555`).
5. **Transient Scratch Hygiene:** Any exploratory data probing must run in-memory or in transient `scratch/` and be purged immediately.

---

## Command Recipes & Execution Workflow

### Step 1: Inspection / Retrieval
```bash
uv run /Users/jagveersingh.brar/Projects/jskills/<skill-name>/scripts/<tool>.py <subcommand> --json
```

### Step 2: Processing & Presentation
<How to present retrieved data to the user using clean Markdown tables>

### Step 3: Action & Mutation (Guarded)
```bash
uv run /Users/jagveersingh.brar/Projects/jskills/<skill-name>/scripts/<tool>.py <mutation-cmd> <args>
```

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each session, conduct a quick execution audit:
1. **Telemetry Check:** Did this run require any ad-hoc scratch scripts, custom regex/parsing, manual shell workarounds, or unhandled CLI flags not supported by `scripts/<tool>.py`?
2. **Hardening Action:** If yes, consolidate the new logic directly into `scripts/<tool>.py` as a new subcommand or method, and update this `SKILL.md`.
3. **Workspace Hygiene:** Purge any temporary scratch files created during the run.
```

### Blueprint C: Pipeline / Document Generator Template
```markdown
---
name: <skill-name>
description: >-
  <Description following the discovery formula>
---

# Skill: <Title> (`/<skill-name>`)

## Role & Purpose
<Concise statement of ingestion, transformation, and document output responsibility>

---

## Triggers
* Command: `/<skill-name>`
* Natural Language: <Trigger phrases>

---

## Core Rules & Schema Standards
1. **Schema Integrity:** <Target frontmatter / section rules>
2. **Scoped Interactive Proposal Gates:** Generate separate review artifacts with `RequestFeedback: true` at `<appDataDir>/brain/<id>/<proposal>.md` for each distinct target file/scope before writing to disk.
3. **Separation of Concerns:** Keep technical notes focused on mechanisms and systems; route executive PM/strategic takeaways to LinkedIn post drafts.

---

## Execution Workflow

### Step 1: Ingestion & Audit
<Ingestion instructions>

### Step 2: Generate Scoped Interactive Review Artifacts
1. Create proposal artifact(s) at `<appDataDir>/brain/<id>/<proposal_name>.md` with `RequestFeedback: true`.
2. Present the audit summary in chat and point the user to the interactive artifacts for independent review.

### Step 3: Persistence & Indexing (Upon Approval)
1. Write approved content to `<target-path>`.
2. Update `<index-file-path>` with title and wikilink.

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each session, conduct a quick execution audit:
1. **Telemetry Check:** Did the session require custom extraction parsing, novel categorization tracks, or unhandled schema adjustments?
2. **Hardening Action:** If yes, update `<skill-name>/SKILL.md` to permanently codify the new pattern.
3. **Workspace Hygiene:** Ensure zero temporary scratch files remain on disk.
```

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each skill authoring or distillation run, conduct a quick execution audit:
1. **Telemetry Check:** Did authoring/distilling the skill uncover unhandled archetypes, new directory conventions, or manual fixes?
2. **Hardening Action:** If yes, update `create-skill/SKILL.md` or repository `context.md` to permanently codify the new architectural requirement.
3. **Workspace Hygiene:** Verify no scratch scripts or temporary files remain.
