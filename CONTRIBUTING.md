# Contributing

## Workflow

1. Branch from `main`.
2. Keep changes focused.
3. Update `README.md` when commands or behavior change.
4. Run local verification before opening a PR.

## Local Verification

```bash
python3 scripts/skill_description_i18n.py --help
python3 scripts/skill_description_i18n.py scan --roots . --format markdown
python3 -m py_compile scripts/skill_description_i18n.py
```

## Rules

- Do not commit secrets, private scan output, local backups, generated caches, or dependency folders.
- Keep Chinese descriptions concise and functional.
- Preserve trigger-critical product names, file types, and command names.
- Use dry-run before applying metadata rewrites.
