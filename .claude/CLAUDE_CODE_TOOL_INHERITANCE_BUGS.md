# Claude Code Tool Inheritance Bugs - Known Issues & Solutions

## Critical Discovery: Tool Configuration Ignored

### The Problem
**Claude Code has systematic bugs where sub-agents receive tools that are NOT in their configuration.**

Even when an agent is configured with:
```yaml
tools: Read, Bash  # ONLY these two tools
```

The agent may still receive access to `Write`, `Grep`, or other tools due to inheritance bugs.

## Affected GitHub Issues
- **Issue #5456**: Sub-agents Don't Inherit Model Configuration
- **Issue #7296**: Agents Don't Inherit MCP Tool Access Despite Connected MCP Servers
- **Issue #5750**: Global Agents Inheritance Broken in Project Context
- **Issue #1224**: Critical Bug: Claude Code CLI making excessive background API calls

## Root Causes

### 1. Configuration Cache Override
```yaml
Problem: Claude Code maintains internal caches that override local agent configs
Effect: Agent gets tools from cache, not from its YAML frontmatter
Example: Agent configured with Read+Bash gets Read+Bash+Write from cache
```

### 2. Scope Inheritance Bug
```yaml
Problem: Sub-agents inherit tool scope from main Claude instance
Effect: Main Claude's tools "leak" to sub-agents despite explicit restrictions
Example: Main Claude has all tools -> Sub-agent gets all tools regardless of config
```

### 3. Global vs Project Context Confusion
```yaml
Problem: Global agent configurations conflict with project-specific ones
Effect: Wrong tool set applied based on which context wins
Example: Global agent with Write tool overrides project agent with Read-only
```

## Symptoms & Detection

### Loop Pattern Detection
```yaml
Common Pattern:
  1. Agent configured: tools: Read, Bash
  2. Agent attempts: Write(filepath)
  3. Error: "File has not been read yet. Read it first before writing to it."
  4. Agent reads file again
  5. Loop continues infinitely

Detection Signs:
  - Agent uses tools not in its configuration
  - "File has not been read yet" errors
  - Infinite read-write loops
  - Excessive API calls for simple tasks
```

### Debugging Method
```bash
# Check if agent is using unauthorized tools
grep -A 5 -B 5 "Write(" agent_execution_log.txt
# Should be EMPTY if agent only has Read, Bash

# Verify agent configuration
grep "tools:" .claude/agents/your-agent.md
# Should match what agent actually uses
```

## Solutions

### Solution 1: Explicit Tool Guards (RECOMMENDED)
Add tool rejection guards directly in agent instructions:

```markdown
## CRITICAL: Tool Inheritance Bug Guard

**IMPORTANT**: Due to Claude Code bug with tool inheritance, this agent may have access to Write tool despite `tools: Read, Bash` configuration.

**IF Write tool is available, DO NOT USE IT**. This agent uses Bash-only processing.

```yaml
Bug Pattern:
  - Agent config: tools: Read, Bash
  - Claude Code provides: Read, Bash, Write (inheritance bug)
  - Prevention: IGNORE Write tool, use ONLY Bash
```

### Solution 2: Bash-Only File Operations
Replace Write tool usage with Bash commands:

```bash
# WRONG (triggers inheritance bug loop):
# Write(filepath, content)

# CORRECT (bypasses bug):
cat > "$filepath" << EOF
$content
EOF

# Or use sed for modifications:
sed -i 's/pattern/replacement/g' "$filepath"
```

### Solution 3: Defensive Programming
Always validate tool availability:

```markdown
### Step 1: Tool Validation
Before processing, confirm which tools are actually available:
- If Write tool appears despite config: IGNORE IT
- Use only tools that are explicitly in the YAML frontmatter
- Document when inheritance bugs are detected
```

## Affected Agents in NOVELSYS-SWARM

### Fixed Agents
- ✅ `orphan-image-processor.md` - Added explicit Write tool rejection guard
- ✅ `system-scanner.md` - Uses Bash-only processing
- ✅ All coordinators - Explicitly avoid Task tool

### Need Review
- 🔍 Any agent experiencing infinite loops
- 🔍 Agents that use Write tool unexpectedly
- 🔍 Agents with "File has not been read yet" errors

## Prevention Guidelines

### For New Agents
1. **Explicit Tool Guards**: Add inheritance bug warnings
2. **Minimal Tool Set**: Only include necessary tools
3. **Bash Preference**: Use Bash instead of Write when possible
4. **Test Tool Isolation**: Verify agent only uses configured tools

### For Existing Agents
1. **Audit Tool Usage**: Check if agents use unauthorized tools
2. **Add Guards**: Document inheritance bug mitigation
3. **Replace Write Calls**: Use Bash alternatives where possible
4. **Test Stability**: Verify no infinite loops

## Monitoring & Detection

### Regular Checks
```bash
# Find agents that might be affected
grep -l "Write.*tool\|tools:.*Write" .claude/agents/*.md

# Check for loop patterns in logs
grep -i "file has not been read yet" *.log

# Verify tool configurations
grep -H "tools:" .claude/agents/*.md | grep -v "Write"
```

### Success Metrics
- ✅ No infinite loops in agent execution
- ✅ Agents use only configured tools
- ✅ No "File has not been read yet" errors
- ✅ Consistent tool behavior across executions

## Workaround Status

| Bug Type | Severity | Workaround Available | Status |
|----------|----------|-------------------|--------|
| Tool Inheritance | HIGH | Yes - Explicit guards | ✅ Implemented |
| Model Config Override | MEDIUM | Yes - Explicit model setting | 🔍 Needs testing |
| MCP Tool Access | LOW | Partial - Manual inclusion | ⚠️ Limited |
| Cache Override | HIGH | Yes - Bash alternatives | ✅ Implemented |

## Future Updates

Monitor these GitHub issues for official fixes:
- Watch issue #5456 for model inheritance fixes
- Watch issue #7296 for MCP tool access fixes
- Watch issue #5750 for global agent fixes
- Subscribe to Claude Code release notes

## Contact

If you encounter new tool inheritance bugs:
1. Document the specific pattern
2. Add to this file
3. Implement workarounds using the patterns above
4. Report to Anthropic if novel behavior

---

**Last Updated**: 2025-09-24
**Version**: v1.0
**Status**: Active workarounds implemented for critical bugs