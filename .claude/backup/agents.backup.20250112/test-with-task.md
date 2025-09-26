---
name: test-with-task
description: Test subagent explicitly with Task tool
tools: Read, Write  # REMOVED Task to prevent recursion - subagents CANNOT have Task
---

# Test With Task

I'm a subagent that explicitly has the Task tool.

## Instructions

When called, I will:
1. Report that I have Task tool
2. Try to use Task to call another agent
3. Document what happens

This tests whether subagents CAN have Task tool or if it causes problems.