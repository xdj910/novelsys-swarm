# Real-Time Update Implementation Plan for NOVELSYS-SWARM

## Current State Analysis

### Existing Update Mechanisms

1. **real-time-context-updater Agent**
   - Already integrated in chapter-start workflow (Steps 5, 7, 12)
   - Updates character development, world details, and plot progression
   - Saves to: `.claude/data/projects/{project}/book_{N}/context/*.json`

2. **entity-dictionary-manager Agent**
   - Creates dictionary from Bible
   - Updates from high-quality chapters (≥95 score)
   - Saves to: `.claude/data/projects/{project}/shared/entity_dictionary.yaml`

3. **context-sync Command**
   - Quality-gated learning (blocks if any chapter <90)
   - Requires 3+ eligible chapters
   - Updates entity dictionary and context files

### Current Gaps

1. **Chapter Metadata Updates** - Not automated
2. **Project Statistics** - Not aggregated in real-time
3. **Current Project Pointer** - No automatic switching
4. **Cross-file Dependencies** - Manual trigger only

## Implementation Strategy

### 1. Chapter Metadata Auto-Update Agent

**New Agent: `metadata-updater`**

```yaml
name: metadata-updater
description: Updates chapter metadata after content changes
```

**Responsibilities:**
- Calculate word_count, character_count, dialogue_lines
- Update last_modified timestamp
- Count estimated scenes
- Save to `meta.json`

**Integration Points:**
- Call after each draft save in chapter-start workflow
- Call after smart-fix modifications
- Call after chapter-continue updates

### 2. Project Statistics Aggregator Agent

**New Agent: `project-stats-aggregator`**

```yaml
name: project-stats-aggregator
description: Aggregates project-wide statistics in real-time
```

**Responsibilities:**
- Sum total_words from all chapters
- Count total_chapters
- Calculate quality_average
- Update last_activity timestamp
- Save to `project.json`

**Integration Points:**
- Call after chapter completion
- Call after quality scoring
- Call during context-sync

### 3. Enhanced Entity Dictionary Updates

**Modify `entity-dictionary-manager`:**

**Add Real-Time Mode:**
```yaml
update_modes:
  batch: "From multiple chapters during context-sync"
  real_time: "From single chapter immediately after scoring"
```

**New Workflow:**
1. After quality-scorer runs
2. If score ≥ 95:
   - Auto-trigger entity-dictionary-manager in real_time mode
   - Update dictionary with new variations
   - Mark chapter as "learned_from"

### 4. Current Project Pointer Manager

**New Agent: `project-context-manager`**

```yaml
name: project-context-manager
description: Manages current project context and switching
```

**Responsibilities:**
- Update current_project.json on project-switch
- Maintain project activity timestamps
- Handle project initialization
- Validate project exists before switch

### 5. Integrated Update Pipeline

**Create New Command: `update-pipeline`**

```yaml
description: Orchestrates all real-time updates after content changes
```

**Workflow:**
1. Detect content change type (new chapter, edit, fix)
2. Launch parallel update agents:
   - metadata-updater
   - project-stats-aggregator
   - entity-dictionary-manager (if quality ≥ 95)
   - real-time-context-updater
3. Verify all updates completed
4. Report update status

## Implementation Steps

### Phase 1: Create Core Update Agents (Priority 1)

1. **metadata-updater.md**
   - Read content.md
   - Calculate statistics
   - Update meta.json

2. **project-stats-aggregator.md**
   - Glob all chapter quality reports
   - Read all meta.json files
   - Aggregate statistics
   - Update project.json

### Phase 2: Enhance Existing Agents (Priority 2)

1. **entity-dictionary-manager.md**
   - Add real_time mode
   - Add auto-trigger logic
   - Track learning history

2. **real-time-context-updater.md**
   - Add metadata update trigger
   - Add project stats trigger
   - Improve error handling

### Phase 3: Create Integration Command (Priority 3)

1. **update-pipeline.md**
   - Detect trigger type
   - Orchestrate parallel updates
   - Handle failures gracefully
   - Report comprehensive status

### Phase 4: Modify Existing Commands (Priority 4)

1. **chapter-start.md**
   - Add metadata-updater after each draft
   - Add project-stats-aggregator after quality scoring
   - Add entity learning if score ≥ 95

2. **smart-fix.md**
   - Add metadata-updater after fixes
   - Trigger entity re-learning if needed

3. **project-switch.md**
   - Update current_project.json
   - Verify project exists
   - Load project context

## File Structure Updates

```
.claude/data/projects/{project}/
├── project.json                    # Auto-updated statistics
├── shared/
│   └── entity_dictionary.yaml      # Auto-updated from chapters
├── book_{N}/
│   ├── context/
│   │   ├── characters.json        # Auto-updated by real-time-context-updater
│   │   ├── plot.json              # Auto-updated by real-time-context-updater
│   │   └── world.json             # Auto-updated by real-time-context-updater
│   └── chapters/
│       └── ch{NNN}/
│           ├── content.md         # Source content
│           ├── meta.json          # Auto-updated metadata
│           └── quality_report.json # Triggers entity learning
└── .claude/data/context/
    └── current_project.json        # Auto-updated pointer
```

## Testing Strategy

1. **Unit Tests:**
   - Each agent independently
   - Verify file creation/update
   - Handle missing files gracefully

2. **Integration Tests:**
   - Full chapter generation with updates
   - Project switching with context
   - Entity learning from high-quality chapters

3. **Performance Tests:**
   - Parallel update efficiency
   - Large project handling
   - Multiple book management

## Success Metrics

1. **Automation Level:**
   - 0 manual update commands needed
   - All 5 core files auto-updated
   - Real-time consistency maintained

2. **Data Accuracy:**
   - Word counts within 1% accuracy
   - Entity dictionary 100% current
   - Project stats always synchronized

3. **Performance:**
   - Updates complete within 5 seconds
   - No blocking of main workflow
   - Parallel execution utilized

## Risk Mitigation

1. **File Locking:**
   - Implement retry logic
   - Use atomic writes
   - Queue updates if needed

2. **Data Corruption:**
   - Backup before update
   - Validate JSON structure
   - Rollback on failure

3. **Performance Impact:**
   - Batch small updates
   - Use parallel execution
   - Cache frequently accessed data

## Timeline

- **Week 1:** Create core update agents
- **Week 2:** Enhance existing agents
- **Week 3:** Create integration command
- **Week 4:** Modify existing commands and test

## Next Steps

1. Create metadata-updater agent
2. Create project-stats-aggregator agent
3. Enhance entity-dictionary-manager with real-time mode
4. Create update-pipeline command
5. Modify chapter-start to integrate updates
6. Test full pipeline with sample project