---
description: Generate a threat model for a system, feature, or architecture
argument-hint: '<system name, feature, or path to design doc>'
---

Load skill: **threat-model-generation**.

The user invoked `/threat-model` for `$ARGUMENTS`. Apply the `threat-model-generation` skill: identify assets, trust boundaries, entry points, and adversaries; enumerate threats (STRIDE-style: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege); for each, note likelihood, impact, and a concrete mitigation. Produce a markdown report. If the input is a path to a design doc, read it first; if it's a system name with no obvious source, ask the user where the architecture is described before guessing.
