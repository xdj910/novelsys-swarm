# Task Wrapper Template for Troubleshooting

## Purpose
This template helps diagnose and fix Task tool invocation issues.

## Correct Task Tool Usage

### [x] CORRECT Format:
```markdown
Task(
    subagent_type="agent-name",
    description="Brief description",
    prompt="Detailed prompt for the agent"
)
```

### [ ] INCORRECT Formats:
```bash
# WRONG - Python script
python claude_subagents.py agent-name "prompt"

# WRONG - Direct Python
python -c "import agent; agent.run()"

# WRONG - Bash execution
bash -c "./run_agent.sh agent-name"
```

## Environment Diagnostic

Run this to check your environment:

```bash
# Check Claude Code environment
echo "CLAUDECODE: $CLAUDECODE"
echo "PATH: $PATH"
echo "Current directory: $(pwd)"
echo "Claude directory: $(ls -la .claude/)"
```

## Common Issues and Fixes

### Issue 1: Python Script Execution
**Symptom**: `python claude_subagents.py` errors
**Cause**: Legacy compatibility mode
**Fix**: Use native Task tool

### Issue 2: Task Tool Not Recognized
**Symptom**: Task calls treated as text
**Cause**: Claude Code not properly initialized
**Fix**: Restart Claude Code session

### Issue 3: Agent Not Found
**Symptom**: "subagent_type not found" errors
**Cause**: Agent name mismatch
**Fix**: Check exact agent name in .claude/agents/

## Testing Task Tool

Test with a simple agent call:

```markdown
Task(
    subagent_type="bible-cache-manager",
    description="Test agent invocation",
    prompt="Check if Bible cache exists for current project"
)
```

If this works, Task tool is functioning correctly.

## Fallback Solution

If Task tool consistently fails, temporarily use direct file operations:

1. Write instructions to a task file
2. Read agent documentation
3. Manually execute agent logic
4. Save results to expected output file

This is NOT recommended for production use.