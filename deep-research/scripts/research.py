# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai>=2.3.0",
# ]
# ///

"""
Unified CLI tool for Google Gemini Deep Research via the Interactions API.
Locked with chmod 555 in the jskills repository.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path


DEFAULT_AGENT = os.environ.get("GEMINI_RESEARCH_AGENT_ID", "deep-research-preview-04-2026")


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            json.dumps({"error": "GEMINI_API_KEY environment variable is not set."})
            if "--json" in sys.argv
            else "Error: GEMINI_API_KEY environment variable is not set.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except ImportError:
        print(
            json.dumps({"error": "google-genai package not found. Run with `uv run`."})
            if "--json" in sys.argv
            else "Error: google-genai package not found. Run with `uv run`.",
            file=sys.stderr,
        )
        sys.exit(1)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:40] or "research"


def cmd_start(args):
    client = get_client()
    agent_id = args.agent or DEFAULT_AGENT

    interaction = client.interactions.create(
        agent=agent_id,
        input=args.prompt,
        background=True,
    )

    result = {
        "status": "started",
        "interaction_id": interaction.id,
        "agent": agent_id,
        "prompt": args.prompt,
        "created_at": datetime.now().isoformat(),
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Deep Research started successfully.")
        print(f"Interaction ID: {interaction.id}")
        print(f"Agent:          {agent_id}")
        print(f"To poll status: uv run research.py poll {interaction.id}")


def cmd_poll(args):
    client = get_client()
    interaction = client.interactions.get(args.interaction_id)

    status = interaction.status
    result = {
        "interaction_id": interaction.id,
        "status": status,
    }

    if status == "completed":
        output_text = interaction.outputs[-1].text if interaction.outputs else ""
        result["output"] = output_text

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(output_text, encoding="utf-8")
            result["output_file"] = str(out_path.resolve())

    elif status == "failed":
        result["error"] = str(interaction.error) if hasattr(interaction, "error") else "Unknown error"

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Interaction: {interaction.id}")
        print(f"Status:      {status}")
        if status == "completed":
            if args.output:
                print(f"Report saved to: {args.output}")
            else:
                print("\n--- REPORT OUTPUT ---")
                print(result.get("output", ""))
        elif status == "failed":
            print(f"Error: {result.get('error')}", file=sys.stderr)


def cmd_run(args):
    client = get_client()
    agent_id = args.agent or DEFAULT_AGENT

    if not args.json:
        print(f"Initiating Google Deep Research...")
        print(f"Prompt: \"{args.prompt}\"")
        print(f"Agent:  {agent_id}")

    interaction = client.interactions.create(
        agent=agent_id,
        input=args.prompt,
        background=True,
    )

    if not args.json:
        print(f"Task started [ID: {interaction.id}]. Polling every {args.interval}s (timeout: {args.timeout}s)...")

    start_time = time.time()
    while True:
        elapsed = int(time.time() - start_time)
        if elapsed > args.timeout:
            err_msg = f"Research timed out after {args.timeout} seconds."
            if args.json:
                print(json.dumps({"error": err_msg, "interaction_id": interaction.id}, indent=2))
            else:
                print(f"\n{err_msg}", file=sys.stderr)
            sys.exit(1)

        interaction = client.interactions.get(interaction.id)
        status = interaction.status

        if status == "completed":
            output_text = interaction.outputs[-1].text if interaction.outputs else ""
            
            # Determine output path
            if args.output:
                out_path = Path(args.output)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                slug = slugify(args.prompt)
                out_path = Path.cwd() / "research" / f"{slug}_{timestamp}.md"

            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(output_text, encoding="utf-8")

            res = {
                "status": "completed",
                "interaction_id": interaction.id,
                "output_file": str(out_path.resolve()),
                "elapsed_seconds": elapsed,
            }

            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"\nResearch successfully completed in {elapsed}s.")
                print(f"Report written to: {out_path.resolve()}")
            break

        elif status == "failed":
            err = str(interaction.error) if hasattr(interaction, "error") else "Unknown error"
            if args.json:
                print(json.dumps({"status": "failed", "interaction_id": interaction.id, "error": err}, indent=2))
            else:
                print(f"\nResearch failed: {err}", file=sys.stderr)
            sys.exit(1)

        if not args.json:
            print(f"[{elapsed}s] Status: {status}... waiting...", flush=True)
        time.sleep(args.interval)


def main():
    parser = argparse.ArgumentParser(
        description="Unified CLI utility for Google Gemini Deep Research via Interactions API."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: start
    p_start = subparsers.add_parser("start", help="Start background research task")
    p_start.add_argument("prompt", help="Research question or brief")
    p_start.add_argument("--agent", help=f"Agent ID (default: {DEFAULT_AGENT})")
    p_start.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    p_start.set_defaults(func=cmd_start)

    # Subcommand: poll
    p_poll = subparsers.add_parser("poll", help="Poll status of an active research task")
    p_poll.add_argument("interaction_id", help="Interaction ID from `start`")
    p_poll.add_argument("--output", "-o", help="File path to write report if completed")
    p_poll.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    p_poll.set_defaults(func=cmd_poll)

    # Subcommand: run
    p_run = subparsers.add_parser("run", help="Start and poll until completion")
    p_run.add_argument("prompt", help="Research question or brief")
    p_run.add_argument("--output", "-o", help="Custom output file destination")
    p_run.add_argument("--agent", help=f"Agent ID (default: {DEFAULT_AGENT})")
    p_run.add_argument("--interval", type=int, default=15, help="Polling interval in seconds (default: 15)")
    p_run.add_argument("--timeout", type=int, default=900, help="Maximum timeout in seconds (default: 900)")
    p_run.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
