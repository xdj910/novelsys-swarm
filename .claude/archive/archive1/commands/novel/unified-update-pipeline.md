---
description: Update all systems after quality approval
argument-hint: <chapter_number>
---

# Unified Update Pipeline

Updating all learning systems for chapter: **$ARGUMENTS**

## Description

This command orchestrates parallel updates to all system components after a chapter achieves the 95+ quality threshold. It ensures entity dictionary, project statistics, and context files all learn from high-quality content.

## Trigger Condition

- **ONLY** when quality_score >= 95
- Automatically called by chapter-start after quality validation
- Can be manually invoked for re-learning from existing chapters

## Execution

Delegating to unified update pipeline coordinator:

Use the unified-update-pipeline-coordinator subagent to orchestrate system updates with these instructions:

Execute parallel update pipeline for chapter: $ARGUMENTS

CRITICAL: All 6 updaters must run IN PARALLEL for performance.

Workflow:
1. Validate prerequisites
   - Verify quality score >= 95
   - Check chapter content exists
   - Get project configuration

2. Launch parallel updaters (ALL AT ONCE)
   - chapter-meta-updater (statistics)
   - entity-dictionary-updater (variations)
   - project-stats-updater (aggregation)
   - characters-context-updater (development)
   - plot-context-updater (progression)
   - world-context-updater (details)

3. Monitor completion
   - Track all 6 updaters
   - Handle any failures gracefully
   - Continue even with partial success

4. Generate summary
   - Report what was learned
   - Show statistics updates
   - Confirm learning complete

Expected time: 10-15 seconds (6x parallel speedup)
All updates are incremental and preserve history.

## Update Components

Each updater handles specific learning:
- **Metadata**: Chapter statistics and markers
- **Entities**: Character/location name variations
- **Statistics**: Project-wide aggregations
- **Characters**: Personality and relationship evolution
- **Plot**: Event progression and thread tracking
- **World**: Location and setting enrichment

## Success Indicators

- [x] All 6 updaters complete
- [x] Learning markers set in meta.json
- [x] Entity dictionary shows new variations
- [x] Context files updated incrementally
- [x] No data loss or corruption

## Performance

- **Sequential**: ~60 seconds (if run one by one)
- **Parallel**: ~10-15 seconds (all at once)
- **Speedup**: 6x performance improvement

## Next Steps

After successful update:
- Chapter is marked as "learned from"
- System knowledge is enriched

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

- Continue with next chapter or publication