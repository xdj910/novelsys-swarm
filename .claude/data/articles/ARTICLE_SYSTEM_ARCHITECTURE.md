# Article System Architecture
*Complete technical architecture and implementation specifications for NOVELSYS-SWARM Article Production System*

**Version**: 3.0
**Updated**: 2025-09-21
**Status**: Architecture Definition Document
**Compliance**: CLAUDE.md 5-Layer Architecture
**New Features**: User Materials Integration System

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [System Components](#system-components)
3. [Command Layer Specifications](#command-layer-specifications)
4. [Coordinator Specifications](#coordinator-specifications)
5. [Agent Specifications](#agent-specifications)
6. [Execution Flow](#execution-flow)
7. [Data Flow and Storage](#data-flow-and-storage)
8. [User Materials Integration](#user-materials-integration)
9. [Implementation Guidelines](#implementation-guidelines)

---

## Architecture Overview

### Five-Layer Architecture Compliance

The Article System follows NOVELSYS-SWARM's mandatory 5-layer architecture:

```
Layer 1: User Interface
         |
         v
Layer 2: Command Layer (.claude/commands/)
         |
         v
Layer 3: Main Claude (Orchestrator with Task tool)
         |
         v
Layer 4: Coordinator Layer (.claude/agents/)
         |
         v
Layer 5: Agent Layer (.claude/agents/)
         |
         v
File System (Data Layer) + User Materials Integration
```

### Key Architectural Principles

1. **No Direct Agent Calls**: Main Claude never calls agents directly, only through coordinators
2. **No Task in Subagents**: Coordinators and Agents CANNOT have Task tool (prevents recursion)
3. **File-Based Communication**: All inter-component communication via file system
4. **Phase-Based Execution**: Work divided into discrete phases with checkpoints
5. **Stateless Components**: Each component execution is independent
6. **User Materials Integration**: System seamlessly incorporates user-provided research

### Component Responsibilities

| Component | Location | Tools | Purpose |
|-----------|----------|-------|---------|
| Commands | .claude/commands/ | None (delegation only) | User interface, context preservation |
| Coordinators | .claude/agents/ | Read, Write, Bash, Grep | Planning and orchestration |
| Agents | .claude/agents/ | Task-specific, NO Task | Single-task execution |
| Main Claude | System | All tools including Task | Central orchestration |

---

## System Components

### Commands (2 files)
- `art.md` - Main entry point for article creation
- `art-brainstorm.md` - Article type setup and configuration

### Coordinator (1 file)
- `art-workflow-coordinator.md` - Orchestrates the 9-phase workflow with user materials support

### Agents (13 files - Updated with User Materials)
Initialization Phase:
- `art-article-initiator.md` - Article folder structure creation (Phase 2) - Updated with 3-folder structure

User Materials Phase:
- `art-materials-processor.md` - User materials analysis and insights extraction (Phase 3A) - NEW

Research Phase:
- `art-trend-researcher.md` - Market trends analysis - Updated with materials integration
- `art-audience-analyst.md` - Target audience profiling - Updated with materials integration
- `art-competitor-scanner.md` - Competition analysis - Updated with materials integration
- `art-topic-explorer.md` - Topic deep-dive - Updated with materials integration

Production Phase:
- `art-article-writer.md` - Content creation - Updated with materials integration
- `art-fact-checker.md` - Fact validation - Updated with materials cross-reference
- `art-quality-scorer.md` - Quality assessment - Updated with materials integration evaluation
- `art-visual-designer.md` - Visual element design
- `art-platform-optimizer.md` - Platform-specific optimization

System Management:
- `art-registry-updater.md` - Registry state management (all phases) - Updated with materials tracking

---

## Command Layer Specifications

### art.md

```yaml
---
name: art
description: Smart article creation with type routing and user materials support
thinking: Delegate to coordinator for workflow orchestration with materials integration
---

Maximum 100 lines
Pure delegation pattern
Contextual information preservation
Smart type-based routing
Coordinator dependency
User materials awareness
```

### art-brainstorm.md

```yaml
---
name: art-brainstorm
description: Article type setup and strategy development
thinking: Direct strategic planning for article types
---

Maximum 100 lines
Strategy-focused delegation
Type configuration
Human-in-loop decisions
Brainstorming workflow
```

---

## Coordinator Specifications

### art-workflow-coordinator.md

**Core Function**: Orchestrate the complete 9-phase article production workflow with user materials integration

**Tool Configuration**: `Read, Write, Bash, Grep` (NO Task tool - prevents recursion)

**Responsibilities**:
- Read current state from registry.json
- Determine current workflow phase (0-9, including 3A for user materials)
- Check for user materials in user_materials/ folder
- Return JSON execution plans for next steps
- Never execute agents directly

**Output**: JSON execution plans returned directly to Main Claude

**Key Safety**: Cannot call other subagents (no Task tool)

**User Materials Support**: Detects materials, routes to processing phase, integrates insights

---

## Agent Specifications

### User Materials Integration Agent (Phase 3A)

**NEW: art-materials-processor.md**

**Core Function**: Analyze user-provided materials and extract insights for research integration

**Tool Configuration**: `Read, Write, Grep`

**Responsibilities**:
- Scan user_materials/ folder for content
- Apply priority system (PRIORITY_, CORE_, SUPP_)
- Extract key themes, insights, and data points
- Generate materials_insights.md for research agent reference
- Map user knowledge to article relevance

**Input Requirements**:
- Working directory: absolute path to article folder
- User materials: in user_materials/ folder with priority prefixes
- Topic context: from metadata.json

**Output**: processed/materials_insights.md with structured analysis

### Research Agents (Phase 3B - Updated)

All research agents follow consistent patterns with materials integration:

**Common Input Requirements**:
- Working directory: absolute path provided by Main Claude
- Research scope: topic-specific parameters
- Strategy context: from strategy documents
- **User materials context**: processed/materials_insights.md (if available)

**Common Output**:
- Research reports: in local agent_outputs/ folder (replaces research/)
- Quality metrics: completion and coverage assessment
- User insights integration: seamlessly incorporated
- Self-evaluation: against minimum requirements

### Production Agents (Phases 4-8 - Updated)

**Content Creation**:
- `art-article-writer.md`: Transform research + user insights into article
- `art-fact-checker.md`: Verify claims against sources + user materials
- `art-quality-scorer.md`: Quality assessment including materials integration

**Publishing Preparation**:
- `art-visual-designer.md`: Create AI generation prompts
- `art-platform-optimizer.md`: Platform-specific optimization

---

## Execution Flow

### Phase-Based Workflow with User Materials

```
Phase 1: Strategy Development
  └─ Coordinator determines requirements
  └─ Interactive brainstorming process

Phase 2: Article Initiation
  └─ art-article-initiator (creates 3-folder structure)
  └─ art-registry-updater (automatic)

Phase 3A: User Materials Processing (NEW - if materials exist)
  └─ art-materials-processor
  └─ Creates processed/materials_insights.md
  └─ art-registry-updater (automatic)

Phase 3B: Research Collection (Parallel - with materials integration)
  ├─ art-trend-researcher (references materials insights)
  ├─ art-audience-analyst (references materials insights)
  ├─ art-competitor-scanner (references materials insights)
  └─ art-topic-explorer (references materials insights)
  └─ art-registry-updater (automatic after completion)

Phase 4: Content Creation (with user materials integration)
  └─ art-article-writer (uses agent_outputs + processed insights)
  └─ art-registry-updater (automatic)

Phase 5: Quality Review (Parallel - with materials validation)
  ├─ art-fact-checker (cross-references user materials)
  └─ art-quality-scorer (evaluates materials integration)
  └─ art-registry-updater (automatic)

Phase 6: Revision Cycle (preserves materials integration)
  └─ Human decision point
  └─ art-registry-updater (automatic)

Phase 7: Visual Production
  └─ art-visual-designer
  └─ art-registry-updater (automatic)

Phase 8: Platform Optimization
  └─ art-platform-optimizer
  └─ art-registry-updater (automatic)

Phase 9: Publishing
  └─ art-registry-updater (marks complete with materials usage)
```

### Coordinator-Agent Flow with Materials

1. **Main Claude** → Task → **art-workflow-coordinator**
2. **Coordinator** analyzes state, detects user materials, returns JSON plan
3. **Main Claude** parses JSON plan
4. **Main Claude** → Task → **Agents** (parallel or sequential, with materials awareness)
5. **Agents** execute, integrate user insights, write results to files
6. **Main Claude** verifies completion, continues to next phase

---

## Data Flow and Storage

### Registry Structure (Updated)
```json
{
  "current_work": {
    "article_id": "20250119_140000_ai_hallucinations",
    "phase": "3A",
    "status": "user_materials_processing",
    "user_materials_detected": true
  }
}
```

### Article Folder Structure (Updated with 3-Folder System)
```
.claude/data/articles/{type}/articles/{timestamp}_{slug}/
├── metadata.json       # Article tracking with materials status
├── user_materials/     # NEW: User drop zone
│   ├── PRIORITY_research_notes.md
│   ├── CORE_competitor_analysis.pdf
│   └── SUPP_background_reading.txt
├── processed/          # NEW: Analyzed user content
│   └── materials_insights.md
├── agent_outputs/      # NEW: System research (replaces research/)
│   ├── trends.md
│   ├── audience.md
│   ├── competitors.md
│   └── topic.md
├── drafts/           # Phase 4-6 outputs
│   ├── v1_draft.md
│   └── final.md
├── reports/          # Phase 5 outputs
│   ├── fact_check.md
│   └── quality_score.md
├── visuals/          # Phase 7 outputs
│   └── production_guide.md
└── published/        # Phase 8 outputs
    ├── medium.md
    ├── substack.md
    ├── beehiiv.md
    └── elevenreader.md
```

### Strategy Folder Structure (Unchanged)
```
.claude/data/articles/{type}/strategy/
├── strategy_v1.0.md
├── voice_guide.md
└── PLATFORM_OPTIMIZATION_STRATEGY.md
```

---

## User Materials Integration

### 3-Folder Architecture

**Design Philosophy**: Separate user content from system processing while maintaining integration

#### 1. user_materials/ (User Drop Zone)
- **Purpose**: Safe space for user-provided research, notes, documents
- **Access**: Read-only by system, full control by user
- **Priority System**: PRIORITY_, CORE_, SUPP_ prefixes for importance ranking
- **Format**: Any format accepted (PDF, MD, TXT, DOCX, etc.)

#### 2. processed/ (System Analysis)
- **Purpose**: System-generated analysis of user materials
- **Key File**: materials_insights.md - structured insights extraction
- **Access**: System-generated, user-readable
- **Integration**: Referenced by all research and production agents

#### 3. agent_outputs/ (System Research)
- **Purpose**: Agent-generated research and analysis
- **Replaces**: Old "research/" folder
- **Integration**: Combines system research with user insights
- **Enhancement**: Research agents reference processed/ insights when available

### User Materials Flow

```
User Materials → user_materials/ → materials-processor → processed/materials_insights.md
                                                               ↓
Research Agents → agent_outputs/ ← Integrates insights from processed/
                       ↓
Article Writer → drafts/ ← Uses both agent_outputs/ and processed/ content
```

### Priority System Implementation

```yaml
PRIORITY_ files:
  - Highest weight in analysis
  - Direct integration into key arguments
  - Featured prominently in insights

CORE_ files:
  - Substantial integration into research strategy
  - Core themes guide research direction
  - Important data points extracted

SUPP_ files:
  - Background context and validation
  - Supporting evidence and examples
  - Enrichment of existing research
```

### Backward Compatibility

The system maintains full backward compatibility:
- Works without user materials (pure agent research)
- No breaking changes to existing workflows
- Optional enhancement when materials provided
- Graceful degradation for empty user_materials/ folder

---

## Implementation Guidelines

### Creating Commands

```markdown
# Command Template
---
name: [command-name]
description: [one-line description]
thinking: [delegation strategy with materials awareness]
---

Maximum 100 lines
Pure delegation
Preserve context
No business logic
User materials support
```

### Creating Coordinator

```markdown
# Coordinator Template
---
name: [coordinator-name]
description: [orchestration purpose with materials integration]
tools: Read, Write, Bash, Grep  # NEVER Task!
thinking: [planning strategy including materials detection]
---

Read state
Detect user materials
Determine phase
Return JSON plan
Never execute
```

### Creating Agents

```markdown
# Agent Template
---
name: [agent-name]
description: [single task with materials integration]
tools: [specific tools]  # NEVER Task!
model: [optional model override]
---

Single responsibility
File I/O only
Materials integration
Self-assessment
Quality checks
```

### Path Resolution Strategy (Updated for 3-Folder System)

**Problem Solved**: Coordinators return path templates, Main Claude resolves actual paths including new folder structure.

#### Path Template System (Updated)

**Coordinator JSON Plans Include**:
```json
{
  "working_directory": "{article_dir}",
  "path_context": {
    "base_path": ".claude/data/articles/{article_type}/content/{article_id}",
    "strategy_dir": "../../../strategy",
    "user_materials_dir": "user_materials",
    "processed_dir": "processed",
    "agent_outputs_dir": "agent_outputs"
  },
  "agents": [
    {
      "name": "art-materials-processor",
      "working_directory": "{article_dir}",
      "inputs": [
        "{user_materials_dir}/",
        "metadata.json"
      ],
      "outputs": [
        "{processed_dir}/materials_insights.md"
      ]
    },
    {
      "name": "art-article-writer",
      "working_directory": "{article_dir}",
      "inputs": [
        "{agent_outputs_dir}/trends.md",
        "{processed_dir}/materials_insights.md",
        "{strategy_dir}/strategy_v1.0.md"
      ]
    }
  ]
}
```

#### Template Variables (Updated)
- `{article_type_dir}` = `.claude/data/articles/{type}`
- `{article_dir}` = `.claude/data/articles/{type}/content/{article_id}`
- `{strategy_dir}` = `strategy` (relative) or `../../../strategy` (from article)
- `{user_materials_dir}` = `user_materials` (relative to working_directory)
- `{processed_dir}` = `processed` (relative to working_directory)
- `{agent_outputs_dir}` = `agent_outputs` (relative to working_directory)
- `{drafts_dir}` = `drafts` (relative to working_directory)
- `{reports_dir}` = `reports` (relative to working_directory)
- `{visuals_dir}` = `visuals` (relative to working_directory)
- `{published_dir}` = `published` (relative to working_directory)

### Recursion Prevention Checklist

- [ ] Commands have no tools
- [ ] Coordinator has NO Task tool
- [ ] Agents have NO Task tool
- [ ] Only Main Claude uses Task
- [ ] No subagent calls subagent

### Windows Compatibility

- [ ] No Unicode characters
- [ ] Use forward slashes in paths
- [ ] UTF-8 encoding for all files
- [ ] ASCII-only in documentation

### Path Resolution Validation

- [ ] Coordinator includes working_directory in JSON plans
- [ ] Coordinator uses template variables, not hardcoded paths
- [ ] Agents document working directory expectation
- [ ] Agents implement defensive input handling
- [ ] Main Claude resolves all template variables before agent calls

### User Materials Integration Validation

- [ ] Agents can operate with or without user materials
- [ ] Priority system implemented in materials processor
- [ ] Research agents reference processed insights when available
- [ ] Article writer integrates both agent outputs and user insights
- [ ] Quality agents evaluate materials integration

---

## Migration Path

### From Current Documentation to Implementation

1. **Phase A: Foundation** (Week 1)
   - Create art.md and art-brainstorm.md commands
   - Implement art-workflow-coordinator.md with materials detection
   - Set up registry.json structure with materials tracking

2. **Phase B: User Materials Integration** (Week 2)
   - Implement art-materials-processor.md agent
   - Update art-article-initiator.md for 3-folder structure
   - Test materials processing workflow

3. **Phase C: Core Agents** (Week 2-3)
   - Update all research agents with materials integration
   - Update production agents with materials awareness
   - Ensure no Task tools in subagents
   - Implement updated path resolution system

4. **Phase D: Integration Testing** (Week 4)
   - Test complete workflow end-to-end with and without materials
   - Validate recursion prevention
   - Confirm Windows compatibility
   - Test backward compatibility

### Validation Checklist

#### Architecture Compliance
- [ ] 5-layer architecture maintained
- [ ] No recursion possible (Task tool only in Main Claude)
- [ ] File-based communication between components
- [ ] Phase-based execution with checkpoints

#### User Materials Integration
- [ ] 3-folder structure correctly implemented
- [ ] Priority system functioning
- [ ] Materials processor creates proper insights
- [ ] Research agents integrate user insights
- [ ] Article writer combines all sources
- [ ] Backward compatibility maintained

#### Business Requirements
- ✓ 9-phase workflow preserved (with 3A addition)
- ✓ 6-8 hour timeline maintained
- ✓ Quality standards (85/100)
- ✓ Human-in-loop decisions
- ✓ 4 platform optimization

---

## Related Documentation

### Business Context
- **Workflow Details** → [ARTICLE_WORKFLOW_DETAIL.md](ARTICLE_WORKFLOW_DETAIL.md) - 9-phase business process with user materials
- **Quality Standards** → [ARTICLE_IO_STANDARDS.md](ARTICLE_IO_STANDARDS.md) - I/O specifications and requirements
- **Platform Strategy** → [PLATFORM_OPTIMIZATION_STRATEGY.md](PLATFORM_OPTIMIZATION_STRATEGY.md) - Platform-specific optimizations

### Implementation Resources
- **System Overview** → [README.md](README.md) - Quick start guide with materials integration
- **Registry Structure** → [registry.json](registry.json) - System state tracking
- **CLAUDE.md Standards** → [../../CLAUDE.md](../../CLAUDE.md) - Architecture compliance requirements

---

*This document serves as the authoritative technical architecture for the Article Production System with User Materials Integration. All implementations must comply with these specifications.*