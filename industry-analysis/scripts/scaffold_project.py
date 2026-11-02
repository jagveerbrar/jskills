#!/usr/bin/env python3
"""Unified project scaffolding CLI for industry-analysis skill.

Executed ONLY after explicit human confirmation at Dialogue Gate 3.
Scaffolds a new project workspace under /Users/jagveersingh.brar/Projects/<slug>/,
writes AGENTS.md, TODOS.md, concept-dossier.md, symlinks context.md,
and registers the project in ~/active-topics.md.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROJECTS_ROOT = Path(os.environ.get("PROJECTS_ROOT", Path.home() / "Projects"))
ACTIVE_TOPICS_PATH = Path(os.environ.get("ACTIVE_TOPICS_PATH", Path.home() / "active-topics.md"))


def scaffold_project(slug: str, title: str, description: str, keywords: str) -> None:
    target_dir = PROJECTS_ROOT / slug
    if target_dir.exists():
        print(f"[!] Warning: Directory already exists at {target_dir}")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"[+] Created directory: {target_dir}")

    # 1. Write AGENTS.md
    agents_content = f"""# CONTEXT & WORKSPACE RULES: {slug}

## 1. Project Overview & Objective
* **Repository Name:** `{slug}`
* **Working Product Title:** *{title}*
* **Core Objective:** {description}
* **Status:** Initial Vetted Wedge (Spun out from `/industry-analysis`).

---

## 2. Core Value Proposition & Target ICP
* **Primary Target ICP:** [Define Beachhead Customer]
* **Core Problem:** [Single irreducible pain point]
* **Economic Impact:** [Quantified cash saved or unlocked per year]

---

## 3. Product Architecture & Delivery Wedge
* **Delivery Mechanism:** [e.g. B2B SaaS Console / Automated Telemetry / Embedded API]
* **Data Plumbing:** [Existing data sources / APIs / Integrations]

---

## 4. Active Phase & Immediate Milestones
* **Current Phase:** Phase 1 — Cold Problem & Advisory Workflow Discovery.
* **Target Milestone:** 10 Customer / Advisor discovery calls to validate WTP.

---

## 5. Key References
* [`concept-dossier.md`](concept-dossier.md) — Comprehensive technical, regulatory, and business case dossier.
* [`TODOS.md`](TODOS.md) — Immediate discovery and validation action items.
"""
    agents_path = target_dir / "AGENTS.md"
    agents_path.write_text(agents_content, encoding="utf-8")
    print(f"[+] Wrote {agents_path}")

    # 2. Symlink context.md -> AGENTS.md
    context_symlink = target_dir / "context.md"
    if not context_symlink.exists():
        try:
            context_symlink.symlink_to("AGENTS.md")
            print(f"[+] Symlinked {context_symlink} -> AGENTS.md")
        except Exception as e:
            print(f"[!] Symlink creation note: {e}")

    # 3. Write TODOS.md
    todos_content = f"""# TODOS: {slug} ({title})

## Phase 1: Customer Discovery & Problem Validation

| Priority | Task | Owner | Status | Deliverable |
| :--- | :--- | :--- | :--- | :--- |
| **P0** | **Map 10 Beachhead ICP Targets:** Identify specific decision-makers and contact profiles. | Founder & AI | Pending | Target list in `outreach-targets.md` |
| **P0** | **Draft Discovery Interview Guide:** Pain-led, non-pitch questions testing WTP and current manual hacks. | Founder & AI | Pending | `discovery-interview-guide.md` |
| **P1** | **Conduct 5–10 Discovery Calls:** Validate friction, unit economics, and channel feasibility. | Founder | Pending | Synthesized interview notes |
| **P1** | **Concierge Audit Specification:** Design a 1-page manual audit to prove immediate cash ROI for a pilot user. | Founder & AI | Pending | `concierge-audit-template.md` |
"""
    todos_path = target_dir / "TODOS.md"
    todos_path.write_text(todos_content, encoding="utf-8")
    print(f"[+] Wrote {todos_path}")

    # 4. Write initial concept-dossier.md
    dossier_content = f"""# Concept Dossier: {slug} (*{title}*)

## 1. Problem & Structural Bottleneck
* **Industry Context:** {description}
* **The Structural Choke Point:** [Why value pools here]

---

## 2. Business Case & Unit Economics
* **Customer Economic Impact:** [Cash saved or unlocked]
* **Pricing Model:** [Value share / SaaS seat]
* **Payback Period:** [< 6 months]

---

## 3. Go-To-Market & Channel Wedge
* **The Agency Wedge:** [Solving the advisor's conflict of interest]
* **B2B2C Channel:** [Independent partners distributing the product]
"""
    dossier_path = target_dir / "concept-dossier.md"
    dossier_path.write_text(dossier_content, encoding="utf-8")
    print(f"[+] Wrote {dossier_path}")

    # 5. Register in active-topics.md
    if ACTIVE_TOPICS_PATH.exists():
        content = ACTIVE_TOPICS_PATH.read_text(encoding="utf-8")
        if f"**{slug}**" not in content:
            new_row = f"| **{slug}** | [`{target_dir}/AGENTS.md`](file://{target_dir}/AGENTS.md) | {description} | `{slug}`, {keywords} | Active | {os.popen('date +%Y-%m-%d').read().strip()} | Discovery calls completed & pilot LOI signed |\n"
            # Append before trailing empty lines
            lines = content.rstrip().split("\n")
            lines.append(new_row.strip())
            ACTIVE_TOPICS_PATH.write_text("\n".join(lines) + "\n\n", encoding="utf-8")
            print(f"[+] Registered {slug} in {ACTIVE_TOPICS_PATH}")
        else:
            print(f"[*] {slug} already registered in {ACTIVE_TOPICS_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold new project workspace from industry-analysis.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scaffold_parser = subparsers.add_parser("scaffold", help="Scaffold a new project workspace")
    scaffold_parser.add_argument("--slug", required=True, help="Directory name under ~/Projects")
    scaffold_parser.add_argument("--title", required=True, help="Working product title")
    scaffold_parser.add_argument("--description", required=True, help="1-sentence objective")
    scaffold_parser.add_argument("--keywords", default="", help="Comma-separated routing keywords")

    args = parser.parse_args()

    if args.command == "scaffold":
        scaffold_project(args.slug, args.title, args.description, args.keywords)


if __name__ == "__main__":
    main()
