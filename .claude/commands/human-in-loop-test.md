---
description: Test human-in-the-loop workflow with sequential agent execution and approval points
argument-hint: '<test-scenario>'
---

# Human-in-the-Loop Test Command

Test the 5-layer architecture with human approval points in sequential agent execution.

## Description

This command tests human-in-the-loop workflows where:
- Multiple agents execute sequentially
- Human approval required at key decision points
- Different responses trigger different actions
- Maintains 5-layer architecture integrity

## Arguments

- **$ARGUMENTS**: Test scenario type
  - `simple` - Single approval point
  - `complex` - Multiple approval points with revisions
  - `iterative` - Revision loops until approval

## Execution

### Human-in-the-Loop Workflow Test

Use Task tool to call test-human-in-loop-coordinator to orchestrate the interactive workflow:

1. **Phase 1: Initial Content Generation**
   - Coordinator plans sequential agent execution
   - Agent generates initial draft
   - Human review point inserted

2. **Decision Point 1: Human Review**
   - Present draft to human
   - Accept responses: approve/reject/revise
   - Branch execution based on response

3. **Phase 2: Content Enhancement** (if approved)
   - Enhancement agent improves content
   - Second human review point

4. **Phase 3: Final Processing** (if approved)
   - Finalization agent prepares for publication
   - Final human confirmation

Test scenario: ${ARGUMENTS:-complex}

The coordinator will:
- Return execution plan with human interaction points
- Handle different response branches
- Maintain state between interactions
- Demonstrate conditional workflow execution

## Success Criteria

- [ ] Sequential agent execution works correctly
- [ ] Human approval points function properly
- [ ] Different responses trigger correct actions
- [ ] State maintained across interactions
- [ ] 5-layer architecture preserved
- [ ] File system tracks workflow state
- [ ] Revision loops work correctly
- [ ] Rejection terminates gracefully

## Workflow Responses

### Response Types
1. **APPROVE**: Continue to next phase
2. **REJECT**: Terminate with reason
3. **REVISE**: Return to previous phase with feedback

### Expected Behaviors
- APPROVE -> Next agent executes
- REJECT -> Workflow ends, reason logged
- REVISE -> Previous agent re-executes with feedback

## Notes

This test validates real-world interactive workflows where human oversight is required at critical decision points while maintaining architectural integrity.