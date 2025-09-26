---
description: Sync novel content to GitHub Issues
argument-hint: <chapter_number> or "all" [--full]
---

# GitHub Content Sync

Syncing novel content to GitHub Issues: **$ARGUMENTS**

## Description

This command synchronizes novel content to GitHub Issues, using Issues as a persistent database for version control and collaboration. Each chapter becomes a tracked Issue with complete content and metadata.

## Sync Architecture

- Issue #1: Bible (project configuration)
- Issue #2: Chapter 1
- Issue #3: Chapter 2
- Issue #N+1: Chapter N

## Execution

Delegating to GitHub sync coordinator:

Use the github-sync-coordinator subagent to sync content to GitHub with these instructions:

Synchronize novel content to GitHub Issues.

Arguments: '$ARGUMENTS'
Parse as:
- Single chapter: '3'  ->  sync chapter 3
- Multiple: '1,2,3'  ->  sync listed chapters
- Range: '1-5'  ->  sync chapters 1-5
- All: 'all'  ->  sync all chapters
- Options: '--full'  ->  force complete replacement

Workflow:
1. Validate GitHub CLI auth and repository
2. Load current project and chapter content
3. Determine sync mode (incremental vs full)
4. Create/update GitHub Issues
5. Format content with metadata
6. Handle batch operations efficiently
7. Manage API rate limits
8. Verify sync success

For each chapter:
- Check if Issue exists
- Create new or update existing
- Include outline, content, metadata
- Add quality scores and version info

Provide:
- Progress tracking during sync
- Issue number mapping
- Error handling and recovery
- Sync verification report

## Sync Modes

- **Incremental** (default): Upload only changes, preserve API quota
- **Full** (--full flag): Complete content replacement
- **Batch**: Process multiple chapters with progress tracking

## Issue Format

Each Issue contains:
- Chapter title and number
- Complete outline
- Full chapter content  
- Metadata (word count, quality score, version)
- Quality report from generation pipeline
- Revision history
- Project tags

## Usage Examples

- `/novel:github-sync 3` - Sync chapter 3
- `/novel:github-sync 1,2,3` - Sync chapters 1, 2, and 3
- `/novel:github-sync all` - Sync all chapters
- `/novel:github-sync 5 --full` - Force full sync of chapter 5
- `/novel:github-sync 1-10` - Sync chapters 1 through 10

## Requirements

- GitHub CLI installed and authenticated
- Repository with Issues enabled
- Sufficient API quota for operations