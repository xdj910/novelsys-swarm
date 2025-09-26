---
description: Create high-quality articles using TTD-DR methodology with three-dimensional quality assessment
argument-hint: '[inspiration] <mode>'
---

# T1-TTD Article Creation System

IMPORTANT: Avoid file names in Task prompts to prevent trigger word errors.

Execute the T1-TTD article creation workflow using the advanced TTD-DR methodology.

## Input Processing
The user input can be any form of inspiration:
- Text descriptions ("I saw an interesting discussion about...")
- File paths (research papers, documents)
- URLs (articles, social media posts)
- Raw ideas or observations

## Workflow Orchestration
Use the t1-ttd-article-coordinator subagent to orchestrate the complete workflow.
The coordinator will analyze the inspiration and return a comprehensive execution plan.

## Quality Standards
- Target: Tier A quality in all three dimensions
- Accuracy: 95%+ verified statements
- Insight: Synthetic level analysis with cross-domain connections
- Originality: <0.5 similarity score with novel concept combinations

## Human Collaboration - Synchronous Checkpoints
The system includes synchronous human-AI collaboration checkpoints that ensure quality:
- **Alpha Checkpoint (Accuracy)**: When confidence <70% - System pauses for verification
- **Beta Checkpoint (Insight)**: When depth insufficient - System waits for enhancement direction
- **Gamma Checkpoint (Originality)**: When similarity >70% - System blocks for adjustment
- **Final Publication**: Explicit user approval required before publication

**CRITICAL**: All checkpoints are synchronous - the system will pause and wait for user input. No timeouts, no auto-continue. User maintains full control.

## Output Delivery
Final deliverables include:
- Complete article with quality certification
- Multi-platform versions (Medium, Substack, ElevenReader)
- Transparent quality assessment report

## Three-Phase Workflow

### Phase 1: Interactive Topic Exploration (5-10 minutes)
Transform user inspiration into a confirmed, strategically-aligned topic through:
- Inspiration parsing and context extraction
- Market landscape exploration and gap identification
- Strategic topic suggestions with alignment scoring
- User-guided refinement and confirmation

**Alpha Checkpoint**: Topic Direction Selection
- System displays 3-5 strategic directions with scores
- User selects preferred approach or requests customization
- System waits for explicit selection (no timeout)
- Refinement cycles available until user satisfied

### Phase 2: TTD-DR Iterative Creation (15-20 minutes)
Generate high-quality content through parallel optimization:
- Intentionally noisy initial draft generation (70% placeholders)
- Parallel variant generation (data-driven, narrative-driven, argument-driven)
- Self-evolution research with multi-candidate optimization
- Three-dimensional quality assessment (accuracy, insight, originality)
- Quality-guided crossover optimization and gate decisions

**Beta Checkpoint**: Quality Enhancement (when triggered)
- System pauses when quality dimensions fall below thresholds
- Clear options presented: Continue/Accept/Adjust
- User decision required before system proceeds
- Multiple checkpoints possible per iteration cycle

### Phase 3: Final Production (3-5 minutes)
Finalize and adapt content for publication:
- Comprehensive final quality audit and certification
- Voice consistency validation and strategic alignment verification
- Multi-platform adaptation with quality badging
- User confirmation with transparent quality reporting

**Gamma Checkpoint**: Publication Decision
- Final quality audit results displayed with certification grades
- Publication options: Publish/Address Issues/Additional Review
- System requires explicit user approval to publish
- No automatic publication - user controls final decision

## Quality Gate System - Synchronous Implementation
Quality checkpoints ensure content meets standards through user-controlled gates:
- **Early completion** when all dimensions reach Tier A (user informed, no auto-advance)
- **Mandatory intervention** when any dimension falls below Tier C (system stops, user decides)
- **Human collaboration** for enhancement opportunities (system pauses, user chooses direction)
- **Transparent progression tracking** with user visibility at each decision point

The system delivers 5x efficiency improvement over manual writing while maintaining 95%+ accuracy and achieving synthetic-level insights with novel concept combinations.

**Key Innovation**: All human collaboration points are synchronous - the system waits for user input rather than proceeding with timeouts or auto-decisions. This ensures quality control remains under user control while leveraging AI efficiency.