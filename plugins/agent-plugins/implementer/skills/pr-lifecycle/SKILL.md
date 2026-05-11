---
name: pr-lifecycle
version: 1.0.0
description: |
  Orchestrate the full ticket-to-PR lifecycle as one continuous flow: branch off the
  current base, make commits, push, open the PR, and address review feedback. Wraps
  create-pr + follow-up-on-pr with implementer-specific framing. Use when implementer
  is dispatched on a Linear ticket and needs the end-to-end path, vs invoking
  create-pr / follow-up-on-pr piecemeal.
---

# PR lifecycle

The job: take a ready ticket (or spec) and drive it to a merged-ready PR. This skill is the implementer agent's main loop. It composes `create-pr` and `follow-up-on-pr` from the code-quality vertical and adds the ticket-context plumbing those lower-level skills don't have.

## Inputs

The skill expects:
- A Linear ticket ID (preferred) **or** a free-form spec describing what to build
- The repo's working tree, clean or close to clean
- `.capsule-factory.yml` with `github.default_base_branch` (default: `main`) and `github.draft_by_default` (default: `false`)

## Workflow

### 1. Branch

Branch name: `<ticket-id-or-slug>-<short-kebab>`. Examples:
- `CAP-42-add-csrf-to-transfer`
- `quick-fix-flaky-test-rerun` (if no ticket)

Branch off `github.default_base_branch` from `.capsule-factory.yml`. Never branch off another feature branch unless the user explicitly asks.

### 2. Make commits

Commits should be meaningful and grouped — don't squash before pushing, don't single-commit everything either. Typical shape:

- Setup / scaffolding (config, dependencies)
- Core implementation
- Tests
- Doc / README updates if user-visible

Run the project's lint/typecheck/test commands between commits when fast. If any of them fail, fix before the next commit, don't carry breakage forward.

### 3. Pre-push checklist

Before pushing:
- Diff is clean (no debug prints, no commented-out code, no `.env` accidentally staged)
- Tests pass locally
- Lint / type-check passes
- The change actually addresses the ticket — re-read the ticket body and check

### 4. Push and open the PR

Call the `create-pr` skill from the code-quality vertical. It handles the gh CLI invocation, the title/body drafting, and the test plan. Pass:

- `--base` = `github.default_base_branch`
- `--draft` if `github.draft_by_default` is true OR the user said draft OR the change is genuinely partial
- The ticket ID for cross-linking (Linear-side via the conventional `Refs: <ticket-id>` line in the body)

After the PR is open, capture:
- PR URL
- PR number
- The body that was used

### 5. Notify

If invoked by epic-conductor (you're inside a team), `SendMessage` to conductor:

> PR <url> open for <ticket-id>. Ready for analyst + qa-capture.

If invoked directly by the user, just print the PR URL.

### 6. Review-comment loop

This is where `follow-up-on-pr` (from code-quality) comes in. The skill normally handles "review this PR" for an arbitrary PR; for implementer, the framing is "respond to comments on YOUR open PR."

For each new review comment that arrives:

| Comment kind          | Action                                                                                  |
|-----------------------|------------------------------------------------------------------------------------------|
| Inline change request | Make the change in the working tree, push, reply on the thread with the commit SHA      |
| Question              | Reply with the answer, no code change                                                    |
| Suggestion (no block) | Decide: take it (change + reply) or skip it (reply with rationale)                       |
| Nit                   | Decide: take it if cheap, otherwise mark "not blocking" and skip                         |
| Critical finding (analyst) | Treat as block: make the change, run analyst's check pattern, push, reply         |
| Verify failure (qa-capture) | Treat as block: reproduce, fix the underlying issue, push, ping qa-capture          |

Push after every meaningful change — small batches of "fix + push + reply" are easier for reviewers to follow than one big "addressed-all-feedback" push.

### 7. Done state

When:
- All review threads are resolved (analyst approved, qa-capture verified)
- CI is green
- No outstanding requests for changes

… then ping conductor: "PR <url> ready for merge decision." Do not merge yourself. Conductor (or the user) makes the merge call.

## Failure handling

- **`git push` rejects** — likely a stale base; rebase on `github.default_base_branch`, force-push the feature branch (only if you own it), continue.
- **CI fails** — read the failure, fix in a new commit, push. If the failure is flaky and unrelated to your change, re-run before assuming it's yours.
- **A review thread escalates into a design disagreement** — stop the implementation work, file the disagreement as a child ticket via conductor, leave the PR in draft.

## What this skill does NOT do

- Does not write the test plan in detail — `create-pr` handles that. Just be specific about which tests passed.
- Does not respond to comments outside your PR. If a reviewer comments on a related PR, that's their PR's lifecycle, not yours.
- Does not merge.
- Does not file follow-up tickets directly — message conductor.
