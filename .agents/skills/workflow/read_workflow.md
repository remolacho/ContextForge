# Read Workflow

## Description
Read and execute steps from a workflow file.

## Command
```bash
cat .agents/workflows/{workflow-name}.md
```

## Parameter
`{workflow-name}`: Name of workflow file (without .md)

## Available Workflows

| Workflow | File | Purpose |
|----------|------|---------|
| init | init_workflow.md | Initialization |
| task_source | task_source_workflow.md | Task source selection |
| plan | plan_workflow.md | Generate implementation plan |
| execute | execute_workflow.md | Execute plan steps |
| finalize | finalize_workflow.md | Commit, push, PR |

## Next Step
Execute referenced workflow
