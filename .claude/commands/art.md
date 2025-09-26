---
description: Smart article creation with type routing
argument-hint: '[topic] or no arguments to continue current work'
---

# Article Production System - Main Entry Point

This command provides intelligent routing for article creation across all registered article types in the system.

## Usage Patterns

**New Article Creation:**
```
/art "AI hallucinations in healthcare"
/art "The future of remote work"
/art "Blockchain beyond cryptocurrency"
```

**Continue Current Work:**
```
/art
```

**System Status Check:**
```
/art status
```

## Smart Routing Logic

The system automatically:
1. Checks for existing work in progress
2. Identifies appropriate article type based on topic
3. Verifies brainstorming completion status
4. Routes to appropriate workflow phase

## Delegation Strategy

For new article creation, use the art-workflow-coordinator subagent to orchestrate the complete 9-phase workflow process.

**Context to provide:**
- Topic: User-provided subject matter
- Article type: Auto-detected or user-selected
- Current system state: From registry analysis
- Target platforms: 3 platforms (Medium, Substack, ElevenReader)
- Language requirement: All outputs must be in English
- Citation requirement: All sources must include precise URLs
- Quality threshold: 85/100 minimum
- Expected timeline: 6-8 hours total production time

The coordinator will analyze the current state and return a JSON execution plan for the appropriate phase, whether starting fresh research or continuing from an existing phase.

## Business Context Preservation

**Critical workflow elements:**
- Research-driven content creation (Phase 3: parallel agent research)
- Human-in-loop quality control (Phase 5-6: review and revision cycles)
- Multi-platform optimization (Phase 8: platform-specific adaptations)
- Visual production integration (Phase 7: AI-generated image prompts)
- Systematic quality assurance (fact-checking and scoring)

**Quality standards maintained:**
- Minimum 2000 words target length
- 85/100 quality score threshold
- 100% fact accuracy requirement
- Platform compliance across all 3 channels
- Voice guide consistency throughout

## Automatic Registry Management (NEW v2.0)

**BREAKTHROUGH: Registry updates are now completely automatic.**

The workflow coordinator automatically includes registry update tasks in every execution plan. The coordinator's plan specifies:

1. **Main phase tasks** (research, writing, quality review, etc.)
2. **Registry update task included** - coordinator plans it as part of workflow
3. **No manual intervention required** - registry stays in sync automatically

**Key Benefits:**
- Zero risk of forgotten registry updates
- Real-time progress tracking
- Consistent system state across all workflows
- Statistics automatically maintained

Follow the coordinator's plan exactly as provided - registry updates are built into the workflow structure.