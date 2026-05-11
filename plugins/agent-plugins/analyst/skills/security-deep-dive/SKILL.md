---
name: security-deep-dive
version: 1.0.0
description: |
  Heavyweight security analysis of a whole subsystem (auth flow, payment pipeline,
  key management, multi-tenant isolation). Produces a written narrative, not a
  diff-level checklist. Use when the user asks for a "security review of X
  subsystem", "audit our auth", or when analyst is dispatched for a subsystem
  scope rather than a PR diff. For PR diffs, use security-review instead.
---

# Security deep-dive

The job: take a subsystem (a directory, a service, a feature spanning multiple modules) and produce a written narrative that walks through trust boundaries, data flows, attack surfaces, mitigations in place, and gaps. Output is a multi-section document, not a findings table.

This skill sits **above** `security-review` and `commit-security-scan`:
- `security-review` reviews a diff. Fast, narrow, repeatable per PR.
- `commit-security-scan` scans a commit for hygiene issues (secrets, deps).
- `security-deep-dive` reviews **a system**. Slow, wide, produced when the system is new, after a major refactor, or before a sensitive launch.

## When to use

- "Audit the new payments service before launch"
- "Review the multi-tenant isolation in the data layer"
- "We've added OAuth — review the full auth flow end-to-end"
- "What happens if someone signs up with a malicious email" (a story-mode analysis)

Don't use this skill for a PR diff. Use `security-review` for that — much cheaper.

## Workflow

### 1. Scope

Define the subsystem explicitly. Bad scopes ("review our security") produce bad analyses. Good scopes:

- A directory: `services/auth/`
- A feature: "the full sign-up to first-transaction flow"
- A boundary: "anything that crosses the customer/admin trust line"

If the scope is too big to hold in head (>5000 lines of code, multiple repos), narrow it. Run the deep-dive in waves rather than producing a thin overview.

### 2. Map the subsystem

Build a mental model before writing any analysis:

- **Entry points** — what triggers code in this subsystem? HTTP routes, queue handlers, scheduled jobs, webhooks, CLI commands.
- **Trust boundaries** — where does code cross from one trust level to another? Network → service. Service → DB. Customer-facing → admin-facing. Service → external API.
- **Assets** — what is this subsystem protecting? PII, credentials, money, internal state, third-party tokens.
- **Adversaries** — who might attack and why? Unauthenticated attacker, authenticated-but-wrong-tenant, malicious admin, compromised dependency, accidental insider.

Capture this as the document's first section.

### 3. Walk the data flows

For each meaningful flow (sign-up, login, payment, password reset, etc.), trace the path from entry to side effect. At each hop, ask:

- What is the trust level here?
- What validation runs?
- What happens if validation is skipped or bypassed?
- What's logged? (And does the log itself create a leak?)
- What's the failure mode? (And does the failure mode leak information?)

Use sequence diagrams (Mermaid) sparingly when a flow has 4+ actors. Skip diagrams for two-actor flows.

### 4. Enumerate threats

Apply STRIDE per flow. For each (flow × STRIDE category), ask: is there a credible threat here? If yes, capture:

- The threat (one sentence)
- Likelihood (high / med / low) — informed by the codebase, not generic CVE statistics
- Impact (high / med / low) — informed by what asset is at stake
- Current mitigation (what stops this today)
- Gap (what's missing or weak)
- Recommendation (concrete, testable)

Be honest about mitigations. "We have CSRF tokens" is meaningless if the tokens aren't validated. Trace the actual code.

### 5. Identify the cross-cutting concerns

Things that don't fit a single flow:

- Secret management (where do API keys live? rotated?)
- Logging hygiene (is auth state logged at the wrong level?)
- Dependency posture (any deps with known CVEs in the subsystem's surface?)
- Configuration drift (does staging differ from prod in load-bearing ways?)
- Failure modes (what happens when an external service is down — does the system fail open?)

Each gets a short section.

### 6. Recommendations

End with a **prioritized** list. Three buckets:

- **Must fix before [launch / next sprint / merge]** — concrete blockers
- **Should fix soon** — meaningful gaps with workarounds
- **Worth tracking** — speculative or low-likelihood, worth a backlog ticket

Each recommendation cites the flow and the file:line where the gap lives.

### 7. Emit via scribe

Hand the payload to scribe. The closest existing schema is `threat-model` — extend with the deep-dive's narrative sections (Scope, Flows, Cross-cutting concerns, Recommendations) or add a new `security-deep-dive` schema to scribe if this becomes recurring.

Write to `reports/YYYY-MM-DD-<subsystem-slug>-deep-dive.html`.

## Style

- Narrative, not bulleted findings. The reader is forming a mental model of the subsystem; bullets short-circuit that.
- Cite file:line for every concrete claim. The reader navigates from your prose into the code.
- Be specific about which adversary each threat assumes. "An authenticated attacker" and "an unauthenticated attacker" have different mitigation surfaces.
- Acknowledge what you didn't analyze. "Out of scope: the third-party fraud-detection service" beats silent omission.
- No "industry best practice" hand-waving. State what the actual issue is in this codebase.

## What this skill does NOT do

- Does not produce PR-comment-ready findings. Use `security-review` for that.
- Does not scan for secrets in commits. Use `commit-security-scan` for that.
- Does not propose code fixes in patch form. Recommendations point at file:line; implementer writes the fix.
- Does not validate that recommendations were taken. That's a follow-up scan, not part of this skill.
