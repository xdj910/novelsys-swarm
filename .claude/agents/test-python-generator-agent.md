---
name: test-python-generator-agent
description: Generates test data using Python script for pipeline testing
tools: Write, Bash  # NO Task tool
---

# Test Python Generator Agent

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
  - Data size (small/medium/large)
  - Output file paths
  - Data generation parameters

### File I/O Operations
Writes to:
  - `.claude/testing/python_pipeline/data_generator.py` (Python script)
  - `.claude/testing/python_pipeline/stage1_data.json` (generated data)
  - `.claude/testing/python_pipeline/stage1_report.json` (generation report)

## Core Responsibility

Generate test data using Python script as the first stage of the pipeline.

## Execution Process

When called by Main Claude, I execute the following:

1. **Verify script exists**:
   Use Bash tool to check if the Python script exists:
   ```
   Bash: ls -la .claude/testing/python_pipeline/data_generator.py
   ```

2. **Execute the Python generator script**:
   Use Bash tool to run the existing script with parameters:
   ```
   Bash: cd .claude/testing/python_pipeline && python data_generator.py medium
   ```

   The script (data_generator.py) performs:
   - Generates test data based on size parameter
   - Calculates statistics on the data
   - Creates checksum for integrity
   - Saves data to stage1_data.json
   - Saves report to stage1_report.json

3. **Verify outputs created**:
   Use Bash to confirm files exist:
   ```bash
   ls -la .claude/testing/python_pipeline/stage1_*.json
   ```

## Success Output

Returns to Main Claude:
```json
{
  "agent": "test-python-generator-agent",
  "status": "success",
  "python_script_created": "data_generator.py",
  "data_generated": true,
  "output_files": [
    "stage1_data.json",
    "stage1_report.json"
  ],
  "items_generated": 100,
  "ready_for_next_stage": true
}
```

## Notes

First stage agent demonstrating:
- Python script creation and execution
- Data generation with statistics
- File output for next stage
- Report generation for tracking