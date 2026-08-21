# Skill Description Translator

把英文或中英混合的 Codex skill 简介整理成简洁中文，方便在 skill 选择器里快速判断每个 skill 的用途。

这个仓库打包了一个可分享的 Codex skill，包含：

- `SKILL.md`：agent 使用说明。
- `scripts/skill_description_i18n.py`：扫描和安全写回工具。
- `agents/openai.yaml` / `agents/interface.yaml`：Codex UI 元数据。

## Preview

处理后，Codex skill 选择器里的简介会变成更容易浏览的中文说明：

![Codex skill 选择器中文简介效果图](docs/images/skill-picker-chinese-descriptions.png)

扫描本机用户 skill 中英文偏重的简介：

```bash
python3 scripts/skill_description_i18n.py scan \
  --roots ~/.codex/skills ~/.agents/skills \
  --format markdown
```

输出示例：

```markdown
| skill | english-heavy | description |
| --- | --- | --- |
| example-skill | True | Generate release notes from Git commits |
```

应用人工确认后的中文简介：

```bash
python3 scripts/skill_description_i18n.py apply \
  --translations translations.json \
  --dry-run

python3 scripts/skill_description_i18n.py apply \
  --translations translations.json
```

## What It Does

- 扫描 Codex skill 目录下的 `SKILL.md` frontmatter。
- 找出英文偏重的 `description`。
- 输出 Markdown 或 JSON 清单，方便人工审阅。
- 支持把确认后的中文简介写回 `SKILL.md`。
- 支持同步更新 `agents/openai.yaml` 的 `interface.short_description`。
- 写回前自动备份被修改的文件。

## When To Use

适合这些情况：

- 本机装了很多 skill，skill 选择器里英文简介太多。
- 想统一把用户安装的 skill 描述改成简洁中文。
- 想给一个 skill 或一批 skill 生成中文 UI 摘要。
- 想安全地批量写回元数据，同时保留备份。

不适合这些情况：

- 翻译正文、文章、README 或代码注释。
- 自动翻译系统内置 skill、插件缓存或第三方包，除非你明确知道要改什么。
- 未经审阅直接批量覆盖元数据。

## Requirements

- Python 3.10+。
- Codex skill 目录，例如 `~/.codex/skills` 或 `~/.agents/skills`。
- 不依赖第三方 Python 包。

## Install

复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R skill-description-translator ~/.codex/skills/skill-description-translator
```

重新打开 Codex 任务，让 skill 列表刷新。

## Usage In Codex

```text
[$skill-description-translator](~/.codex/skills/skill-description-translator/SKILL.md) 扫描本机用户 skill 的英文简介，先给我预览，不要写回。
```

如果你确认要写回，可以明确说明：

```text
把刚才确认的翻译写回这些 skill，先 dry-run，再备份并应用。
```

## CLI Usage

扫描默认用户 skill：

```bash
python3 scripts/skill_description_i18n.py scan
```

扫描多个根目录：

```bash
python3 scripts/skill_description_i18n.py scan \
  --roots ~/.codex/skills ~/.agents/skills \
  --format markdown
```

包含所有 skill，而不只英文偏重项：

```bash
python3 scripts/skill_description_i18n.py scan \
  --roots ~/.codex/skills \
  --all \
  --format json
```

准备翻译文件：

```json
[
  {
    "path": "/Users/example/.codex/skills/example-skill",
    "description_zh": "生成发布说明并整理 Git 变更摘要",
    "short_description_zh": "生成发布说明"
  }
]
```

先预演：

```bash
python3 scripts/skill_description_i18n.py apply \
  --translations translations.json \
  --dry-run
```

确认后写回：

```bash
python3 scripts/skill_description_i18n.py apply \
  --translations translations.json
```

## Safety Model

- 默认只扫描，不写文件。
- `apply` 只处理你在 `translations.json` 中列出的路径。
- 写回 `SKILL.md` 前会生成 `*.bak-YYYYMMDD-HHMMSS` 备份。
- 只有存在 `agents/openai.yaml` 时才会尝试更新 `short_description`。
- 不会自动改 bundled、cache、system skill，除非你把这些路径显式写进输入。

## Project Structure

```text
SKILL.md                         Codex skill instructions.
scripts/skill_description_i18n.py Scan and apply helper.
agents/openai.yaml               Codex UI metadata.
agents/interface.yaml            Alternate UI metadata.
```

## Verification

```bash
python3 scripts/skill_description_i18n.py --help
python3 scripts/skill_description_i18n.py scan --roots . --format markdown
python3 -m py_compile scripts/skill_description_i18n.py
```

Repository prep check:

```bash
python3 /Users/kityhello/.codex/skills/github-publish-prep/scripts/validate_github_publish_prep.py .
```

## Security Notes

- Skill descriptions can mention product names or internal systems. Review output before publishing.
- Do not commit generated `translations.json` if it contains private local paths you do not want public.
- Do not commit backup files created by `apply`.
- Do not run `apply` against system or plugin cache paths unless you intentionally want to modify them.

## License

MIT. See [LICENSE](LICENSE).
