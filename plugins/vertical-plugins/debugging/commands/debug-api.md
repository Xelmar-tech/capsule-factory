---
description: Debug API calls and HTTP traffic
argument-hint: '["intercept" | "mock" | "analyze"] <target>'
---

# Debug API Command

Intercept and debug HTTP traffic.

## Workflow

### Step 1: Target Selection

Determine what to intercept:
- CLI command: `httptoolkit intercept curl https://api.example.com`
- Running service: `httptoolkit intercept --pid 12345`
- Script: `httptoolkit intercept node script.js`

### Step 2: Intercept

Use `http-toolkit-intercept` skill to capture traffic.

### Step 3: Analyze

Inspect:
- Request/response headers
- Body content
- Status codes
- Timing data

### Step 4: Report

Output findings with specific issues and recommendations.
