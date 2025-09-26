# Claude Code Architecture Templates v6.8
*Last Updated: 2025-09-26*

## Purpose

These templates implement the **official Claude Code architecture** with **recursion-safe patterns** discovered through extensive research and testing. Part of the [NOVELSYS-SWARM Documentation System](/SYSTEM_INDEX.md).

## Core Documents

### ARCHITECTURE_GOLD_STANDARD.md
- **Purpose**: Universal system design patterns
- **Authority**: Implementation Guide (subordinate to CLAUDE.md)
- **Contains**: 7-part gold standard from 6 proven tests
- **Scope**: ANY Claude Code system, not just novels

## Templates

### 1. TEMPLATE_command.md
- **Purpose**: User-facing commands (slash commands)
- **Length**: 50-120 lines acceptable (business completeness priority)
- **Pattern**: Pure delegation to Main Claude
- **Key Feature**: Declarative, not executable

### 2. TEMPLATE_coordinator.md
- **Purpose**: Complex workflow orchestration
- **Length**: <250 lines optimal, must return JSON execution plans
- **Tools**: `Read, Write, Grep` (NEVER Task or Bash - prevents recursion and self-execution)
- **Pattern**: Returns execution plans, doesn't execute
- **Key Feature**: Subagent that plans but doesn't call other subagents

### 3. TEMPLATE_agent.md
- **Purpose**: Single-responsibility task execution
- **Length**: <500 lines (complex agents), <200 lines preferred
- **Tools**: Only what's needed for the specific task (NEVER Task)
- **Pattern**: Receives paths, executes, saves results
- **Key Feature**: Focused expertise, no coordination

## Architecture Pattern

```
User Input
    |
Command File (declarative instructions)
    |
Main Claude (reads and interprets)
    |-> Simple task: Direct execution
    |-> Complex task: Task -> Coordinator (get plan)
    |                  |
    |              Returns JSON plan
    |                  |
    |-> Main Claude executes plan: Task -> Agents (parallel/sequential)
                                           |
================================================
    File System / Data Layer
    (Communication & Persistence)
================================================
```

### The Critical Fourth Component: Data Layer

The File System/Data Layer is the **foundation** that prevents recursion:
- **Communication**: Agents communicate through files, not function calls
- **Persistence**: All state is stored in files
- **Decoupling**: No direct agent-to-agent calls possible
- **Parallelism**: Multiple agents can work simultaneously

See [ARCHITECTURE_data_layer.md](ARCHITECTURE_data_layer.md) for detailed I/O patterns.

## Critical Rules (Prevent Recursion)

### CORRECT Patterns

1. **Command Pattern**:
   ```markdown
   Use the chapter-start-coordinator subagent to orchestrate chapter generation.
   ```
   Main Claude reads this and uses Task to call coordinator.

2. **Coordinator Pattern**:
   ```yaml
   tools: Read, Write, Grep  # NO Task or Bash tools
   ```
   Returns plan, doesn't execute.

3. **Agent Pattern**:
   ```python
   # Receives specific paths
   INPUT: /full/path/to/file.yaml
   # Executes single task
   # Saves to specified location
   ```

### WRONG Patterns (Cause Recursion)

1. **Coordinator with Task**:
   ```yaml
   tools: Task  # RECURSION RISK!
   ```

2. **Coordinator calling agents**:
   ```markdown
   # WRONG in coordinator:
   Use Task to call scene-generator...  # Subagent calling subagent!
   ```

3. **Command with implementation**:
   ```markdown
   # WRONG in command:
   def process_chapter():  # Commands aren't code!
   ```

## Key Discoveries

### From Official Documentation
- Claude Code is "low-level and unopinionated"
- Task tool enables parallel subagent execution
- Each subagent has independent context window
- Main Claude coordinates all execution

### From Community Research
- Hub-and-spoke prevents communication chaos
- Coordinator pattern separates planning from execution
- Context isolation prevents token pollution
- Parallel execution capped at 10 concurrent tasks

### From Testing (test-recursion)
- Subagents with Task calling other subagents = recursion crash
- Coordinators without Task = safe planning layer
- Main Claude as central orchestrator = stable execution

## Usage Guide

### Creating a New Command
1. Copy `TEMPLATE_command.md`
2. Target <100 lines, 50-120 acceptable for business completeness
3. Focus on WHAT, not HOW
4. Delegate complex logic to coordinator

### Creating a New Coordinator
1. Copy `TEMPLATE_coordinator.md`
2. Set `tools: Read, Write, Grep` (no Task or Bash!)
3. Return JSON execution plan
4. Include full paths, not templates

### Creating a New Agent
1. Copy `TEMPLATE_agent.md`
2. Define single responsibility
3. List only needed tools
4. Focus on excellent execution of one task

## Validation Checklist

Before deploying any new component:

- [ ] **Command**: Under 120 lines? Pure delegation?
- [ ] **Coordinator**: No Task or Bash tools? Returns plan only?
- [ ] **Agent**: Single responsibility? Clear I/O?
- [ ] **Paths**: Full paths prepared by Main Claude?
- [ ] **Tools**: Minimum necessary tools declared?
- [ ] **Recursion**: No subagent calling subagent?

## References

- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code/)
- [Sub-Agents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- Test validation: `/test-recursion` command

## Philosophy

> "Commands describe intentions,
> Coordinators plan execution,
> Main Claude orchestrates reality,
> Agents perform focused work."

This separation ensures:
- **No recursion** (coordinators can't call agents)
- **Clear responsibilities** (each layer has a purpose)
- **Optimal performance** (parallel execution where possible)
- **Maintainability** (changes don't cascade)

## See Also - Documentation Network

### System Authority
- **[/CLAUDE.md](/CLAUDE.md)** - Core system rules and golden principles
- **[/SYSTEM_INDEX.md](/SYSTEM_INDEX.md)** - Master documentation index

### Related Templates
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page rapid reference
- **[ARCHITECTURE_data_layer.md](ARCHITECTURE_data_layer.md)** - Deep dive into file system layer

### Live Support
- **[claude-code-expert.md](../agents/claude-code-expert.md)** - Expert agent for troubleshooting

### Test Commands
- `/architecture-test` - Validate system architecture
- `/parallel-test` - Test parallel execution
- `/io-patterns-test` - Test I/O patterns

---

*These templates represent the synthesis of official documentation, community best practices, and empirical testing to create a robust, recursion-safe architecture for Claude Code applications.*

**Template Version**: v6.8 | **Authority**: [CLAUDE.md](/CLAUDE.md) | **Status**: Production Ready

## What's New in v6.8

### Critical Template Fixes
- **TEMPLATE_agent.md**: Fixed execution ambiguity by replacing "Step 1/2/3" with "Single Execution Process" with internal phases
- **TEMPLATE_coordinator.md**: Enhanced planning-only role clarity with stronger architectural boundaries
- **README.md**: Resolved command length contradiction - aligned with CLAUDE.md authority (50-120 lines acceptable)
- **All templates**: Strengthened intent vs action language to prevent architectural confusion

### Enhanced Architecture Understanding
- **Single Execution Clarity**: Agent templates now clearly indicate ONE execution with multiple internal phases
- **Planning Boundaries**: Coordinator templates emphasize planning brain vs execution hands separation
- **Consistent Guidelines**: Removed conflicting length requirements and aligned with system authority

### Previous Features (v6.5-6.7)
- **Human-in-Loop Standardization**: Simple 1/2 numeric choice format with infinite modify capability
- **Large File Handling**: Chunked reading patterns and Python integration
- **Tool Selection Clarity**: Enhanced tool assignment guidelines for proper agent functionality
- **Self-Execution Prevention**: Three-layer prevention strategy for coordinator role discipline