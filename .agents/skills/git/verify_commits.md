# Git Verify Commits

## Description
Show commits on current branch compared to base.

## Command
```bash
git log origin/{base-branch}..HEAD --oneline
```

## Expected Output
```
abc1234 (HEAD) Message 1
def5678 Message 2
```

## Note
If more than 1 commit, PR will squash automatically via GitHub.

## Warning
```
IMPORTANT: PR should have 1 commit.
Squash will be done via GitHub automatically.
```

## Next Step
Return to invoking workflow
