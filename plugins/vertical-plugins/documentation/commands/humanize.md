---
description: Rewrite AI-flavored prose to sound like a person wrote it
argument-hint: '<file path> or "selection" / "last response"'
---

Load skill: **human-writing**.

The user invoked `/humanize` on `$ARGUMENTS`. Apply the `human-writing` skill: strip filler ("serves as," "in the evolving landscape," "showcases," em-dash overuse, rule-of-three padding, copula avoidance, negative parallelisms, AI vocabulary). Preserve meaning and technical accuracy. Return the rewrite as an edit if the target is a file, or as plain text if the target is a snippet.
