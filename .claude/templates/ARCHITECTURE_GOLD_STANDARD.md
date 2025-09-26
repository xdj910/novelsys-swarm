# Architecture Gold Standard v1.0
*Universal System Design Principles from 6 Proven Test Patterns*
*Part of [NOVELSYS-SWARM Documentation System](/SYSTEM_INDEX.md)*
*Last Updated: 2025-09-14*

## Document Authority & Purpose

**Authority Level**: Implementation Guide (subordinate to [CLAUDE.md](/CLAUDE.md))
**Relationship**: This document translates CLAUDE.md rules into practical patterns
**Scope**: Universal patterns applicable to ANY Claude Code system

## Executive Summary

This document establishes the **Architecture Gold Standard** - universal design principles extracted from 6 successfully tested patterns. These principles apply to ANY system built on Claude Code architecture, not just novel generation. All patterns comply with CLAUDE.md v6.2 specifications.

---

## 🏛️ Part 1: Architecture Patterns

### 1.1 Five-Layer Universal Architecture

```
┌─────────────────────────────────────┐
│        User Interface Layer         │
│         (Commands/API)               │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│      Orchestration Layer            │
│        (Main Claude)                 │
└──────────┬─────────┬────────────────┘
           │         │
┌──────────┴───┐  ┌──┴────────────────┐
│  Planning    │  │   Execution       │
│  Layer       │  │   Layer           │
│(Coordinators)│  │   (Agents)        │
└──────────────┘  └───────────────────┘
           │         │
┌──────────┴─────────┴────────────────┐
│        Data/Communication Layer     │
│          (File System)              │
└─────────────────────────────────────┘
```

#### Layer Responsibilities

| Layer | Responsibility | Tools | Key Rule |
|-------|---------------|-------|----------|
| **User Interface** | Accept input, display output | N/A | <100 lines, pure delegation |
| **Orchestration** | Central control and scheduling | All including Task | Only layer that calls subagents |
| **Planning** | Analyze and return execution plans | Read, Write, Bash, Grep | NO Task tool, prevents recursion |
| **Execution** | Perform specific tasks | Task-specific only | Single responsibility, NO Task |
| **Data/Communication** | Store state, enable communication | File I/O | Atomic operations, no direct calls |

### 1.2 Communication Patterns

#### Producer-Consumer Pattern
```yaml
Producer:
  Output: data.json
  Method: Atomic write (.tmp + mv)

Consumer:
  Input: data.json
  Method: Read when ready

Benefits:
  - Decoupled execution
  - No synchronization needed
  - Clear data flow
```

#### Shared Reference Pattern
```yaml
Writer:
  Creates: reference.json
  Frequency: Once or periodic updates

Readers:
  Access: reference.json
  Concurrency: Unlimited parallel reads

Use Cases:
  - Configuration files
  - Reference data (dictionaries, rules)
  - Cached computations
```

#### Version Control Pattern
```yaml
Versioning:
  Format: file.v{N}.ext
  Retention: Keep all versions

Benefits:
  - Complete history
  - Rollback capability
  - Audit trail
```

---

## 🔄 Part 2: Workflow Patterns

### 2.1 Sequential Pipeline Workflow

```
Stage 1 -> Validate -> Stage 2 -> Validate -> Stage 3 -> Validate -> Complete
```

**Implementation:**
```json
{
  "workflow": "pipeline",
  "stages": [
    {"stage": 1, "agent": "processor-1", "validate": true},
    {"stage": 2, "agent": "processor-2", "validate": true},
    {"stage": 3, "agent": "processor-3", "validate": true}
  ],
  "abort_on_failure": true
}
```

**Use When:**
- Data must flow through stages
- Each stage depends on previous
- Quality gates needed

### 2.2 Parallel Batch Workflow

```
        ┌-> Task A ->┐
Input ->├-> Task B ->├-> Merge
        └-> Task C ->┘
```

**Implementation:**
```json
{
  "workflow": "parallel_batch",
  "execution": "concurrent",
  "tasks": [
    {"agent": "processor-a", "output": "result-a.json"},
    {"agent": "processor-b", "output": "result-b.json"},
    {"agent": "processor-c", "output": "result-c.json"}
  ],
  "merge_strategy": "collect_all"
}
```

**Use When:**
- Tasks are independent
- Performance is critical
- Same operation on multiple items

### 2.3 Human-in-Loop Workflow

```
Generate -> Review -> Decision
                    ├-> Approve -> Continue
                    ├-> Revise -> Regenerate
                    └-> Reject -> Terminate
```

**Implementation:**
```json
{
  "workflow": "human_in_loop",
  "gates": [
    {
      "after": "generation",
      "prompt": "Review and decide",
      "branches": {
        "approve": "next_stage",
        "revise": "retry_with_feedback",
        "reject": "terminate"
      }
    }
  ]
}
```

**Use When:**
- Quality control critical
- Creative decisions needed
- Risk management required

### 2.4 Multi-Phase Coordinator Workflow

```
Coordinator 1 -> Execute Plan 1 -> Coordinator 2 -> Execute Plan 2
    (Analyze)      (Agents)        (Generate)      (Agents)
```

**Implementation:**
```json
{
  "workflow": "multi_coordinator",
  "phases": [
    {
      "coordinator": "analysis-coordinator",
      "execution": "agents from plan",
      "output": "analysis_results/"
    },
    {
      "coordinator": "generation-coordinator",
      "input": "analysis_results/",
      "execution": "agents from plan"
    }
  ]
}
```

**Use When:**
- Complex multi-stage operations
- Different expertise per phase
- Adaptive workflows needed

---

## 🏗️ Part 3: System Architecture Principles

### 3.1 Recursion Prevention Architecture

```
SAFE Architecture:
  Main Claude -> Task -> Subagent (no Task) [YES]
  File System -> Communication -> No direct calls [YES]

UNSAFE Architecture:
  Subagent -> Task -> Another Subagent [NO] (RECURSION!)
  Direct function calls between agents [NO]
```

### 3.2 Data Integrity Architecture

```yaml
Atomic Operations:
  Write: file.tmp -> mv file.tmp file
  Read: Check exists -> Read -> Validate
  Update: Read -> Modify -> Atomic write

Guarantees:
  - No partial writes
  - No corruption on crash
  - Consistent state always
```

### 3.3 Scalability Architecture

```yaml
Horizontal Scaling:
  - Up to 10 parallel agents
  - File-based work distribution
  - No shared memory/state

Vertical Scaling:
  - Pipeline stages can be deep
  - Coordinator phases unlimited
  - Version history unbounded
```

---

## 👥 Part 4: Division of Labor

### 4.1 Component Responsibility Matrix

| Component | Primary Role | What It Does | What It NEVER Does |
|-----------|-------------|--------------|-------------------|
| **Command** | Interface | Delegates to Main Claude | Implements logic |
| **Main Claude** | Orchestrator | Calls subagents, schedules | Business logic |
| **Coordinator** | Planner | Returns execution plans | Executes plans |
| **Agent** | Worker | Executes single task | Calls other agents |
| **File System** | Communicator | Stores state, enables IPC | Direct messaging |

### 4.2 Decision Rights

```yaml
Who Decides What:
  User:
    - High-level goals
    - Quality thresholds
    - Approval/rejection

  Main Claude:
    - Execution strategy (parallel/serial)
    - Agent selection
    - Error handling

  Coordinator:
    - Task breakdown
    - Dependency ordering
    - Resource requirements

  Agent:
    - Implementation details
    - Optimization choices
    - Output format (within spec)
```

### 4.3 Data Ownership

```yaml
Clear Ownership Rules:
  One Writer Per File:
    - Each file has single owner agent
    - Prevents write conflicts
    - Clear responsibility

  Shared Reads Allowed:
    - Multiple agents can read same file
    - Reference data pattern
    - Cache friendly

  Version Control:
    - Never overwrite, create versions
    - Maintain history
    - Enable rollback
```

---

## 📋 Part 5: Implementation Standards

### 5.1 Workflow Selection Guide

```yaml
Choose Pipeline When:
  - Sequential dependencies exist
  - Data transformation needed
  - Quality gates required

Choose Parallel When:
  - Tasks independent
  - Performance critical
  - Batch processing

Choose Human-in-Loop When:
  - Quality control needed
  - Creative decisions
  - Risk management

Choose Multi-Coordinator When:
  - Complex analysis required
  - Multiple expertise domains
  - Adaptive behavior needed
```

### 5.2 Performance Standards

| Pattern | Expected Performance | Overhead |
|---------|---------------------|----------|
| Serial Pipeline | Baseline (1x) | Minimal |
| Parallel Batch | 3-10x faster* | ~10% coordination |
| Human-in-Loop | Variable | User think time |
| Multi-Coordinator | 1.5-2x slower | Planning overhead |

*Performance gains verified in `/parallel-test` with actual 3x improvement for 3 concurrent agents

### 5.3 Error Handling Standards

```yaml
Error Propagation:
  Agent Error -> Report to Main Claude -> Decide action

Recovery Strategies:
  Retry: Transient failures (network, timing)
  Fallback: Use alternative agent/approach
  Graceful Degradation: Partial results better than none
  Abort: Critical failure, maintain consistency
```

---

## 🎯 Part 6: Universal Application Examples

### Example 1: Data Processing System
```yaml
Architecture: Pipeline + Parallel
Workflow:
  1. Parallel ingestion (multiple sources)
  2. Pipeline transformation (clean -> validate -> enrich)
  3. Parallel output (multiple destinations)
```

### Example 2: Document Generation System
```yaml
Architecture: Multi-Coordinator + Human-in-Loop
Workflow:
  1. Analysis coordinator (understand requirements)
  2. Human approval gate
  3. Generation coordinator (create content)
  4. Human review gate
  5. Publishing coordinator (format and deliver)
```

### Example 3: Testing Framework
```yaml
Architecture: Parallel + Pipeline
Workflow:
  1. Parallel test execution
  2. Pipeline results (collect -> analyze -> report)
  3. Human review of failures
```

### Example 4: ML Training Pipeline
```yaml
Architecture: Pipeline + Version Control
Workflow:
  1. Data preparation pipeline
  2. Training with checkpoints (versions)
  3. Evaluation pipeline
  4. Model versioning and rollback
```

---

## 🔒 Part 7: Compliance Checklist

### Architecture Compliance
- [ ] Five layers properly separated
- [ ] Only Main Claude has Task tool
- [ ] Coordinators return JSON plans only
- [ ] Agents have single responsibility
- [ ] File system used for all communication

### Workflow Compliance
- [ ] Clear workflow pattern selected
- [ ] Validation points identified
- [ ] Error handling defined
- [ ] Performance expectations set

### Data Compliance
- [ ] Atomic operations for all writes
- [ ] Version control where needed
- [ ] Clear file ownership
- [ ] No direct agent communication

### Safety Compliance
- [ ] No recursion possible
- [ ] No race conditions
- [ ] Graceful error handling
- [ ] Data integrity guaranteed

---

## 📚 Quick Reference Card

### The 5 Layers
1. **User Interface** - Commands
2. **Orchestration** - Main Claude
3. **Planning** - Coordinators
4. **Execution** - Agents
5. **Data** - File System

### The 4 Workflows
1. **Pipeline** - Sequential stages
2. **Parallel** - Concurrent tasks
3. **Human-in-Loop** - User decisions
4. **Multi-Coordinator** - Complex phases

### The 3 Communications
1. **Producer-Consumer** - Decoupled flow
2. **Shared Reference** - Common data
3. **Version Control** - History tracking

### The 2 Safety Rules
1. **No Task in subagents** - Prevents recursion
2. **Atomic writes always** - Prevents corruption

### The 1 Golden Principle
**File System is the nervous system** - All communication flows through files

---

## Appendix: Proven Test References

All principles in this document are derived from successful tests:
- `/architecture-test` - Layer validation
- `/parallel-test` - Concurrent execution
- `/python-pipeline-test` - Pipeline workflow
- `/human-in-loop-test` - User interaction
- `/multi-coordinator-test` - Phase coordination
- `/io-patterns-test` - Communication patterns

---

## Related Documentation

### Core References
- **[CLAUDE.md](/CLAUDE.md)** - System authority and rules (v6.2)
- **[SYSTEM_INDEX.md](/SYSTEM_INDEX.md)** - Complete documentation map
- **[NOVEL_SYSTEM_PATTERNS.md](NOVEL_SYSTEM_PATTERNS.md)** - Novel-specific implementation

### Templates
- **[TEMPLATE_command.md](../templates/TEMPLATE_command.md)** - Command creation
- **[TEMPLATE_coordinator.md](../templates/TEMPLATE_coordinator.md)** - Coordinator patterns
- **[TEMPLATE_agent.md](../templates/TEMPLATE_agent.md)** - Agent patterns

### Windows Path Handling
```yaml
CRITICAL for Windows:
  Wrong: ls -la "D:\path\file.txt"  # Backslash escapes
  Correct: ls -la .claude/testing/*.json  # Relative
  Correct: ls -la "D:/path/file.txt"  # Forward slashes
```

---

**Version**: 1.0 | **Status**: Gold Standard | **Applicability**: Universal

*This is not just theory-it's proven architecture with 100% test success rate.*