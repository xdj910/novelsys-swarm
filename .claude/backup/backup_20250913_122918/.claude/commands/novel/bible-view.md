---
description: View and analyze project Bible content
argument-hint: [section]
---

# Bible View Command

Display the project Bible with formatting, analysis, and optional section filtering.

## Command Usage

- `/novel:bible-view` - View entire Bible with analysis
- `/novel:bible-view characters` - View only characters section  
- `/novel:bible-view plot` - View only plot section
- `/novel:bible-view world` - View only world/universe section
- `/novel:bible-view themes` - View only themes section
- `/novel:bible-view voice` - View only voice profile section

## Implementation

This command uses the bible-view-coordinator subagent to orchestrate comprehensive Bible viewing with:

- **Smart Planning**: Coordinator analyzes requirements and creates execution plan
- **Bible Loading**: Validates file existence and structure  
- **Bilingual Display**: English content with Chinese section headers
- **Completeness Analysis**: Identifies missing elements and quality issues
- **Navigation Support**: Related commands and next steps recommendations
- **Error Handling**: Graceful failure with recovery suggestions

## Execution Steps

### Step 1: Identify Current Project

Use the bible-view-coordinator subagent to:
1. Load current project configuration from `.claude/data/context/current_project.json`
2. Extract project name and validate project exists
3. Determine current book number from project metadata
4. Construct Bible file path: `.claude/data/projects/{project}/book_{N}/bible.yaml`

### Step 2: Orchestrate Bible Display

The coordinator will create a comprehensive execution plan covering:

**Phase 1: Bible Loading and Validation**
- Validate Bible file exists and has proper YAML structure
- Check for required sections and content completeness
- Handle missing file scenarios with clear error messages

**Phase 2: Content Formatting and Display** 
- Apply section filtering based on user arguments
- Generate bilingual formatted output with English/Chinese headers
- Implement syntax highlighting and visual separators
- Perform completeness analysis with percentage scoring

**Phase 3: Related Commands and Next Steps**
- Generate contextual command recommendations
- Provide specific improvement suggestions based on analysis
- Display navigation options for related novel operations

### Step 3: Error Recovery

If Bible not found:
``
Bible not found for project: {project_name}
Use /novel:bible-create to generate one
``

If project not set:
``
No active project. Use /novel:project-switch <project_name> first
``

## Expected Output

The bible-viewer agent will display:

1. **Formatted Bible Content** with bilingual headers
2. **Completeness Analysis** showing missing elements and quality score  
3. **Related Commands** for next actions (bible-create, chapter-start, etc.)
4. **Navigation Suggestions** based on Bible completeness state

## Features

- **Section Filtering**: Focus on specific Bible sections
- **Bilingual Support**: English content with Chinese annotations
- **Quality Analysis**: Completeness scoring and improvement suggestions
- **Smart Navigation**: Context-aware command recommendations
- **Error Resilience**: Clear error messages with recovery guidance

## Notes

- Bible is the foundation document - always display clearly with analysis
- Bilingual support helps Chinese users understand English Bible content  
- Section filtering helps focus on specific planning aspects
- Analysis provides quick health check of Bible completeness and quality
- Related commands guide users to appropriate next actions