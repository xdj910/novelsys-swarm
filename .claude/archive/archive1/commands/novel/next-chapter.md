---
description: Write the next chapter in sequence
---

# Next Chapter Command

Automatically write the next chapter in your current project.

## Purpose

Continue writing without tracking chapter numbers. The system automatically:
- Finds the last completed chapter
- Calculates the next number
- Ensures narrative continuity
- Maintains quality standards

## Execution

Delegating to next-chapter-coordinator:

Use the next-chapter-coordinator subagent to generate the next sequential chapter with these instructions:

Determine the next chapter number and orchestrate its generation.

Ensure:
- Correct sequential numbering
- Narrative continuity from previous chapter
- 95+ quality score achievement
- Proper progress tracking

## Output

The coordinator handles:
- Automatic chapter number detection
- Continuity validation
- Generation orchestration via chapter-start-coordinator
- Progress tracking and book completion detection

All outputs are saved to the appropriate chapter directory.

## Next Steps

After successful generation:
- Review the generated chapter
- Continue with another: `/novel:next-chapter`

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/outline.json`
  - `.claude/data/projects/{project}/book_{N}/bible.yaml`
  - `.claude/data/context/current_project.json`

- **Writes to**:
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/content.md`
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/meta.json`

- Or use specific number: `/novel:chapter-start {N}`