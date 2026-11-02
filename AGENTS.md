# Project Context: jskills

## 1. Project Overview
* **Project Name:** jskills
* **Core Objective:** Central, LLM/provider-agnostic resident repository for custom skills, prompts, and prompt templates.

---

## 2. Architecture & Conventions
* **Skill Structure:** Each skill is a dedicated folder containing an uppercase `SKILL.md` with standard YAML frontmatter (`name`, `description`).
* **Discovery & Symlink Hub:** Consolidated into the provider-neutral global hub `~/.agents/skills` via symlinks managed by [`scripts/sync-skills.sh`](file:///Users/jagveersingh.brar/Projects/jskills/scripts/sync-skills.sh). Precedence hierarchy: Private custom skills in `~/Projects/jskills-private` take precedence over public custom skills in `~/Projects/jskills`, which take precedence over upstream clones in `~/Projects/external-skills`.
* **Unified Domain Tooling & Anti-Sprawl Architecture:** Tool-based skills must encapsulate their entire automation, inspection, and mutation logic within a single, modular CLI utility (`scripts/<tool>.py`) with subcommands. Agents must never spawn fragmented one-off scratch scripts (`inspect_*.py`, `dump_*.py`, `parse_*.py`) in repository or project directories.
* **Transient Scratch Policy:** If exploratory probing is necessary to reverse-engineer unknown schemas, code must execute in-memory or within transient `scratch/` folders and be purged immediately upon task conclusion.
* **The Improvement Flywheel:** Every skill must embed a post-execution self-audit hook. If an agent discovers missing primitives, new subcommands, or schema adjustments, it must proactively propose hardening that logic directly into the skill's CLI tools and `SKILL.md`.
* **Resident Script Immutability & Permission Lock:** Resident CLI utilities (`scripts/*.py`) must enforce strict immutable permissions (`chmod 555`, read/execute only). Any workflow modifying scripts must conduct an automated Chief Security Officer audit (`/cso`) and re-lock permissions before completing.

---

## 3. Constraints & Guidelines
* **Do:**
  * Keep skill instructions atomic, highly selective, and procedural.
  * Follow the progressive disclosure model (lean `SKILL.md`, separate references/scripts if needed).
  * Always execute live searches across local skills (`jskills`, `~/.agents/skills`) and vetted registries ([`references/skill-registries.md`](file:///Users/jagveersingh.brar/Projects/jskills/references/skill-registries.md)) before proposing or scaffolding any new skill or tool, presenting a structured Prior Art Audit Table in the chat turn.
  * Standardize CLI scripts on extensible subcommands with structured `--json` and human-readable output formats.
  * Embed the `## 🔄 Self-Evolution & Tooling Flywheel` section in every skill definition.
  * For skills proposing changes across multiple target files or distinct scopes, generate separate review artifacts with independent feedback controls (`RequestFeedback: true`) rather than bundling changes into a single artifact.
  * Maintain strict separation of concerns: technical mechanisms and systems in vault notes, strategic PM/leadership takeaways in LinkedIn posts.
  * **Pre-Mutation Alignment Gates:** Skill generation (`create-skill`) and evolution (`evolve-skill`) workflows must enforce an explicit review gate presenting plans/blueprints to the user before mutating disk files.
  * **Downstream Ecosystem Ripple Audits:** When evolving an upstream skill whose inputs, outputs, CLI interfaces, or data contracts change, audit downstream consumers across `jskills/` and active registries to prevent silent handoff breaks.
  * **Full-Post LinkedIn Invariants:** When generating thought leadership, enforce ultra-compactness (<280 words, max 25–30 lines) across the *entire post*, relatable PM wit throughout, zero backend infrastructure jargon, and high-stakes operational punchlines.
* **Do Not:**
  * Propose or scaffold a new skill from scratch without first verifying and documenting that no suitable off-the-shelf implementation exists upstream.
  * Move skills out of `jskills` to tool-specific folders; use configuration entries instead.
  * Use lowercase `skill.md` filenames.
  * Emit persistent throwaway scripts into workspaces; consolidate primitives into unified tools.
  * Discard agent runtime scratch scripts without checking if they reveal missing tool primitives.

