#!/usr/bin/env python3
"""Scan Codex skills and safely apply reviewed Chinese description metadata."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import shutil
import sys
from typing import Any


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
DESC_RE = re.compile(r"(?m)^description:\s*(.*)$")
SHORT_DESC_RE = re.compile(r"(?m)^(\s*short_description:\s*)(.*)$")


def expand_roots(values: list[str]) -> list[pathlib.Path]:
    return [pathlib.Path(v).expanduser().resolve() for v in values]


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0] in {'"', "'"} and value[-1:] == value[0]:
        body = value[1:-1]
        if value[0] == '"':
            return body.replace('\\"', '"').replace('\\\\', '\\')
        return body.replace("''", "'")
    return value


def extract_description(skill_md: pathlib.Path) -> str | None:
    text = read_text(skill_md)
    match = FRONTMATTER_RE.search(text)
    if not match:
        return None
    desc = DESC_RE.search(match.group(1))
    if not desc:
        return None
    return unquote_yaml_scalar(desc.group(1))


def is_english_heavy(text: str) -> bool:
    latin = len(re.findall(r"[A-Za-z]", text))
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    return latin >= 12 and latin > cjk


def iter_skills(roots: list[pathlib.Path]):
    seen: set[pathlib.Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for skill_md in root.glob("*/SKILL.md"):
            folder = skill_md.parent.resolve()
            if folder in seen:
                continue
            seen.add(folder)
            desc = extract_description(skill_md)
            if desc is None:
                continue
            yield {
                "name": folder.name,
                "path": str(folder),
                "skill_md": str(skill_md),
                "description": desc,
                "english_heavy": is_english_heavy(desc),
            }


def cmd_scan(args: argparse.Namespace) -> int:
    rows = list(iter_skills(expand_roots(args.roots)))
    if args.only_english_heavy:
        rows = [row for row in rows if row["english_heavy"]]
    rows.sort(key=lambda item: item["name"])

    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    print("| skill | english-heavy | description |")
    print("| --- | --- | --- |")
    for row in rows:
        desc = str(row["description"]).replace("|", "\\|").replace("\n", " ")
        print(f"| {row['name']} | {row['english_heavy']} | {desc} |")
    return 0


def backup(path: pathlib.Path) -> pathlib.Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_suffix(path.suffix + f".bak-{stamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def replace_frontmatter_description(text: str, value: str) -> str:
    match = FRONTMATTER_RE.search(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    frontmatter = match.group(1)
    if not DESC_RE.search(frontmatter):
        raise ValueError("missing description field")
    new_frontmatter = DESC_RE.sub(f"description: {yaml_scalar(value)}", frontmatter, count=1)
    return text[: match.start(1)] + new_frontmatter + text[match.end(1) :]


def replace_openai_short_description(text: str, value: str) -> str:
    if not SHORT_DESC_RE.search(text):
        return text
    return SHORT_DESC_RE.sub(lambda m: m.group(1) + yaml_scalar(value), text, count=1)


def cmd_apply(args: argparse.Namespace) -> int:
    data = json.loads(read_text(pathlib.Path(args.translations).expanduser()))
    if not isinstance(data, list):
        raise SystemExit("translations JSON must be a list")

    changes: list[str] = []
    for item in data:
        if not isinstance(item, dict) or "path" not in item:
            raise SystemExit("each translation must include path")
        folder = pathlib.Path(str(item["path"])).expanduser().resolve()
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            raise SystemExit(f"missing SKILL.md: {skill_md}")

        if item.get("description_zh"):
            old = read_text(skill_md)
            new = replace_frontmatter_description(old, str(item["description_zh"]))
            if new != old:
                changes.append(str(skill_md))
                if not args.dry_run:
                    backup(skill_md)
                    skill_md.write_text(new, encoding="utf-8")

        if item.get("short_description_zh"):
            openai_yaml = folder / "agents" / "openai.yaml"
            if openai_yaml.exists():
                old = read_text(openai_yaml)
                new = replace_openai_short_description(old, str(item["short_description_zh"]))
                if new != old:
                    changes.append(str(openai_yaml))
                    if not args.dry_run:
                        backup(openai_yaml)
                        openai_yaml.write_text(new, encoding="utf-8")

    prefix = "Would update" if args.dry_run else "Updated"
    for path in changes:
        print(f"{prefix}: {path}")
    if not changes:
        print("No changes.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="list installed skills and descriptions")
    scan.add_argument("--roots", nargs="+", default=["~/.codex/skills"], help="skill root directories")
    scan.add_argument("--format", choices=["markdown", "json"], default="markdown")
    scan.add_argument("--only-english-heavy", action="store_true", default=True)
    scan.add_argument("--all", dest="only_english_heavy", action="store_false")
    scan.set_defaults(func=cmd_scan)

    apply = sub.add_parser("apply", help="apply reviewed Chinese translations")
    apply.add_argument("--translations", required=True, help="JSON file with path and translated fields")
    apply.add_argument("--dry-run", action="store_true")
    apply.set_defaults(func=cmd_apply)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
