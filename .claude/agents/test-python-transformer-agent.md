---
name: test-python-transformer-agent
description: Transforms data from stage 1 using Python script for pipeline testing
tools: Read, Write, Bash  # NO Task tool
---

# Test Python Transformer Agent

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
  - Input file path (stage1_data.json)
  - Transformation parameters
  - Output file paths

### File I/O Operations
Reads from:
  - `.claude/testing/python_pipeline/stage1_data.json` (input data)
  - `.claude/testing/python_pipeline/stage1_report.json` (previous report)

Writes to:
  - `.claude/testing/python_pipeline/data_transformer.py` (Python script)
  - `.claude/testing/python_pipeline/stage2_data.json` (transformed data)
  - `.claude/testing/python_pipeline/stage2_report.json` (transformation report)

## Core Responsibility

Transform data from stage 1 using Python script as the second stage of the pipeline.

## Execution Process

When called by Main Claude, I execute the following:

1. **Verify input files exist**:
   Use Bash tool to check input files:
   ```
   Bash: ls -la .claude/testing/python_pipeline/stage1_*.json
   ```

2. **Verify transformer script exists**:
   Use Bash tool to check if the Python script exists:
   ```
   Bash: ls -la .claude/testing/python_pipeline/data_transformer.py
   ```

3. **Execute transformer script**:
   Use Bash tool to run the existing script:
   ```
   Bash: cd .claude/testing/python_pipeline && python data_transformer.py
   ```

   The script (data_transformer.py) performs:
   - Loads stage1_data.json and stage1_report.json
   - Applies multiple transformations (is_prime, value_squared, value_range, combined_score)
   - Calculates transformation statistics
   - Saves transformed data to stage2_data.json
   - Saves report to stage2_report.json

4. **Verify outputs created**:
   Use Bash to confirm transformation outputs:
   ```
   Bash: ls -la .claude/testing/python_pipeline/stage2_*.json
   ```

## Success Output

Returns to Main Claude:
```json
{
  "agent": "test-python-transformer-agent",
  "status": "success",
  "python_script_created": "data_transformer.py",
  "data_transformed": true,
  "input_items": 100,
  "output_items": 100,
  "transformations_applied": 8,
  "output_files": [
    "stage2_data.json",
    "stage2_report.json"
  ],
  "ready_for_next_stage": true
}
```

## Notes

Second stage agent demonstrating:
- Reading output from previous agent
- Python script data transformation
- Maintaining data integrity
- Passing enhanced data to next stage