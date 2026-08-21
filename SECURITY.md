# Security Policy

## Sensitive Areas

This skill scans local skill metadata and may expose local paths, internal tool names, product names, or private workflow descriptions in generated reports.

## Reporting

Please report security issues privately to the repository maintainer. Do not open a public issue containing secrets, private paths, internal repository names, account data, screenshots, or logs.

## Handling Local Metadata

- Review scan output before publishing it.
- Do not commit generated `translations.json` files if they include private local paths or internal names.
- Do not commit `*.bak-*` backup files created by the apply command.
- Do not run write-back against bundled, cache, system, or plugin skill directories unless you explicitly intend to modify those files.
- Rotate or remove any exposed credential immediately if one appears in skill metadata.
