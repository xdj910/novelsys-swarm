---
description: Generate new chapter with quality validation
argument-hint: <chapter_number>
---

# Chapter Generation

Generating chapter **$ARGUMENTS** with comprehensive quality validation.

## Description

This command orchestrates the complete chapter generation pipeline, including:

- Entity validation against dictionary
- Detailed outline generation
- Multi-specialist content creation
- Quality scoring and validation
- 95+ quality threshold enforcement

## Execution

**EXECUTE:** Delegating to chapter-start-coordinator:

Use the chapter-start-coordinator subagent to generate chapter $ARGUMENTS with the following requirements:

Orchestrate the complete generation pipeline for chapter $ARGUMENTS.

Ensure:
- 95+ quality score achieved
- Full Bible compliance  
- Entity consistency verified
- All outputs saved to correct paths

## Output

The coordinator manages all aspects of chapter generation including:
- 10-step optimized specialist pipeline orchestration (8 core + 1 conditional genre + 1 voice)
- Quality validation and enforcement (95+ required)
- File management and metadata updates
- Error handling and retry logic

All outputs are saved to:
`.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/`

## Next Steps

After successful generation:
- **If quality >=95**: 
  - Continue: `/novel:next-chapter` or `/novel:chapter-start {N+1}`
  - Update context: `/novel:context-sync` to learn from high-quality chapter
- **If quality 90-94**:
  - Fix issues: `/novel:smart-fix {N}` to improve quality
  - Then continue with next chapter
- **If quality <90**:
  - Major revision needed - review quality_report.json
  - Consider regenerating chapter

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/outline.json`
  - `.claude/data/projects/{project}/book_{N}/bible.yaml`
  - `.claude/data/context/current_project.json`

- **Writes to**:
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/content.md`
  - `.claude/data/projects/{project}/book_{N}/chapters/ch{NNN}/meta.json`

- **Check progress**: `/novel:status` for overall statistics