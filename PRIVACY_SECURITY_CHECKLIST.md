# Privacy And Security Checklist

## Do Not Commit

- `.env`, credentials, API keys, tokens, cookies, SSH keys, certificates.
- Generated scan outputs containing private paths or internal skill names.
- `translations.json` files containing private absolute paths.
- Backup files such as `*.bak-*`.
- Logs, screenshots, dependency folders, caches, or databases.

## Current File Scan

```bash
rg -n --hidden -g '!.git' -g '!node_modules' -g '!dist' -g '!build' -g '!coverage' \
  'AKIA|BEGIN (RSA|OPENSSH|PRIVATE) KEY|ghp_|github_pat_|xox[baprs]-|sk_live_|sk_test_|pk_live_|whsec_|api[_-]?key|secret|token|password|passwd|cookie|authorization|bearer' .
```

## High-Risk File Scan

```bash
find . -path ./.git -prune -o -type f \( \
  -name '.env' -o -name '*.env' -o -name '*.pem' -o -name '*.key' -o \
  -name 'credentials.json' -o -name 'service-account*.json' -o \
  -name '*.bak' -o -name '*.bak-*' -o -name '*.log' -o \
  -name 'translations.json' \
\) -print
```

## Git History Scan

```bash
git log --all --stat
git log --all -p -- . ':!LICENSE'
```

If `gitleaks` is installed:

```bash
gitleaks detect --source . --no-git --redact
```

## Response Rules

- Current-file secret: remove it, rotate it, and re-scan.
- Private scan output: remove it or replace with a synthetic example.
- Git-history secret: stop and decide whether history rewriting is required before publishing.
- Unclear internal project name: treat it as private until proven safe.
