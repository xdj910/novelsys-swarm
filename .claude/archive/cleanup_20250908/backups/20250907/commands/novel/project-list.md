---
description: List all novel projects and status
---

# Project List Command

Display all novel projects with detailed status information.

## Execution Steps

### Step 1: Discover All Projects

Use Bash to find all projects:
```
ls -d .claude/data/projects/*/ 2>/dev/null || echo "No projects found"
```

For each project directory found, collect project name.

### Step 2: Analyze Each Project Status

For each project, execute Task:
```
Task(
    subagent_type="director",
    description="Analyze project status",
    prompt="""
    Analyze the current status of project: {project_name}

    READ these files to understand project state:
    1. .claude/data/projects/{project_name}/project.json (if exists)
    2. .claude/data/projects/{project_name}/book_{current_book}/bible.yaml (check if Bible created)
    3. .claude/data/projects/{project_name}/entity_dictionary.yaml (check if exists)
    4. Count chapters: .claude/data/projects/{project_name}/chapters/ch*/content.md
    5. Check quality scores: .claude/data/projects/{project_name}/chapters/ch*/quality_check.json

    Analyze and report:
    - Project name and type
    - Bible status (exists/complete/missing)
    - Total chapters planned vs completed
    - Average quality score (if available)
    - Last modification date
    - Current phase (setup/writing/revision/complete)
    - Any blocking issues

    WRITE status report to:
    .claude/data/projects/{project_name}/status_report.json

    Format:
    {
        "project_name": "name",
        "project_type": "series/standalone",
        "bible_status": "complete/partial/missing",
        "chapters": {
            "planned": 50,
            "completed": 12,
            "in_progress": 1,
            "quality_passed": 10
        },
        "average_quality": 92.5,
        "last_modified": "2024-01-01",
        "current_phase": "writing",
        "blocking_issues": [],
        "next_recommended_action": "Continue chapter 13"
    }
    """
)
```

### Step 3: Compile Project Summary

After analyzing all projects, create a consolidated view:

```
Read all .claude/data/projects/*/status_report.json files
Compile into a summary table
```

### Step 4: Display Project Status Table

Format output as:

```
NOVEL PROJECTS STATUS
=====================

Project Name          | Type       | Bible | Chapters    | Quality | Phase      | Last Updated
---------------------|------------|-------|-------------|---------|------------|-------------
Island Inn Mysteries | series     | [x]     | 12/50 (24%) | 92.5    | writing    | 2024-01-01
Mystery at Moonlight | standalone | [x]     | 5/20 (25%)  | 88.2    | revision   | 2024-01-02
[Project 3]          | ...        | ...   | ...         | ...     | ...        | ...

SUMMARY
-------
Total Projects: 3
Active Projects: 2 (Island Inn Mysteries, Mystery at Moonlight)
Completed Projects: 0
Projects Needing Attention: 1 (Mystery at Moonlight - quality below 90)

RECOMMENDED NEXT ACTIONS
------------------------
1. Island Inn Mysteries: Continue writing (/novel:next-chapter)
2. Mystery at Moonlight: Run quality fix on chapters 3-5 (/novel:smart-fix 3)
```

### Step 5: Identify Projects Needing Attention

Highlight projects with:
- No Bible created
- Low quality scores (< 90)
- Long time since last update (> 7 days)
- Blocking issues present

## Display Formatting

### Color Coding (if terminal supports)
- 🟢 Green: Healthy projects (quality > 90, recently updated)
- 🟡 Yellow: Needs attention (quality 85-90, or > 7 days old)
- 🔴 Red: Blocked or critical issues (quality < 85, missing Bible)

### Progress Indicators
- Use percentage for chapter completion
- Show quality trend ( ^  improving,  v  declining,  ->  stable)


## Error Handling

If no projects exist:
```
No projects found.

To create your first project, use:
/novel:project-new <project_name>
```

If project is corrupted:
```
Project "{name}" has corrupted data.
Recommended: Check .claude/data/projects/{name}/ for issues
```

## Quick Actions

After listing, suggest contextual commands:
- For project with no Bible: `/novel:bible-create`
- For project with low quality: `/novel:smart-fix [chapters]`
- For project ready to continue: `/novel:next-chapter`
- For completed project: `/novel:book-complete`

## Success Criteria

- All projects discovered and listed
- Accurate status for each project
- Clear visual presentation
- Actionable recommendations provided
- No false positives in issue detection

---
**Execute analysis for comprehensive project overview.**