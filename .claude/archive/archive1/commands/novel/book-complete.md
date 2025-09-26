---
name: book-complete
description: Complete and archive the current book
---

# Complete and Archive Book

Finalize the current book, run final quality checks, and prepare for the next phase.

## Purpose

This command orchestrates the complete book finalization process:
- Verifies all chapters are complete
- Runs final quality validation
- Merges chapters into manuscript
- Archives all book artifacts
- Prepares for series continuation

## Execution

Delegating to book-complete-coordinator:

Use the book-complete-coordinator subagent to complete and archive the current book with these instructions:

Orchestrate the book completion process.

Ensure:
- All chapters are complete
- Quality meets 95+ standard
- Full manuscript is assembled
- Archive is properly created
- Series progress is updated

## Output

The coordinator manages:
- Final quality validation
- Manuscript assembly
- Archive creation
- Completion certification
- Series progress updates

All outputs are saved to:
`.claude/data/projects/{project}/archives/book_{N}/`

## Next Steps

After completion:
- Review completion report
- Start next book: `/novel:next-book`

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

- Or extend series: `/novel:extend-series`