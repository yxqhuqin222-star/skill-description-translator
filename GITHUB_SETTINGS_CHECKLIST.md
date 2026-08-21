# GitHub Settings Checklist

Apply these settings after the repository is created and pushed.

## Basic Metadata

- [ ] Description explains this is a Codex skill for Chinese skill-description localization.
- [ ] Add topics such as `codex-skill`, `agent-skills`, `metadata`, `i18n`, `python`.
- [ ] Confirm repository visibility is intended.

## Branch Protection

- [ ] Protect `main`.
- [ ] Require pull request review if collaborating.
- [ ] Require status checks when CI exists.
- [ ] Restrict force pushes.
- [ ] Restrict branch deletion.

## Security

- [ ] Enable Dependabot alerts.
- [ ] Enable Dependabot security updates.
- [ ] Enable secret scanning if available for the repository plan and visibility.
- [ ] Enable push protection if available.

## Actions

- [ ] Set default workflow permissions to read-only.
- [ ] Require approval for outside collaborators where appropriate.

## Merge Strategy

- [ ] Enable squash merge.
- [ ] Disable merge commits if you prefer linear history.
- [ ] Delete branches after merge.

## Post-Upload Review

- [ ] Review the public repository page while logged out or in a private browser.
- [ ] Confirm no private paths, scan output, or backup files appear.
