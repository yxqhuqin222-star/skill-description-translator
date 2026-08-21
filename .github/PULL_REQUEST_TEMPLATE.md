## Summary

Describe the change and why it is needed.

## Verification

- [ ] `python3 scripts/skill_description_i18n.py --help`
- [ ] `python3 scripts/skill_description_i18n.py scan --roots . --format markdown`
- [ ] `python3 -m py_compile scripts/skill_description_i18n.py`
- [ ] Documentation updated if behavior changed

## Secret And Privacy Check

- [ ] No `.env` files, credentials, logs, screenshots, local backups, generated scan outputs, or generated translations with private paths

## Risk

Describe behavioral, compatibility, or metadata-write risk.
