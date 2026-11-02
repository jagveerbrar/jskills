# Curated Agent Skill Registries & Sources

A high-signal reference directory for discovering, auditing, and importing production-grade AI agent skills and MCP workflow patterns.

---

## 1. Core Online Registries

| Source / Repository | Best Suited For | Security / Quality Bar | Primary Focus |
| :--- | :--- | :--- | :--- |
| **[`anthropics/skills`](https://github.com/anthropics/skills)** | Core documents, MCP tools, reference patterns | **Highest** *(First-party reference)* | Official agent patterns, deterministic tool-calling conventions, foundational workflows |
| **[`VoltAgent/awesome-agent-skills`](https://github.com/VoltAgent/awesome-agent-skills)** | Stack-specific vendor skills (Next.js, Stripe, Supabase, etc.) | **High** *(Aggregates verified teams)* | Framework integrations, third-party SaaS APIs, specialized full-stack developer patterns |
| **[`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)** | Engineering workflow pipelines & QA gates | **High** *(Production-grade, vetted)* | Code review, web performance audits, QA test generation, automated refactoring |

---

## 2. Complementary & Official Ecosystem Sources

| Source / Repository | Best Suited For | Security / Quality Bar | Primary Focus |
| :--- | :--- | :--- | :--- |
| **[`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers)** | Official & reference MCP server implementations | **Highest** *(Official Anthropic/Linux Foundation)* | Standardized protocol servers (Postgres, Git, Filesystem, Memory, Slack, Google Drive) |
| **[`vercel-labs/ai`](https://github.com/vercel/ai)** | Next.js / React agentic UX & tool calling | **High** *(Official Vercel Labs)* | Generative UI, streaming primitives, edge-runtime agent pipelines |
| **[`garrytan/gstack`](https://github.com/garrytan/gstack)** | Founder, CEO, design, & eng review pipelines | **High** *(Battle-tested developer tooling)* | Autonomous multi-perspective reviews (`/autoplan`, `/browse`, `/plan-ceo-review`, `/qa`) |

---

## 3. Ingestion & Adaptation Checklist

When importing external skills into the [`jskills`](file:///Users/jagveersingh.brar/Projects/jskills) repository:

1. **Format Standardization:**
   - Ensure the root file is uppercase [`SKILL.md`](file:///Users/jagveersingh.brar/Projects/jskills/create-skill/SKILL.md#L25).
   - Format description frontmatter using the discovery formula (`[Capability summary]. [Key operations]. Activate on "/<trigger>" or when <context>`).
2. **Unified CLI Architecture:**
   - Consolidate multiple ad-hoc scripts into a single `scripts/<tool>.py` with subcommands.
3. **Safety & Permissions:**
   - Audit external scripts for unsafe network calls, credential leaking, or unconfirmed destructive mutations.
   - Enforce read-only inspection by default; require user confirmation for mutations.
4. **Clean Dependencies:**
   - Use standard `uv run` runners for Python tooling with explicit inline dependencies (`# /// script`).
