# test-recursion

## Purpose
Test proper Task tool usage patterns that avoid recursion crashes in Claude Code.

## Architecture (方案A - 扁平化架构)
```
User -> /test-recursion
         v
    Main Claude (has Task)
         ├-> Task -> test-coordinator (planning only, no Task)
         └-> Task -> test-agent (execution only, no Task)
``

## Instructions
YOU (main Claude) directly coordinate both agents:

### STEP 1: Get Test Plan
Use Task tool to call test-coordinator:
- subagent_type: "test-coordinator"  
- description: "Create test execution plan"
- prompt: "Analyze requirements and create a detailed test plan. Return the plan structure only. Do NOT execute anything."

### STEP 2: Execute Test  
Use Task tool to call test-agent:
- subagent_type: "test-agent"
- description: "Execute extended stability test"
- prompt: "Execute your full extended stability test process. Create test.txt and run all 10 phases. This will take 1-2 minutes."

### STEP 3: Verify Results
Read the created test files and report:
- Test plan from coordinator
- Execution results from agent
- Architecture validation: No recursion crashes

## Key Points
- **Only main Claude uses Task tool**
- **Subagents cannot call other subagents**
- **This prevents recursion and crashes**

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/test/test-plan.json` (test execution plan from coordinator)
  - `.claude/test/test.txt` (test results from agent)
  - `.claude/test/test-results.json` (detailed test results)

- **Writes to**:
  - `.claude/test/test-plan.json` (generated test plan)
  - `.claude/test/test.txt` (test execution log)
  - `.claude/test/test-results.json` (test outcome summary)
  - `.claude/test/recursion-validation.txt` (recursion safety verification)