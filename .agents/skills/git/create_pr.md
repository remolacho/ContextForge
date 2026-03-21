# Git Create Pull Request

## Description
Create a pull request using GitHub CLI.

## Command
```bash
gh pr create \
  --title "{MCF-XXX}: {title}" \
  --body "{body}" \
  --base {base-branch} \
  --head {head-branch}
```

## Parameters
- `title`: Format `{MCF-XXX}: {task title}`
- `body`: PR description (see pr_template.md)
- `base`: `development` for features, `main` for hotfixes
- `head`: Branch name

## PR Body Template
```markdown
## Summary

- {change 1}
- {change 2}
- Tests verified

## Links

| Resource | URL |
|----------|-----|
| YouTrack | https://communities.youtrack.cloud/issue/{MCF-XXX} |
```

## Next Step
Return to invoking workflow
