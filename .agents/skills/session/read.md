# Session Read

## Description
Read active session file to resume workflow.

## Command
```bash
ls -la .context/session_*.md 2>/dev/null | tail -1
```

## Check Session
| Result | Action |
|--------|--------|
| Session exists | Read and show summary, wait "retomar" or "nueva" |
| No session | Create new session |

## Resume
If "retomar":
- Read session_*.md
- Continue from last step

## New Session
If "nueva":
- Delete session_*.md
- Create new session

## Next Step
Based on session status
