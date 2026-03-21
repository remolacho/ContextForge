# Make Check

## Description
Run full verification: lint, typecheck, and tests.

## Command
```bash
make check
```

## Individual Commands

### Run Lint
→ Leer `.agents/skills/checks/run_lint.md`

```bash
make lint
```

### Run Typecheck
→ Leer `.agents/skills/checks/run_typecheck.md`

```bash
make typecheck
```

### Run Tests
→ Leer `.agents/skills/checks/run_tests.md`

```bash
make test
```

## Expected Output
```
=== Lint ===
✓ Passed

=== Typecheck ===
✓ Passed

=== Tests ===
✓ Passed

=== All checks passed ===
```

## Failure Output
```
=== Lint ===
✗ Failed
[errors]

=== Typecheck ===
✗ Failed
[errors]

=== Tests ===
✗ Failed
[errors]
```

## Validation
Must pass before FINALIZE and before commits.

## Next Step
Return to invoking workflow
