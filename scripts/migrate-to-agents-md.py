#!/usr/bin/env python3
"""
Migrates context.md files across all projects in ~/Projects/ to canonical AGENTS.md.
Creates a backward-compatibility symlink: context.md -> AGENTS.md.
"""

import os
from pathlib import Path

PROJECTS_DIR = Path("/Users/jagveersingh.brar/Projects")

def migrate():
    print(f"Scanning {PROJECTS_DIR} for context.md files...")
    migrated = 0
    skipped = 0

    for root, dirs, files in os.walk(PROJECTS_DIR):
        # Ignore hidden folders (.git, .gemini, etc.)
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        
        current_dir = Path(root)
        context_file = current_dir / "context.md"
        agents_file = current_dir / "AGENTS.md"

        if context_file.exists():
            # If context.md is already a symlink pointing to AGENTS.md, skip
            if context_file.is_symlink() and context_file.resolve() == agents_file.resolve():
                print(f"  [ALREADY MIGRATED] {current_dir.relative_to(PROJECTS_DIR)}")
                skipped += 1
                continue

            # If AGENTS.md already exists and is not a symlink, back up context.md
            if agents_file.exists() and not agents_file.is_symlink():
                print(f"  [NOTICE] Both exist in {current_dir.relative_to(PROJECTS_DIR)}. Ensuring canonical AGENTS.md...")
                # If AGENTS.md has content, just ensure context.md symlinks to it
                if context_file.is_symlink():
                    context_file.unlink()
                else:
                    context_file.rename(current_dir / "context.md.bak")
                context_file.symlink_to("AGENTS.md")
                migrated += 1
                continue

            # Standard migration: rename context.md -> AGENTS.md, create relative symlink
            print(f"  [MIGRATING] {current_dir.relative_to(PROJECTS_DIR)}: context.md -> AGENTS.md")
            context_file.rename(agents_file)
            context_file.symlink_to("AGENTS.md")
            migrated += 1

    print(f"\nMigration complete: {migrated} directories migrated, {skipped} already compliant.")

if __name__ == "__main__":
    migrate()
