---
description: Synchronize context and update entity dictionary
argument-hint: [section] e.g., "characters" or "all"
---

# Context Synchronization Command (Enhanced v2.0)

Synchronize context with **quality-gated learning** from high-scoring chapters: **$ARGUMENTS** (optional: specific context area)

## 🎯 Core Enhancement: Quality-Gated Learning

### Learning Triggers
```yaml
automatic_triggers:
  
blocking_conditions:
```

## 📚 Entity Dictionary Integration

### Pre-Sync Dictionary Check
```bash
# Get current project
# Read current project using Read tool: .claude/data/context/current_project.json
# Extract the 'project' field from the JSON

# Check entity dictionary status
echo "📚 Checking Entity Dictionary status..."
- Use Read tool: `.claude/data/projects/{current_project}/shared/entity_dictionary.yaml`
- If exists, display entity count from metadata
- If not exists, create using entity-dictionary-creator subagent
```

## 🔍 Enhanced Sync Process

### Phase 0: Quality Validation (NEW)

**Check if we should proceed with sync and learning:**

1. **Ensure directories exist:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{current_project}/quality-reports`
   - Use Bash tool: `mkdir -p .claude/data/projects/{current_project}/learning_reports`
   
2. **Get all chapter quality scores:**
   - Use Glob tool: `.claude/data/projects/{current_project}/quality-reports/ch*_individual.json`
   - Create lists for eligible and blocked chapters

2. **Evaluate each quality report:**
   For each report found:
   - Use Read tool on report path
   - Parse JSON to extract:
     * Chapter number
     * Overall score
     * Bible compliance percentage
     * Critical issue count
   
3. **Categorize chapters:**
   - **Eligible (for learning):**
     * Score >= 95
     * Bible compliance = 100%
     * Critical issues = 0
     * Add to eligible list with score and path
   
   - **Blocked (low quality):**
     * Score < 90
     * Add to blocked list with reason

4. **Make sync decision:**
   - **If any chapters blocked (score < 90):**
     * Display: "[ ] Error: Sync blocked - {count} chapters below quality threshold"
     * List each blocked chapter with reason
     * Stop sync process
   
   - **If fewer than 3 eligible chapters:**
     * Display: "WARNING:️ Warning: Only {count} eligible chapters (need 3+)"
     * Stop sync process
   
   - **If 3+ eligible chapters:**
     * Display: "[x] {count} chapters eligible for learning"
     * Proceed with sync using eligible chapters

### Phase 1: Context Audit (Enhanced)

**Audit context with entity variation awareness:**
    
    # Original audit tasks
    timestamp_issues = scan_timestamp_inconsistencies()
1. **Identify existing conflicts:**
   - Check for timeline inconsistencies
   - Find character state conflicts
   - Detect world rule violations

2. **Audit entity variations:**
   - Use Glob tool: `.claude/data/projects/{current_project}/chapters/*/content.md`
   - For each chapter found:
     * Use Read tool on chapter file
     * Check all entity references
     * Compare against entity dictionary
     * Find unapproved variations
   
3. **Check entity consistency:**
   For each entity type (locations, characters):
   - Get canonical name from dictionary
   - Search for non-standard references
   - Flag potential issues
   - Record for review

4. **Return audit results:**
   - Timestamp issues found
   - Conflicts identified
   - Entity variation problems

### Phase 2: Pattern Learning (NEW)

**Extract patterns from high-quality chapters:**

1. **Initialize learning report:**
   - Create report structure with:
     * Current timestamp
     * Chapters analyzed list
     * Patterns learned list
     * Entity updates list

2. **Process each eligible chapter:**
   For each chapter in eligible list:
   - Check if already learned from
   - Skip if already processed
   - Use Read tool: `.claude/data/projects/{current_project}/chapters/ch{NNN}/content.md`
   
3. **Learn entity variations:**
   - Analyze chapter content
   - Identify new entity references
   - Evaluate variation quality
   - Determine confidence score
   
4. **Process learning results:**
   - Add chapter to analyzed list
   - Record patterns found
   - Display: "📖 Chapter {num}: {count} patterns found"
   - If auto-accepted: Display "[x] Auto-accepted: {count}"
   - If pending: Display "🔍 Pending review: {count}"

5. **Save learning report:**
   - Generate timestamp for filename  
   - Use Write tool: `.claude/data/projects/{current_project}/learning_reports/sync_{timestamp}.json`
   - Save complete learning report as JSON

### Phase 2.5: Book Outline Progress Update (NEW)

**Update book outline tracking after chapters complete:**

1. **Read book outline if exists:**
   - Use Read tool: `.claude/data/projects/{current_project}/shared/book_outline.yaml`
   - If not exists, skip this phase
   - Extract chapter completion tracking

2. **Mark completed chapters:**
   For each eligible chapter:
   - Mark chapter as "completed" in outline
   - Record actual word count vs target
   - Note any deviations from planned beats

3. **Update progression tracking:**
   - Plot milestones reached
   - Tension peaks achieved
   - Clue discoveries completed
   - Character arc checkpoints passed

4. **Save outline progress:**
   - Use Write tool: `.claude/data/projects/{current_project}/shared/book_outline_progress.json`
   ```json
   {
     "chapters_completed": [1, 2, 3, 4, 5],
     "milestones_reached": ["inciting_incident", "first_clue"],
     "deviations_noted": [],
     "last_sync": "timestamp"
   }
   ```

### Phase 3: Character Development Sync (Enhanced)

**Track character growth and relationship evolution:**

1. **Initialize character tracking:**
   - Create empty character states dictionary
   - Prepare to track growth and relationships

2. **Read current character states:**
   - Use Read tool: `.claude/data/projects/{current_project}/context/characters.json`
   - If file doesn't exist, create empty structure
   - Extract development_tracking from characters context

3. **Process chapters chronologically:**
   - Sort eligible chapters by number
   - For each chapter in order:
     * Use Read tool: `.claude/data/projects/{current_project}/chapters/ch{NNN}/meta.json`
     * Extract character development data

4. **Track character developments:**
   For each character in chapter metadata:
   - Initialize character state if new:
     * Progression list
     * Relationships dictionary
     * Speech patterns list
   - Add development to progression
   - Update relationship dynamics
   - Record speech pattern evolution

5. **Merge and save states:**
   - Merge new states with existing characters.json
   - Prioritize chronological order
   - Use Write tool: `.claude/data/projects/{current_project}/context/characters.json`
   - Save merged character context with updated development_tracking

### Phase 4: World Context Evolution (Enhanced)

**Track world details as they evolve:**

1. **Initialize world context structure:**
   - Locations dictionary
   - Cultural details dictionary
   - Temporal markers list

2. **Process chapters chronologically:**
   For each eligible chapter (sorted by number):
   - Use Read tool: `.claude/data/projects/{current_project}/chapters/ch{NNN}/content.md`
   - Extract world-building elements

3. **Extract world details from content:**
   - Location descriptions and details
   - Cultural references and customs
   - Time markers and progression

4. **Update world context:**
   For each location found:
   - Create entry if new location
   - Add details with chapter reference
   - Track evolution across chapters
                'chapter': chapter_num,
                'details': details
            })
        
        world_context['cultural_details'].update(cultural)
        world_context['temporal_markers'].extend(temporal)
    
    # Save world context  
    Write(".claude/data/projects/{current_project}/context/world.json", json.dumps(world_context, indent=2))
    
    return world_context
```

### Phase 5: Entity Dictionary Learning
```bash
# Update Entity Dictionary from high-quality chapters
echo "📚 Updating Entity Dictionary from high-quality chapters..."

# Get quality reports and update dictionary
for report_file in .claude/data/projects/$current_project/quality-reports/ch*_individual.json; do
    if [ -f "$report_file" ]; then
        # Extract chapter number and score
        chapter_num=$(basename "$report_file" | sed 's/ch\([0-9]*\)_individual.json/\1/')
        # Read the report file and extract overall_score field (default to 0 if not found)
        
        # Update dictionary if score >= 95
        # Check if quality score is 95 or higher
        # If score >= 95:
            Display: "   Learning from chapter $chapter_num (score: $score)..."
            - Use Task tool with subagent_type: "entity-dictionary-updater"
            - Description: "Update dictionary from chapter"
            - Prompt: "Update entity dictionary for project '{current_project}' from chapter {chapter_num} (quality score: {score}). Read the chapter from .claude/data/projects/{current_project}/chapters/ch{NNN}/content.md, identify entity variations, and update the dictionary at .claude/data/projects/{current_project}/shared/entity_dictionary.yaml"
    fi
done

### Phase 6: Update Commands Integration

**Record sync completion and next triggers:**

1. **Create sync metadata:**
   - Record current timestamp
   - List chapters that were synced
   - Mark dictionary as updated
   - Mark character states as updated
   - Mark world context as updated

2. **Set next sync triggers:**
   - Chapter count: After 5 more chapters
   - Quality threshold: Maintain 95+ requirement
   - Manual trigger: Always available

3. **Save metadata:**
   - Use Write tool: `.claude/data/projects/{current_project}/sync_metadata.json`
   - Save complete sync metadata as JSON
   - Return metadata for confirmation

## 📊 Enhanced Output Reports

### Sync Summary Report
```markdown
## Context Sync Report

### 📖 Book Outline Progress
- Chapters completed: 5/30
- Plot milestones reached: 2/8
- On track with outline: Yes
- Deviations noted: 0

### 📚 Entity Dictionary Updates
- Patterns learned: 12
- Auto-accepted variations: 8
- Pending review: 4
- Chapters analyzed: [1, 2, 3, 5, 7]

### 👥 Character Evolution
- Sarah Mitchell: Growing comfort with island life
- Carmen Rodriguez: Deepening friendship with Sarah
- Relationship progression tracked

### 🌍 World Context
- New location details: 5 additions
- Cultural insights: 3 new patterns
- Timeline consistency: Verified

### [x] Quality Validation
- All synced chapters: 95+ score
- Bible compliance: 100%
- No critical issues

### 💡 Recommendations
- Review 4 pending entity variations
- Consider character voice adjustments
- Next sync after 5 more quality chapters
```

## 🎮 Manual Controls

### Review Pending Patterns

**Show pending patterns for review:**

1. **Get pending reviews:**
   - Read entity dictionary pending list
   - Sort by confidence score

2. **Display each pattern:**
   For each pending pattern:
   - Show: "{index}. '{pattern}' for {entity}"
   - Show: "Confidence: {score}"
   - Show: "From chapter: {number}"

3. **Approve or reject patterns:**
   - To approve: Use pattern index from list
   - To reject: Provide pattern index and reason
   - Updates entity dictionary accordingly

## 🚀 Usage Examples

### Basic Quality-Gated Sync
```bash
/novel:context-sync
# Automatically checks quality and syncs if eligible
```

### Force Sync Specific Area
```bash
/novel:context-sync characters
# Sync only character development
```

### Review Learning Status
```bash
/novel:context-sync status
# Shows learning status without syncing
```

## ℹ️ Important Notes

1. **Quality Gate is Mandatory**: Sync will not proceed with low-quality chapters
2. **Entity Dictionary Auto-Updates**: High-confidence patterns are automatically added
3. **Manual Review Required**: Some patterns need human confirmation
4. **Chronological Processing**: Ensures proper progression tracking
5. **Bible Authority**: Bible remains source of truth for conflicts


---
**Context Sync v2.0**
*Intelligent synchronization that learns from excellence*