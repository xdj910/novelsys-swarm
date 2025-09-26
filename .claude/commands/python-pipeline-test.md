---
description: Test Python script pipeline through multiple agents with data transformation
argument-hint: '<data-size>'
---

# Python Pipeline Test Command

Test sequential Python script execution through multiple agents with data transformation.

## Description

This command tests a data processing pipeline where:
- Agent 1 generates data using Python
- Agent 2 transforms the data using Python
- Agent 3 analyzes the transformed data using Python
- Main Claude reads and presents the final results

## Arguments

- **$ARGUMENTS**: Data size for testing
  - `small` - 10 data points
  - `medium` - 100 data points (default)
  - `large` - 1000 data points

## Execution

### Python Pipeline Test Workflow

Use Task tool to call test-python-pipeline-coordinator to get the execution plan.

After receiving the plan from coordinator, Main Claude MUST:
1. Execute each agent in sequence
2. After each agent, verify output files exist using Bash
3. Only proceed to next agent if files are confirmed
4. If any verification fails, report the error and stop

Verification commands to use (use forward slashes or relative paths):
- After Agent 1: `ls -la .claude/testing/python_pipeline/stage1_*.json`
- After Agent 2: `ls -la .claude/testing/python_pipeline/stage2_*.json`
- After Agent 3: `ls -la .claude/testing/python_pipeline/stage3_*.json`

Note: Always use relative paths or forward slashes to avoid Windows path escaping issues.

1. **Phase 1: Data Generation**
   - Agent 1 generates test data using Python
   - Creates JSON report with statistics

2. **Phase 2: Data Transformation**
   - Agent 2 reads Agent 1's output
   - Applies transformations using Python
   - Creates enhanced report

3. **Phase 3: Data Analysis**
   - Agent 3 reads Agent 2's output
   - Performs analysis using Python
   - Creates final report

4. **Phase 4: Result Presentation**
   - Main Claude reads final output
   - Presents results to user

Test parameters:
- Data size: ${ARGUMENTS:-medium}
- Pipeline stages: 3
- Output format: JSON

## Success Criteria

- [ ] Agent 1 Python script generates data successfully
- [ ] Agent 2 Python script reads and transforms data
- [ ] Agent 3 Python script analyzes transformed data
- [ ] Data flows correctly through pipeline
- [ ] No data loss between stages
- [ ] Final output readable by Main Claude

## Expected Output

Main Claude will present:
- Original data statistics from Agent 1
- Transformation summary from Agent 2
- Analysis results from Agent 3
- Pipeline execution metrics

## Notes

This test validates Python script interoperability between agents while maintaining 5-layer architecture.