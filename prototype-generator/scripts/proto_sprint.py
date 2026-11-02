#!/usr/bin/env python3
"""
proto_sprint.py — Deterministic CLI utility for the Prototype Generator skill.

Handles scaffolding of prototype directories in ~/Projects/RawIdeas/<slug>,
asset management, and updating the centralized ideas.md backlog.
"""

import argparse
import json
import os
import sys
from pathlib import Path

RAW_IDEAS_DIR = Path(os.environ.get("RAW_IDEAS_DIR", Path.home() / "Projects" / "RawIdeas"))
IDEAS_MD_PATH = Path(os.environ.get("IDEAS_MD_PATH", RAW_IDEAS_DIR / "ideas.md"))


def init_prototype(slug: str, title: str, json_output: bool = False):
    """Initializes a new prototype directory structure under ~/Projects/RawIdeas/<slug>."""
    safe_slug = Path(slug).name
    proto_dir = RAW_IDEAS_DIR / safe_slug
    assets_dir = proto_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "status": "success",
        "slug": slug,
        "title": title,
        "path": str(proto_dir),
        "assets_path": str(assets_dir)
    }

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"✅ Initialized prototype directory: {proto_dir}")
        print(f"📁 Assets directory ready: {assets_dir}")


def register_idea(slug: str, title: str, status: str = "Pitched", memo: str = "", notes: str = "", json_output: bool = False):
    """Updates ~/Projects/RawIdeas/ideas.md to add or update an idea entry."""
    if not IDEAS_MD_PATH.exists():
        print(f"❌ Error: {IDEAS_MD_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    content = IDEAS_MD_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()

    memo_link = f" See [{Path(memo).name}]({memo})." if memo else ""
    full_notes = f"{notes}{memo_link}".strip()

    updated = False
    new_lines = []
    max_id = 0

    for line in lines:
        if line.strip().startswith("|") and not line.strip().startswith("| #") and not line.strip().startswith("|---"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                try:
                    curr_id = int(parts[1])
                    if curr_id > max_id:
                        max_id = curr_id
                except ValueError:
                    pass

                if slug.lower() in parts[2].lower() or title.lower() in parts[2].lower():
                    parts[2] = f"**{title}**"
                    parts[3] = status
                    parts[4] = full_notes
                    line = f"| {' | '.join(parts[1:-1])} |"
                    updated = True

        new_lines.append(line)

    if not updated:
        new_id = max_id + 1
        new_row = f"| {new_id} | **{title}** | {status} | {full_notes} |"
        insert_idx = len(new_lines)
        for idx, l in enumerate(new_lines):
            if "## Discarded" in l:
                insert_idx = idx - 1
                break
        new_lines.insert(insert_idx, new_row)

    IDEAS_MD_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    res = {
        "status": "success",
        "action": "updated" if updated else "created",
        "slug": slug,
        "title": title,
        "idea_status": status,
        "notes": full_notes,
        "registry_file": str(IDEAS_MD_PATH)
    }

    if json_output:
        print(json.dumps(res, indent=2))
    else:
        print(f"✅ Registered '{title}' in {IDEAS_MD_PATH} (Status: {status})")


def discard_idea(slug: str, title: str, reason: str = "", json_output: bool = False):
    """Logs or moves an idea to the '## Discarded / Deprioritized' section of ideas.md."""
    if not IDEAS_MD_PATH.exists():
        print(f"❌ Error: {IDEAS_MD_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    content = IDEAS_MD_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith("|") and not line.strip().startswith("| #") and not line.strip().startswith("|---"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                if slug.lower() in parts[2].lower() or title.lower() in parts[2].lower():
                    continue
        new_lines.append(line)

    entry = f"* **{title}:** {reason}".strip()
    discard_idx = -1
    for idx, l in enumerate(new_lines):
        if "## Discarded" in l:
            discard_idx = idx
            break

    if discard_idx != -1:
        insert_pos = discard_idx + 1
        while insert_pos < len(new_lines) and new_lines[insert_pos].strip() == "":
            insert_pos += 1
        new_lines.insert(insert_pos, entry)
    else:
        new_lines.append("")
        new_lines.append("## Discarded / Deprioritized")
        new_lines.append("")
        new_lines.append(entry)

    IDEAS_MD_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    res = {
        "status": "success",
        "action": "discarded",
        "slug": slug,
        "title": title,
        "reason": reason,
        "registry_file": str(IDEAS_MD_PATH)
    }

    if json_output:
        print(json.dumps(res, indent=2))
    else:
        print(f"🛑 Discarded '{title}' in {IDEAS_MD_PATH}: {reason}")


def list_prototypes(json_output: bool = False):
    """Lists all available prototype directories in ~/Projects/RawIdeas/."""
    prototypes = []
    if RAW_IDEAS_DIR.exists():
        for item in RAW_IDEAS_DIR.iterdir():
            if item.is_dir() and item.name not in (".git", ".system_generated"):
                has_index = (item / "index.html").exists()
                has_design = (item / "DESIGN.md").exists()
                prototypes.append({
                    "slug": item.name,
                    "path": str(item),
                    "has_index": has_index,
                    "has_design": has_design
                })

    if json_output:
        print(json.dumps(prototypes, indent=2))
    else:
        print(f"📦 Prototypes found in {RAW_IDEAS_DIR}:")
        for p in prototypes:
            status_flags = []
            if p["has_index"]:
                status_flags.append("🌐 index.html")
            if p["has_design"]:
                status_flags.append("🎨 DESIGN.md")
            flags_str = f" ({', '.join(status_flags)})" if status_flags else ""
            print(f"  - {p['slug']}{flags_str}")


def main():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    parser = argparse.ArgumentParser(description="Prototype Generator CLI helper.", parents=[common_parser])
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: init
    init_parser = subparsers.add_parser("init", help="Initialize prototype directory", parents=[common_parser])
    init_parser.add_argument("--slug", required=True, help="Slug identifier for the prototype")
    init_parser.add_argument("--title", required=True, help="Title of the venture idea")

    # Subcommand: register
    reg_parser = subparsers.add_parser("register", help="Register or update idea in ideas.md", parents=[common_parser])
    reg_parser.add_argument("--slug", required=True, help="Slug identifier")
    reg_parser.add_argument("--title", required=True, help="Title of the venture idea")
    reg_parser.add_argument("--status", default="Pitched", help="Idea status (e.g. Pitched, In-Review, Testing)")
    reg_parser.add_argument("--memo", default="", help="Path to decision memo file")
    reg_parser.add_argument("--notes", default="", help="Brief notes / value wedge")

    # Subcommand: discard
    disc_parser = subparsers.add_parser("discard", help="Record idea as discarded/deprioritized in ideas.md", parents=[common_parser])
    disc_parser.add_argument("--slug", required=True, help="Slug identifier")
    disc_parser.add_argument("--title", required=True, help="Title of the venture idea")
    disc_parser.add_argument("--reason", required=True, help="Failure rationale / termination post-mortem")

    # Subcommand: list
    subparsers.add_parser("list", help="List existing prototypes", parents=[common_parser])

    args = parser.parse_args()

    if args.command == "init":
        init_prototype(args.slug, args.title, json_output=args.json)
    elif args.command == "register":
        register_idea(args.slug, args.title, status=args.status, memo=args.memo, notes=args.notes, json_output=args.json)
    elif args.command == "discard":
        discard_idea(args.slug, args.title, reason=args.reason, json_output=args.json)
    elif args.command == "list":
        list_prototypes(json_output=args.json)


if __name__ == "__main__":
    main()
