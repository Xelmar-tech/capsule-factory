---
description: Materialize env files for the current repo from Bitwarden
argument-hint: '[<project> <env>] (default: capxul dev)'
---

Load skill: **manage-secrets**.

The user invoked `/materialize-env` with arguments `$ARGUMENTS`. Apply the `manage-secrets` skill: parse `<project> <env>` (default `capxul dev`), fetch the manifest from the Bitwarden MCP, verify destinations are git-ignored, and write the env files with mode 0600. Print paths and key-names only — never values.

If the user explicitly passes `production`, require an in-chat confirmation before proceeding.
