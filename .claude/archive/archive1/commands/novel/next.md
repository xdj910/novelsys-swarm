---
description: Recommend optimal next tasks for novel project
argument-hint: '[filter] e.g., "chapter", "quality", "context", "series", or none for all'
---

# Next Task Recommendation

Analyzing project to recommend optimal next actions with filter: **$ARGUMENTS**

## Description

This command provides intelligent task recommendations based on comprehensive project analysis. It evaluates:

- Current project state and progress
- Task dependencies and blockers
- Parallel execution opportunities
- Quality improvement needs
- Strategic priorities

## Execution

Delegating to recommendation coordinator for strategic analysis:

Use the next-recommendation-coordinator subagent to analyze and recommend next tasks with these instructions:

Analyze the current novel project state and recommend optimal next actions.

Filter: '$ARGUMENTS' (if specified)
- 'chapter': Focus on content generation tasks
- 'quality': Prioritize quality improvements
- 'context': Context and consistency tasks
- 'series': Series-level planning tasks
- none or 'all': Comprehensive analysis

Perform multi-dimensional analysis:
1. Assess current project state (Bible, chapters, quality)
2. Map task dependencies and identify blockers
3. Find parallel execution opportunities
4. Calculate priority scores using weighted matrix
5. Generate actionable recommendations

Provide:
- Top priority action with specific command
- Parallel opportunities for efficiency
- Critical blockers to resolve
- Strategic insights for project optimization

Output should be immediately actionable with clear next steps.

## Priority Matrix

The coordinator uses a weighted scoring system:
- **Impact**: 40% - Effect on overall project
- **Urgency**: 25% - Time sensitivity
- **Effort**: 15% - Work required
- **Dependencies**: 10% - Unblocking value
- **Parallelization**: 10% - Concurrent potential

## Output Format

Receive prioritized recommendations including:
- 🎯 Top priority action with command
- ALERT: Parallel execution opportunities
- 🚨 Critical blockers to resolve
- 📊 Project health metrics
- 💡 Strategic optimization advice

## Usage Examples

- `/novel:next` - Comprehensive analysis
- `/novel:next chapter` - Focus on content generation
- `/novel:next quality` - Quality improvement priorities

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

- `/novel:next series` - Series planning recommendations