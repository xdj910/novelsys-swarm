---
name: brainstorm
description: Interactive brainstorming system for writing projects
---

# Brainstorm Command

Enhanced brainstorming system with optional project management. Guides users through interactive brainstorming and manages writing projects.

## Execution Flow

### Step 1: Initialize and Check Projects (Optional Enhancement)
1. First, try to call `project-manager` with "initialize" operation
   - This ensures data structure exists
   - If project-manager unavailable: Skip to legacy mode

2. If initialization successful:
   - Call `project-manager` with "scan projects" to show existing projects
   - Display project list if any exist

3. If initialization fails or project-manager unavailable:
   - Proceed directly to brainstorming (pure legacy mode)
   - Use knowledge_base/ for all storage

2. If projects exist, display:
   ```
   EXISTING PROJECTS:
   [1] Tropical Mystery (45% - Writing)
   [2] AI Article (20% - Research)
   [N] Start New Project

   Choose [1-2/N]:
   ```

### Step 2: Route Based on Choice
- **Continue existing**: Load project context, call brainstorm-coordinator with project ID
- **New project**: Call project-manager to create project, then brainstorm-coordinator
- **No projects/Legacy**: Direct to brainstorm-coordinator without project ID

### Step 3: Brainstorming Session
1. Call brainstorm-coordinator with:
   - Current input (start/continue/user choice)
   - Project ID (actual ID like "20250117_143022_mystery" or "none")
2. Receive JSON plan from coordinator
3. Determine save path based on response:
   - If `project_id` != "none" AND `storage_mode` == "project":
     → Save to `.claude/data/projects/{actual_project_id}/brainstorm/session_state.json`
   - Otherwise:
     → Save to `knowledge_base/brainstorm/session_state.json`
4. Display interaction prompt to user
5. Wait for user input
6. Repeat until session complete

### Step 4: Status Updates (When Project Mode)
- After brainstorm completion: Call project-manager "update status {id} researching"
- After research trigger: Update status accordingly
- Maintain project lifecycle through status transitions

## What the Coordinator Provides

The coordinator returns JSON plans with:
- Interactive prompts and options
- Session state updates (for you to save)
- Next action instructions
- Research agent recommendations when ready

## Your Responsibilities

As Main Claude, you must:
1. Execute the brainstorm-coordinator
2. Handle all file I/O based on the plan
3. Display prompts to the user
4. Process user input
5. Loop until completion

## Backward Compatibility

The command works in two modes:
1. **Legacy Mode** (no project management): Direct brainstorming as before
2. **Project Mode** (with project-manager): Full project lifecycle support

This ensures existing workflows continue to work while adding project management as an optional enhancement.

## Integration Notes

- Project management is **optional** - system works without it
- Falls back gracefully if project-manager unavailable
- Preserves all existing brainstorm-coordinator functionality
- Compatible with existing knowledge_base structure