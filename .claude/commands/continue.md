---
name: continue
description: Quickly resume work on the most recent project
---

# Continue Command

Fast-track command to resume your most recent writing project without navigation menus.

## Execution Flow

### Step 1: Find Recent Project
1. Call `project-manager` agent with "get recent" operation
2. Receive most recent project details
3. If no projects exist, redirect to `/brainstorm` command

### Step 2: Display Project Context
Show brief project summary:
```
Resuming: Tropical Mystery Novel
Status: Writing (45% complete)
Last activity: 2 hours ago
Current: Chapter 6 - The Storm Arrives
```

### Step 3: Route to Appropriate Workflow
Based on project status, immediately route to:

#### Status: planning
- Call `brainstorm-coordinator` with project ID
- Pass "continue" flag to skip welcome

#### Status: researching
- Display research options
- Suggest next research agent based on gaps

#### Status: outlining
- Show current outline
- Open for editing/expansion

#### Status: writing
- Display current chapter/section
- Show word count and progress
- Open for continued writing

#### Status: editing
- Show editing checklist
- Resume at last edit point

#### Status: paused
- Ask reason for pause
- Offer to resume or archive

#### Status: completed
- Congratulate on completion
- Offer to start new project

## Quick Actions

After resuming, provide quick action menu:
```
Quick Actions:
[S] Save progress
[V] View project stats
[C] Change to different project
[P] Pause project
[H] Help with current task
```

## Fallback Behavior

### No Recent Project
```
No recent projects found.
Would you like to:
[1] Start a new project
[2] View all projects
[3] Import existing work

Redirecting to /brainstorm command...
```

### Multiple Recent (same timestamp)
```
Multiple projects updated today:
[1] Tropical Mystery Novel (writing)
[2] AI Best Practices (research)

Which would you like to continue? [1-2]:
```

## Integration Points

### With project-manager
- Get most recent project
- Update last accessed time
- Track session duration

### With specific phase agents
- Pass project context
- Skip redundant welcomes
- Maintain continuity

## Optimizations

### Speed Features
1. Skip all menus and prompts
2. Direct routing to work
3. Auto-load last working file
4. Restore cursor position (if applicable)

### Context Preservation
1. Load previous session state
2. Show recent changes/edits
3. Remind of next planned action
4. Display relevant notes

## Success Metrics

1. Time to resume work: <5 seconds
2. Correct workflow routing: 100%
3. Context properly restored
4. User can immediately continue work
5. No lost progress from last session