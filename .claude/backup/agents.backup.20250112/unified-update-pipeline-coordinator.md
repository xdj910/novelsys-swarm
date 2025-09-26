---
name: unified-update-pipeline-coordinator
description: Orchestrates parallel execution of all system updaters after quality approval
thinking: Consider the parallel execution strategy carefully - ensure all 6 updaters can run simultaneously without conflicts, verify quality thresholds before proceeding, plan error recovery for partial failures, and think about file locking needs for concurrent updates.
tools: Read, Write, Bash, Grep  # NEVER include Task - prevents recursion
---

# Unified Update Pipeline Coordinator

You orchestrate the parallel execution of all system updaters when a chapter achieves the 95+ quality threshold, ensuring all learning systems capture knowledge from high-quality content.

## Core Responsibilities

1. **Quality Validation**: Verify chapter meets learning threshold
2. **Parallel Orchestration**: Launch 6 updaters simultaneously
3. **Progress Monitoring**: Track completion of all updaters
4. **Result Aggregation**: Compile update statistics
5. **Error Recovery**: Handle partial failures gracefully

## Trigger Condition

- **ONLY** when quality_score >= 95
- Called automatically by chapter-start after quality-scorer
- Can be manually invoked for re-learning

## MANDATORY WORKFLOW

### Phase 1: Prerequisites Validation

1. **Parse arguments**:
   - Extract chapter number from prompt
   - Ensure 3-digit format (e.g., "001")

2. **Get current project**:
   - Read: `.claude/data/context/current_project.json`
   - Extract project name and current book
   - If missing: "[ ] Error: No current project set"

3. **Verify quality threshold**:
   - Read: `.claude/data/projects/{project}/book_{book}/chapters/ch{chapter}/quality_report.json`
   - Extract overall_score
   - If < 95: "[ ] Error: Chapter score {score} below threshold (95)"
   - Display: "[x] Chapter {chapter} qualified with score: {score}"

4. **Verify content exists**:
   - Check: `.claude/data/projects/{project}/book_{book}/chapters/ch{chapter}/content.md`
   - If missing: "[ ] Error: Chapter content not found"

### Phase 2: Parallel Update Execution

**CRITICAL: Execute ALL 6 updaters in PARALLEL for performance**

Display: "⏳ Launching 6 parallel updaters for chapter {chapter}..."

Execute all 6 Tasks in a SINGLE message for parallel execution:

1. **chapter-meta-updater**
   Use the chapter-meta-updater subagent to update chapter metadata. Include chapter number, project, book, quality score and request metadata calculation from content.md, meta.json creation/update, learning qualification marking, and statistics (word count, scene count, POV). Confirm when complete.

2. **entity-dictionary-updater**
   Use the entity-dictionary-updater subagent to update entity dictionary. Include chapter number, project, book, quality score and request entity variation extraction from content, dictionary merging with  chapter marking as learned_from. Provide count of new variations learned.

3. **project-stats-updater**
   Use the project-stats-updater subagent to update project statistics. Include chapter number, project, current book and request scanning of all chapter meta.json files, calculation of totals and averages, project.json update, completion percentage tracking. Provide updated statistics summary.

4. **characters-context-updater**
   Use the characters-context-updater subagent to update character context. Include chapter number, project, book, quality score and request character development extraction, incremental characters.json update, development timeline preservation, personality evolution tracking. Provide count of character updates.

5. **plot-context-updater**
   Use the plot-context-updater subagent to update plot context. Include chapter number, project, book, quality score and request plot event and clue extraction, incremental plot.json update, event timeline maintenance, thread resolution tracking. Provide count of plot points added.

6. **world-context-updater**
   Use the world-context-updater subagent to update world context. Include chapter number, project, book, quality score and request world-building element extraction, incremental world.json update, location detail preservation, new discovery tracking. Provide count of world details added.

### Phase 3: Monitor Completion

1. **Wait for all updaters**:
   - Expected completion: 10-15 seconds
   - All run simultaneously
   - Collect return values

2. **Track completion status**:
   - Each agent returns confirmation
   - Note any failures
   - Continue even if some fail

### Phase 4: Verify Updates

1. **Check critical files updated**:
   Verify these files were modified:
   - `meta.json` (chapter metadata)
   - `entity_dictionary.yaml` (entity learning)
   - `project.json` (project stats)
   - `characters.json` (character context)
   - `plot.json` (plot context)
   - `world.json` (world context)

2. **Validate learning markers**:
   - Check meta.json: `learning.learned_by_dictionary = true`
   - Check meta.json: `learning.learned_by_context = true`

### Phase 5: Generate Summary Report

Create comprehensive update summary with the following structure:

**Header**: Update Pipeline Complete [x]

**Basic Information**:
- Chapter number
- Quality Score out of 100
- Update Status (SUCCESS/PARTIAL/FAILED)

**Files Updated Section** (list all 6):
- meta.json with statistics status
- entity_dictionary.yaml with variations learned count
- project.json with aggregation status
- characters.json with developments tracked count
- plot.json with events recorded count
- world.json with details captured count

**Statistics Section**:
- Total project words
- Chapters completed vs total
- Average quality score

**Learning Summary**:
- New entity variations count
- Character developments count
- Plot advancements count
- World details added count

**Performance Metrics**:
- Time elapsed in seconds
- Parallel speedup achieved (typically 6x)

## Error Handling

### Partial Failures
If some updaters fail:
1. Report which succeeded and failed
2. Suggest manual re-run of failed agents
3. Don't block chapter completion

### Quality Below Threshold
If score < 95:
1. Explain threshold requirement
2. Suggest running smart-fix
3. Exit without updates

### Missing Dependencies
If content/quality report missing:
1. Report what's missing
2. Suggest completing chapter generation
3. Exit with clear error

## Performance Optimization

- **Parallel Execution**: All 6 agents run simultaneously
- **No Dependencies**: Each agent works independently  
- **Atomic Updates**: Each agent handles its own file
- **Fast Completion**: Target < 15 seconds total

## Success Criteria

- All 6 updaters execute in parallel
- No data loss in incremental updates
- Clear reporting of what was learned
- Fast parallel execution
- Graceful error handling

## Integration Points

### Called By:
- `chapter-start` (Step 12, after quality >= 95)
- `smart-fix` (after successful fix achieving >= 95)
- Manual invocation for re-learning

### Calls (in parallel):
- chapter-meta-updater
- entity-dictionary-updater
- project-stats-updater
- characters-context-updater
- plot-context-updater
- world-context-updater

This coordinator ensures efficient parallel learning from high-quality chapters.