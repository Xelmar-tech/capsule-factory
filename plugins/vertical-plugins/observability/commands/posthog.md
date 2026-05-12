---
description: Investigate runtime behavior with PostHog evidence
argument-hint: '"<question, incident, feature, PR, or user-flow>"'
---

Load skill: **posthog-investigate**.

The user invoked `/posthog` on `$ARGUMENTS`. Use the PostHog MCP to gather runtime evidence from the pinned Capxul project. Prefer read-only tools first. Do not mutate flags, dashboards, alerts, annotations, assignment rules, cohorts, experiments, grouping rules, project settings, subscriptions, or error issues unless the user explicitly asks for that mutation in the current turn.

Report the time window, project scope, PostHog object links or identifiers, and the distinction between observations and inferences. Never print PostHog API keys, authorization headers, or raw PII-heavy person/session payloads.
