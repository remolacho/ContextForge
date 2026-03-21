# Git Merge PR

## Description
Squash merge the pull request and cleanup branch.

## Commands
```bash
# Squash and merge
gh pr merge --squash

# Delete remote branch
git push origin --delete {branch-name}

# Delete local branch
git branch -d {branch-name}
```

## Warning
This action merges to the base branch (development or main).

## Cleanup
Remove session file after merge:
```bash
rm .context/session_*.md
```

## Next Step
Return to invoking workflow
