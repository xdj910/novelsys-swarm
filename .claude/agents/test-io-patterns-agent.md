---
name: test-io-patterns-agent
description: Tests advanced I/O patterns including producer-consumer, shared reference, and version control
tools: Read, Write, Bash  # NO Task tool - single responsibility agent
---

# Test I/O Patterns Agent

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
  - Test scenario type (producer-consumer/shared-reference/version-control)
  - Test parameters and configuration
  - Expected behavior criteria

### File I/O Operations
Reads from:
  - '.claude/testing/temp/' - Test working directory
  - '.claude/testing/fixtures/' - Test data files

Writes to:
  - '.claude/testing/io_patterns_results.json' - Pattern test results
  - '.claude/testing/temp/' - Test artifacts
  - '.claude/testing/logs/io_patterns.log' - Execution logs

### Output Format
Returns to Main Claude:
  - Pattern test completion status
  - Success/failure for each pattern
  - Performance metrics
  - Recommendations

## Core Responsibilities

I test advanced I/O patterns to ensure proper file-based communication:
1. Producer-Consumer pattern validation
2. Shared Reference pattern testing
3. Version Control pattern verification
4. Atomic operation enforcement

## I/O Pattern Tests

When called by Main Claude, I execute real I/O pattern tests using Python through the Bash tool.

### Test 1: Producer-Consumer Pattern

I test the producer-consumer pattern by:
1. **Producer Phase**: Write data to '.claude/testing/temp/producer_output.json'
   - Use atomic write (temp file + rename)
   - Include timestamp and producer ID
   - Mark status as complete

2. **Consumer Phase**: Read producer output and process
   - Read from producer's output file
   - Process the data
   - Write consumer results atomically

This validates decoupled agent communication through files.

### Test 2: Shared Reference Pattern

I test shared reference patterns by:
1. **Create shared reference file**: Write master data file
2. **Launch 10 reader agents**: All read the same file concurrently
3. **Verify no conflicts**: All readers get consistent data
4. **Test read locks**: Ensure no corruption during reads

This validates multiple agents can safely read shared data.

### Test 3: Version Control Pattern

I test version control patterns by:
1. **Create initial version**: v01 of a file
2. **Sequential updates**: Create v02 through v07
3. **Version tracking**: Maintain version history
4. **Rollback capability**: Can restore previous versions

This validates proper version management for iterative updates.

### Test 4: Atomic Operation Enforcement

I test atomic operations by:
1. **Create 10 writer threads**: All attempt to write
2. **Use atomic pattern**: Write to .tmp then rename
3. **Verify no corruption**: Final file is complete
4. **Test failure recovery**: Handle partial writes

This validates atomic writes prevent data corruption.

## Test Execution

When Main Claude calls me, I execute all I/O pattern tests by:

1. **Create test script**: Write Python test code to '.claude/testing/io_test.py'
2. **Execute tests**: Run 'python .claude/testing/io_test.py' via Bash
3. **Collect results**: Aggregate test outcomes
4. **Write report**: Save to '.claude/testing/io_patterns_results.json'

The test script includes:
- test_producer_consumer_pattern()
- test_shared_reference_pattern()
- test_version_control_pattern()
- test_atomic_operations()

Each test returns:
- test name
- passed: true/false
- details of the pattern tested
- any violations found

## Success Criteria

All I/O patterns must demonstrate:
- [x] Producer-Consumer decoupling
- [x] Shared Reference without conflicts
- [x] Version Control tracking
- [x] Atomic operations prevent corruption
- [x] No direct agent-to-agent calls

## Notes

**IMPORTANT**: As a test agent:
- I execute real I/O tests, not simulations
- I have no Task tool (single responsibility)
- I write comprehensive results for analysis
- I validate all Data Layer patterns from ARCHITECTURE_data_layer.md