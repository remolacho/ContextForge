# YouTrack Update Issue

## Description
Update issue state or fields in YouTrack.

## Tool
Use `youtrack_update_issue` with the following structure:

```json
{
  "issueId": "{MCF-XXX}",
  "customFields": {
    "State": "{new-state}"
  }
}
```

## Common State Updates

| Workflow Step | State |
|---------------|-------|
| After PLAN | "In Progress" / "En curso" |
| After FINALIZE | "Done" |

## Example
```json
{
  "issueId": "MCF-123",
  "customFields": {"State": "Done"}
}
```

## Next Step
Return to invoking workflow
