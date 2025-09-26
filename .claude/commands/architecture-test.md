---
description: Execute Claude Code architecture standardization validation tests for system stability and compliance
argument-hint: '<test-type>'
---

# Architecture Test Command

Execute comprehensive Claude Code architecture validation tests to verify recursion protection, architecture patterns, I/O flows, and standardization compliance.

## Description

This command executes a comprehensive architecture test suite through a coordinator-managed workflow. The process involves two phases: first getting an execution plan from the coordinator, then executing that plan through multiple test agents.

**IMPORTANT**: This is a multi-step execution command that requires Main Claude to:
1. Call the coordinator to get the execution plan
2. Execute each phase of the returned plan sequentially
3. Complete all phases for full architecture validation

The test suite contains 17+ test scenarios to validate the NOVELSYS-SWARM system's Claude Code architecture implementation against 2024-2025 standards. Tests run in complete isolation without affecting the existing system, with automatic cleanup of temporary test files upon completion.

## Arguments

- **$ARGUMENTS**: Test type and scope parameters (optional)
  - `full` - Complete test suite (default)
  - `recursion` - Recursion protection tests only
  - `architecture` - Architecture pattern tests only
  - `io` - I/O flow tests only
  - `compliance` - Standardization compliance tests only
  - `quick` - Quick test (core scenarios)

## Execution

### Architecture Validation Test Execution

Execute comprehensive Claude Code architecture validation testing through coordinator-managed workflow.

**CRITICAL**: Main Claude must execute the complete workflow as follows:

1. **Phase 1: Get Execution Plan**
   - Use Task to call test-architecture-coordinator
   - Coordinator will return JSON execution plan with 6 phases
   - Plan specifies agents to execute and their sequence

2. **Phase 2: Execute Plan**
   - Main Claude MUST execute each phase in the returned plan
   - Use Task to call each agent specified in the plan
   - Execute phases sequentially: Environment Setup -> Core Tests -> I/O Tests -> Validation -> Results -> Cleanup

3. **Phase 3: Complete Workflow**
   - Follow the coordinator's plan completely
   - Do not stop after receiving the plan - execute it
   - Each phase must complete before proceeding to next phase

**Expected Execution Sequence (Main Claude must follow):**

After receiving the coordinator's JSON plan, Main Claude will execute:

1. **Environment Setup Phase:**
   - Task -> test-environment-setup-agent
   - Creates test directories and fixtures
   - Prepares test infrastructure

2. **Core Architecture Tests Phase:**
   - Task -> test-execution-agent
   - Executes recursion prevention, I/O isolation, architecture validation
   - Tests basic system compliance

3. **Real Parallel Execution Test Phase:**
   - Task -> test-parallel-coordinator (get parallel plan)
   - Task -> test-parallel-agent-a, test-parallel-agent-b, test-parallel-agent-c (simultaneously)
   - Validates true concurrent execution

4. **Advanced I/O Pattern Tests Phase:**
   - Task -> test-io-patterns-agent
   - Tests producer-consumer, shared-reference, version-control patterns

5. **Format and Standards Validation Phase:**
   - Task -> test-validation-agent
   - Validates documentation formats and JSON plan structures

6. **Result Collection Phase:**
   - Task -> test-result-collector-agent
   - Aggregates all test results and generates final report

7. **Safe Cleanup Phase:**
   - Task -> test-cleanup-agent
   - Cleans only .claude/testing/temp/ directory

Test parameters:
- Test type: ${ARGUMENTS:-full}
- Expected duration: 10-15 minutes
- Total phases: 6-7
- Safe cleanup: Only .claude/testing/temp/ directory

The test requires the following components to be present:
- test-architecture-coordinator
- test-environment-setup-agent
- test-execution-agent
- test-result-collector-agent
- test-cleanup-agent

If these components are not available, they must be created first before running the test.

## Cleanup Strategy

**IMPORTANT**: Cleanup operations strictly limited to `.claude/testing/` directory:

```bash
# Correct cleanup scope
.claude/testing/temp/*       # Temporary test files
.claude/testing/fixtures/*   # Test fixtures (if needed)

# Never clean
.claude/commands/*           # Command files
.claude/agents/*             # Agent files
.claude/testing/reports/*    # Test reports
.claude/testing/framework/*  # Test framework
```

## Output

### Generated File Locations
- **Test Report**: `.claude/testing/reports/test_summary_[timestamp].md`
- **Validation Log**: `.claude/testing/reports/validation.log`

### Report Content
1. Recursion safety validation results
2. Parallel execution test results
3. I/O isolation validation results
4. Standards compliance check results
5. Improvement recommendations

## Success Criteria

**Complete Execution Requirements:**
- [ ] Phase 1: Coordinator returns complete JSON execution plan
- [ ] Phase 2: Main Claude executes ALL phases in the plan (not just gets the plan)
- [ ] All 6-7 phases complete successfully in sequence
- [ ] Environment setup, tests, parallel execution, I/O patterns, validation, results, cleanup

**Test Results Requirements:**
- [ ] All 17+ tests pass with 100% success rate
- [ ] Zero recursion violations detected (no Task in subagents)
- [ ] Parallel execution efficiency > 50%
- [ ] All I/O patterns validate correctly
- [ ] Safe cleanup completes without touching production files
- [ ] Final test report generated in .claude/testing/reports/

## Next Steps

After successful execution:
- **Review results**: Check `.claude/testing/reports/final_report.md` for detailed analysis
- **Fix violations**: If any issues found, address Task tool violations in affected files
- **Run specific tests**: Use `/architecture-test recursion` to test only specific areas
- **Multi-coordinator test**: Run `/multi-coordinator-test` to validate coordinator collaboration

## Notes

### Safety Assurance
- **Cleanup scope restriction**: Only clean files under `.claude/testing/temp/`
- **Protect production files**: Never touch `.claude/commands/` and `.claude/agents/`
- **Preserve test reports**: `.claude/testing/reports/` permanently retained
- **No destructive operations**: Never delete framework or command files