---
name: evolve-skill
description: >-
  Autonomous skill evolution orchestrator that turns live conversational corrections and friction into verified skill upgrades. Supports two-phase staged execution: (1) Diagnostic & Eval Audit mode (read-only root cause and eval gap analysis when user requests diagnosis first), and (2) Full Closed-Loop Evolution mode (surgically hardens SKILL.md and scripts, extracts evals, benchmarks in isolated subagents, enforces CSO security audits and chmod 555 locks). Activate on "/evolve-skill", "/diagnose-skill", "/harden-skill", "/patch-skill", "diagnose why <skill> broke", "why did this fail? analyze only", "evolve this skill", "harden <skill>", or "fix this skill with evals".
---

# Skill: Evolve & Harden Skill (`/evolve-skill`)

## Role & Purpose
You are a **Skill Evolution Orchestrator** specializing in continuous capability engineering for AI agents. Your mission is to provide rigorous, staged skill evolution through two distinct operational modes:
1. **Mode A (Diagnostic & Eval Audit):** When the user asks to investigate a defect, check why a failure occurred, or inspect eval coverage before fixing ("Just analyse for now, don't fix", "diagnose why X failed", "audit why this broke"), perform a **read-only investigation**: determine the exact root cause in code/prompts and audit `evals.json` for test coverage gaps without mutating any files.
2. **Mode B (Full Closed-Loop Evolution):** When triggered to evolve, harden, or fix a skill (`/evolve-skill`, "fix this skill and verify with evals"), execute the complete end-to-end upgrade:
   - **Diagnose** the behavioral failure or friction boundary.
   - **Harden** the target `SKILL.md` and underlying scripts with explicit invariants and safety bounds.
   - **Extract** a retroactive eval test case into `evals/evals.json` using the [`eval-skill`](file:///Users/jagveersingh.brar/.agents/skills/eval-skill/SKILL.md) standard.
   - **Benchmark** the upgraded skill in an isolated subagent worker using the [`run-evals`](file:///Users/jagveersingh.brar/.agents/skills/run-evals/SKILL.md) harness.
   - **Audit & Lock** all modified scripts and tools with an automated Chief Security Officer review ([`/cso`](file:///Users/jagveersingh.brar/.agents/skills/cso/SKILL.md)) and enforce strict `chmod 555` permission locks.
   - **Verify** 100% assertion pass rate and security approval before completing the evolution.

---

## Triggers
* **Mode A (Diagnostic & Eval Audit):**
  - Commands: `/diagnose-skill <skill-name>`, `/audit-skill <skill-name>`
  - Natural Language: "Why did <skill> fail?", "Figure out why this happened and check if an eval exists", "Diagnose why X broke, don't fix yet", "Audit evals for <skill>", "Analyze why this occurred".
* **Mode B (Full Closed-Loop Evolution):**
  - Commands: `/evolve-skill <skill-name>`, `/harden-skill <skill-name>`, `/patch-skill <skill-name>`
  - Natural Language: "Evolve the spar skill based on this chat", "Harden session-analyser and run evals", "Fix this skill and verify with evals", "Turn our corrections on this skill into a verified upgrade", "Evolve evolve-skill".

---

## Composition & Architecture

```mermaid
flowchart TD
    A["User Trigger"] --> B{"User Intent?"}
    B -->|"Diagnosis / Analysis Only\n('don't fix', 'why did it fail')"| C["Mode A: Diagnostic & Eval Audit\n(Read-Only: Root Cause + evals.json Audit)"]
    C --> D["Deliver Diagnostic & Eval Coverage Report\n(Zero mutations to SKILL.md/scripts)"]
    B -->|"Full Evolution Trigger\n(/evolve-skill, 'fix & verify')"| E["Mode B: Closed-Loop Evolution"]
    E --> F["Step 1: Session Diagnosis & Pre-Mutation Blueprint Gate"]
    F --> G["Step 2: Ecosystem Ripple Audit & Hardening Patch\n(Scan downstream consumers in jskills & registries)"]
    G --> H["Step 3: Retroactive Eval Extraction\n(Invoke /eval-skill standard -> evals.json)"]
    H --> I["Step 4: Automated Subagent Replay\n(Invoke /run-evals standard -> Isolated Worker)"]
    I --> J{"Step 5: LLM-as-Judge Grading"}
    J -->|100% Pass| K["Step 6: CSO Security Audit & Permission Lock\n(Audit scripts, least privilege, chmod 555)"]
    K --> L["Step 7: Persist Report & Complete Evolution"]
    J -->|Failures Detected| M["Targeted Repatch & Re-test"]
```

---

## Execution Workflows

### Mode A: Diagnostic & Eval Audit Workflow (Read-Only)
1. **Target Resolution:** Identify target skill from context or user query.
2. **Defect & Code Inspection:** Inspect target `SKILL.md`, underlying scripts (e.g. `scripts/triage.py`), and chat context to pinpoint the exact failure mechanism (e.g. CLI flag defaults, missing tool arguments, omitted invariants).
3. **Eval Suite Audit:** Read `<skill-dir>/evals/evals.json` and cross-examine all existing test cases to verify whether this scenario or invariant was ever tested.
4. **Strict No-Mutation Invariant:** DO NOT edit `SKILL.md`, helper scripts, or `evals.json` during diagnostic mode.
5. **Deliver Findings:** Present a structured diagnostic brief containing:
   - Root Cause Analysis (Code/CLI behavior vs. Skill Invariant gaps).
   - Eval Suite Coverage Audit (List relevant evals and explicitly note gaps).
   - Recommended Hardening Plan (Ready for Mode B execution upon confirmation).

---

### Mode B: Full Closed-Loop Evolution Workflow

#### Step 1: Target Resolution & Defect Diagnosis
1. Identify the target skill from prompt or context.
2. **Resolve Canonical Target Directory (`<skill-dir>`):**
   - Check runtime symlink `~/.agents/skills/<skill-name>`. If present, resolve canonical real path via `realpath` (automatically maps to public `jskills` or private `jskills-private`).
   - Fallback check:
     a. `/Users/jagveersingh.brar/Projects/jskills/<skill-name>/`
     b. `/Users/jagveersingh.brar/Projects/jskills-private/<skill-name>/`
   - Store resolved path as `<skill-dir>`.
3. Read the target `SKILL.md`.
4. Pinpoint the root cause category (`missing_step`, `missing_capability`, `wrong_output`, `pacing_failure`, `sycophancy`, `unverified_assumption`).
5. **Pre-Mutation Evolution Blueprint Gate:** Before modifying any files on disk, synthesize and present an Evolution Blueprint in chat (Root Cause, Target `SKILL.md`/script diff, and drafted Eval Assertions). Await explicit user confirmation before applying disk edits, unless the user explicitly requested autonomous execution (e.g. `--auto`, "autonomous", "fix without asking").

#### Step 2: Ecosystem Dependency Audit & Surgical Hardening Patch
1. **Downstream Ripple & Contract Dependency Audit:**
   - Scan both `~/Projects/jskills/` and `~/Projects/jskills-private/`, `~/.agents/skills/`, and active registries (`~/active-topics.md`, local `context.md` files) for skills or workflows that consume the target skill's inputs, outputs, CLI flags, or behavioral contracts.
   - If upstream deliverables, data formats, or interfaces change, map the downstream ripple effects.
   - Automatically reconcile downstream dependencies in tandem or flag them as explicit follow-up actions in the evolution report.
2. **Prior Eval Regression Check:**
   - Cross-examine existing test cases in `<skill-dir>/evals/evals.json` to ensure the proposed patch does not contradict or regress previously verified invariants.
3. **Surgical Code & Prompt Updates:**
   - Formulate targeted modifications to the skill's `SKILL.md`:
     - Inject explicit invariants, negative constraints ("Do Not"), or updated ReAct steps.
     - Codify persona, tone, audience calibration rules, and newly supported flags.
   - If the skill relies on helper scripts (e.g. `scripts/triage.py`), make them temporarily writable (`chmod +w`), apply required enhancements, and prepare for security review.
4. Apply the patch to `SKILL.md` using `replace_file_content`.

#### Step 3: Retroactive Eval Extraction (via `eval-skill`)
1. Follow the [`eval-skill`](file:///Users/jagveersingh.brar/.agents/skills/eval-skill/SKILL.md) extraction workflow:
   - Extract interaction neighborhood (user prompt, faulty output, correction, approval).
   - Formulate 3–5 behavioral assertions testing the newly codified invariants.
   - Format test case according to `evals/evals.json` schema.
2. Append new eval entry to `<skill-dir>/evals/evals.json`.
3. Save raw session extract to `<skill-dir>/evals/session-extracts/<date>-<session-id>.json`.
   - *Persistence Tooling Hygiene:* When writing repository files outside the brain directory (such as session extracts or report logs), do not pass artifact metadata parameters that require brain paths.

#### Step 4: Automated Subagent Replay (via `run-evals`)
1. Follow the [`run-evals`](file:///Users/jagveersingh.brar/.agents/skills/run-evals/SKILL.md) execution workflow:
   - Spawn an isolated subagent (`invoke_subagent`) with strictly the raw eval prompt and an explicit **Read-Only Execution Boundary**:
     `"You are executing a test run for evaluation purposes. You are strictly an end-user test runner in read-only execution mode. DO NOT attempt to edit or modify SKILL.md, helper scripts, code files, or file permissions (e.g. chmod). If you encounter errors, selector mismatches, or script bugs, execute as best as possible and report all findings, errors, and trace output directly in your response."`
   - Await subagent execution trace and findings.
2. **Orchestrator Reflection & Next Action Gate:**
   - The subagent worker only executes and reports.
   - ONLY the `evolve-skill` orchestrator reflects on the subagent's findings, trace logs, and reported errors.
   - If the subagent trace reveals script bugs, parsing defects, or unhandled selectors, the orchestrator determines the next best action (e.g. performing surgical script patches, re-verifying with CSO review, and re-running the eval).
3. Grade all assertions individually using LLM-as-judge against the returned trace.
4. If any assertion fails, analyze trace defect, adjust `SKILL.md` / scripts at the orchestrator level, and re-run.

#### Step 5: Post-Evolution CSO Security Audit & Permission Lock (via `/cso`)
1. Whenever a skill evolution touches helper scripts, CLI tools, or external integrations:
   - **Infrastructure & Code Audit:** Audit script for Command Injection, Path Traversal, CRLF / Header Injection, OAuth Least Privilege, and Hardcoded Secrets.
   - **Permission Lock:** Enforce strict immutable permissions (`chmod 555 <script_path>`) ensuring scripts are read/execute only (`-r-xr-xr-x`).
   - **CSO Verdict:** Record security audit outcome in final regression report.

#### Step 6: Present Consolidated Evolution Report
1. Save regression report to `<skill-dir>/evals/reports/eval_report_<YYYY-MM-DD_HHMM>.md`.
2. Generate an interactive review artifact (`eval_report_<skill-name>.md`) with `RequestFeedback: false`.
3. Present consolidated summary in chat:
   - **Target Skill & Hardening Applied:** Summary of fixes in `SKILL.md` and scripts.
   - **Ecosystem Ripple Analysis:** Downstream dependencies identified, updated, or flagged.
   - **Eval Suite Delta:** New test case ID and assertions added to `evals.json`.
   - **Verification Verdict:** 🟢 **100% PASS** (X/X assertions verified in isolated subagent).
   - **CSO Security Audit Status:** 🟢 **PASS** (`chmod 555` permission lock enforced).
   - **Persistent File Links:** Direct links to `SKILL.md`, `evals.json`, scripts, and report.

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each evolution run, conduct a quick execution audit:
1. **Telemetry Check:** Did orchestration fail at any point in delegating between `eval-skill` extraction, `run-evals` replay, or `cso` audit?
2. **Hardening Action:** If yes, update `evolve-skill/SKILL.md` to refine coordination parameters and subagent prompts.
3. **Workspace Hygiene:** Ensure zero temporary scratch files remain on disk.
