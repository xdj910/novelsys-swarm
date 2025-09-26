---
name: BASE_AGENT_TEMPLATE
description: Base template for all agents 
tools: Read, Write, Bash  # NO Task tool - prevents recursion
---

# BASE AGENT TEMPLATE - Context Firewall Enabled

## CRITICAL: DO NOT CREATE PYTHON SCRIPTS

You must DIRECTLY perform your task and save the result.
DO NOT create Python scripts or any executable files.
DO NOT use programming languages as an intermediary step.
Simply read the required files, execute your task, and save the output directly.

## CRITICAL: Context Firewall Output Requirements

**NOTE**: This section describes a Context Firewall design that was not fully implemented.
The system has been archived. Agents now save outputs directly to project directories.

### ORIGINAL DESIGN (for reference only):

1. **SUMMARY (50 chars max)** - Return to main thread
2. **DETAILS (unlimited)** - Save to file

### Output Structure (archived design)

YAML structure that was planned:
- summary: "[Core finding in 50 chars]" (returned to main thread)
- detail_file: ".claude/context/details/{your_agent_name}_{chapter}_{timestamp}.md"
- detail_content: Full analysis content with:
  * Complete analysis (unlimited length)
  * All findings, evidence, quotes, suggestions
  * Preserved details for later access

## Implementation Example

When analyzing a chapter:

**Implementation Process:**

1. **Perform full analysis:**
   - Analyze chapter content comprehensively
   - Generate complete analysis (10,000+ words if needed)

2. **Extract core summary:**
   - Compress key findings to max 50 characters
   - Example format: "Ch3:92/100,good dialogue,weak pacing,3 plot holes"

3. **Save full details:**
   - Use Write tool: `.claude/context/details/my_analysis.md`
   - Store complete analysis with all findings

4. **Return summary to main thread:**
   - Provide only the compressed 50-character summary
   - Preserve all detail information in file

## Benefits of Context Firewall

1. **70% Token Savings** - Main thread stays clean
2. **Zero Detail Loss** - Everything saved to files
3. **Better Performance** - Faster agent execution
4. **Cleaner Context** - No pollution between agents

## File Storage Convention

File structure that was planned:
- .claude/context/details/ directory containing:
  * continuity_guard_ch01_20250831.md
  * plot_hole_ch01_20250831.md
  * conflict_resolver_ch01_20250831.md
  * quality_scorer_ch01_20250831.md
  * index.json (Maps summaries to detail files)

## REMEMBER

- **ALWAYS** compress output to 50 chars for main thread
- **ALWAYS** save full details to file
- **NEVER** return full analysis to main thread
- **NEVER** lose any detail information

This is MANDATORY for all agents to reduce token usage by 70%.