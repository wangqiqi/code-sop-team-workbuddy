#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the installable code-sop-team.zip from the repository root.

Standard library only. Validation must pass before a zip is produced.

Usage:
    python scripts/build_package.py
    python scripts/build_package.py --output dist/code-sop-team.zip
    python scripts/build_package.py --expect-version 1.5.3
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_package import validate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PKG_NAME = "code-sop-team"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SKIP_TOP = {".github", "scripts", "dist", "output"}
SKIP_FILE_NAMES = {".gitkeep", ".DS_Store", "Thumbs.db", "RELEASE_NOTES.md"}
SKIP_SUFFIXES = (".pyc", ".pyo", ".zip")


def _should_skip(rel: Path) -> bool:
    parts = rel.parts
    if parts[0] in SKIP_TOP:
        return True
    for part in parts:
        if part.startswith(".") and part != ".codebuddy-plugin":
            return True
        if part in {"__pycache__", "node_modules"}:
            return True
    if rel.name in SKIP_FILE_NAMES:
        return True
    if rel.name.endswith(SKIP_SUFFIXES):
        return True
    return False


def build(output: Path, expect_version: str = "") -> Path:
    errors, warnings, version = validate()
    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(f"FAILED: {len(errors)} validation error(s); packaging aborted")
    if expect_version and expect_version != version:
        raise SystemExit(
            f"FAILED: expected version {expect_version}, plugin.json says {version}"
        )

    output = output if output.is_absolute() else ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    files: List[Path] = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if _should_skip(rel):
            continue
        files.append(p)

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            rel = p.relative_to(ROOT)
            info = zipfile.ZipInfo(f"{PKG_NAME}/{rel.as_posix()}", FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (p.stat().st_mode & 0xFFFF) << 16
            zf.writestr(info, p.read_bytes())

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    size_kb = output.stat().st_size / 1024
    print(f"OK: packaged {len(files)} files -> {output}")
    print(f"    version: {version}")
    print(f"    size: {size_kb:.1f} KB")
    print(f"    sha256: {digest}")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Package code-sop-team as a zip")
    parser.add_argument("--output", default="dist/code-sop-team.zip")
    parser.add_argument("--expect-version", default="")
    args = parser.parse_args()
    build(Path(args.output), args.expect_version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
