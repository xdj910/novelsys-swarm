---
description: Switch to different novel project
argument-hint: <project_name>
---

# Project Switch

Switching active project to: **$ARGUMENTS**

## Description

This command switches between novel projects while preserving context and work state. It validates the target project and ensures a clean transition.

## Execution

Delegating to project switch coordinator:

Use the project-switch-coordinator subagent to switch the active project with these instructions:

Switch the active novel project to: $ARGUMENTS

Workflow:
1. Validate target project
   - Verify project exists
   - Check essential files (project.json)
   - Warn if Bible missing
   - Validate project structure

2. Save current context
   - Capture work state
   - Save pending tasks
   - Record quality metrics
   - Create context snapshot

3. Clean transition
   - Clear active context
   - Flush caches
   - Complete pending operations

4. Activate target project
   - Load project configuration
   - Restore previous context if exists
   - Scan project status
   - Update current_project.json

5. Generate status report
   - Show project overview
   - Display progress metrics
   - List pending tasks
   - Provide recommendations

Ensure:
- No data loss during switch
- Context properly preserved
- Target project ready to use
- Clear guidance for resuming work

If project not found, list available projects.
If Bible missing, warn but allow switch.

## Process Includes

1. **Validation**: Verify target project health
2. **Preservation**: Save current project state
3. **Transition**: Clean context switch
4. **Activation**: Load target project
5. **Recovery**: Restore previous context if available

## Context Management

- Current project state saved to `context_snapshot.json`
- Previous work context restored when returning
- Pending tasks preserved across switches
- Quality metrics maintained

## Success Indicators

- [x] Project found and validated
- [x] Current context saved
- [x] Target project activated
- [x] Previous context restored (if exists)
- [x] Ready to resume work

## Usage Examples

- `/novel:project-switch MyNovel` - Switch to MyNovel project
- `/novel:project-switch TestProject` - Switch to test project
- `/novel:project-switch Series1` - Switch to series project

## Next Steps

After switching:
1. Check status: `/novel:status`
2. View Bible: `/novel:bible-view`
3. Resume work: `/novel:next`
4. Generate chapter: `/novel:chapter-start N`