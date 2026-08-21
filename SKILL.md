---
name: skill-description-translator
description: "将英文或中英混合的 Codex skill 简介翻译成简洁中文，方便在 skill 选择器中浏览；适用于本地化 skill picker、检查 SKILL.md description、生成 agents/openai.yaml 中文摘要或安全写回元数据。"
---

# Skill Description Translator

## Purpose

Turn English-heavy skill introductions into short, natural Chinese descriptions that are easier to scan in the Codex skill picker.

Default to a safe preview. Only write back to existing skills when the user explicitly asks to apply changes.

## Workflow

1. Clarify scope only if it is ambiguous: one skill, one folder, or all installed user skills.
2. Scan candidate skills with `scripts/skill_description_i18n.py scan`.
3. Translate only the user-facing intent, not internal implementation details.
4. Keep trigger-critical keywords when useful, especially product names, file types, command names, and skill names.
5. Preview the proposed Chinese descriptions before writing.
6. Apply changes only after explicit approval, using backups.

## Chinese Description Style

- Use 简体中文.
- Prefer one compact sentence.
- Keep UI descriptions around 20-50 Chinese characters when possible.
- Start with the capability or outcome, not “这个 skill 可以”.
- Preserve untranslatable nouns such as Codex, GitHub, Vercel, Next.js, PDF, PRD, API, CLI.
- Translate verbs naturally: “Generate” -> “生成”, “Audit” -> “审查/评估”, “Use when” -> omit unless needed.
- Avoid marketing tone, emoji, and exaggerated claims.
- Do not remove important trigger hints if the original description uses MUST USE, file extensions, named platforms, or safety boundaries.

## Write Policy

For normal requests, produce a table with:

- skill name
- current description
- proposed Chinese description
- whether a write-back is recommended

When the user asks to apply:

- Back up every edited file.
- Update `SKILL.md` frontmatter `description` only for the selected skills.
- Update `agents/openai.yaml` `interface.short_description` only when it exists or when the user asks for UI metadata.
- Do not edit bundled/cache/system skills unless the user explicitly includes them in scope.

## Script

Use the helper for scanning and safe metadata updates:

```bash
python3 /Users/kityhello/.codex/skills/skill-description-translator/scripts/skill_description_i18n.py scan --roots ~/.codex/skills ~/.agents/skills --format markdown
```

To apply reviewed translations:

```bash
python3 /Users/kityhello/.codex/skills/skill-description-translator/scripts/skill_description_i18n.py apply --translations translations.json --dry-run
python3 /Users/kityhello/.codex/skills/skill-description-translator/scripts/skill_description_i18n.py apply --translations translations.json
```

The translations JSON should be:

```json
[
  {
    "path": "/absolute/path/to/skill",
    "description_zh": "用中文概括这个 skill 的用途",
    "short_description_zh": "更短的中文 UI 简介"
  }
]
```

Use `description_zh` for `SKILL.md`; use `short_description_zh` for `agents/openai.yaml`.
