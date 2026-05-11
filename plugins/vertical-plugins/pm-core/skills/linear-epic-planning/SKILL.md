---
name: linear-epic-planning
version: 1.0.0
description: |
  Plan epics and break them into Linear issues with proper priorities, labels, and assignments.
  Use when the user wants to "plan an epic," "break down a feature," or "create Linear issues."
---

# Linear Epic Planning

Break high-level goals into actionable, trackable Linear issues.

## Workflow

### 1. Understand the Epic

Read the epic description or Linear epic URL. Identify:
- **Goal**: What does success look like?
- **Scope**: What's in and out?
- **Constraints**: Deadline, dependencies, resources
- **Stakeholders**: Who needs to review or approve?

### 2. Decompose into Issues

Create 3-7 child issues. Each issue must be:
- **Completable in 1-3 days**
- **Independently verifiable** (clear acceptance criteria)
- **Properly scoped** (not too big, not too small)

Issue template:
```
Title: [Verb] [noun] — e.g., "Implement OAuth login flow"
Description: Context + acceptance criteria
Priority: urgent | high | normal | low
Labels: feature, bug, refactor, etc.
Assignee: @person or unassigned
Parent: Link to epic
```

### 3. Set Dependencies

Identify which issues block others:
- API contract must be defined before frontend integration
- Database migration before feature code
- Design approval before implementation

Use Linear's "blocked by" / "blocks" relationships.

### 4. Create in Linear

Use Linear MCP to create issues:
```
mcp__linear__createIssue
  title: "..."
  description: "..."
  priority: 1
  teamId: "..."
  projectId: "..."
  parentId: "<epic-id>"
```

### 5. Report

Output:
- Epic summary
- Created issues with URLs
- Suggested execution order
- Blockers and risks

## Anti-patterns

- **Mega-issues**: "Implement the entire app" — break it down
- **Vague criteria**: "Make it work" — define "work" explicitly
- **Missing dependencies**: Issues that can't start because blockers weren't identified
