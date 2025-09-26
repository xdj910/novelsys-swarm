---
description: Create new series Bible with brainstorming
argument-hint: <series_name> e.g., "The Midnight Detective"
---

# Novel Bible Creation Command

Think deeply about creating a comprehensive series Bible for: **$ARGUMENTS**

## Description

This command orchestrates comprehensive Bible creation through interactive brainstorming and structured generation, ensuring 95+ quality score.

## Execution

Delegating to bible-architect for comprehensive Bible creation:

Use the bible-architect subagent to create a comprehensive Bible for $ARGUMENTS with these instructions:

Think deeply and create a comprehensive Bible for: $ARGUMENTS

Before proceeding, think more about:
- Genre conventions and reader expectations for this type of story
- Character psychology depth and realistic development arcs  
- World-building consistency and internal logic systems
- Plot structure that supports the intended scope and pacing

Workflow:
1. Context Loading:
   - Review any previous Bible templates in .claude/data/templates/
   - Analyze user's requirements for the new series

2. Guided Brainstorming:
   - Series Foundation: Genre, setting, tone, target audience
   - Character Development: Protagonist, antagonists, supporting cast
   - World Building: Geography, culture, rules, constraints  
   - Story Architecture: Central mystery/conflict, resolution mechanism
   - Quality Standards: Specific quality targets and success metrics

3. Bible Generation:
   - Initialize entity dictionary for this project
   - Specify genre in series_metadata for genre-aware validation
   - Set quality standard: 95+ for all generated content

4. Requirements:
   - Conduct interactive brainstorming for all Bible components
   - Generate detailed character profiles with depth
   - Build consistent world with clear rules
   - Design compelling central mystery/conflict
   - Score the Bible quality (target: 95+)
   - Include genre specification for context-aware generation
   - Initialize entity tracking for consistent naming

5. File Management:
   - Save Bible to: .claude/data/projects/{project}/book_{N}/bible.yaml
   - Initialize entity dictionary: .claude/data/projects/{project}/shared/entity_dictionary.yaml
   - Update context files for characters, plot, and world
   - Set project status to bible_created

6. Validation:
   - Run consistency checks across all Bible components
   - Verify completeness of essential elements
   - Ensure 95+ quality score
   - Generate improvement recommendations if needed

Output a complete, validated Bible with all required components.

## Output

The bible-architect will produce:
- `.claude/data/projects/{project}/book_{N}/bible.yaml` - Main Bible file
- `.claude/data/projects/{project}/shared/entity_dictionary.yaml` - Entity dictionary
- Validation report with 95+ quality score
- Clear next steps for chapter generation

## Next Steps

After successful Bible creation:
- **Review Bible**: `/novel:bible-view` to examine content
- **Start writing**: `/novel:chapter-start 1` to begin first chapter
- **Check status**: `/novel:status` to see project overview
- **Extend series**: `/novel:extend-series` if planning multiple books