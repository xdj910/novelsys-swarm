# Article Production System

## Overview
The NOVELSYS-SWARM article production system supports multiple article types with centralized registry tracking and type-specific workflows.

## System Architecture

### Directory Structure
```
.claude/data/articles/
├── README.md                    # This file - system overview
├── ARTICLE_WORKFLOW.md         # Complete production workflow
├── PLATFORM_OPTIMIZATION_STRATEGY.md  # Unified platform optimization
├── registry.json               # Central registry for all article types and tracking
│
└── {article_type}/             # Each article type folder
    ├── README.md               # Type-specific documentation
    ├── strategy/               # Shared strategy files
    └── articles/               # Article content folders
        └── {timestamp}_{slug}/ # Individual articles
```

## Available Article Types

### 1. AI Realist (`ai_realist/`)
- **Description**: 2000-word B2B skeptical AI analysis
- **Target**: Decision makers evaluating AI adoption
- **Platforms**: Medium, Substack, Beehiiv, ElevenReader
- **Status**: Active
- **Documentation**: [ai_realist/README.md](ai_realist/README.md)

### 2. [Future Types]
Additional article types can be added following the same structure.

## General Workflow with User Materials Integration

### Phase 1: Type Selection & Brainstorming
```
User: /art-brainstorm
System: Checks registry → Shows available types
        ↓
Check: brainstorming_status.ready_for_creation
  ├─ FALSE → Brainstorming Phase
  │   └─ Creates: strategy/, voice_guide.md, README.md
  │       └─ Sets: ready_for_creation = true
  └─ TRUE → Skip to Article Creation
```

### Phase 2: Article Creation
```
User: /art "specific topic"
System: Creates timestamp folder
        └── {timestamp}_{slug}/
            ├── metadata.json
            ├── user_materials/     # User drop zone
            ├── processed/          # Analyzed user content
            ├── agent_outputs/      # System-generated research
            ├── drafts/
            ├── reports/            # Quality check reports
            ├── visuals/
            └── published/
```

### Phase 3: Production Pipeline
```
Phase 3A: User Materials Processing (if materials provided)
   └── materials-processor → processed/materials_insights.md

Phase 3B: Research (Parallel agents - with materials integration)
   ├── trend-analyzer      → agent_outputs/trends.md
   ├── audience-profiler   → agent_outputs/audience.md
   ├── competitor-scanner  → agent_outputs/competitors.md
   └── topic-explorer      → agent_outputs/topic.md

   Note: All research agents can reference processed/materials_insights.md

Phase 4: Writing
   └── article-writer → drafts/v1_draft.md
       (Uses both agent_outputs/ and processed/ content)

Phase 5: Quality Review (Parallel)
   ├── article-fact-checker → reports/fact_check_report.md
   └── article-quality-scorer → reports/quality_score_report.md

Phase 6: Human Decision
   └── Review reports → Approve or Request Revision

Phase 7: Visual Production
   └── visual-creator → visuals/visual_production_guide.md

Phase 8: Platform Optimization
   └── platform-optimizer → published/{platform}.md
   └── Uses PLATFORM_OPTIMIZATION_STRATEGY.md

Phase 9: Publishing
   └── Update registry → Mark complete
```

Each phase updates the registry tracking system.

## User Materials Integration System

### 3-Folder Structure
The new user materials integration system uses three specialized folders:

#### 1. user_materials/ (User Drop Zone)
- **Purpose**: Safe space for users to place their research, notes, documents
- **Priority System**: Files prefixed with PRIORITY_, CORE_, SUPP_ for importance
- **Content**: User-provided materials in any format
- **Processing**: Materials remain untouched in original format

#### 2. processed/ (Analyzed User Content)
- **Purpose**: System analysis of user materials
- **Key File**: `materials_insights.md` - comprehensive analysis
- **Content**: Structured insights, themes, key findings from user materials
- **Created by**: materials-processor agent in Phase 3A

#### 3. agent_outputs/ (System Research)
- **Purpose**: System-generated research and analysis
- **Replaces**: Old "research/" folder
- **Content**: Agent-generated research files (trends.md, audience.md, etc.)
- **Integration**: Agents can reference processed/ insights when available

### User Materials Flow
```
User materials → user_materials/ → processed/materials_insights.md
                                           ↓
                    agent_outputs/ ← Research agents reference insights
                           ↓
                    drafts/ ← Article writer uses both sources
```

### Backward Compatibility
- System works without user materials (pure agent research)
- When user materials exist, they enhance rather than replace agent research
- Priority system ensures critical user content gets primary attention

## Registry System

The registry provides centralized tracking across all article types in a single JSON file:

- **registry.json**: All registered types, configurations, current work status, and statistics

The registry contains:
- Article type definitions and configurations
- Current production status for each type
- Global and type-specific statistics
- Brainstorming completion status

## Common Structure for All Article Types

### Timestamp-Based Folders
Every article gets a unique folder: `{timestamp}_{slug}/`
- Example: `20250118_143022_ai_risks/`
- Benefits: No conflicts, chronological, parallel work

### Standard Subfolders
```
{timestamp}_{slug}/
├── metadata.json      # Article tracking
├── user_materials/    # User drop zone (new)
├── processed/         # Analyzed user content (new)
├── agent_outputs/     # System research (replaces research/)
├── drafts/           # Version history
├── visuals/          # Images and prompts
└── published/        # Platform versions
```

### Metadata Standard
Every article has `metadata.json` tracking:
- ID, title, type, status
- Word count (current/target)
- Phase completion timestamps
- Platform publishing status
- Production metrics
- User materials status (new)

## Adding New Article Types

To add a new article type:

1. Create folder: `.claude/data/articles/{new_type}/`
2. Add README.md with type-specific documentation
3. Create strategy folder if needed
4. Register in `registry.json` under article_types
5. Update this README with type information

## Integration Points

### With Brainstorming
- Brainstorm coordinator reads registry
- Offers registered article types
- Routes to type-specific flows

### With User Materials
- materials-processor analyzes user content
- Priority system (PRIORITY_, CORE_, SUPP_) guides processing
- Insights integrate with agent research automatically

### With Agents
- `visual-creator`: Generates image prompts
- `trend-analyzer`: Market research (checks processed/ for user insights)
- `audience-profiler`: Target audience analysis (uses user materials if available)
- Type-specific agents as needed

### With Commands
- `/art-brainstorm`: Setup new article type
- `/art [topic]`: Smart routing for article creation with materials support
- `/art-status`: Check current article status

## Quality Standards

All article types should maintain:
- Clear documentation in README
- Registry integration
- Timestamp-based structure
- Metadata tracking
- Platform optimization
- User materials integration support

## Navigation Guide

### Core Documentation
- **System Architecture** → [ARTICLE_SYSTEM_ARCHITECTURE.md](ARTICLE_SYSTEM_ARCHITECTURE.md)
- **Business Workflow** → [ARTICLE_WORKFLOW_DETAIL.md](ARTICLE_WORKFLOW_DETAIL.md)
- **Quality Standards** → [ARTICLE_IO_STANDARDS.md](ARTICLE_IO_STANDARDS.md)
- **Platform Strategy** → [PLATFORM_OPTIMIZATION_STRATEGY.md](PLATFORM_OPTIMIZATION_STRATEGY.md)

### Implementation Resources
- **Article Type Example** → [ai_realist/README.md](ai_realist/README.md)
- **System Registry** → [registry.json](registry.json)
- **Adding New Types** → Follow structure in System Architecture doc

---

*System Version: 4.0 | Updated: 2025-09-21 | Status: Active with User Materials Integration*