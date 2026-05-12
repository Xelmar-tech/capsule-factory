#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / ".agents" / "codex-migration-map.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(errors, f"{rel(path)}: invalid JSON: {exc}")
        return {}


def validate_frontmatter(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(errors, f"{rel(path)}: missing YAML frontmatter")
        return
    end = text.find("\n---", 4)
    if end == -1:
        fail(errors, f"{rel(path)}: unterminated YAML frontmatter")
        return
    frontmatter = text[4:end]
    if not re.search(r"^name:\s*\S+", frontmatter, re.MULTILINE):
        fail(errors, f"{rel(path)}: frontmatter missing name")
    if not re.search(r"^description:\s*", frontmatter, re.MULTILINE):
        fail(errors, f"{rel(path)}: frontmatter missing description")


def validate_plugin_manifests(errors: list[str]) -> None:
    claude_manifests = sorted(ROOT.glob("plugins/**/.claude-plugin/plugin.json"))
    if not claude_manifests:
        fail(errors, "no Claude plugin manifests found")

    for claude_manifest in claude_manifests:
        codex_manifest = claude_manifest.parent.parent / ".codex-plugin" / "plugin.json"
        if not codex_manifest.exists():
            fail(errors, f"{rel(claude_manifest)}: missing sibling {rel(codex_manifest)}")
            continue
        claude = load_json(claude_manifest, errors)
        codex = load_json(codex_manifest, errors)
        if claude.get("name") != codex.get("name"):
            fail(errors, f"{rel(codex_manifest)}: name does not match Claude manifest")
        if claude.get("version") != codex.get("version"):
            fail(errors, f"{rel(codex_manifest)}: version does not match Claude manifest")
        for key in ("name", "version", "description", "interface"):
            if key not in codex:
                fail(errors, f"{rel(codex_manifest)}: missing required Codex field {key}")
        if "skills" not in codex and (codex_manifest.parent.parent / "skills").exists():
            fail(errors, f"{rel(codex_manifest)}: plugin has skills but no skills path")
        for prompt in codex.get("interface", {}).get("defaultPrompt", []):
            if len(prompt) > 128:
                fail(errors, f"{rel(codex_manifest)}: interface.defaultPrompt exceeds 128 characters")


def validate_marketplaces(errors: list[str]) -> None:
    claude = load_json(CLAUDE_MARKETPLACE, errors)
    codex = load_json(CODEX_MARKETPLACE, errors)
    claude_plugins = {entry.get("name") for entry in claude.get("plugins", [])}
    codex_plugins = {entry.get("name") for entry in codex.get("plugins", [])}
    missing = sorted(name for name in claude_plugins - codex_plugins if name)
    extra = sorted(name for name in codex_plugins - claude_plugins if name)
    for name in missing:
        fail(errors, f"{rel(CODEX_MARKETPLACE)}: missing plugin entry {name}")
    for name in extra:
        fail(errors, f"{rel(CODEX_MARKETPLACE)}: extra plugin entry {name}")

    for entry in codex.get("plugins", []):
        name = entry.get("name", "<unknown>")
        source = entry.get("source", {})
        if source.get("source") != "local":
            fail(errors, f"{rel(CODEX_MARKETPLACE)}: {name} source must be local")
        path = source.get("path")
        if not path or not path.startswith("./"):
            fail(errors, f"{rel(CODEX_MARKETPLACE)}: {name} source.path must start with ./")
        elif not (ROOT / path[2:]).exists():
            fail(errors, f"{rel(CODEX_MARKETPLACE)}: {name} source path does not exist: {path}")
        policy = entry.get("policy", {})
        if policy.get("installation") not in {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}:
            fail(errors, f"{rel(CODEX_MARKETPLACE)}: {name} has invalid policy.installation")
        if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
            fail(errors, f"{rel(CODEX_MARKETPLACE)}: {name} has invalid policy.authentication")
        if not entry.get("category"):
            fail(errors, f"{rel(CODEX_MARKETPLACE)}: {name} missing category")


def validate_agent_templates(errors: list[str]) -> None:
    for claude_agent in sorted(ROOT.glob("plugins/agent-plugins/*/agents/*.md")):
        name = claude_agent.stem
        template = claude_agent.parent.parent / "codex-agents" / f"{name}.toml"
        if not template.exists():
            fail(errors, f"{rel(claude_agent)}: missing Codex agent template {rel(template)}")
            continue
        try:
            data = tomllib.loads(template.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"{rel(template)}: invalid TOML: {exc}")
            continue
        for key in ("name", "description", "model", "model_reasoning_effort", "sandbox_mode", "developer_instructions"):
            if key not in data:
                fail(errors, f"{rel(template)}: missing {key}")
        if data.get("name") != name:
            fail(errors, f"{rel(template)}: name must be {name}")
        if data.get("sandbox_mode") not in {"read-only", "workspace-write", "danger-full-access"}:
            fail(errors, f"{rel(template)}: invalid sandbox_mode")


def validate_skills(errors: list[str]) -> None:
    for skill in sorted(ROOT.glob("plugins/**/skills/*/SKILL.md")):
        validate_frontmatter(skill, errors)


def validate_migration_map(errors: list[str]) -> None:
    data = load_json(MAP_PATH, errors)
    for section in ("plugins", "commands", "runtime_terms"):
        if section not in data:
            fail(errors, f"{rel(MAP_PATH)}: missing {section}")
    for plugin in data.get("plugins", []):
        for key in ("claude_manifest", "codex_manifest"):
            path = ROOT / plugin.get(key, "")
            if not path.exists():
                fail(errors, f"{rel(MAP_PATH)}: missing mapped {key}: {plugin.get(key)}")
        if "claude_agent" in plugin:
            for key in ("claude_agent", "codex_agent_template"):
                path = ROOT / plugin.get(key, "")
                if not path.exists():
                    fail(errors, f"{rel(MAP_PATH)}: missing mapped {key}: {plugin.get(key)}")
    for command in data.get("commands", []):
        for key in ("claude_command", "codex_skill"):
            path = ROOT / command.get(key, "")
            if not path.exists():
                fail(errors, f"{rel(MAP_PATH)}: missing mapped {key}: {command.get(key)}")
    for skill in data.get("codex_only_skills", []):
        path = ROOT / skill.get("codex_skill", "")
        if not path.exists():
            fail(errors, f"{rel(MAP_PATH)}: missing mapped codex_skill: {skill.get('codex_skill')}")


def validate_codex_phrase_hygiene(errors: list[str]) -> None:
    banned = (
        "TeamCreate",
        "SendMessage",
        "TaskOutput",
        "~/.claude/settings.json",
        ".factory",
        "DROID_PLUGIN_ROOT",
        "droid-dev",
        "@droid",
    )
    targets: list[Path] = []
    targets.extend(ROOT.glob("plugins/**/.codex-plugin/plugin.json"))
    targets.extend(ROOT.glob("plugins/**/codex-agents/*.toml"))
    targets.append(ROOT / "plugins" / "vertical-plugins" / "infra" / "skills" / "capsule-setup" / "SKILL.md")
    targets.append(ROOT / "AGENTS.md")

    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for term in banned:
            if term in text:
                fail(errors, f"{rel(path)}: Codex-facing file contains Claude/Droid-only term {term!r}")


def main() -> int:
    errors: list[str] = []
    validate_plugin_manifests(errors)
    validate_marketplaces(errors)
    validate_agent_templates(errors)
    validate_skills(errors)
    validate_migration_map(errors)
    validate_codex_phrase_hygiene(errors)

    if errors:
        print("Codex migration validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Codex migration validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
