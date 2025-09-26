# Claude Code Architecture Quick Reference v6.6
*Part of [NOVELSYS-SWARM Documentation System](/SYSTEM_INDEX.md) | Authority: [CLAUDE.md](/CLAUDE.md)*
*Implementation Guide: [ARCHITECTURE_GOLD_STANDARD.md](ARCHITECTURE_GOLD_STANDARD.md)*

## One-Line Rules

| Component | Tools | Purpose | Key Rule |
|-----------|-------|---------|----------|
| **Command** | N/A (text file) | User interface | <100 lines target (50-120 acceptable), pure delegation |
| **Coordinator** | Read, Write, Bash, Grep | Plan orchestration | NO Task tool, return JSON plans, <250 lines |
| **Agent** | Task-specific tools only | Execute single task | Single responsibility, <500 lines, NO Task |
| **Main Claude** | All tools including Task | Central orchestrator | Only one who calls subagents |

## Execution Flow

```
Command -> Main Claude -> Task -> Coordinator -> Returns Plan
                         |
                   Main Claude -> Task -> Agents (parallel/sequential)
                                           |
                   =============================
                   File System (Communication)
                   =============================
```

## Recursion Prevention

### SAFE
```yaml
# Coordinator
tools: Read, Write, Bash
# Returns: JSON plan
```

### DANGEROUS
```yaml
# Coordinator
tools: Task  # or empty (might inherit)
# Tries to: Call other agents
```

## Windows Path Handling

### Bash Command Paths
```bash
# CORRECT (use these):
ls -la .claude/testing/*.json          # Relative paths (BEST)
ls -la "D:/project/file.txt"           # Forward slashes
ls -la "D:\\project\\file.txt"         # Double backslashes

# WRONG (will fail):
ls -la "D:\project\file.txt"           # Single backslashes get escaped
```

## File Patterns

### Command (<100 lines)
```markdown
---
description: Brief description
argument-hint: '[required] <optional>'
---

Use the [name]-coordinator subagent to orchestrate...
```

### Coordinator (Planning Only)
```yaml
---
name: xxx-coordinator
tools: Read, Write, Bash  # NEVER Task
thinking: Complex reasoning needed
---

Return JSON plan for Main Claude to execute
```

### Agent (Single Task)
```yaml
---
name: xxx-agent
tools: Read, Write  # Only what's needed
description: Specific task for auto-delegation
---

Execute one task, save to provided path
```

## Naming Consistency

### Component Names vs Dictionary Keys
```python
# Component names use hyphens
agent_name = "quality-scorer"
coordinator_name = "chapter-start-coordinator"

# Dictionary keys use underscores
dict_key = name.lower().replace(' ', '_').replace('-', '_')
# "Producer-Consumer" -> "producer_consumer"
# "quality-scorer" -> "quality_scorer"
```

## Key Insights

1. **Coordinators are subagents** - They can't call other subagents
2. **Main Claude is the orchestrator** - Only it uses Task tool
3. **Commands are text** - Not code, just instructions
4. **Agents are tools** - Single purpose, no coordination
5. **Naming consistency** - Hyphens in names, underscores in keys
6. **Large files need chunking** - Files >256KB require sequential 2000-line reading
7. **Python for bulk, agents for intelligence** - Division of labor is critical
8. **Human-in-Loop uses 1/2 choices** - Simple numeric input, infinite modify loops
9. **Avoid trigger words in Task prompts** - Use descriptions not file names (v6.6)

## Architecture Metaphor

- **Commands**: The script (what should happen)
- **Main Claude**: The director (decides how)
- **Coordinators**: The choreographers (plan the moves)
- **Agents**: The performers (execute their parts)

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Coordinator with Task tool | Recursion crash | Remove Task from tools |
| Command >120 lines | May lack focus | Balance delegation vs necessary context |
| Agent doing multiple tasks | Confusion, errors | Split into multiple agents |
| Hardcoded paths in agents | Inflexibility | Accept paths from Main Claude |
| Coordinator executing tasks | Recursion risk | Return plan, don't execute |
| Large file single Read call | Tool fails, partial data | Use chunked reading (2000-line chunks) |
| File names in Task prompts | "Prompt too long" error | Use descriptive language (v6.6) |

## Tool Sets

### Typical Coordinator Tools
```yaml
tools: Read, Write, Bash, Grep  # Analysis & planning
```

### Typical Agent Tools
```yaml
tools: Read, Write  # Simple I/O
tools: Read, Write, Bash  # With system operations
tools: Read, Grep  # Analysis only
```

### NEVER in Subagents
```yaml
tools: Task  # Only Main Claude should have this
```

## File System / Data Layer

### Why It's Critical
- **Prevents Recursion**: No direct agent calls = no infinite loops
- **Enables Parallelism**: Agents write to different files simultaneously
- **Provides Persistence**: All state saved to disk
- **Allows Debugging**: Can inspect intermediate files

### I/O Best Practices
```python
# CORRECT - Atomic Write
Write("file.tmp", content)
Bash("mv file.tmp file")

# WRONG - Direct Write (corruption risk)
Write("file", content)
```

### Communication Pattern
```
Agent A -> Write -> data.json
                      |
Agent B -> Read -> data.json -> Write -> result.json
                                           |
                                   Agent C -> Read
```

## Trigger Word Prevention (NEW in v6.6)

### Problem
Task tool fails with "Prompt too long" when certain file names appear in prompts

### Trigger Words to Avoid
```
system_scan.json
.claude/agents/*.md
.claude/report/*/specific_file.json
```

### Safe Patterns
```yaml
WRONG: "Process system_scan.json"
RIGHT: "Process scan data in report directory"

WRONG: "Analyze .claude/report/xxx/system_scan.json"
RIGHT: "Analyze latest scan results"
```

### Implementation
- **Commands**: Warn Main Claude about trigger words
- **Coordinators**: Return directory + type, not file names
- **Agents**: Build paths internally from safe inputs

## Large File Handling (NEW in v6.4)

### When to Use Chunked Reading
```python
# File size check
if file_size > 256KB:
    # Use chunked reading pattern
    total_lines = bash: wc -l file_path
    chunk_size = 2000  # Proven optimal size

    for offset in range(0, total_lines, chunk_size):
        chunk = Read(file_path, offset=offset, limit=chunk_size)
        process_chunk(chunk)
```

### Division of Labor
```yaml
Use Python Scripts for:
  - Bulk file scanning (100x faster)
  - Data collection and aggregation
  - Files over 2MB

Use Agents with Chunked Reading for:
  - Intelligent file analysis
  - Context-aware processing
  - Files 256KB - 2MB
```

## Human-in-Loop Pattern (NEW in v6.5)

### Standard Choice Format
```
Options:
1) Approve - Continue to next stage
2) Modify - Provide feedback for revision

Enter choice [1/2]: _
```

### Flow Pattern
```python
Display Content -> Human Choice -> [1: Continue] or [2: Feedback -> Regenerate -> Loop]

Key Principles:
- Only two options needed (no Reject)
- Numeric input (1/2) not text
- Infinite modify capability
- Human controls all decisions
```

## Success Metrics

- Commands: <100 lines YES
- Coordinators: Return plans in <5 seconds YES
- Agents: Complete in <30 seconds YES
- No recursion crashes YES
- Clear error messages YES
- Atomic file operations YES

## See Also

- **Full Rules**: [CLAUDE.md](/CLAUDE.md)
- **Templates**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE_data_layer.md](ARCHITECTURE_data_layer.md)
- **Expert Help**: [claude-code-expert.md](../agents/claude-code-expert.md)
- **Navigation**: [SYSTEM_INDEX.md](/SYSTEM_INDEX.md)

---

**Remember**: *Coordinators plan, Main Claude orchestrates, Agents execute, Files communicate*

**Version**: v6.2 | **Status**: Production Ready