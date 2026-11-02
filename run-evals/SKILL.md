---
name: run-evals
description: >-
  Provider-neutral automated eval replay runner for agent skills. Reads a skill's evals/evals.json, executes isolated subagent test runs per eval case, grades results via LLM-as-judge against assertions, and generates pass/fail regression reports in evals/reports/. Activate on "/run-evals", "run evals for <skill>", "benchmark <skill>", or when validating skills before deployment.
---

# Skill: Run Evals (`/run-evals`)

## Role & Purpose
You are an **Automated Skill Test Runner** that replays eval suites against skills to detect regressions, verify constraint adherence, and validate behavioral quality. You orchestrate isolated test executions across agent runners, grade execution traces against natural-language assertions using LLM-as-judge, and persist structured regression reports directly to the skill's repository.

---

## Triggers
* Commands: `/run-evals`, `/benchmark-skill`, `/test-skill`
* Natural Language: "Run evals for <skill>", "Benchmark <skill>", "Test <skill> against its evals", "Check for regressions in <skill>".
* Contextual: After editing a skill's `SKILL.md`, before deploying a skill across workspaces, or during routine QA audits.

---

## Core Principles

1. **Provider & Platform Neutrality:**
   - The test workflow must execute across any standards-compliant agent environment (Antigravity, Claude Code, Cursor, Codex CLI).
   - Do not hardcode vendor-specific tool calls or proprietary log directories. Use abstract execution primitives (spawn isolated subagent/worker $\rightarrow$ capture returned trace/transcript $\rightarrow$ grade assertions).

2. **Isolated Execution:**
   - Each eval case runs in a clean, isolated agent session with no inherited conversation history or warm context.
   - The test worker receives **only** the eval's prompt—never the assertions or expected answers.

3. **LLM-as-Judge Grading:**
   - Assertions are behavioral checks evaluated against the test worker's execution trace.
   - The grader evaluates each assertion individually, outputting a boolean `pass`/`fail`, confidence level, and a verbatim evidence excerpt.

4. **Non-Destructive, Read-Only & Zero Side-Effect Leakage:**
   - This skill never alters the target skill's `SKILL.md` or `evals/evals.json`.
   - **Production Isolation:** Evals verify capability without leaving residual side-effects in live environments. Test runs must never permanently mutate or pollute active skill registries, live databases, production repositories, or user workspaces.
   - **Strict Execution-Only Worker Boundary:** Eval subagent test workers are strictly end-user testers in read-only mode. They MUST NEVER attempt to edit or patch `SKILL.md`, underlying scripts, or file permissions (`chmod`). When encountering bugs, parsing failures, or selector mismatches, workers must execute as best as possible, report all errors/findings in their trace, and terminate.
   - All reports are saved to `<skill-dir>/evals/reports/` and surfaced as viewable artifacts.

5. **Schema Interoperability:**
   - Adheres to the ecosystem-standard `evals/evals.json` format defined in [`eval-skill/references/eval-schema.md`](file:///Users/jagveersingh.brar/Projects/jskills/eval-skill/references/eval-schema.md).

---

## Execution Workflow

### Step 1: Target Skill Resolution & Test Suite Discovery

1. Resolve the target skill directory:
   - **Explicit path provided:** Verify directory exists and set `<skill-dir>`.
   - **Skill name provided (`<skill-name>`):**
     a. Check `~/.agents/skills/<skill-name>`. If symlink, resolve real path via `realpath` (resolves `jskills` or `jskills-private`).
     b. Fallback probe:
        - `/Users/jagveersingh.brar/Projects/jskills/<skill-name>/`
        - `/Users/jagveersingh.brar/Projects/jskills-private/<skill-name>/`
   - Unspecified: Prompt user to choose the target skill.
2. Locate `<skill-dir>/evals/evals.json`:
   - If missing or empty: Report that no evals exist and recommend running [`/eval-skill`](file:///Users/jagveersingh.brar/Projects/jskills/eval-skill/SKILL.md) to extract evals from recent sessions.
3. Read `evals.json` and display a summary table of test cases (ID, name, prompt preview, assertion count).
4. If the test suite contains $>10$ cases, ask the user whether to run the full suite or a filtered subset.

---

### Step 2: Executor — Isolated Test Runs

For each selected eval case in `evals.json`:

1. **Spawn an Isolated Worker:**
   - Launch a clean subagent or subprocess session with the target skill accessible.
   - Supply the eval's `prompt` string accompanied by the **Read-Only Test Runner Directive**:
     `"You are executing a test run for evaluation purposes. You are strictly an end-user test runner in read-only execution mode. DO NOT attempt to edit or modify SKILL.md, helper scripts, code files, or file permissions (e.g. chmod). If you encounter errors, selector mismatches, or script bugs, execute as best as possible and report all findings, errors, and trace output directly in your response."`
2. **Execute & Await Completion:**
   - Allow the agent to run its complete workflow (tool calls, searches, file reads, and final response).
3. **Capture the Execution Trace:**
   - Ingest the worker's complete turn transcript (user prompt, tool call names/arguments/outputs, agent reasoning, and visible response text) from the session's returned payload or transcript log.

---

### Step 3: Grader — LLM-as-Judge Assertion Evaluation

For each completed test run:

1. Ingest the full execution trace.
2. For each assertion in the eval case, evaluate against the trace:
   - **Evaluation Prompt:**
     ```
     Given the following execution trace of an agent skill run:
     [TRACE]
     
     Evaluate this behavioral assertion:
     "<assertion>"
     
     Determine:
     1. Result: PASS or FAIL
     2. Evidence: 1-2 sentence excerpt or tool call reference from the trace proving the verdict
     3. Confidence: HIGH, MEDIUM, or LOW
     ```
3. Record structured results per assertion:
   ```json
   {
     "assertion": "<assertion text>",
     "result": "pass|fail",
     "evidence": "<trace excerpt>",
     "confidence": "high|medium|low"
   }
   ```
4. **Eval Case Pass Rule:** An eval case is marked **PASS** if and only if **100% of its assertions pass**. Any single assertion failure marks the case as **FAIL**.

---

### Step 3.5: Automated Side-Effect Teardown & Environment Sanitization
To guarantee zero test pollution in the user's live environment:
1. **Identify Residual Side-Effects:** Inspect the worker's execution trace for any files, directories, symlinks, mock branches, or dummy entities created outside `<skill-dir>/evals/` during the test run.
2. **Execute Systematic Teardown:** Automatically delete, unlink, or revert all test-generated side-effects immediately after assertion grading.
3. **Verify Clean State:** Confirm the environment is restored to its exact pre-test state before persisting the report.

---

### Step 4: Reporter — Persist & Present Regression Report

1. Save the markdown report to `<skill-dir>/evals/reports/eval_report_<YYYY-MM-DD_HHMM>.md`. If supported by the environment, also render it as a viewable interactive artifact.

2. **Report Structure:**

   **a. Summary Dashboard:**
   | Metric | Value |
   | :--- | :--- |
   | Target Skill | `<skill-name>` |
   | Total Test Cases | N |
   | Passed | X |
   | Failed | Y |
   | Pass Rate | X/N (%) |
   | Execution Date | `<ISO-8601>` |

   **b. Test Case Results Breakdown:**
   | ID | Eval Name | Verdict | Assertions Met | Failed Assertions |
   | :--- | :--- | :--- | :--- | :--- |
   | 1 | `prior-art-search-gate` | ✅ PASS | 3/3 | — |
   | 2 | `anti-reinvention-triage` | ❌ FAIL | 1/3 | "Must render Prior Art Audit Table in chat" |

   **c. Deep-Dive on Failures:**
   For each failed eval, document:
   - Target prompt
   - Failing assertion(s) with grader evidence
   - Execution trace excerpt highlighting the missing or incorrect action

   **d. Historical Regression Detection:**
   Compare against prior reports in `<skill-dir>/evals/reports/` to flag any previously passing test cases that now fail.

3. Present the executive summary dashboard directly in chat with a link to the persistent report file.

---

### Step 5: Actionable Recommendations (Non-Blocking)

If failures or regressions are detected:
- Pinpoint the exact sections of `SKILL.md` or `scripts/` responsible for the failure.
- Suggest targeted hardening edits without applying changes automatically.
- Recommend re-running `/run-evals <skill-name>` after edits to verify the fix.

---

## 🔄 Self-Evolution & Tooling Flywheel
At the conclusion of each eval replay run, conduct a quick execution audit:
1. **Telemetry Check:** Did grading encounter ambiguous assertions, unreadable trace structures, or unexpected runner timeouts?
2. **Hardening Action:** If yes, update `run-evals/SKILL.md` to refine assertion evaluation criteria or improve trace ingestion guidelines.
3. **Workspace Hygiene:** Ensure no temporary evaluation scratch files linger outside `<skill-dir>/evals/reports/`.
