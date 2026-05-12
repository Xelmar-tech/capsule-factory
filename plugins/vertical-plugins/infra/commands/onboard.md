---
description: Walk a user through Capsule Factory install, MCP setup, and validation
argument-hint: '[--check] [--client claude|codex] [--repo <path>]'
---

Load skill: **capsule-onboarding**.

The user invoked `/onboard` with `$ARGUMENTS`. Guide them through Capsule Factory installation, plugin refresh, MCP setup, per-repo configuration, and validation. Explain what each vertical, agent, and command is for, but keep the output practical and checklist-driven.

If `--check` is present, run in verification mode: inspect the available plugin list, MCP settings, required env names, and repo config. Report `ok`, `missing`, or `blocked` for each gate. Do not ask the user to paste secret values.
