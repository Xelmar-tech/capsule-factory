---
description: Review changed code for reuse, quality, and efficiency, then fix any issues
argument-hint: '[optional path or scope: e.g. "src/foo" or "staged only"]'
---

Load skill: **simplify**.

The user invoked `/simplify`. Apply the `simplify` skill to the changed code in the current working tree (or the scope hinted by `$ARGUMENTS`, if any). Look for: unused parameters, dead branches, abstractions that hide a single call site, error handling for impossible states, and three-similar-lines that should still be three similar lines (not a premature abstraction). Make the fixes inline; do not just produce a report.
