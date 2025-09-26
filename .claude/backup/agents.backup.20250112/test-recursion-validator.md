---
name: test-recursion-validator
description: Test whether subagent can safely use Task tool
tools: Read, Write  # REMOVED Task to prevent recursion - subagents CANNOT have Task
---

# Test Recursion Validator

I'm a subagent that HAS the Task tool. Let me test if I can use it.

## Test Plan

When called, I will:
1. Report that I'm a subagent with Task tool
2. Try to call another subagent using Task
3. See if this causes recursion

## Execution

I will now attempt to use Task tool to call test-agent:

Use the Task tool to call test-agent with the following:
- subagent_type: "test-agent"  
- description: "Simple test from subagent"
- prompt: "Just create a simple test.txt file saying 'Called from subagent'"

If this works without crashing, it proves subagents CAN use Task.
If it crashes, it confirms the recursion problem.