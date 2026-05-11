---
name: commit-security-scan
version: 1.0.0
description: |
  Analyze code changes for security vulnerabilities using LLM reasoning and threat model patterns.
  Use for PR reviews, weekly scans, or monitoring.
---

# Commit Security Scan

Run security analysis on recent commits.

## Workflow

### 1. Get Commits

```bash
git log --oneline -20
```

Or for a PR:
```bash
gh pr diff <number>
```

### 2. Analyze Each Change

Look for:
- New dependencies (check for known vulnerabilities)
- Input handling (sanitization, validation)
- Auth changes (new endpoints, permission changes)
- Secret handling (API keys, tokens, passwords)
- Data flow (where user input goes)

### 3. Check Dependencies

```bash
npm audit  # or equivalent
```

### 4. Report

```
## Security Scan: <date range>

### Commits Scanned
- abc1234: feat: add user profile page
- def5678: fix: resolve auth bypass

### Findings
| Commit | Severity | Issue | Action |
|--------|----------|-------|--------|
| abc1234 | Medium | New dependency `lodash` — check CVEs | Run npm audit |

### Clean
- def5678: No security concerns
```

## Integration

Run automatically on:
- Every PR (via CI)
- Weekly scheduled scan
- Before releases
