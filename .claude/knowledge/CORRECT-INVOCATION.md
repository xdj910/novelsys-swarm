# CORRECT SUBAGENT INVOCATION IN CLAUDE CODE

## WARNING:️ CRITICAL CORRECTION (2025-09-11)

This document contains the CORRECT information about how to invoke subagents in Claude Code, based on official documentation.

## [x] CORRECT METHOD: Natural Language

Claude Code uses **natural language** to invoke subagents. This is the ONLY valid method.

### Examples of Correct Invocation

**In Commands:**
```markdown
Use the chapter-start-coordinator subagent to orchestrate the complete generation pipeline for chapter $ARGUMENTS.
```

**In Coordinators:**
```markdown
Now I'll orchestrate the pipeline:
1. Use the entity-validator subagent to validate all entities
2. Use the outline-generator subagent to create chapter outline
3. Use the scene-generator subagent for initial draft
```

**Alternative phrasings (all valid):**
- "Use the [name] subagent to..."
- "Have the [name] subagent..."
- "Ask the [name] subagent to..."
- "The [name] subagent should..."

## [ ] INCORRECT METHODS (DO NOT USE)

### 1. Task() Function - DOES NOT EXIST
```python
# WRONG - This is pseudo-code, not real
Task(
    subagent_type="scene-generator",
    description="Generate scene",
    prompt="Create chapter 1"
)
```
**WHY IT'S WRONG:** Task() is pseudo-code that appears in some documentation as an example, but it is NOT a real function in Claude Code.

### 2. Python Scripts - DO NOT EXIST
```bash
# WRONG - This script doesn't exist
python claude_subagents.py --agent scene-generator
```
**WHY IT'S WRONG:** There is no claude_subagents.py script. This was a misunderstanding.

### 3. Direct Execution - NOT SUPPORTED
```bash
# WRONG - Cannot execute .md files
./agents/scene-generator.md
```
**WHY IT'S WRONG:** Markdown files are not executable. They are configuration files.

## 📚 Official Documentation Structure

### Command Files (.claude/commands/)
```yaml
---
description: Command description
argument-hint: [required] <optional>
allowed-tools: Read, Write, Bash, Grep
---

# Command content using natural language to invoke subagents
```

### Subagent Files (.claude/agents/)
```yaml
---
name: agent-name
description: When to invoke this agent
tools: Read, Write, Bash  # optional
thinking: true            # optional for complex agents
---

# System prompt for the agent
```

## 🎯 Key Principles

1. **Natural Language Only** - All subagent invocation uses natural language
2. **File-Based Communication** - Agents communicate through files, not return values
3. **No Functions** - There are no function calls in Claude Code subagent invocation
4. **No Scripts** - There are no Python or other scripts for agent execution

## 💡 Best Practices

1. **Be Clear** - Use clear natural language when invoking subagents
2. **Specify Requirements** - Tell the subagent what files to read/write
3. **Check Files** - Verify output files after subagent execution
4. **No Return Values** - Don't expect return values; check files instead

## WARNING:️ Important Reminder

If you see any documentation or code that uses Task() functions or Python scripts for subagent invocation, it is **INCORRECT**. Always use natural language as shown in this document.

---
**This is the authoritative guide for Claude Code subagent invocation.**