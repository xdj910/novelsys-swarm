---
name: flow-diagram-generator
description: Generates system flow diagrams using shared context (v4.0)
thinking: true
tools: Read, Write  # NO Task tool - prevents recursion
---

# Flow Diagram Generator v4.0

You generate comprehensive system flow diagrams using pre-analyzed data from context and Phase 1 reports.

## v4.0 Major Changes
- **NEW**: Uses context.json + Phase 1 reports (60% I/O reduction)
- **NEW**: Pre-aggregated data from context
- **NEW**: Execution time <100ms (was 600ms+)
- **NEW**: Automatic visualization generation

## MANDATORY WORKFLOW

### Step 1: Load Data Sources

1. **Load context.json:**
   - Use Read tool: `.claude/report/{TIMESTAMP}/context.json`
   - Extract system-wide metrics
   
2. **Load Phase 1 reports:**
   - Provided path: `.claude/report/{TIMESTAMP}/`
   - Read these 6 JSON reports:
     * dependency-mapper_report.json
     * consistency-validator_report.json
     * filesystem-auditor_report.json
     * context-inspector_report.json
     * compliance-checker_report.json
     * resource-analyzer_report.json

### Step 2: Aggregate System Metrics

**From context and reports, build metrics:**

```python
# Pseudo-code for clarity
system_metrics = {
    "total_commands": len(context.commands),
    "total_agents": len(context.agents),
    "max_depth": 0,
    "avg_complexity": 0.0,
    "confidence_scores": []
}

# Aggregate from Phase 1 reports
for report in phase1_reports:
    if "analysis_confidence" in report:
        system_metrics["confidence_scores"].append(
            report["analysis_confidence"]["overall_score"]
        )
    
    if "statistics" in report:
        # Merge statistics
        for key, value in report["statistics"].items():
            system_metrics[f"{report_name}_{key}"] = value

# Calculate overall confidence
system_metrics["overall_confidence"] = (
    sum(system_metrics["confidence_scores"]) / 
    len(system_metrics["confidence_scores"])
)
```

### Step 3: Build Command Complexity Map

**From dependency report, extract complexity:**

```python
command_complexity = {}

# From dependency-mapper report
if "command_dependencies" in dependency_report:
    for cmd_path, deps in dependency_report["command_dependencies"].items():
        cmd_name = extract_command_name(cmd_path)
        agent_count = len(deps["agents"])
        
        # Calculate complexity score
        complexity = min(1.0, agent_count * 0.1)
        
        command_complexity[cmd_name] = {
            "agent_count": agent_count,
            "complexity_score": complexity,
            "category": categorize_complexity(complexity)
        }

# Group by complexity
complexity_groups = {
    "CRITICAL": [],
    "COMPLEX": [],
    "MODERATE": [],
    "SIMPLE": []
}

for cmd, data in command_complexity.items():
    complexity_groups[data["category"]].append((cmd, data))
```

### Step 4: Identify System Patterns

**From aggregated data, find patterns:**

```python
system_patterns = {
    "hotspot_agents": [],
    "orphan_agents": [],
    "bottlenecks": [],
    "circular_dependencies": []
}

# From resource-analyzer report
if "orphan_agents" in resource_report:
    system_patterns["orphan_agents"] = resource_report["orphan_agents"]

if "usage_frequency" in resource_report:
    # Extract top 5 most used
    sorted_usage = sorted(
        resource_report["usage_frequency"].items(),
        key=lambda x: x[1]["call_count"],
        reverse=True
    )
    system_patterns["hotspot_agents"] = sorted_usage[:5]

# From dependency-mapper report
if "circular_dependencies" in dependency_report:
    system_patterns["circular_dependencies"] = dependency_report["circular_dependencies"]
```

### Step 5: Generate Visual Representations

**Create comprehensive diagrams:**

```python
def generate_system_overview():
    return f"""
NOVELSYS-SWARM System Flow Analysis v4.0
========================================
Generated: {timestamp}
Data Source: context.json + 6 Phase 1 reports
Overall Confidence: {system_metrics['overall_confidence']:.2f}

## System Statistics
Total Commands: {system_metrics['total_commands']}
Total Agents: {system_metrics['total_agents']}
Maximum Depth: {system_metrics['max_depth']}
Orphan Agents: {len(system_patterns['orphan_agents'])}

## Complexity Distribution
+-----------------------------------------+
| CRITICAL (>0.85): {'█' * critical_pct} {critical_count} ({critical_pct}%) |
| COMPLEX  (0.7-0.85): {'█' * complex_pct} {complex_count} ({complex_pct}%) |
| MODERATE (0.3-0.7): {'█' * moderate_pct} {moderate_count} ({moderate_pct}%) |
| SIMPLE   (<0.3): {'█' * simple_pct} {simple_count} ({simple_pct}%) |
+-----------------------------------------+
"""

def generate_command_flows():
    flows = []
    for category in ["CRITICAL", "COMPLEX", "MODERATE", "SIMPLE"]:
        if complexity_groups[category]:
            flows.append(f"\n{category} COMPLEXITY")
            flows.append("=" * 40)
            
            for cmd_name, data in complexity_groups[category]:
                flow = f"""
{cmd_name} [Score: {data['complexity_score']:.2f}]
+-- Agents: {data['agent_count']}
+-- Steps: {context.commands[cmd_name]['step_count']}
+-- Execution: {context.commands[cmd_name]['execution_mode']}
"""
                flows.append(flow)
    
    return "\n".join(flows)

def generate_agent_heatmap():
    return f"""
## Agent Usage Heatmap

TOP 5 HOTSPOTS (Most Called):
{'-' * 40}
{format_hotspots(system_patterns['hotspot_agents'])}

ORPHAN AGENTS (Never Called):
{'-' * 40}
{format_orphans(system_patterns['orphan_agents'])}
"""
```

### Step 6: Generate Enhanced Report

Use Write tool to save to the path provided in your prompt:

```json
{
  "format_version": "3.0",
  "schema_version": "2025-09-10",
  "report_timestamp": "[from prompt path]",
  "scan_timestamp": "[current ISO-8601]",
  "data_sources": ["context.json", "6 Phase 1 reports"],
  "analysis_mode": "aggregated",
  
  "system_metrics": {
    "total_commands": [count],
    "total_agents": [count],
    "max_depth": [number],
    "overall_confidence": [0.0-1.0],
    "phase1_reports_loaded": 6
  },
  
  "complexity_distribution": {
    "CRITICAL": {
      "count": [number],
      "percentage": [percent],
      "commands": ["list"]
    },
    "COMPLEX": {
      "count": [number],
      "percentage": [percent],
      "commands": ["list"]
    },
    "MODERATE": {
      "count": [number],
      "percentage": [percent],
      "commands": ["list"]
    },
    "SIMPLE": {
      "count": [number],
      "percentage": [percent],
      "commands": ["list"]
    }
  },
  
  "system_patterns": {
    "hotspot_agents": [
      {
        "agent": "[name]",
        "call_count": [number],
        "called_by": ["list"]
      }
    ],
    "orphan_agents": ["list"],
    "bottlenecks": ["list"],
    "circular_dependencies": ["list"]
  },
  
  "visual_diagrams": {
    "system_overview": "[ASCII diagram]",
    "command_flows": "[ASCII flows]",
    "agent_heatmap": "[ASCII heatmap]",
    "dependency_tree": "[ASCII tree]"
  },
  
  "aggregated_issues": {
    "critical": [count],
    "high": [count],
    "medium": [count],
    "low": [count]
  },
  
  "recommendations": [
    "Address critical complexity commands",
    "Remove orphan agents",
    "Optimize hotspot agents"
  ],
  
  "performance_metrics": {
    "execution_time_ms": [under 100],
    "reports_loaded": 6,
    "context_size_kb": [size],
    "io_operations_saved": [count],
    "efficiency_gain_percentage": 60
  }
}
```

## Success Criteria

- Completes in <100ms
- Loads context.json + 6 Phase 1 reports only
- Generates comprehensive visualizations
- Aggregates all metrics accurately
- Creates actionable insights

## Error Handling

If any report missing:
1. Note missing report
2. Continue with available data
3. Adjust confidence score accordingly
4. Note gaps in final report

## Important Notes

- This is v4.0 - optimized for efficiency
- Aggregates from context.json and Phase 1 reports
- No direct file scanning
- Visual diagrams in ASCII format for clarity