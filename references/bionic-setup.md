# Bionic (LM Studio) Configuration Reference

This guide details how to configure **Bionic** in LM Studio to automatically align with your local agent setup.

---

## 1. System Prompt Preset (One-Time Setup in LM Studio)
In LM Studio:
1. Go to **My Models** or **Active Preset Settings**.
2. In the **System Prompt** field, paste:

```text
You are an expert engineering and product agent.
Mandatory Startup Action: On the very first user turn, immediately read /Users/jagveersingh.brar/global-context.md via file reading tool.
When working in any project directory, treat AGENTS.md in the workspace root as the authoritative project context, rules, and milestones.
```

---

## 2. Project Execution in Bionic
* When opening any project folder from `/Users/jagveersingh.brar/Projects/` in Bionic:
  * Bionic will automatically detect and ingest [`AGENTS.md`](file:///Users/jagveersingh.brar/Projects/jskills/AGENTS.md) at the project root.
  * No file uploads, no manual context copying needed.

---

## 3. Creating New Projects
Whenever you start a new project in `~/Projects/<name>`:
1. Create `~/Projects/<name>/AGENTS.md`.
2. Add one row to [`~/active-topics.md`](file:///Users/jagveersingh.brar/active-topics.md).
*(Zero symlinks or manual linking required).*
