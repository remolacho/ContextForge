# Validate File Exists

## Description
Check if a file exists at the given path.

## Command
```bash
test -f {file-path} && echo "exists" || echo "not_found"
```

## Parameters
`{file-path}`: Path to file to check

## Transitions

| Result | Next Step |
|--------|-----------|
| exists | Continue |
| not_found | Show error, request retry |

## Next Step
Based on validation result
