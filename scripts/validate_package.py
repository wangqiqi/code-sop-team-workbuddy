#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expert package schema validation for CI (Python standard library only).

Why a local validator: the WorkBuddy runtime rejected members[].name written as
`displayName`, but the official validator did not catch it. This script checks
the runtime-critical fields before CI packages or publishes anything.

Usage:
    python scripts/validate_package.py
    python scripts/validate_package.py --print-version
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / ".codebuddy-plugin" / "plugin.json"
SETTINGS_JSON = ROOT / "settings.json"
RELEASE_NOTES = ROOT / "RELEASE_NOTES.md"

EXPECTED_NAME = "code-sop-team"
VALID_EXPERT_TYPES = {"expert", "team"}
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
I18N_FIELDS = (
    "displayName",
    "profession",
    "displayDescription",
    "defaultInitPrompt",
)


def _load_json(path: Path, errors: List[str]) -> Dict:
    try:
        with path.open("r", encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        errors.append(f"缺少文件: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        errors.append(f"JSON 解析失败 {path.relative_to(ROOT)}: {e}")
    except OSError as e:
        errors.append(f"无法读取 {path.relative_to(ROOT)}: {e}")
    return {}


def _check_i18n(obj: Dict, field: str, errors: List[str], ctx: str) -> None:
    if field not in obj:
        errors.append(f"{ctx}: 缺少字段 '{field}'")
        return
    value = obj[field]
    if not isinstance(value, dict):
        errors.append(f"{ctx}: '{field}' 必须是含 en/zh 的对象")
        return
    for lang in ("en", "zh"):
        if not isinstance(value.get(lang), str) or not value[lang].strip():
            errors.append(f"{ctx}: '{field}.{lang}' 为必填且不能为空")


def _path_from_plugin(raw: str) -> Path:
    raw = str(raw)
    if raw.startswith("./"):
        raw = raw[2:]
    return ROOT / raw


def _check_frontmatter(path: Path, errors: List[str], require_name_match: bool) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        errors.append(f"无法读取 {path.relative_to(ROOT)}: {e}")
        return
    if not text.startswith("---"):
        errors.append(f"{path.relative_to(ROOT)}: 缺少 YAML frontmatter")
        return
    m = re.search(r"^name:\s*(.+?)\s*$", text, re.MULTILINE)
    if not m:
        errors.append(f"{path.relative_to(ROOT)}: frontmatter 缺少 name")
        return
    name = m.group(1).strip().strip("'\"")
    if require_name_match and name != path.stem:
        errors.append(
            f"{path.relative_to(ROOT)}: frontmatter name '{name}' 与文件名 '{path.stem}' 不一致"
        )


def validate() -> Tuple[List[str], List[str], str]:
    """Return (errors, warnings, version)."""
    errors: List[str] = []
    warnings: List[str] = []

    pj = _load_json(PLUGIN_JSON, errors)
    if not pj:
        return errors, warnings, ""

    name = pj.get("name", "")
    version = pj.get("version", "")
    if name != EXPECTED_NAME:
        errors.append(f"plugin.json: name 应为 '{EXPECTED_NAME}'，实际为 '{name}'")
    if not VERSION_RE.match(str(version)):
        errors.append(f"plugin.json: version 必须为 x.y.z，实际为 '{version}'")
    for field in ("description",):
        if not isinstance(pj.get(field), str) or not pj[field].strip():
            errors.append(f"plugin.json: 缺少字段 '{field}'")

    if pj.get("expertType") not in VALID_EXPERT_TYPES:
        errors.append(f"plugin.json: expertType 必须为 expert/team，实际为 '{pj.get('expertType')}'")
    if pj.get("plugin") != name:
        errors.append("plugin.json: 'plugin' 必须等于 'name'")

    agent_name = pj.get("agentName", "")
    if not agent_name:
        errors.append("plugin.json: 缺少 agentName")
    elif not (ROOT / "agents" / f"{agent_name}.md").is_file():
        errors.append(f"plugin.json: 找不到 agents/{agent_name}.md")

    for field in I18N_FIELDS:
        _check_i18n(pj, field, errors, "plugin.json")

    dd_zh = pj.get("displayDescription", {}).get("zh", "")
    if isinstance(dd_zh, str) and not (40 <= len(dd_zh) <= 50):
        warnings.append(
            f"plugin.json: displayDescription.zh 为 {len(dd_zh)} 字，建议 40-50 字"
        )
    if pj.get("profession") != pj.get("displayName"):
        warnings.append("plugin.json: profession 与 displayName 不一致")

    tags = pj.get("tags", [])
    if not isinstance(tags, list) or len(tags) != 3:
        errors.append(f"plugin.json: 必须恰好 3 个 tags，实际 {len(tags) if isinstance(tags, list) else '非数组'}")
    prompts = pj.get("quickPrompts", [])
    if not isinstance(prompts, list) or len(prompts) != 3:
        errors.append(
            f"plugin.json: 必须恰好 3 个 quickPrompts，实际 {len(prompts) if isinstance(prompts, list) else '非数组'}"
        )
    for ctx, arr in (("tags", tags), ("quickPrompts", prompts)):
        if not isinstance(arr, list):
            continue
        for i, item in enumerate(arr):
            if not isinstance(item, dict) or not item.get("en") or not item.get("zh"):
                errors.append(f"plugin.json: {ctx}[{i}] 缺少 en/zh 字段")

    avatar = pj.get("avatar", "")
    if avatar and not _path_from_plugin(avatar).is_file():
        errors.append(f"plugin.json: avatar 文件不存在: {avatar}")

    agents = pj.get("agents", [])
    if not isinstance(agents, list) or not agents:
        errors.append("plugin.json: agents 列表为空")
    else:
        for raw in agents:
            p = _path_from_plugin(raw)
            if not p.is_file():
                errors.append(f"plugin.json: agents 路径不存在: {raw}")
            else:
                _check_frontmatter(p, errors, require_name_match=True)

    skills = pj.get("skills", [])
    if not isinstance(skills, list) or not skills:
        errors.append("plugin.json: skills 列表为空")
    else:
        for raw in skills:
            p = _path_from_plugin(raw)
            skill_md = p / "SKILL.md" if p.is_dir() else p
            if not skill_md.is_file():
                errors.append(f"plugin.json: skill 缺少 SKILL.md: {raw}")
            else:
                _check_frontmatter(skill_md, errors, require_name_match=False)

    if pj.get("expertType") == "team":
        team = pj.get("teamInfo", {})
        if not isinstance(team, dict):
            errors.append("plugin.json: teamInfo 必须是对象")
        else:
            lead = team.get("leadAgent", "")
            members_agents = team.get("memberAgents", [])
            if not lead:
                errors.append("plugin.json: teamInfo.leadAgent 不能为空")
            if not isinstance(members_agents, list):
                errors.append("plugin.json: teamInfo.memberAgents 必须是数组")
                members_agents = []
            if lead and lead in members_agents:
                errors.append("plugin.json: teamInfo.memberAgents 不应包含 leadAgent")

        members = pj.get("members", [])
        if not isinstance(members, list) or not members:
            errors.append("plugin.json: team 类型必须有 members 数组")
        else:
            ids = []
            leads = []
            for i, member in enumerate(members):
                ctx = f"plugin.json.members[{i}]"
                if not isinstance(member, dict):
                    errors.append(f"{ctx}: 必须是对象")
                    continue
                _check_i18n(member, "name", errors, ctx)
                _check_i18n(member, "profession", errors, ctx)
                mid = member.get("id", "")
                if not mid:
                    errors.append(f"{ctx}: 缺少 id")
                else:
                    ids.append(mid)
                    if not (ROOT / "agents" / f"{mid}.md").is_file():
                        errors.append(f"{ctx}: 找不到 agents/{mid}.md")
                member_avatar = member.get("avatar", "")
                if member_avatar and not _path_from_plugin(member_avatar).is_file():
                    errors.append(f"{ctx}: avatar 文件不存在: {member_avatar}")
                if member.get("role") == "lead":
                    leads.append(mid)
            if len(leads) != 1:
                errors.append(f"plugin.json: members 必须恰好 1 个 role=lead，实际 {len(leads)}")
            if isinstance(members_agents, list) and set(ids) != set(members_agents) | set(leads):
                errors.append("plugin.json: members 的 id 与 teamInfo.memberAgents + leadAgent 不一致")

        settings = _load_json(SETTINGS_JSON, errors)
        if settings and settings.get("agent") != agent_name:
            errors.append(
                f"settings.json: agent='{settings.get('agent')}' 与 plugin.json.agentName='{agent_name}' 不一致"
            )

    if version and RELEASE_NOTES.is_file():
        try:
            notes = RELEASE_NOTES.read_text(encoding="utf-8")
            if f"## v{version}" not in notes and f"# v{version}" not in notes:
                warnings.append(f"RELEASE_NOTES.md 中没有 v{version} 条目标题")
        except OSError as e:
            warnings.append(f"无法读取 RELEASE_NOTES.md: {e}")

    return errors, warnings, str(version)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate code-sop-team expert package")
    parser.add_argument("--print-version", action="store_true", help="only print validated version")
    args = parser.parse_args()

    errors, warnings, version = validate()
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if errors:
        print(f"FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1
    if args.print_version:
        print(version)
    else:
        print(f"OK: schema valid, version={version}, warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
