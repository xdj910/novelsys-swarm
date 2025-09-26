---
description: List all novel projects and status
---

# Project List Command

Display all novel projects with detailed status information and management options.

## Command Usage

- `/novel:project-list` - Show all projects with comprehensive status details

## Implementation

This command uses project analysis capabilities to provide comprehensive project listing with:

- **Project Discovery**: Scan and identify all available novel projects
- **Status Analysis**: Analyze progress, quality metrics, and current state for each project
- **Management Options**: Provide project switching and management commands
- **Summary Statistics**: Display system-wide project statistics and insights
- **Active Project**: Highlight current active project with detailed status

## Execution Steps

### Step 1: Project Discovery and Analysis

Discover all novel projects by:
1. Scanning `.claude/data/projects/` directory for project folders
2. Loading project metadata and progress information
3. Analyzing current status and completion metrics for each project
4. Identifying active project from current context

### Step 2: Status Analysis and Display

Generate comprehensive project listing showing:

**Project Information Display**
- Project names with creation dates and last activity
- Progress metrics (chapters completed, word counts, quality scores)
- Current status (active, in-progress, completed, archived)
- Next recommended actions for each project

**Active Project Highlighting**
- Clear identification of currently active project
- Detailed status for active project including recent activity
- Quick action suggestions for current project

**Management Options**
- Project switching commands for easy navigation
- Creation options for new projects
- Archive and cleanup suggestions for completed projects

### Step 3: System Summary

Provide system-wide insights including:
- Total projects and overall progress statistics
- System health and optimization recommendations
- Quick commands for common project operations

## Expected Output

Display format includes:

1. **Active Project Status** - Current project with detailed metrics
2. **Available Projects** - List of all projects with status summaries  
3. **System Statistics** - Overall system health and usage metrics
4. **Quick Commands** - Project switching and management options

## Features

- **Comprehensive Listing**: All projects with detailed status information
- **Smart Highlighting**: Active project clearly identified with enhanced details
- **Progress Metrics**: Word counts, chapter progress, quality scores
- **Management Tools**: Easy project switching and organization
- **System Health**: Overall system status and optimization insights

## Notes

- Project list provides complete overview of all novel writing projects
- Status information helps prioritize work and identify next actions
- Management options streamline project organization and workflow
- System statistics provide insights into overall writing productivity