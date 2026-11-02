# Eval Schema Reference

Reference schema for skill evaluation artifacts, compatible with the [`anthropics/skills`](https://github.com/anthropics/skills) eval ecosystem.

## `evals/evals.json` Structure

```json
{
  "skill_name": "<skill-name>",
  "evals": [
    {
      "id": 1,
      "eval_name": "descriptive-eval-name",
      "prompt": "The user prompt that triggered the skill",
      "expected_output": "What the skill should produce",
      "assertions": [
        "Must execute prior art search before proposing a new skill",
        "Must render Prior Art Audit Table in visible response",
        "Must not scaffold without user confirmation"
      ],
      "classification": "pass|fail|inconclusive",
      "source_session": "conversation-id-or-null",
      "extracted_at": "2026-08-28T11:42:00+02:00"
    }
  ]
}
```

## Field Reference

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `skill_name` | string | Yes | Name matching the skill's frontmatter `name` |
| `evals[].id` | integer | Yes | Auto-incrementing eval ID |
| `evals[].eval_name` | string | Yes | Human-readable description of what this eval tests |
| `evals[].prompt` | string | Yes | The exact or representative user prompt |
| `evals[].expected_output` | string | Yes | Description of correct behavior/output |
| `evals[].assertions` | string[] | Yes | Behavioral checks (natural language or deterministic) |
| `evals[].classification` | enum | Yes | `pass`, `fail`, or `inconclusive` |
| `evals[].source_session` | string | No | Conversation ID the eval was extracted from (null if forward-authored) |
| `evals[].extracted_at` | string | No | ISO-8601 timestamp of extraction |

## Root Cause Categories (for `fail` evals)

| Category | Description |
| :--- | :--- |
| `missing_step` | A prescribed workflow step was skipped |
| `wrong_output` | Output produced was factually or structurally incorrect |
| `skipped_gate` | A mandatory gate (e.g., prior art search, review gate) was bypassed |
| `tool_failure` | A tool call failed or returned unexpected results |
| `hallucinated_content` | Skill produced fabricated information |
| `other` | Uncategorized failure |

## Session Extract Structure (`session-extracts/<date>-<id>.json`)

```json
{
  "skill_name": "<skill-name>",
  "conversation_id": "<id>",
  "extracted_at": "<ISO-8601>",
  "invocation_turn": 42,
  "reaction_end_turn": 46,
  "classification": "pass|fail|inconclusive",
  "root_cause": "skipped_gate|null",
  "confidence": "high|medium|low",
  "transcript_excerpt": [
    {"turn": 42, "role": "user", "content": "..."},
    {"turn": 43, "role": "assistant", "content": "..."},
    {"turn": 44, "role": "user", "content": "..."}
  ],
  "proposed_assertions": [
    "Must execute search_web before proposing greenfield"
  ]
}
```
