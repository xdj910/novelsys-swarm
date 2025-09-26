---
description: Create new series Bible with brainstorming
argument-hint: <series_name> e.g., "The Midnight Detective"
---

# Novel Bible Creation Command

Think deeply about creating a comprehensive series Bible for: **$ARGUMENTS**

Before proceeding, think more about:
- Genre conventions and reader expectations for this type of story
- Character psychology depth and realistic development arcs  
- World-building consistency and internal logic systems
- Plot structure that supports the intended scope and pacing

## Execution Flow

### Phase 1: Context Loading
1. Review any previous Bible templates in `.claude/data/templates/`
2. Analyze user's requirements for the new series

### Phase 2: Guided Brainstorming  
Launch the bible-architect agent to conduct interactive brainstorming:

- **Series Foundation**: Genre, setting, tone, target audience
- **Character Development**: Protagonist, antagonists, supporting cast
- **World Building**: Geography, culture, rules, constraints  
- **Story Architecture**: Central mystery/conflict, resolution mechanism
- **Quality Standards**: Specific quality targets and success metrics

**Launch bible-architect agent for brainstorming and generation:**

- Use Task tool with subagent_type: "bible-architect"
- Description: "Create comprehensive Bible"
- Prompt: "Create a comprehensive Bible for: {ARGUMENTS}
  * Initialize entity dictionary for this project
  * Specify genre in series_metadata for genre-aware validation
  * Set quality standard: 95+ for all generated content
  * Requirements:
    1. Conduct interactive brainstorming for all Bible components
    2. Generate detailed character profiles with depth
    3. Build consistent world with clear rules
    4. Design compelling central mystery/conflict
    5. Set quality standards (target: 95+ score)
    6. Include genre specification for context-aware generation
    7. Initialize entity tracking for consistent naming
    
    Output a complete bible.yaml with genre clearly specified.
    """
)
```

### Phase 3: Bible Generation
1. Check current project: Read(".claude/data/context/current_project.json")
2. **CORRECTED**: Save generated Bible: Write(".claude/data/projects/{project_name}/book_{current_book}/bible.yaml", bible_content)
4. Create character profiles in project context
5. Update project metadata with Bible creation timestamp

### Phase 4: Context Update
1. Update project context: Write(".claude/data/projects/{project_name}/context/characters.json")
2. Initialize plot tracking: Write(".claude/data/projects/{project_name}/context/plot.json")
3. Populate world details: Write(".claude/data/projects/{project_name}/context/world.json")
4. Update project status to "bible_created"
5. **[ENHANCED]** Initialize entity dictionary with Bible entities
6. **[ENHANCED]** Set project genre in metadata for all future commands

### Phase 5: Validation
1. Run consistency checks across all Bible components
2. Verify completeness of essential elements
3. Score the Bible quality (target: 95+)
4. Generate improvement recommendations if needed

## Output Format

The command should produce:
- `.claude/data/projects/{project}/book_{current_book}/bible.yaml` - Main Bible file
- `.claude/data/projects/{project}/shared/entity_dictionary.yaml` - Entity dictionary
- Validation report with quality score
- Next steps recommendations

## Quality Gates

- **Completeness**: All essential sections must be filled
- **Consistency**: No contradictions between components  
- **Depth**: Characters and world must be sufficiently detailed
- **Usability**: Bible must be actionable for content generation


Execute this workflow systematically, ensuring each phase completes successfully before proceeding to the next.