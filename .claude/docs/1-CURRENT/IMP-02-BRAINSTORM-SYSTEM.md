# IMP-02-BRAINSTORM-SYSTEM - Interactive Brainstorming Framework
*Command-Triggered Content Type Routing System*

## System Overview

The brainstorm system provides intelligent, interactive exploration for 5 content types:
- Blog Posts
- Articles
- Short Stories
- Novels
- Series

## Components

### 1. /brainstorm Command
**Location**: `.claude/commands/brainstorm.md`
**Purpose**: Entry point for interactive brainstorming
**Trigger**: `/brainstorm` command (NOT natural language)

### 2. brainstorm-coordinator
**Location**: `.claude/agents/brainstorm-coordinator.md`
**Type**: Coordinator (returns JSON plans, no Task tool)
**Purpose**: Progressive exploration with type-specific guidance

## Architecture Design

```
User Input: /brainstorm
    |
brainstorm command
    |
Main Claude -> Task -> brainstorm-coordinator
    |
    Returns JSON plan with:
    - Interactive prompts
    - Type-specific exploration
    - Progressive deepening
    |
Main Claude displays and processes user choices
    |
File System: knowledge_base/brainstorm/
```

## Content Type Workflows

### Blog Post (Shortest: 2-3 phases)
1. Choose topic area and angle
2. Define headline and key points
3. Output: Brief outline with hooks

### Article (Short: 3-4 phases)
1. Select expertise domain
2. Define problem and solution
3. Structure with sections
4. Output: Detailed outline with research points

### Short Story (Medium: 4-5 phases)
1. Choose genre and mood
2. Define core conflict
3. Develop character basics
4. Build story arc
5. Output: Story framework with scenes

### Novel (Long: 6-7 phases)
1. Select genre and sub-genre
2. Build premise and theme
3. Develop main characters
4. Design plot structure
5. Create world details
6. Plan chapter breakdown
7. Output: Comprehensive novel blueprint

### Series (Extended: 8-9 phases)
1. Choose genre and scale
2. Define series premise
3. Build series bible basics
4. Design overarching plot
5. Plan individual books
6. Develop recurring elements
7. Create mythology/lore
8. Define evolution strategy
9. Output: Complete series framework

## Progressive Exploration Pattern

### Phase Structure
Each phase returns JSON with:
```json
{
  "interaction_type": "choice_prompt|text_input|multi_select",
  "display_text": "Question or prompt text",
  "options": {...},
  "valid_inputs": [...],
  "session_state": {
    "content_type": "blog|article|short_story|novel|series",
    "phase": 1-9,
    "collected_data": {...},
    "exploration_depth": {
      "type": 0.0-1.0,
      "genre": 0.0-1.0,
      "concept": 0.0-1.0
    }
  },
  "next_action": "continue|complete|wait_for_user_input"
}
```

### Exploration Depth Tracking
- Each dimension scored 0.0-1.0
- Offers deeper exploration when <0.7
- Suggests completion when all >0.8
- User can always choose depth level

## File System Structure

### Session Management
```
knowledge_base/brainstorm/
├── session_state.json       # Current session
├── history/                  # Past sessions
│   └── [timestamp]/
│       ├── session_log.json
│       └── brainstorm_output.json
└── templates/               # Type-specific templates
```

### Output Artifacts

#### Primary Output: brainstorm_output.json
```json
{
  "session_metadata": {
    "timestamp": "ISO-8601",
    "content_type": "selected_type",
    "total_phases": N,
    "duration_minutes": N
  },
  "project_definition": {
    "type": "content_type",
    "genre": "if_applicable",
    "title_working": "working_title",
    "premise": "core_concept",
    "target_audience": {...}
  },
  "core_concept": {
    "hook": "main_hook",
    "themes": [...],
    "unique_angle": "what_makes_special"
  },
  "detailed_breakdown": {
    "structure": {...},
    "components": [...],
    "milestones": [...]
  },
  "exploration_summary": {
    "depth_scores": {
      "type": 1.0,
      "genre": 0.8,
      "concept": 0.9
    },
    "total_completion": 0.9,
    "suggested_next_steps": [...]
  },
  "ready_for": ["research", "outlining", "writing"]
}
```

## Success Criteria

### Quantifiable Metrics
1. **Completion Rate**: >80% of started sessions reach output
2. **Exploration Depth**: Average >0.7 across dimensions
3. **Decision Clarity**: <3 revision loops per phase
4. **Output Usability**: Can proceed to research/writing

### Quality Indicators
1. **Coherent Concept**: Clear, actionable project definition
2. **Sufficient Detail**: Appropriate depth for content type
3. **User Satisfaction**: Positive progression feedback
4. **Next Step Clarity**: Clear path forward

### Validation Checks
```python
def validate_brainstorm_success(output):
    checks = {
        "has_working_title": bool(output["project_definition"]["title_working"]),
        "has_premise": bool(output["project_definition"]["premise"]),
        "exploration_adequate": output["exploration_summary"]["total_completion"] > 0.6,
        "ready_for_next": len(output["ready_for"]) > 0,
        "type_appropriate_depth": check_depth_for_type(output)
    }
    return all(checks.values())
```

## Integration with Research System

After successful brainstorming:
1. Output feeds into research-coordinator
2. Content type determines research depth
3. Genre/topic guide agent selection
4. Session data preserved for continuity

## Key Features

### Command-Based Triggering
- Explicit `/brainstorm` command
- NOT natural language activation
- Clear start/stop boundaries

### Type-Specific Intelligence
- Different exploration depths
- Appropriate phase counts
- Tailored questions per type

### Progressive Exploration
- 1-2 options at a time
- Avoids overwhelming users
- Natural conversation flow

### State Persistence
- Session saved after each interaction
- Can resume interrupted sessions
- History tracking for patterns

## Technical Implementation

### CLAUDE.md Compliance
- Coordinator has NO Task tool
- Returns JSON plans only
- File-based communication
- No recursion possible

### I/O Specifications
```yaml
Input Requirements:
  - Initial: /brainstorm command
  - During: User choices/text inputs
  - Context: Previous session state

File I/O Operations:
  - Reads: session_state.json, templates
  - Writes: session updates, final output
  - Format: JSON with UTF-8 encoding

Output Format:
  - Interactive: JSON plan for display
  - Final: brainstorm_output.json
  - Ready for: research system integration
```

## References
- Command: `.claude/commands/brainstorm.md`
- Coordinator: `.claude/agents/brainstorm-coordinator.md`
- Architecture: `SYS-01-ARCHITECTURE.md`
- Research System: `IMP-01-RESEARCH-SYSTEM.md`
- CLAUDE.md v6.6 for technical rules