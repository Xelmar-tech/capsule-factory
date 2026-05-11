---
name: skill-creation
version: 1.0.0
description: |
  Create, improve, and manage skills. Use when the user wants to:
  - Create new skills from scratch or from session learnings
  - Improve existing skills based on user preferences
  - Analyze sessions to identify patterns worth codifying
  - Understand best practices for agentic skill design
  This is a meta-skill for self-improvement and continuous learning.
---

# Skill Creation

Build and improve skills for the PM team.

## Why Skills?

Every solved problem usually dies with the session. Skills turn "I figured this out once" into "I know how to do this."

## Basic Format

Skills live in a folder with a `SKILL.md` file:

```
plugins/vertical-plugins/<plugin>/skills/<skill-name>/
└── SKILL.md
```

YAML frontmatter + markdown content:

```markdown
---
name: my-skill
version: 1.0.0
description: |
  What this skill does.
  When to use it.
---

# My Skill

Instructions go here.
```

## When to Create a Skill

Ask yourself:
- Did I have to dig around to figure this out?
- Would I be annoyed if I had to solve this again?
- Is there something here that isn't obvious from the docs?

If yes to any, extract it.

## Design Tips

**Start small.** A skill that does one thing well beats one that tries to cover everything.

**Include verification.** How do you know it worked?

```markdown
## Verify it worked

Run `npm test` and make sure nothing broke.
```

**Document failures too.** What doesn't work? What should you avoid?

```markdown
## What not to do

Don't run this on a dirty git working directory.
```

**Keep it fresh.** Skills rot. Update or delete stale ones.

## Improving Skills

Signs a skill needs work:
- Users ask follow-up questions after it runs
- It fails on edge cases that keep coming up
- There's a better approach now

When updating, bump the version. Breaking changes → bump major version.

## The Loop

1. Work on something
2. Notice when you learn something non-obvious
3. Extract it as a skill
4. Use the skill next time
5. Improve based on how it goes
6. Repeat
