# Pre-Upload Checklist

## Repository

- [ ] Confirm this is the intended repository root.
- [ ] Confirm branch and remote before pushing.
- [ ] Confirm README, LICENSE, SECURITY, CONTRIBUTING, and GitHub templates are present.
- [ ] Confirm `.gitignore` excludes local scan output, backups, logs, and generated artifacts.

## Content

- [ ] `SKILL.md` describes safe preview before write-back.
- [ ] `scripts/skill_description_i18n.py` passes Python compile check.
- [ ] README includes install, usage, CLI examples, safety model, verification, and security notes.

## Privacy And Security

- [ ] No `.env` files.
- [ ] No API keys, tokens, cookies, private URLs, account IDs, internal scan outputs, or screenshots.
- [ ] No local backup files such as `*.bak-*`.
- [ ] No generated `translations.json` with private paths.

## Verification

```bash
python3 scripts/skill_description_i18n.py --help
python3 scripts/skill_description_i18n.py scan --roots . --format markdown
python3 -m py_compile scripts/skill_description_i18n.py
python3 /Users/kityhello/.codex/skills/github-publish-prep/scripts/validate_github_publish_prep.py .
```

## Pause Conditions

Pause before uploading if scan output contains private names, Git history contains private data, license choice is unclear, or the target GitHub repository visibility is uncertain.
