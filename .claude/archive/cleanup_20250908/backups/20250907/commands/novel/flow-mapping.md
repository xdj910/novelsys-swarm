---
description: Map system execution flows and dependencies
---

# Flow Mapping - System Execution Blood Vessel Diagram

Maps the complete execution flow of all commands, showing detailed agent call trees and dependencies.

## Purpose

Generate a comprehensive "blood vessel diagram" showing:
- How each command executes step by step
- Which agents are called and in what order
- Nested agent-to-agent dependencies
- Parallel vs sequential execution patterns
- Complexity metrics for each command

## MANDATORY WORKFLOW

**CRITICAL: Throughout this workflow, you will see {FLOW_TIMESTAMP_VALUE} placeholders. You MUST replace ALL occurrences with the actual timestamp generated in Step 1 (e.g., "20250906_160000"). This ensures all components use the same timestamp.**

### Step 1: Initialize Flow Analysis Environment

1. **Create timestamp and temp directory:**
   - Use Bash tool: `date +%Y%m%d_%H%M%S`
   - Store the output as FLOW_TIMESTAMP_VALUE (e.g., "20250906_160000")
   - Use Bash tool: `mkdir -p .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}` (replace {FLOW_TIMESTAMP_VALUE} with actual value)
   - Remember this FLOW_TIMESTAMP_VALUE for all subsequent steps
   - Display: "[x] Temp directory created: .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}"
   - Display: "ℹ️ Analysis files will be preserved for debugging"

2. **Get command list:**
   - Use Glob tool: `.claude/commands/novel/*.md`
   - Store list of all command files
   - Count total commands for parallel execution
   - Display: "Found {N} commands to analyze"

### Step 2: Launch Dynamic Parallel Analysis

**CRITICAL: Execute ALL command-flow-mapper Tasks in ONE message for true parallel execution**

**IMPORTANT: In each Task's prompt below, replace ALL {FLOW_TIMESTAMP_VALUE} placeholders with the actual timestamp from Step 1**

For each command file found in Step 1, create and execute Task calls:

```
# All Tasks must be in the same message for parallel execution!
# Dynamic number based on actual command count

Task(
    subagent_type="command-flow-mapper",
    description="Analyze bible-create flow",
    prompt="""
    Analyze the execution flow of this command.
    
    Command file: .claude/commands/novel/bible-create.md
    Temp directory: .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}/
    
    Follow these steps:
    1. Read and parse the command file
    2. Extract all steps and agent calls (subagent_type patterns)
    3. For each agent found, read its file and find nested calls
    4. Build complete execution tree (max depth: 5)
    5. Calculate complexity metrics
    
    Save your analysis to:
    .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}/bible-create.json
    
    Include: step breakdown, agent tree, complexity score, issues found
    """
)

Task(
    subagent_type="command-flow-mapper",
    description="Analyze chapter-start flow",
    prompt="[Similar for chapter-start.md]"
)

# ... Continue for ALL commands found in Step 1
```

Display: "⏳ Launched {N} parallel mappers..."

### Step 3: Wait and Verify Completion

1. **Allow time for parallel execution:**
   - Use Bash tool: `sleep 5`  # Brief wait for fast commands
   - Use Bash tool: `sleep 10` # Additional wait for complex analysis
   - Display: "[x] Parallel analysis phase complete"

2. **Verify all reports generated:**
   - Count expected files:
     - Use Bash tool: `find .claude/commands/novel -name "*.md" -type f | wc -l`
     - Store as expected_count
   - Count actual files:
     - Use Bash tool: `find .claude/temp/flow_{FLOW_TIMESTAMP_VALUE} -name "*.json" -type f | wc -l`
     - Store as actual_count
   - Display status:
     - If counts match: Display "[x] All {count} command flows analyzed successfully"
     - If counts differ: Display warning and list missing files

### Step 4: Generate Unified Blood Vessel Diagram

Launch the diagram generator to merge all results:

```
Task(
    subagent_type="flow-diagram-generator",
    description="Generate system flow diagram",
    prompt="""
    Create a comprehensive system execution flow diagram.
    
    The timestamp for this run is: {FLOW_TIMESTAMP_VALUE}
    Read all analysis reports from: .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}/*.json
    
    Build unified diagram showing:
    1. Command Complexity Overview (grouped by high/medium/low)
    2. Detailed Execution Flows (step-by-step with nesting)
    3. Agent Dependency Graph (most called, deep chains)
    4. System-Wide Patterns (bottlenecks, unused agents)
    
    Include ASCII art visualizations and tree structures.
    
    Save final report to:
    .claude/report/{FLOW_TIMESTAMP_VALUE}/system_flow_diagram.md
    """
)
```

### Step 5: Preserve Analysis Files

1. **Verify final report exists:**
   - Use Bash tool:
   ```bash
   # Use the timestamp from Step 1
   if [ -f ".claude/report/{FLOW_TIMESTAMP_VALUE}/system_flow_diagram.md" ]; then
       echo "[x] Final report generated successfully"
   else
       echo "[ ] Error: Final report not found! Check temp files for debugging"
       exit 1
   fi
   ```

2. **Report temporary file location:**
   - Use Bash tool:
   ```bash
   # Use the timestamp from Step 1
   echo "=== Analysis Files Preserved ==="
   echo "Location: .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}/"
   echo "Contents: Individual command flow analysis JSON files"
   file_count=$(find .claude/temp/flow_{FLOW_TIMESTAMP_VALUE} -name "*.json" -type f 2>/dev/null | wc -l)
   echo "Files preserved: $file_count JSON reports"
   echo "Note: These files can be reviewed for debugging or detailed analysis"
   ```

3. **Display completion:**
   ```
   === Flow Mapping Complete ===
   
   Report saved to: .claude/report/{FLOW_TIMESTAMP_VALUE}/system_flow_diagram.md
   Temporary files: PRESERVED in .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}/
   ```

### Step 6: Display Summary

1. **Show report location:**
   - Use the FLOW_TIMESTAMP_VALUE from Step 1
   - Display: "Full report: .claude/report/{FLOW_TIMESTAMP_VALUE}/system_flow_diagram.md"

2. **Quick preview (first 50 lines):**
   - Use Read tool with limit=50: `.claude/report/{FLOW_TIMESTAMP_VALUE}/system_flow_diagram.md`
   - Display preview to user

## Expected Output Structure

```
NOVELSYS-SWARM System Execution Flows
======================================
Generated: 2024-XX-XX

## Command Complexity Summary
High (30+): chapter-start(45), project-new(38), system-check(35)
Medium (15-29): next-book(22), quality-check-cross(18)
Low (<15): status(5), project-list(7)

## Detailed Execution Flows

### chapter-start [Complexity: 45]
Step 1: Validate arguments
Step 2: Read context files
Step 5: Generate chapter
  +- director [depth:0]
      +- outline-generator [depth:1]
      +- scene-generator [depth:1] x3 PARALLEL
      |   +- character-psychology-specialist [depth:2]
      |   +- dialogue-master-specialist [depth:2]
      +- continuity-guard-specialist [depth:1]
          +- entity-validator [depth:2]

[... continues for all commands ...]
```

## Error Handling

- If some mappers fail: Continue with available reports
- If generator fails: Check temp files manually in .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}/
- Individual JSON files preserved for debugging

## Success Criteria

- All commands analyzed in parallel
- Complete execution trees mapped
- Unified diagram generated
- Analysis files preserved for review

## Notes

- Dynamic parallel execution based on command count
- Maximum recursion depth: 5 levels
- Temporary files preserved in .claude/temp/flow_{FLOW_TIMESTAMP_VALUE}/
- Results saved to permanent report directory .claude/report/
- Preserved files useful for debugging and detailed analysis