---
name: test-python-analyzer-agent
description: Analyzes transformed data from stage 2 using Python script for pipeline testing
tools: Read, Write, Bash  # NO Task tool
---

# Test Python Analyzer Agent

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
  - Input file path (stage2_data.json)
  - Analysis parameters
  - Output file paths

### File I/O Operations
Reads from:
  - `.claude/testing/python_pipeline/stage2_data.json` (transformed data)
  - `.claude/testing/python_pipeline/stage2_report.json` (transformation report)
  - `.claude/testing/python_pipeline/stage1_report.json` (original report)

Writes to:
  - `.claude/testing/python_pipeline/data_analyzer.py` (Python script)
  - `.claude/testing/python_pipeline/stage3_final.json` (final analysis)
  - `.claude/testing/python_pipeline/stage3_report.json` (analysis report)

## Core Responsibility

Analyze transformed data from stage 2 using Python script as the final stage of the pipeline.

## Execution Process

When called by Main Claude, I execute the following:

1. **Verify input files exist**:
   Use Bash tool to check all required input files:
   ```
   Bash: ls -la .claude/testing/python_pipeline/stage*.json
   ```

2. **Verify analyzer script exists**:
   Use Bash tool to check if the Python script exists:
   ```
   Bash: ls -la .claude/testing/python_pipeline/data_analyzer.py
   ```

3. **Execute analyzer script**:
   Use Bash tool to run the existing script:
   ```
   Bash: cd .claude/testing/python_pipeline && python data_analyzer.py
   ```

   The script (data_analyzer.py) performs:
   - Loads stage2_data.json and all previous reports
   - Performs deep analysis on the transformed data
   - Validates data flow integrity across pipeline stages
   - Identifies patterns, outliers, and correlations
   - Saves comprehensive analysis to stage3_analysis.json
   - Saves report to stage3_report.json
   - Creates human-readable PIPELINE_SUMMARY.txt

4. **Verify final outputs**:
   Use Bash to confirm all outputs:
   ```
   Bash: ls -la .claude/testing/python_pipeline/stage3_*.json
   ```

5. **Read final result for Main Claude**:
   Use Read tool to get the final analysis:
   ```
   Read: .claude/testing/python_pipeline/stage3_final.json
   ```
   Return the content to Main Claude for presentation.

## Success Output

Returns to Main Claude:
```json
{
  "agent": "test-python-analyzer-agent",
  "status": "success",
  "python_script_created": "data_analyzer.py",
  "analysis_completed": true,
  "items_analyzed": 100,
  "analysis_types": 6,
  "output_files": [
    "stage3_final.json",
    "stage3_report.json"
  ],
  "pipeline_complete": true,
  "ready_for_presentation": true
}
```

## Notes

Final stage agent demonstrating:
- Reading outputs from all previous stages
- Comprehensive Python data analysis
- Pipeline integrity verification
- Final results preparation for Main Claude