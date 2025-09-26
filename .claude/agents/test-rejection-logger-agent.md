---
name: test-rejection-logger-agent
description: Logs rejection reasons and workflow termination details for human-in-loop testing
tools: Read, Write  # NO Task tool
---

# Test Rejection Logger Agent

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
  - Rejection phase
  - Rejection reason
  - Workflow state at rejection
  - Files created before rejection

### File I/O Operations
Reads from:
  - `.claude/testing/human_in_loop/workflow_state.json`
  - Any draft files created before rejection

Writes to:
  - `.claude/testing/human_in_loop/rejection_log.json`
  - `.claude/testing/human_in_loop/termination_report.md`

## Core Responsibility

Log workflow rejections and create termination reports for human-in-loop test validation.

## Logging Process

When called by Main Claude after a REJECT response:

1. **Capture rejection context**:
   - Phase where rejection occurred
   - Reason provided by human
   - Workflow progress at termination
   - Files created before rejection

2. **Create rejection log**:
   ```json
   {
     "rejection_id": "unique_id",
     "timestamp": "ISO-8601",
     "workflow_id": "test_workflow_id",
     "rejection_point": {
       "phase": "phase_2",
       "after_agent": "test-content-enhancer-agent",
       "files_reviewed": ["draft_v2.md"]
     },
     "rejection_details": {
       "reason": "Quality standards not met",
       "human_feedback": "Content lacks required technical depth",
       "workflow_state": "terminated"
     },
     "workflow_progress": {
       "phases_completed": ["phase_1"],
       "phases_rejected": ["phase_2"],
       "total_revisions": 0,
       "time_to_rejection": "5 minutes"
     },
     "artifacts_created": [
       "draft_v1.md",
       "draft_v2.md",
       "workflow_state.json"
     ]
   }
   ```

3. **Generate termination report**:
   ```markdown
   # Workflow Termination Report

   **Date**: [timestamp]
   **Workflow ID**: [workflow_id]
   **Status**: TERMINATED BY USER

   ## Rejection Summary
   - **Phase**: Phase 2 - Content Enhancement
   - **Reason**: Quality standards not met
   - **Feedback**: "Content lacks required technical depth"

   ## Workflow Progress at Termination
   - Phases Completed: 1 of 3
   - Files Created: 2
   - Human Interactions: 2
   - Final Decision: REJECT

   ## Artifacts Preserved
   All work products have been preserved for review:
   - draft_v1.md (Phase 1 - Approved)
   - draft_v2.md (Phase 2 - Rejected)
   - workflow_state.json (Complete history)

   ## Validation Success
   This rejection demonstrates:
   - Human-in-loop control working correctly
   - Workflow termination on demand
   - State preservation on rejection
   - Graceful handling of negative feedback

   ## Test Conclusion
   The human-in-loop test successfully validated:
   - Rejection paths execute correctly
   - Workflow terminates gracefully
   - Reasons are captured and logged
   - 5-layer architecture maintained throughout
   ```

## Success Output

Returns to Main Claude:
```json
{
  "agent": "test-rejection-logger-agent",
  "status": "success",
  "rejection_logged": true,
  "termination_report_created": true,
  "workflow_terminated_gracefully": true,
  "test_validation": "rejection_path_confirmed"
}
```

## Notes

This agent demonstrates:
- Graceful workflow termination
- Rejection reason capture
- Audit trail maintenance
- Test validation of negative paths