---
description: Switch to different novel project
argument-hint: <project_name>
---

# Project Switch Command

Switch the active novel project to: **$ARGUMENTS**

## Pre-Validation

### Step 1: Verify Target Project Exists

Check if the project exists:
```
if [ -d ".claude/data/projects/$ARGUMENTS" ]; then
    echo "Project '$ARGUMENTS' found"
else
    echo "ERROR: Project '$ARGUMENTS' does not exist"
    echo "Available projects:"
    ls -d .claude/data/projects/*/ | xargs -n1 basename
    exit 1
fi
```

### Step 2: Verify Project Health

**CRITICAL**: Validate target project has required files:

1. **Check project.json:**
   - Use Read tool: `.claude/data/projects/$ARGUMENTS/project.json`
   - If missing, STOP with error: "Cannot switch - Target project '$ARGUMENTS' missing project.json"
   - Verify JSON is valid and has required fields

2. **Warn about missing Bible:**
   - Use Read tool: `.claude/data/projects/$ARGUMENTS/book_{current_book}/bible.yaml`
   - If missing, Display: "WARNING:️ Warning: Target project '**$ARGUMENTS**' missing Bible - create one with /novel:bible-create"
   - This is a warning, not a blocker

3. **Check series architecture consistency:**
   - If target project has series_bible.yaml, validate it exists
   - If project type is "series", ensure proper book structure

## Switching Process

### Step 3: Save Current Project Context

Before switching, save the current project's state:

Execute Task:
```
Task(
    subagent_type="director",
    description="Save current project context",
    prompt="""
    Save the context of the currently active project before switching.

    DETERMINE current project by reading:
    - .claude/data/context/current_project.json

    If a current project exists:

    READ and save:
    - Current chapter being worked on
    - Any unsaved progress markers
    - Recent quality scores
    - Active issues or todos

    WRITE context snapshot to:
    .claude/data/projects/{current_project}/context_snapshot.json

    Include:
    {
        "last_active": "timestamp",
        "last_chapter_worked": "ch013",
        "pending_tasks": [],
        "quality_status": "summary",
        "switch_reason": "user requested switch to $ARGUMENTS"
    }
    """
)
```

### Step 4: Update Active Project Pointer

Update the system to point to new project using dedicated updater:

```
Task(
    subagent_type="current-project-updater",
    description="Switch to project $ARGUMENTS",
    prompt="""
    Switch current project to: $ARGUMENTS
    
    Required actions:
    1. Verify project '$ARGUMENTS' exists
    2. Check for essential project files
    3. Update current_project.json with new pointer
    4. Record switch timestamp
    5. Update last_activity in target project.json
    
    Return confirmation with project stats.
    """
)
```

### Step 5: Load New Project Context

Execute Task:
```
Task(
    subagent_type="director",
    description="Load new project context",
    prompt="""
    Load the context for project: $ARGUMENTS

    READ these files:
    1. .claude/data/projects/$ARGUMENTS/project.json
    2. .claude/data/projects/$ARGUMENTS/bible.yaml
    3. .claude/data/projects/$ARGUMENTS/entity_dictionary.yaml
    4. .claude/data/projects/$ARGUMENTS/context_snapshot.json (if exists)
    5. Count existing chapters in /chapters/
    6. Check latest quality scores

    Analyze and determine:
    - Project type and genre
    - Current progress (chapters completed)
    - Last activity timestamp
    - Next recommended action
    - Any pending issues from last session

    WRITE project activation report to:
    .claude/data/context/active_project_status.json

    Format:
    {
        "project_name": "$ARGUMENTS",
        "activated_at": "timestamp",
        "project_type": "type",
        "bible_status": "complete/partial/missing",
        "progress": {
            "chapters_completed": 12,
            "chapters_planned": 50,
            "last_chapter": "ch012",
            "next_chapter": "ch013"
        },
        "quality_summary": {
            "average_score": 92.5,
            "chapters_needing_fix": []
        },
        "recommended_next_action": "Continue chapter 13",
        "restored_context": {
            "from_previous_session": true/false,
            "pending_tasks": []
        }
    }

    Also UPDATE the main context files:
    - .claude/data/context/entity_context.md with this project's entities
    - .claude/data/context/chapter_summaries.md with this project's chapter summaries
    - .claude/data/context/active_threads.md with this project's plot threads
    """
)
```

### Step 6: Display Switch Confirmation

After successful switch, display:

```
PROJECT SWITCHED SUCCESSFULLY
============================

Previous Project: [old_project_name]
- Context saved at: [timestamp]

Active Project: $ARGUMENTS
- Type: [series/standalone]
- Genre: [genre]
- Progress: 12/50 chapters (24%)
- Average Quality: 92.5
- Last Activity: [date]

CURRENT STATUS
--------------
[x] Bible: Complete
[x] Entity Dictionary: 45 entries
[x] Chapters Written: 12
WARNING: Chapters Needing Review: Ch007 (score: 87)

RECOMMENDED NEXT ACTIONS
------------------------
1. Continue writing chapter 13: /novel:next-chapter
2. Fix quality issues in Ch007: /novel:smart-fix 7
3. Review overall progress: /novel:status

PROJECT CONTEXT RESTORED
------------------------
[[x]] Character states from Ch012 loaded
[[x]] Active plot threads restored
[[x]] Writing style parameters set
[[x]] Genre conventions loaded
```

## Context Synchronization

### Step 7: Sync Agent Memory

Ensure all agents are aware of the project switch:

```
Update these context files that agents read:
1. .claude/data/context/current_project.json  ->  {"current_project": "$ARGUMENTS"}
2. .claude/data/context/entity_context.md  ->  Project's entities
3. .claude/data/context/active_threads.md  ->  Project's threads
4. .claude/data/context/writing_style.md  ->  Project's style guide
5. .claude/data/context/quality_standards.md  ->  Project's standards
```

- **project-stats-updater.sh**: Updates statistics
- **auto-entity-sync.sh**: Syncs entity context for new project

## Error Handling

### Project Not Found
```
ERROR: Project '$ARGUMENTS' does not exist.

Available projects:
- Island_Inn_Mysteries
- Mystery_at_Moonlight
- [other_projects]

Usage: /novel:project-switch <project_name>
```

### No Bible Found
```
WARNING: Project '$ARGUMENTS' has no Bible created.

You should create a Bible first:
/novel:bible-create

Or continue without Bible (not recommended):
/novel:chapter-start 1
```

### Corrupted Project
```
ERROR: Project '$ARGUMENTS' appears corrupted.

Missing required files:
- project.json

Recommended actions:
1. Check .claude/data/projects/$ARGUMENTS/
2. Restore from backup if available
3. Or create new project: /novel:project-new $ARGUMENTS
```

## Success Criteria

- Current project context properly saved
- New project successfully loaded
- All context files updated
- Agents aware of project switch
- User informed of project status
- Recommendations provided

## Quick Switch Feature

For frequently switched projects, maintain a recent list:
```
Recent Projects:
1. Island_Inn_Mysteries (last: today)
2. Mystery_at_Moonlight (last: yesterday)
3. [project_3] (last: 3 days ago)

Quick switch: /novel:project-switch 1
```

---
**Execute switch carefully to maintain context integrity.**