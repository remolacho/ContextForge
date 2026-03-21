# YouTrack Add Comment

## Description
Add a comment to an issue in YouTrack.

## Tool
Use `youtrack_add_issue_comment` with the following parameters:

| Parameter | Value |
|-----------|-------|
| issueId | {MCF-XXX} |
| text | Comment body (markdown) |

## Comment Template
```markdown
## PR Created

PR: {PR_URL}

## Summary of Changes

- [x] {change 1}
- [x] {change 2}
- [x] Tests verified

## Verification

| Verification | Status |
|--------------|--------|
| Lint | ✅ passed |
| Typecheck | ✅ passed |
| Tests | ✅ passed |
```

## Next Step
Return to invoking workflow
