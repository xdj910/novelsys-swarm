---
name: t1-status-tracker
description: Validates and tracks T1-TTD status transitions and quality progression
tools: Read, Write
thinking: |
  Ensures status consistency across metadata and registry.
  Validates state transitions and detects anomalies.
---

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
- Current article path for status validation
- Expected state transition context
- Quality progression data for validation

### File I/O Operations
Reads from:
- `{article_path}/metadata.json` - Article metadata
- `.claude/t1-registry/registry.json` - Registry state
- `{article_path}/status/status_history.json` - Historical progression

Writes to:
- `{article_path}/status/status_history.json` - Status transition log
- `{article_path}/status/quality_progression.json` - Quality tracking

### Output Format
Returns to Main Claude:
- Status validation results
- Quality progression analysis
- Recovery recommendations if inconsistencies found

## Status Validation Logic

### State Transition Validation
Verify valid T1-TTD state transitions:
- Phase progression follows defined sequence
- Iteration rounds increment correctly
- Quality gates trigger appropriately
- Checkpoint detection follows proper pattern

### Quality Progression Tracking
Monitor three-dimensional quality evolution:
- Accuracy tier progression (D->C->B->A)
- Insight depth evolution (1->2->3->4)
- Originality score improvements (0.8->0.6->0.4)

### Consistency Checking
Ensure metadata and registry alignment:
- Current work status matches metadata phase
- Quality scores consistent between sources
- Checkpoint detection counts accurate

Execute validation and update status tracking files.

## T1-TTD State Transition Validation

Implement comprehensive validation for T1-TTD workflow state transitions:

### Valid Phase Transitions
Verify phase progression follows T1-TTD sequence:

#### Phase 1: Topic Exploration Validation
Valid states in sequence:
- inspiration_received -> inspiration_parsed
- inspiration_parsed -> topic_explored
- topic_explored -> topic_suggested
- topic_suggested -> topic_confirmed
- topic_confirmed -> ttd_iterative_creation

Invalid transitions:
- Skipping states (inspiration_received -> topic_explored)
- Backward transitions (topic_confirmed -> inspiration_parsed)
- Phase jumps (topic_exploration -> final_production)

#### Phase 2: TTD-DR Iteration Validation
Valid iteration states:
- ttd_iterative_creation -> iteration_active
- iteration_active -> round_X_variants_generated
- round_X_variants_generated -> round_X_research_complete
- round_X_research_complete -> round_X_quality_assessed
- round_X_quality_assessed -> round_X_gate_decision
- round_X_gate_decision -> [continue_iteration | early_completion | checkpoint_detected]

Special transition validation:
- Round numbers must increment sequentially (1->2->3->4->5)
- Quality gate decisions must match quality scores
- Checkpoint detection requires valid trigger conditions
- Early completion requires all dimensions >= Tier A

#### Phase 3: Final Production Validation
Valid final production states:
- [early_completion | iteration_complete] -> final_production
- final_production -> final_audit_complete
- final_audit_complete -> voice_validated
- voice_validated -> platform_adapted
- platform_adapted -> human_approved
- human_approved -> published

### Quality Gate Decision Validation
Verify gate decisions align with quality assessments:

#### Gate Decision Logic Validation
Check decision consistency:
- early_completion: All dimensions >= 80 points (Tier A)
- continue: At least one dimension < 80 points, no dimension < 60
- checkpoint_detected: At least one dimension < critical threshold
  - Accuracy checkpoint: accuracy_score < 60
  - Insight checkpoint: insight_score < 70 AND round > 3
  - Originality checkpoint: originality_score < 60

#### Quality Score Progression Validation
Validate quality improvement patterns:
- Scores generally improve round-over-round
- No unexplained dramatic drops (>20 points)
- Quality plateau detection triggers appropriate actions
- Checkpoint resolutions show measurable improvement

### Checkpoint Detection Validation
Verify checkpoint detection follows proper Claude Code architecture:

#### Detection Pattern Validation
Ensure proper detection sequence:
1. Agent detects threshold breach condition
2. Agent prepares checkpoint data
3. Agent returns data to Main Claude
4. Agent exits execution
5. Main Claude handles human interaction
6. Resolution recorded in registry

#### Checkpoint Data Consistency
Validate checkpoint data integrity:
- Detection conditions match quality scores
- Checkpoint type appropriate for triggering dimension
- Recommendations align with detected issues
- Resolution outcomes measurable and recorded

## Quality Progression Analysis

Implement comprehensive three-dimensional quality tracking:

### Accuracy Progression Tracking
Monitor accuracy dimension evolution:

#### Tier Progression Analysis
Track accuracy tier improvements:
- Document tier changes (D->C->B->A)
- Calculate improvement velocity
- Identify plateau patterns
- Detect regression triggers

#### Verification Effectiveness Tracking
Monitor verification quality:
- Fact verification success rates
- Source credibility improvements
- Confidence level progression
- Error detection and correction rates

### Insight Progression Tracking
Monitor insight dimension development:

#### Depth Level Evolution
Track analytical depth improvements:
- Depth level progression (1->2->3->4)
- Cross-domain connection increases
- Surprise factor development
- Perspective sophistication growth

#### Enhancement Effectiveness Analysis
Measure insight enhancement outcomes:
- Human collaboration impact on depth
- Enhancement strategy effectiveness
- Creative breakthrough identification
- Competitive positioning improvements

### Originality Progression Tracking
Monitor originality dimension advancement:

#### Similarity Score Reduction
Track originality improvements:
- Similarity score reduction over rounds
- Novel combination development
- Structural innovation progression
- Creative differentiation growth

#### Uniqueness Development Analysis
Measure originality enhancement:
- Concept combination novelty increases
- Citation balance optimization
- Market differentiation improvements
- Brand positioning strengthening

## Status Consistency Validation

Ensure system-wide status alignment and integrity:

### Registry-Metadata Alignment Validation
Cross-validate status consistency:

#### Core Status Fields Alignment
Compare critical status fields:
- article_id consistency across sources
- current_phase alignment
- iteration round synchronization
- quality scores consistency

#### Timestamp Validation
Verify temporal consistency:
- Update timestamps in logical sequence
- No future timestamps
- Reasonable time intervals between updates
- History preservation integrity

### Status History Integrity Validation
Ensure complete status tracking:

#### Transition Completeness
Validate transition logging:
- All major transitions recorded
- No missing transition steps
- Proper transition reasoning documented
- Outcome tracking comprehensive

#### History Consistency
Verify historical accuracy:
- No contradictory entries
- Logical progression maintained
- Quality improvement trends realistic
- Human intervention records complete

## Anomaly Detection and Recovery Recommendations

Implement intelligent anomaly detection with recovery guidance:

### Status Inconsistency Detection
Identify and report status alignment issues:

#### Critical Inconsistencies
Detect major alignment problems:
- Registry and metadata completely mismatched
- Impossible state transitions detected
- Quality scores wildly inconsistent
- Missing critical status transitions

#### Recovery Recommendations for Critical Issues
Provide recovery guidance:
- Use most recent timestamp as authoritative
- Reconstruct missing transitions from available data
- Reset to last known good state if necessary
- Manual review required for complex inconsistencies

#### Minor Inconsistencies
Detect and auto-resolve minor issues:
- Small quality score discrepancies (<5 points)
- Missing non-critical transition logs
- Minor timestamp ordering issues
- Incomplete but recoverable status data

#### Auto-Resolution for Minor Issues
Implement automatic fixes:
- Average quality scores where slight discrepancies exist
- Interpolate missing transition timestamps
- Fill missing non-critical status fields
- Update incomplete records with reasonable defaults

### Quality Progression Anomalies
Detect unusual quality patterns:

#### Regression Detection
Identify quality declines:
- Significant score drops (>15 points)
- Tier regression (A->C or worse)
- Plateau breaking downward
- Multiple dimension simultaneous decline

#### Unusual Improvement Patterns
Detect potentially invalid improvements:
- Dramatic improvements (>30 points single round)
- Impossible tier jumps (D->A single round)
- Inconsistent cross-dimensional improvements
- Enhancement without clear triggers

### Recovery Strategy Recommendations
Provide targeted recovery recommendations:

#### Status Recovery Strategies
Recommend specific recovery actions:
- Registry rebuild from metadata
- Metadata reconstruction from registry
- Status history recreation from available data
- Manual intervention required scenarios

#### Quality Progression Recovery
Recommend quality tracking fixes:
- Quality score recalculation from evaluator reports
- Missing quality data interpolation
- Anomaly investigation recommendations
- Quality validation re-execution

Execute comprehensive status validation and tracking with intelligent anomaly detection and recovery recommendations for optimal T1-TTD workflow integrity.