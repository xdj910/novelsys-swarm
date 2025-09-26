---
description: Map system execution flows and dependencies
---

# Flow Mapping - System Execution Analysis

Generate comprehensive execution flow diagrams showing command  ->  coordinator  ->  agent call trees and dependencies.

## Command Usage

- `/novel:flow-mapping` - Generate complete system flow analysis with dependency mapping

## Implementation

This command uses the flow-diagram-generator subagent to orchestrate comprehensive system flow analysis with:

- **Command Analysis**: Map all novel commands to their coordinator and agent dependencies
- **Flow Visualization**: Generate detailed execution flow diagrams with call trees
- **Dependency Mapping**: Identify sequential vs parallel execution patterns
- **Complexity Metrics**: Calculate execution complexity for each command
- **System Health**: Analyze system architecture compliance and optimization opportunities
- **Output Generation**: Create comprehensive flow diagrams and analysis reports

## Execution Steps

### Step 1: System Flow Analysis

Use the flow-diagram-generator subagent to:
1. Scan all novel commands in `.claude/commands/novel/`
2. Analyze each command's coordinator and agent dependencies
3. Map execution patterns and call trees
4. Identify parallel vs sequential execution opportunities

### Step 2: Comprehensive Flow Generation

The flow-diagram-generator will create structured analysis covering:

**Phase 1: Command Discovery and Analysis**
- Discover all novel commands and their structures
- Parse coordinator and agent delegation patterns
- Identify direct execution violations and compliance issues

**Phase 2: Flow Mapping and Visualization**
- Generate detailed execution flow diagrams for each command
- Map agent-to-agent dependencies and call chains
- Create system-wide execution flow overview

**Phase 3: Analysis and Optimization**
- Calculate complexity metrics for each execution chain
- Identify optimization opportunities and bottlenecks
- Generate compliance reports and improvement recommendations

### Step 3: Report Generation

Generate comprehensive system analysis including:
- Detailed flow diagrams for each command
- System-wide dependency mapping
- Complexity analysis and optimization opportunities
- Architecture compliance assessment and recommendations

## Expected Output

The flow-diagram-generator will provide:

1. **Command Flow Diagrams** showing execution paths for each novel command
2. **System Dependency Map** illustrating inter-command relationships
3. **Complexity Metrics** with execution time estimates and resource usage
4. **Architecture Compliance** analysis with violation identification
5. **Optimization Recommendations** for improving system performance

## Features

- **Comprehensive Analysis**: Complete system flow mapping and visualization
- **Dependency Tracking**: Clear visualization of command interdependencies
- **Performance Metrics**: Execution complexity and optimization analysis
- **Compliance Validation**: Architecture pattern compliance assessment
- **Visual Output**: Clear diagrams and reports for system understanding

## Notes

- Flow mapping provides deep insights into system architecture and performance
- Dependency analysis helps identify optimization opportunities
- Compliance validation ensures architectural pattern adherence
- Visual output makes complex system relationships easy to understand

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

- Results help optimize command execution and system architecture