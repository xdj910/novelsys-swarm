---
description: Execute real parallel execution test to validate Claude Code concurrent capabilities
argument-hint: '<test-mode>'
---

# Parallel Test Command

Test true parallel execution capabilities of the Claude Code architecture by running multiple agents simultaneously and measuring performance gains.

## Description

This command executes a real parallel execution test to validate that Main Claude can successfully coordinate multiple agents running concurrently through the Task tool. Unlike simulation-based tests, this performs actual parallel agent execution and measures true performance improvements.

## Arguments

- **$ARGUMENTS**: Test mode (optional)
  - `full` - Complete parallel test with baseline comparison (default)
  - `quick` - Parallel execution only
  - `baseline` - Serial execution baseline only

## Execution

### Parallel Test Execution

Use the test-parallel-coordinator subagent to orchestrate real parallel execution testing.

The coordinator will plan:
1. Test environment setup with shared data
2. Serial baseline execution (agents run one by one)
3. Parallel execution (agents run simultaneously via Task calls)
4. Performance analysis and efficiency calculation

Test parameters:
- Test mode: ${ARGUMENTS:-full}
- Expected efficiency gain: >50%
- Concurrent agents: 3 (test-parallel-agent-a, b, c)

Main Claude will execute the parallel phase by calling all three test agents simultaneously:
```
Task -> test-parallel-agent-a (concurrent)
Task -> test-parallel-agent-b (concurrent)
Task -> test-parallel-agent-c (concurrent)
```

## Success Criteria

- [x] Serial baseline completes successfully
- [x] Parallel execution shows overlapping timestamps
- [x] Performance efficiency gain >50%
- [x] No file corruption during concurrent access
- [x] All agents complete independently

## Expected Results

Successful parallel testing demonstrates:
- **True Concurrency**: Agent execution times overlap
- **Performance Gain**: 60-70% efficiency improvement
- **File Safety**: Concurrent file access without corruption
- **Architecture Validation**: Claude Code supports real parallel execution

## Output

### Generated Files
- **Test Results**: `.claude/testing/temp/agent_*_result.json`
- **Performance Report**: `.claude/testing/reports/parallel_test_results.json`
- **Execution Logs**: `.claude/testing/temp/agent_*_log.txt`

## Notes

This test validates the core Claude Code architecture principle that agents can execute independently and concurrently through file-based communication, demonstrating true parallel processing capabilities.