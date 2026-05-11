---
description: Run a security scan on code changes
argument-hint: '["pr" | "commit" | "weekly"] [target]'
---

# Security Scan Command

Run security analysis on code changes.

## Workflow

### Step 1: Target Selection

Determine scope:
- PR: `gh pr diff <number>`
- Commit: `git diff HEAD~1`
- Weekly: `git log --oneline -50`

### Step 2: Scan

Use `security-review` or `commit-security-scan` skill to analyze changes.

### Step 3: Validate

Use `vulnerability-validation` to triage findings.

### Step 4: Report

Output structured findings with severity and recommendations.
