---
name: threat-model-generation
version: 1.0.0
description: |
  Generate a STRIDE-based security threat model for a repository.
  Use when setting up security monitoring, onboarding new projects, or before major releases.
---

# Threat Model Generation

Create a STRIDE threat model for a codebase.

## Workflow

### 1. Understand the System

Read:
- README.md
- Architecture docs
- API endpoints
- Data flow diagrams
- Authentication/authorization setup

### 2. Identify Assets

What needs protection?
- User data (PII, credentials)
- Financial data
- API keys and secrets
- Intellectual property
- Infrastructure access

### 3. Apply STRIDE

For each component, identify threats:

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation |
|-----------|----------|-----------|-------------|-----------------|-----|-----------|
| API Gateway | Missing auth | Rate limit bypass | No audit logs | Error messages leak info | No rate limits | Admin endpoints exposed |
| Database | — | SQL injection | — | Unencrypted backups | Connection pool exhaustion | Overprivileged user |

### 4. Score Risks

| Likelihood | Impact | Risk |
|------------|--------|------|
| High | High | Critical |
| High | Low | Medium |
| Low | High | Medium |
| Low | Low | Low |

### 5. Output

```
## Threat Model: <Project Name>

### Assets
1. User credentials (Critical)
2. API keys (High)

### Threats
| ID | Component | Threat | Risk | Mitigation |
|----|-----------|--------|------|------------|
| T1 | API Gateway | Auth bypass | Critical | Add JWT validation |

### Mitigations
1. [Specific action with owner and deadline]

### Acceptance
- [ ] All critical/high risks have mitigations
- [ ] Mitigations are implemented and tested
```

## Anti-patterns

- **Generic threats**: "The app might be hacked" → be specific
- **Missing mitigations**: Identifying threats without fixing them
- **Not reviewing**: Threat models go stale as code changes
