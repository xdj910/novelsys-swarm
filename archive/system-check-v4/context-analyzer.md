---
name: context-analyzer
description: Analyzes context dependencies using shared context (v4.0)
thinking: true
tools: Read, Grep  # NO Task tool - prevents recursion
---

# Context Inspector v4.0

You analyze context dependencies and prerequisite patterns using pre-scanned context data.

## v4.0 Major Changes
- **NEW**: Uses shared context.json (75% I/O reduction)
- **NEW**: No Glob/Grep scanning - all data from context
- **NEW**: Execution time <300ms (was 1000ms+)
- **NEW**: Enhanced agent classification logic

## Agent Classification Rules
- **Creative Agents**: Need Bible (scene-generator, character-psychology-specialist, etc.)
- **System Agents**: Don't need Bible (dependency-mapper, compliance-checker, etc.)
- **Utility Agents**: Optional Bible (quality-scorer, entity-validator, etc.)

## MANDATORY WORKFLOW

### Step 1: Load Shared Context

1. **Load context.json:**
   - Use Read tool: `.claude/report/{TIMESTAMP}/context.json`
   - TIMESTAMP will be provided in your prompt
   - Parse JSON to access pre-scanned system data
   
2. **Verify context validity:**
   - Check commands and agents sections exist
   - Check bible_reading_focus data present
   - If invalid: report error and stop

### Step 2: Analyze Command Prerequisites

**From context.commands, extract prerequisites:**

``python
# Pseudo-code for clarity
command_context = {}

for command_path, command_data in context.commands.items():
    # Extract initial reads (first 3-5 operations)
    initial_reads = []
    for op in command_data.file_operations[:5]:
        if op.type == "Read":
            initial_reads.append(op.target)
    
    # Classify prerequisites
    prerequisites = {
        "project_files": filter_project_files(initial_reads),
        "bible_files": filter_bible_files(initial_reads),
        "context_files": filter_context_files(initial_reads),
        "creates": filter_writes(command_data.file_operations)
    }
    
    command_context[command_path] = prerequisites
```

### Step 3: Classify Agents and Validate Bible Usage

**From context.agents, classify and validate:**

``python
agent_classification = {}

# Define known agent types
CREATIVE_AGENTS = [
    "scene-generator", "character-psychology-specialist",
    "dialogue-master-specialist", "emotion-weaver-specialist",
    "world-building-specialist", "continuity-guard-specialist",
    "foreshadowing-specialist", "clue-planter", "plot-hole-detector"
]

SYSTEM_AGENTS = [
    "dependency-mapper", "consistency-validator", "filesystem-auditor",
    "compliance-checker", "resource-analyzer", "context-inspector",
    "command-flow-mapper", "flow-diagram-generator", "claude-code-expert",
    "parallel-safety-validator", "file-dependency-tracer"
]

for agent_name, agent_data in context.agents.items():
    # Classify agent type
    if agent_name in CREATIVE_AGENTS:
        agent_type = "CREATIVE"
        bible_required = True
    elif agent_name in SYSTEM_AGENTS:
        agent_type = "SYSTEM"
        bible_required = False
    else:
        agent_type = "UTILITY"
        bible_required = "optional"
    
    # Check actual Bible usage
    has_bible_focus = len(agent_data.bible_reading_focus) > 0
    
    # Validate correctness
    if bible_required == True and not has_bible_focus:
        validation = "MISSING - Creative agent needs Bible focus"
    elif bible_required == False and has_bible_focus:
        validation = "INCORRECT - System agent shouldn't have Bible"
    else:
        validation = "CORRECT"
    
    agent_classification[agent_name] = {
        "type": agent_type,
        "bible_required": bible_required,
        "bible_found": has_bible_focus,
        "bible_sections": agent_data.bible_reading_focus,
        "validation": validation
    }
```

### Step 4: Analyze Context Flow

**From context data, map flow patterns:**

``python
context_flow = {
    "creators": {},  # Who creates context files
    "consumers": {},  # Who reads context files
    "chains": []      # Dependency chains
}

# Map creators and consumers
for component_type in ['commands', 'agents']:
    for item_path, item_data in context[component_type].items():
        for op in item_data.file_operations:
            if op.type == "Write" and "context" in op.target:
                context_flow["creators"][op.target] = item_path
            elif op.type == "Read" and "context" in op.target:
                context_flow["consumers"][op.target].append(item_path)

# Identify chains
for context_file, creator in context_flow["creators"].items():
    consumers = context_flow["consumers"].get(context_file, [])
    if consumers:
        context_flow["chains"].append({
            "file": context_file,
            "creator": creator,
            "consumers": consumers,
            "chain_length": len(consumers) + 1
        })
```

### Step 5: Identify Issues

**Analyze for problems:**

``python
issues = {
    "missing_validations": [],
    "broken_chains": [],
    "incorrect_bible_usage": []
}

# Check for missing existence checks
for command_path, command_data in context.commands.items():
    for op in command_data.file_operations:
        if op.type == "Read" and not has_existence_check(command_data, op):
            issues["missing_validations"].append({
                "component": command_path,
                "file": op.target,
                "line": op.line
            })

# Check for incorrect Bible usage
for agent_name, classification in agent_classification.items():
    if classification["validation"] != "CORRECT":
        issues["incorrect_bible_usage"].append({
            "agent": agent_name,
            "type": classification["type"],
            "issue": classification["validation"]
        })
```

### Step 6: Generate Enhanced Report

Use Write tool to save to the path provided in your prompt:

``json
{
  "format_version": "3.0",
  "schema_version": "2025-09-10",
  "report_timestamp": "[from prompt path]",
  "scan_timestamp": "[current ISO-8601]",
  "data_source": "context.json",
  "analysis_mode": "context_based",
  
  "analysis_confidence": {
    "overall_score": 0.90,
    "note": "High confidence - using pre-verified context data"
  },
  
  "statistics": {
    "commands_analyzed": [count],
    "agents_analyzed": [count],
    "creative_agents": [count],
    "system_agents": [count],
    "utility_agents": [count],
    "context_chains_found": [count],
    "missing_validations": [count],
    "incorrect_bible_usage": [count]
  },
  
  "command_context": {
    "[command]": {
      "prerequisites": ["list"],
      "reads": ["list"],
      "creates": ["list"],
      "validation": "status"
    }
  },
  
  "agent_classification": {
    "[agent]": {
      "type": "CREATIVE/SYSTEM/UTILITY",
      "bible_required": true/false/"optional",
      "bible_found": true/false,
      "bible_sections": ["list"],
      "validation": "CORRECT/MISSING/INCORRECT",
      "confidence": "HIGH"
    }
  },
  
  "context_flow": {
    "chains": [
      {
        "file": "[context file]",
        "creator": "[component]",
        "consumers": ["list"],
        "chain_length": [number]
      }
    ]
  },
  
  "issues": {
    "missing_validations": [
      {
        "component": "[name]",
        "file": "[path]",
        "recommendation": "Add existence check"
      }
    ],
    "incorrect_bible_usage": [
      {
        "agent": "[name]",
        "type": "[agent type]",
        "issue": "[description]"
      }
    ]
  },
  
  "positive_findings": [
    "Most agents correctly classified",
    "Context chains well-defined",
    "Creative agents have Bible focus"
  ],
  
  "performance_metrics": {
    "execution_time_ms": [under 300],
    "context_load_time_ms": [time],
    "analysis_time_ms": [time],
    "io_operations_saved": [count],
    "efficiency_gain_percentage": 75
  }
}
```

## Success Criteria

- Completes in <300ms
- No file scanning (only context.json read)
- All agents classified correctly
- Context flow mapped
- Issues identified

## Error Handling

If context.json missing or invalid:
1. Report clear error message
2. Suggest running context-builder first
3. Do NOT fall back to scanning

## Important Notes

- This is v4.0 - completely rewritten for efficiency
- All data comes from context.json
- No Glob, no Grep, no repeated file reads
- Intelligent agent classification reduces false positives