---
name: autoresearch
version: 1.0.0
description: |
  Autonomous experiment loop for optimization research.
  Use when the user wants to "optimize performance," "run experiments," or "tune parameters."
---

# Autoresearch

Run autonomous optimization experiments with structured measurement.

## Workflow

### 1. Define the Target

What metric are you optimizing?
- Build time (seconds)
- Bundle size (KB)
- Test speed (seconds)
- Memory usage (MB)
- Accuracy (%)

### 2. Establish Baseline

Measure current performance:
```bash
# Example: build time
time npm run build
```

Record:
- Baseline value
- Variance (run 3-5 times)
- Measurement method

### 3. Design Experiments

Generate ideas to improve the metric:
- Config changes (webpack, babel, etc.)
- Code changes (algorithms, data structures)
- Dependency changes (upgrade, swap, remove)

### 4. Run Experiment

For each idea:
1. Create branch: `git checkout -b experiment/idea-name`
2. Apply change
3. Measure: run the same benchmark 3-5 times
4. Record: mean, median, standard deviation

### 5. Evaluate

Compare to baseline:
- **Improvement**: Keep the change, merge to main
- **Regression**: Revert, document why it failed
- **No change**: Document, move on

### 6. Iterate

Repeat until:
- Metric target reached
- Diminishing returns (no improvement in N attempts)
- Time budget exhausted

## Confidence Scoring

Use MAD (Median Absolute Deviation) to assess result reliability:

```
results = [12.3, 11.9, 12.1, 12.4, 12.0]
median = 12.1
mad = median(|result - median| for each result)
confidence = mad / median
```

Lower confidence = more reliable result.

## Logging

Record every experiment:
```
## Experiment Log

| # | Idea | Branch | Mean | Baseline | Delta | Confidence | Verdict |
|---|------|--------|------|----------|-------|------------|---------|
| 1 | Enable tree-shaking | exp/tree-shake | 10.2s | 12.1s | -15.7% | 0.02 | KEEP |
| 2 | Disable sourcemaps | exp/no-source | 12.3s | 12.1s | +1.7% | 0.03 | REVERT |
```

## Anti-patterns

- **Changing multiple things**: One variable at a time
- **Small sample size**: Run at least 3 times
- **Ignoring variance**: Noisy results need more samples
- **Not reverting**: Keep experiments that don't help
