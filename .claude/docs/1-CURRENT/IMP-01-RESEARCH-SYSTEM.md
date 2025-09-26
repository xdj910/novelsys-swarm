# Research System Documentation Index
*Last Updated: 2025-01-16*

## System Overview

The NOVELSYS-SWARM Research System is an intelligent, progressive exploration framework that helps authors research and plan writing projects through natural language conversation. The system features 6 specialized research agents, 1 coordinator, and a comprehensive bible generation system.

## Documentation Structure

```
Research System Documentation
│
├── Core Architecture
│   ├── Progressive Exploration Pattern
│   ├── PROACTIVE Agent Triggering
│   └── Human Review Integration
│
├── Research Components (7 total)
│   ├── Coordinator (1)
│   │   └── research-coordinator
│   │
│   └── Research Agents (6)
│       ├── trend-analyzer
│       ├── competitor-scanner
│       ├── audience-profiler
│       ├── voice-analyzer
│       ├── topic-explorer
│       └── bible-generator
│
├── Data Flow
│   ├── 5 Research JSON Files
│   └── 7 Production Documents
│
└── User Workflows
    ├── Progressive Research Flow
    ├── Review & Approval Gates
    └── Bible Generation Process
```

## 1. Core Concepts

### Progressive Exploration Pattern
**Philosophy**: Research happens step-by-step based on user choices, not all at once.

```yaml
Traditional (Batch) Approach:
  User request → Run ALL agents → Overwhelming results

Progressive Approach:
  User interest → Suggest 1-2 next steps → User chooses → Execute → Feedback → Next suggestion
```

### PROACTIVE Agent Triggering
Agents automatically engage based on natural language patterns without explicit commands:

```yaml
Trigger Examples:
  "I want to write..." → research-coordinator activates
  "what's popular" → trend-analyzer activates
  "target readers" → audience-profiler activates
  "competitors" → competitor-scanner activates
```

### Human Review Integration
Every stage includes human approval before proceeding:

```yaml
Review Points:
  1. After each research agent completes
  2. Before bible generation begins
  3. After each document is generated
  4. Support for partial regeneration
```

## 2. Research Components

### Research Coordinator
**File**: `.claude/agents/research-coordinator.md`
**Role**: Analyzes conversation state and suggests next research steps
**Key Features**:
- Returns 1-2 agent suggestions, not comprehensive plans
- Provides rationale for each suggestion
- Supports backtracking and direction changes
- No Task tool (prevents recursion)

### Research Agents (Data Collection)

#### trend-analyzer
**Output**: `knowledge_base/trends/trend_analysis_[timestamp].json`
**Triggers**: "market trends", "what's popular", "business opportunities"
**Research**: Market size, growth patterns, seasonal trends, platform data

#### competitor-scanner
**Output**: `knowledge_base/competitors/[niche]_[timestamp].json`
**Triggers**: "competitors", "competition", "market saturation"
**Research**: Competition analysis, gaps, opportunities, differentiation

#### audience-profiler
**Output**: `knowledge_base/audience/audience_profile_[timestamp].json`
**Triggers**: "readers", "audience", "target market", "who will read"
**Research**: Demographics, behaviors, preferences, discovery channels

#### voice-analyzer
**Output**: `knowledge_base/voice/comprehensive_voice_analysis_[timestamp].json`
**Triggers**: Writing style discussions, voice exploration
**Research**: 15 voice samples, 12 sentence patterns, vocabulary tiers, implementation guide

#### topic-explorer
**Output**: `knowledge_base/topics/topic_analysis_[timestamp].json`
**Triggers**: "story ideas", "themes", "what to write about", "plot concepts"
**Research**: High-opportunity themes, settings, plot structures

### Bible Generator (Synthesis)

#### bible-generator
**Input**: All 5 JSON research files
**Output**: 7 production-ready documents:

1. **series_bible.yaml** - Comprehensive project bible (15.9KB)
   - Genre positioning, target audience, voice framework
   - Market strategy, series planning, confidence scores

2. **VOICE_STYLE_GUIDE.md** - Implementation guide (12.2KB)
   - Core voice identity, sentence patterns
   - Vocabulary management, dialogue system
   - Cultural integration guidelines

3. **VOICE_CONSISTENCY_CHECKLIST.md** - Daily checklist (9.9KB)
   - Pre-writing preparation
   - During writing checks
   - Chapter completion review

4. **CARIBBEAN_CULTURAL_AUTHENTICITY_GUIDE.md** - Cultural standards (14.9KB)
   - Cultural elements, sensitivity guidelines
   - Code-switching patterns, community dynamics

5. **ENVIRONMENTAL_ACCURACY_STANDARDS.md** - Setting accuracy (16.0KB)
   - Scientific accuracy requirements
   - Geographic and climate details
   - Conservation themes integration

6. **SERIES_PLAN_10_BOOKS.md** - Long-term planning (17.2KB)
   - Individual book concepts
   - Series arc development
   - Character progression

7. **CHARACTER_DEVELOPMENT_FRAMEWORK.md** - Character system (18.0KB)
   - Development arcs, voice differentiation
   - Cultural representation, relationship evolution

## 3. Data Flow Architecture

```
User Conversation
    ↓
Main Claude (detects triggers)
    ↓
research-coordinator (suggests next steps)
    ↓
User Choice
    ↓
Execute Selected Agent
    ↓
Generate Research JSON (5 types total)
    ↓
User Review & Approval
    ↓
bible-generator (synthesis)
    ↓
7 Production Documents
```

### Research JSON Structure

Each research agent produces structured JSON with:
- Metadata (timestamp, confidence scores, sources)
- Key findings organized by category
- Actionable insights and recommendations
- Cross-references to related research

### Document Generation Logic

The bible-generator performs intelligent synthesis:
- **Combination**: Merging related data from multiple JSONs
- **Derivation**: Inferring new insights from patterns
- **Expansion**: Creating detailed guides from summary data
- **Specialization**: Splitting single data source into multiple focused documents

## 4. User Workflows

### Initial Exploration Flow
```yaml
1. User: "I'm thinking about writing a mystery novel"
2. System: Suggests trend-analyzer OR topic-explorer
3. User: Chooses market trends
4. System: Runs trend-analyzer, shows complete results
5. User: Reviews and decides next direction
6. System: Suggests logical next steps based on findings
```

### Deep Research Flow
```yaml
1. Complete initial exploration (2-3 agents)
2. System suggests targeted research based on gaps
3. User approves specific deep-dive agents
4. Iterative refinement until research complete
5. Proceed to bible generation when ready
```

### Bible Generation Flow
```yaml
1. Review all 5 research JSONs (complete content)
2. Approve or request additional research
3. bible-generator creates 7 documents
4. Review each document (full content displayed)
5. Request modifications if needed
6. Partial regeneration for specific documents
7. Final approval when satisfied
```

## 5. Implementation Status

### Completed Features ✅
- All 7 research system components created and tested
- PROACTIVE triggering implemented
- Progressive exploration pattern active
- JSON research file generation working
- 7-document bible generation functional
- Human review capability confirmed feasible

### Technical Validations ✅
- No recursion risks (coordinators have no Task tool)
- Large file handling (chunked reading for 1MB+ files)
- Windows compatibility (path handling)
- Trigger word safety (avoiding Task tool errors)
- State management through file system

### Pending Enhancements 🔄
- Formal review command implementation
- Draft/final version management
- Component dependency tracking
- Quality scoring system

## 6. Usage Guidelines

### Best Practices
1. **Start broad, then focus** - Begin with market or topic exploration
2. **Review at each step** - Don't skip research reviews
3. **Iterate on voice** - Voice development often needs multiple rounds
4. **Validate cultural elements** - Ensure authenticity with expert review
5. **Test with samples** - Write sample chapters before full commitment

### Common Patterns
```yaml
Market-First Path:
  trend → competitor → audience → voice → topics → bible

Creative-First Path:
  topics → voice → audience → trends → competitor → bible

Voice-First Path:
  voice → topics → audience → trends → competitor → bible
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not triggering | Check trigger words in conversation |
| Large JSON display | Claude can handle full content, no summary needed |
| Partial regeneration needed | Specify which documents to regenerate |
| State lost between sessions | Check knowledge_base folder for previous research |

## 7. File Organization

```
knowledge_base/
├── trends/
│   └── trend_analysis_[timestamp].json
├── competitors/
│   └── [niche]_[timestamp].json
├── audience/
│   └── audience_profile_[timestamp].json
├── voice/
│   └── comprehensive_voice_analysis_[timestamp].json
├── topics/
│   └── topic_analysis_[timestamp].json
└── bible/
    ├── series_bible.yaml
    ├── VOICE_STYLE_GUIDE.md
    ├── VOICE_CONSISTENCY_CHECKLIST.md
    ├── CARIBBEAN_CULTURAL_AUTHENTICITY_GUIDE.md
    ├── ENVIRONMENTAL_ACCURACY_STANDARDS.md
    ├── SERIES_PLAN_10_BOOKS.md
    └── CHARACTER_DEVELOPMENT_FRAMEWORK.md
```

## 8. Integration with Main System

### Relationship to CLAUDE.md
- Follows 5-layer architecture
- Implements PROACTIVE agent patterns
- Uses progressive execution model
- Maintains recursion safety rules

### Relationship to Templates
- Agents follow TEMPLATE_agent.md structure
- Coordinator follows TEMPLATE_coordinator.md pattern
- No commands needed (PROACTIVE triggering)

## Quick Reference

### Trigger Phrases
- "I want to write" → Activates research system
- "market trends" → trend-analyzer
- "competitors" → competitor-scanner
- "target readers" → audience-profiler
- "writing style" → voice-analyzer
- "story ideas" → topic-explorer

### Key Numbers
- **6** research agents
- **1** coordinator
- **5** research JSON files
- **7** production documents
- **1-2** suggestions per step (progressive)
- **15** voice samples per analysis
- **10+** books series planning

### Critical Rules
- Coordinator returns plans, doesn't execute
- Agents have no Task tool (prevents recursion)
- Full content display for review (no summaries)
- User controls every step
- Support infinite revision loops

---

*This index documents the complete NOVELSYS-SWARM Research System as implemented and tested.*