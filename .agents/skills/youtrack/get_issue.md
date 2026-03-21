# YouTrack Get Issue

## Description
Retrieve issue information from YouTrack by URL or ID.

## Tool
Use `youtrack_get_issue` with the issue ID.

## Input
Extract MCF-XXX from URL or user input.

## Validation
Validate format: `MCF-\d+`

| Result | Action |
|--------|--------|
| Valid | Continue to get info |
| Invalid | Show error, request retry |

## Output
```
Issue {MCF-XXX} found:

Title: {summary}
Description: {description}
State: {state}
```

## Next Step
Return to invoking workflow
