---
description: Setup new article type with strategy development
argument-hint: '[type_name] or no arguments to see available types'
---

# Article Type Setup & Brainstorming System

This command initiates the strategic brainstorming process for new article types or manages existing type configurations.

## Usage Patterns

**Setup New Article Type:**
```
/art-brainstorm "tech_skeptic"
/art-brainstorm "startup_realist"
```

**View Available Types:**
```
/art-brainstorm
```

**Modify Existing Strategy:**
```
/art-brainstorm "ai_realist" --modify
```

## System Integration

The command checks registry.json to determine if brainstorming is needed:
- If brainstorming_status.ready_for_creation = false: Run full strategy development
- If brainstorming_status.ready_for_creation = true: Skip to article creation flow
- If type doesn't exist: Create new type entry and begin brainstorming

## Delegation Strategy

Use the art-workflow-coordinator subagent to orchestrate the interactive brainstorming workflow.

**Context for new type setup:**
- Action: setup_new_type or modify_existing_type
- Type ID: User-provided identifier
- Registry status: Current brainstorming completion state
- Required outputs: strategy document, voice guide, README

**Context for existing type:**
- Action: show_available_types
- Registry data: All registered types with status
- Routing decision: Direct to article creation if ready

## Brainstorming Workflow Components

**Strategic Development Process (Phase 1):**
1. Interactive audience profiling (target demographics and psychographics)
2. Value proposition definition (unique angles and differentiators)
3. Content distribution strategy (article type percentages)
4. Voice and tone establishment (writing style characteristics)
5. Publishing strategy (platform focus and frequency)

**Required Deliverables:**
- strategy/strategy_v1.0.md: Complete content strategy
- strategy/voice_guide.md: Writing style and tone guidelines
- README.md: Type documentation and overview

**Quality Assurance:**
- Completeness verification of all strategy elements
- Voice guide clarity assessment for production use
- Strategy actionability scoring (minimum 85%)

The coordinator will manage the interactive Q&A process and generate the complete strategic foundation before marking the type as ready for article production.

## Success Criteria

Upon completion:
- registry.json updated with ready_for_creation = true
- All strategy documents created and validated
- Type available for immediate article creation via /art command