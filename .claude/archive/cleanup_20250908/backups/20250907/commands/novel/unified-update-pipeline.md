---
description: Update all systems after quality approval
argument-hint: <chapter_number>
---

# Unified Update Pipeline Command

Coordinates all file updates after a chapter achieves quality score >= 95.

## Purpose

This command orchestrates parallel execution of all update agents to ensure:
- Chapter metadata is recorded
- Entity dictionary learns from high-quality content  
- Project statistics are aggregated
- Context files capture developments
- All updates happen atomically

## Trigger Condition

- **ONLY** when quality_score >= 95
- Called automatically by chapter-start after quality-scorer
- Can be manually invoked for re-learning

## MANDATORY EXECUTION SEQUENCE

### Step 1: Validate Prerequisites

1. **Get current project:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - Extract project name and current book
   - If missing, Display: "[ ] Error: No current project set"

2. **Parse chapter argument:**
   - Format: `$ARGUMENTS` or from prompt
   - Ensure 3-digit format (e.g., "001")

3. **Verify quality threshold:**
   - Use Read tool: `.claude/data/projects/{project}/book_{book}/chapters/ch{chapter}/quality_report.json`
   - Extract overall_score
   - If < 95, Display: "[ ] Error: Chapter score {score} below threshold (95)"
   - Display: "[x] Chapter {chapter} qualified with score: {score}"

4. **Verify content exists:**
   - Use Read tool: `.claude/data/projects/{project}/book_{book}/chapters/ch{chapter}/content.md`
   - If missing, Display: "[ ] Error: Chapter content not found"
   - Display: "[x] Chapter content verified"

### Step 2: Launch Parallel Update Pipeline

**CRITICAL: Execute ALL 6 updaters in PARALLEL**

When you reach this step, you MUST:
1. Display: "⏳ Launching 6 parallel updaters..."
2. Use Task tool 6 times in a SINGLE message
3. Each Task call must use a different updater agent

**The 6 updater agents to launch (ALL in parallel):**

1. **chapter-meta-updater**: Update metadata for chapter {chapter}
   - Description: "Update chapter metadata"
   - Instructions: "Update metadata for chapter {chapter}, Project: {project}, Book: {book}, Quality score: {score}
     Required actions: 1. Calculate statistics from content.md, 2. Create/update meta.json, 3. Mark as qualified for learning"

2. **entity-dictionary-updater**: Learn from high-quality chapter {chapter}
   - Description: "Update entity dictionary"  
   - Instructions: "Learn from high-quality chapter {chapter}, Project: {project}, Book: {book}, Quality score: {score}
     Required actions: 1. Extract entity variations from content, 2. Merge with existing dictionary, 3. Mark chapter as learned_from"

3. **project-stats-updater**: Aggregate project statistics after chapter {chapter}
   - Description: "Update project statistics"
   - Instructions: "Aggregate project statistics after chapter {chapter}, Project: {project}, Current book: {book}
     Required actions: 1. Scan all chapter meta.json files, 2. Calculate totals and averages, 3. Update project.json"

4. **characters-context-updater**: Track character development from chapter {chapter}
   - Description: "Update character context"
   - Instructions: "Track character development from chapter {chapter}, Project: {project}, Book: {book}, Quality score: {score}
     Required actions: 1. Extract character developments, 2. Update characters.json incrementally, 3. Preserve development timeline"

5. **plot-context-updater**: Track plot progression from chapter {chapter}
   - Description: "Update plot context"
   - Instructions: "Track plot progression from chapter {chapter}, Project: {project}, Book: {book}, Quality score: {score}
     Required actions: 1. Extract plot events and clues, 2. Update plot.json incrementally, 3. Maintain event timeline"

6. **world-context-updater**: Track world details from chapter {chapter}
   - Description: "Update world context"
   - Instructions: "Track world details from chapter {chapter}, Project: {project}, Book: {book}, Quality score: {score}
     Required actions: 1. Extract world-building elements, 2. Update world.json incrementally, 3. Preserve location details"

**IMPORTANT EXECUTION NOTES:**
- You MUST launch ALL 6 agents in ONE message with 6 Task tool calls
- Do NOT skip any agents - all 6 are required
- Pass the project, book, chapter, and quality score to each agent
- Each agent operates independently and in parallel

### Step 3: Monitor Completion

1. **Wait for all agents to complete:**
   - Display: "⏳ Running 6 parallel updaters..."
   - Expected completion: ~10-15 seconds
   - All agents run simultaneously

2. **Track completion status:**
   - Each agent returns confirmation
   - Collect all confirmations
   - Note any failures

### Step 4: Verify Updates

1. **Check critical files updated:**
   ```bash
   # Verify key files exist and are recent
   - meta.json (must exist)
   - entity_dictionary.yaml (must be updated)
   - project.json (must reflect new totals)
   - characters.json (must have chapter in learned list)
   - plot.json (must have chapter in learned list)
   - world.json (must have chapter in learned list)
   ```

2. **Validate learning markers:**
   - Use Read tool: `meta.json`
   - Confirm `learning.learned_by_dictionary = true`
   - Confirm `learning.learned_by_context = true`

### Step 5: Generate Summary Report

Create comprehensive update summary:

```markdown
## Update Pipeline Complete [x]

**Chapter**: {chapter}
**Quality Score**: {score}/100
**Update Status**: SUCCESS

### Files Updated (6):
1. [x] meta.json - Statistics recorded
2. [x] entity_dictionary.yaml - {N} variations learned
3. [x] project.json - Totals aggregated
4. [x] characters.json - {N} developments tracked
5. [x] plot.json - {N} events recorded
6. [x] world.json - {N} details captured

### Statistics:
- Total project words: {total_words}
- Chapters completed: {completed}/{total}
- Average quality: {avg_quality}

### Learning Summary:
- New entity variations: {entity_count}
- Character developments: {character_count}
- Plot advancements: {plot_count}
- World details added: {world_count}

**Time elapsed**: {seconds}s
```

## Error Handling

### Partial Failures

If some agents fail:
1. Report which succeeded and which failed
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

## Manual Invocation

Can be manually called to re-learn from a chapter:

```bash
/novel:unified-update-pipeline 003
```

This allows:
- Re-learning after manual edits
- Fixing missed updates
- Testing the pipeline

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

### Not Called:
- current-project-updater (only for project switching)

## Performance Considerations

1. **Parallel Execution**: All 6 agents run simultaneously
2. **No Dependencies**: Each agent works independently
3. **Atomic Updates**: Each agent handles its own file
4. **Fast Completion**: Target < 15 seconds total

## Success Criteria

- All 6 core files updated successfully
- No data loss in incremental updates
- Clear reporting of what was learned
- Fast parallel execution
- Graceful error handling

## Important Notes

- **95+ Only**: Never run for lower quality chapters
- **Parallel Always**: Must launch all agents in one message
- **Incremental Safety**: Context agents must preserve history
- **Learning Tracking**: Mark all chapters as learned_from
- **No Rollback**: Updates are permanent once written