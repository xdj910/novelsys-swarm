---
description: Show detailed status of current project
---

# Project Status Report

Display comprehensive project status with progress analysis, quality metrics, and intelligent recommendations.

## Command Usage

- `/novel:status` - Show complete project status with bilingual output

## Implementation

This command uses the status-coordinator subagent to orchestrate comprehensive project status reporting with:

- **Data Collection**: Load project metadata, progress, and chapter information
- **Statistics Analysis**: Calculate progress metrics, quality scores, and temporal analysis  
- **Bilingual Reporting**: Generate formatted output with English/Chinese labels
- **Quality Integration**: Include quality metrics and consistency analysis
- **Smart Recommendations**: Provide context-aware next step suggestions
- **Error Handling**: Graceful handling of missing files or incomplete data

## Execution Steps

### Step 1: Project Context Analysis

Use the status-coordinator subagent to:
1. Load current project from `.claude/data/context/current_project.json`
2. Validate project exists and essential files are accessible
3. Extract project metadata and current book/chapter status
4. Identify data sources for comprehensive analysis

### Step 2: Comprehensive Status Generation

The coordinator will create a structured execution plan covering:

**Phase 1: Project Context Loading**
- Load current project configuration and metadata
- Validate data source availability
- Handle missing project scenarios with clear error messages

**Phase 2: Statistics Generation**
- Calculate progress metrics (chapters, word counts, completion percentages)
- Analyze quality scores and consistency metrics
- Compute temporal analysis (project age, activity patterns, estimates)
- Identify recent activity and chapter modifications

**Phase 3: Status Report Generation**
- Generate formatted bilingual status report
- Include visual progress indicators and quality metrics
- Provide intelligent recommendations based on project state
- Display contextual quick commands for next actions

### Step 3: Error Recovery

If no project set:
```
[ ] Error: No active project. Use /novel:project-new to create a new project.
```

If project files missing:
```
WARNING: Warning: Some project files missing, showing partial status
Missing: [list of missing files]
Suggestion: Run /novel:system-check for validation
```

## Expected Output

The status-report-generator agent will display:

1. **Project Overview** with bilingual headers and basic metadata
2. **Progress Analysis** with visual progress bars and completion metrics
3. **Quality Metrics** showing average scores and consistency indicators
4. **Recent Activity** highlighting latest chapters and modifications
5. **Bible Summary** with character, setting, and conflict overview
6. **Intelligent Recommendations** based on current project state
7. **Quick Commands** for contextual next actions

## Features

- **Bilingual Display**: English and Chinese labels throughout
- **Visual Progress**: Progress bars and formatted statistics
- **Quality Integration**: Quality scores and consistency analysis
- **Smart Recommendations**: Context-aware suggestions for next steps
- **Error Resilience**: Partial reporting when data is incomplete
- **Quick Commands**: One-click access to relevant operations

## Notes

- Status report provides comprehensive project health overview
- Bilingual formatting helps both English and Chinese users
- Intelligent recommendations guide optimal next actions
- Quality metrics integration provides actionable feedback

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

- Error handling ensures useful output even with missing data