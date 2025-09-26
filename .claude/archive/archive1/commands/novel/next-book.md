---
description: Generate next book in series
---

# Next Book Generation

Initializing the next book in your series.

## Description

This command orchestrates the creation of subsequent books in a series, managing:

- Series continuity and progression
- Character and world evolution
- Plot thread transitions
- Book-specific bible generation
- Proper series structure setup

## Execution

Delegating to next book coordinator:

Use the next-book-coordinator subagent to create the next book in the series with these instructions:

Orchestrate creation of the next book in the current series.

Workflow:
1. Validate series state and prerequisites
   - Verify series bible exists and is complete
   - Count existing books and determine next number
   - Check previous book completion status

2. Plan book transition
   - Extract previous book end state
   - Conduct transition brainstorming:
     * Time gap since previous book
     * Opening situation/hook
     * Character evolution
     * World changes
   - Map continuing/new/resolved threads

3. Generate book-specific bible
   - Invoke transition-continuity-reviewer for validation
   - Create bible via bible-architect
   - Validate quality via bible-reviewer (95+ required)

4. Initialize book structure
   - Create directory structure
   - Setup tracking files
   - Generate transition documentation

Ensure:
- Full series continuity maintained
- No dropped plot threads
- Logical character progression
- Bible supports 95+ quality chapters

Provide clear success report with next steps.

## Prerequisites

- Active series project (not standalone)
- Complete series bible
- Previous book(s) in reasonable state
- Clear series progression plan

## Process Includes

1. **Continuity Analysis**: Review previous book endings
2. **Transition Planning**: Bridge between books
3. **Interactive Brainstorming**: Time gaps and evolution

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

4. **Bible Generation**: Book-specific while series-aligned
5. **Quality Validation**: Ensure 95+ bible score
6. **Structure Setup**: Initialize new book directories

## Next Steps After Success

1. Review new book bible: `/novel:bible-view`
2. Start first chapter: `/novel:chapter-start 1`
3. Check series progress: `/novel:standup`

## Error Handling

- Missing series bible: Cannot proceed
- Incomplete previous book: Warning with option to continue
- Continuity violations: Requires resolution
- Bible quality < 95: Iterative improvement