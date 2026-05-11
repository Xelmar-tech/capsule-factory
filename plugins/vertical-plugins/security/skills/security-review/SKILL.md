---
name: security-review
version: 1.0.0
description: |
  Scan code changes for security vulnerabilities using STRIDE threat modeling, validate findings for exploitability, and output structured results for downstream processing.
  Use when the user asks for a "security review," "security scan," or "check for vulnerabilities."
---

# Security Review

Scan code changes for security issues.

## Workflow

### 1. Get the Diff

```bash
git diff HEAD~1
```

Or for a PR:
```bash
gh pr diff <number>
```

### 2. Apply STRIDE

For each change, check:

| Threat | What to look for |
|--------|-----------------|
| **S**poofing | Auth bypass, missing identity checks |
| **T**ampering | Input validation gaps, missing integrity checks |
| **R**epudiation | Missing audit logs, no traceability |
| **I**nformation Disclosure | Secrets in code, over-logging, PII exposure |
| **D**enial of Service | Unbounded loops, resource exhaustion |
| **E**levation of Privilege | Missing authorization checks, role bypass |

### 3. Validate Findings

For each potential issue:
- Is it exploitable in practice?
- What's the blast radius?
- Is it a false positive?

### 4. Output

```
## Security Review: <PR/title>

### Findings
| Severity | Category | Location | Description | Exploitable? |
|----------|----------|----------|-------------|--------------|
| High | Injection | src/api.ts:45 | Unsanitized user input in SQL | Yes |

### Recommendations
1. [Specific fix with code example]

### False Positives
1. [Why this is not a real issue]
```

## Anti-patterns

- **Vague findings**: "This might be insecure" → be specific
- **Missing severity**: Every finding needs impact assessment
- **No code references**: Line numbers and file paths required
