---
description: Create new novel project with comprehensive Bible
argument-hint: '[project_name] (optional - will be determined through brainstorming)'
---

# Create New Novel Project

Creating a new novel project: **$ARGUMENTS** (or determining name through brainstorming if not provided)

## Description

This command initializes a new novel project with comprehensive brainstorming and Bible generation. The process includes:

- Interactive brainstorming to determine project name (if not provided)
- Series architecture and format planning
- Genre and market positioning
- Comprehensive Bible creation
- Project structure initialization
- Quality validation (Bible must score 95+)

## Execution

Delegating to project coordinator for comprehensive project setup:

Use the project-new-coordinator subagent to create a new novel project with these instructions:

Create a new novel project. Project name: '$ARGUMENTS' (use 'TBD' if empty).

If project name is empty or 'TBD':
- Start with interactive brainstorming to determine the project concept
- Help user choose an appropriate project name based on the story idea
- Then proceed with the project setup using the chosen name

Guide the user through comprehensive brainstorming covering:
1. Project format (series/standalone/trilogy)
2. Language variant and style preferences
3. Genre, subgenre, and market positioning
4. Character and world architecture
5. Series planning (if applicable)

Then orchestrate:
- Bible generation via bible-architect
- Quality validation via bible-reviewer (must score 95+)
- Project structure creation
- Entity dictionary initialization

Ensure the project is fully configured and ready for chapter generation.
Provide clear next steps for the user.

## Success Criteria

- Bible created with 95+ quality score
- Project structure initialized correctly
- Entity dictionary created
- Project registered in system
- User receives clear next steps

## Next Steps

After successful creation:
1. Review Bible: `/novel:bible-view`
2. Generate first chapter: `/novel:chapter-start 1`

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

3. Check project status: `/novel:status`