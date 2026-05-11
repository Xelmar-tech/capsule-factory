---
description: Run an autonomous optimization experiment
argument-hint: '"<metric to optimize>" ["build time" | "bundle size" | "test speed"]'
---

# Experiment Command

Run an autonomous optimization experiment loop.

## Workflow

### Step 1: Define Target

Determine the metric to optimize and target value.

### Step 2: Baseline

Measure current performance using `autoresearch` skill.

### Step 3: Generate Ideas

Brainstorm 3-5 approaches to improve the metric.

### Step 4: Run Experiments

For each idea:
1. Create branch
2. Apply change
3. Measure 3-5 times
4. Record results

### Step 5: Evaluate

Compare to baseline. Keep improvements, revert regressions.

### Step 6: Report

Output experiment log with verdicts for each idea.
