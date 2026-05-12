#!/usr/bin/env python3
from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path


AGENTS = ("epic-conductor", "implementer", "analyst", "qa-capture", "debug-guru")


def run_git_root(cwd: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"not a git repository: {cwd}")
    return Path(result.stdout.strip()).resolve()


def source_checkout_root(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        if (parent / ".agents" / "codex-migration-map.json").exists() and (
            parent / "plugins" / "agent-plugins"
        ).exists():
            return parent
    return None


def cache_root(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        if parent.name != "capsule-factory":
            continue
        if (parent / "infra").exists() and (parent / "epic-conductor").exists():
            return parent
    return None


def template_for(source_root: Path, name: str) -> Path | None:
    source_template = source_root / "plugins" / "agent-plugins" / name / "codex-agents" / f"{name}.toml"
    if source_template.exists():
        return source_template

    plugin_dir = source_root / name
    if plugin_dir.exists():
        versions = sorted((p for p in plugin_dir.iterdir() if p.is_dir()), reverse=True)
        for version_dir in versions:
            cache_template = version_dir / "codex-agents" / f"{name}.toml"
            if cache_template.exists():
                return cache_template

    return None


def resolve_source_root(script_path: Path, override: str | None) -> Path:
    if override:
        root = Path(override).expanduser().resolve()
        if not root.exists():
            raise SystemExit(f"source root does not exist: {root}")
        return root

    checkout = source_checkout_root(script_path)
    if checkout:
        return checkout

    cache = cache_root(script_path)
    if cache:
        return cache

    raise SystemExit(
        "could not locate Capsule Factory source. Pass --source-root pointing to the repo checkout "
        "or ~/.codex/plugins/cache/capsule-factory."
    )


def install_agent(template: Path, destination: Path, force: bool, dry_run: bool) -> str:
    if destination.exists():
        if filecmp.cmp(template, destination, shallow=False):
            return f"unchanged {destination}"
        if not force:
            return f"differs   {destination} (skipped; rerun with --force to replace)"
        action = "replace"
    else:
        action = "install"

    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template, destination)
    return f"{action:<9} {destination}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Capsule Factory Codex agent templates.")
    parser.add_argument("--repo", default=".", help="Target repo root or any path inside it.")
    parser.add_argument("--source-root", help="Capsule Factory source checkout or installed cache root.")
    parser.add_argument("--force", action="store_true", help="Replace differing destination TOML files.")
    parser.add_argument("--dry-run", action="store_true", help="Report actions without writing files.")
    args = parser.parse_args()

    target_root = run_git_root(Path(args.repo).expanduser().resolve())
    source_root = resolve_source_root(Path(__file__).resolve(), args.source_root)
    destination_root = target_root / ".codex" / "agents"

    print(f"target_repo={target_root}")
    print(f"source_root={source_root}")

    missing: list[str] = []
    for name in AGENTS:
        template = template_for(source_root, name)
        if template is None:
            missing.append(name)
            continue
        destination = destination_root / f"{name}.toml"
        print(install_agent(template, destination, args.force, args.dry_run))

    if missing:
        print("missing templates: " + ", ".join(missing), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
