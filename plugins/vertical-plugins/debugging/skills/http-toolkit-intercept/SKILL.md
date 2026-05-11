---
name: http-toolkit-intercept
version: 1.0.0
description: |
  Intercept and debug HTTP traffic from any CLI, service, or script using HTTP Toolkit.
  Use when the user asks to "debug API calls," "intercept requests," or "inspect traffic."
---

# HTTP Toolkit Intercept

Intercept and debug HTTP traffic.

## When to Use

- API call debugging
- Request/response inspection
- Authentication flow tracing
- Performance analysis
- Mocking external services

## Setup

```bash
# Install HTTP Toolkit
npm install -g @httptoolkit/cli

# Start interception
httptoolkit intercept
```

## Intercepting

### CLI Tools
```bash
# Intercept curl
httptoolkit intercept curl https://api.example.com

# Intercept any command
httptoolkit intercept npm test
```

### Services
```bash
# Intercept a running service
httptoolkit intercept --pid 12345
```

### Scripts
```bash
# Intercept a Node.js script
httptoolkit intercept node script.js
```

## Analyzing Traffic

### Request Details
- Method, URL, headers
- Body content
- Query parameters

### Response Details
- Status code
- Headers
- Body content

### Timing
- DNS lookup
- Connection time
- Time to first byte
- Total duration

## Mocking

```bash
# Mock a response
httptoolkit mock https://api.example.com/users --response '{"users":[]}'
```

## Exporting

```bash
# Save to HAR file
httptoolkit export --format har --output traffic.har
```

## Anti-patterns

- **Intercepting everything**: Focus on the specific flow
- **Ignoring HTTPS**: Need certificate trust for HTTPS
- **Not filtering**: Too much noise without filters
- **Missing timing data**: Enable timing collection
