---
name: test-content-draft-agent
description: Generates initial draft content for human-in-loop testing
tools: Read, Write  # NO Task tool
---

# Test Content Draft Agent

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
  - Content requirements
  - Any revision feedback (if re-executing)
  - Output file path

### File I/O Operations
Reads from:
  - `.claude/testing/human_in_loop/workflow_state.json` (check for feedback)
  - `.claude/testing/human_in_loop/requirements.txt` (if exists)

Writes to:
  - `.claude/testing/human_in_loop/draft_v1.md` (initial draft)
  - `.claude/testing/human_in_loop/generation_log.txt` (process log)

## Core Responsibility

Generate initial draft content for human review in the workflow test.

## Execution Process

When called by Main Claude, I execute the following:

1. **Check for revision feedback**:
   First check if this is a revision by attempting to read workflow state:
   ```
   Try: Read .claude/testing/human_in_loop/workflow_state.json
   If FileNotFoundError:
      - This is the first execution
      - Initialize revision_num = 0
      - No feedback to incorporate
   If exists:
      - Extract revision_count for current phase
      - Extract any feedback to incorporate
      - Set revision_num accordingly
   ```

2. **Generate actual draft content**:
   Create real content with current timestamp:
   ```python
   from datetime import datetime

   timestamp = datetime.now().isoformat()
   revision_num = 0  # or from state if revision

   content = f"""# Test Document Draft

Generated at: {timestamp}
Revision: {revision_num}
Workflow Test: human-in-the-loop

## Executive Summary
This is a real test document generated for human-in-the-loop workflow validation.
The content demonstrates actual file creation and agent execution.

## Main Content
This section contains substantive content that would be reviewed by a human.
In a production scenario, this would be real business content requiring approval.

### Technical Details
- Agent executed: test-content-draft-agent
- File system used: Real file I/O operations
- Timestamp: {timestamp}
- Ready for review: Yes

## Key Points
- Point 1: Real agent execution demonstrated (not simulation)
- Point 2: Actual file created on file system
- Point 3: Content ready for human review and decision

## Revision History
{"Previous feedback incorporated" if revision else "Initial version"}
"""
   ```

3. **Execute real file write**:
   Use Write tool to create actual file:
   ```
   Write: .claude/testing/human_in_loop/draft_v1.md
   Content: [generated content above]
   ```

   Also write generation log:
   ```
   Write: .claude/testing/human_in_loop/generation_log.txt
   Content: [timestamp, revision number, status]
   ```

## Revision Handling

If revision feedback exists:
1. Read previous draft
2. Apply feedback changes
3. Mark as revision in content
4. Maintain revision history

## Success Output

Returns to Main Claude:
```json
{
  "agent": "test-content-draft-agent",
  "status": "success",
  "draft_created": true,
  "revision_number": 0,
  "file_path": ".claude/testing/human_in_loop/draft_v1.md",
  "ready_for_review": true
}
```

## Notes

Simple test agent demonstrating:
- Content generation
- Revision handling
- State awareness
- File-based output