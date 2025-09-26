---
# TEMPLATE_command.md v6.6 - Updated 2025-09-15 with Trigger Word Prevention
description: [Brief description of what this command does - REQUIRED]
argument-hint: '[required_arg] <optional_arg>' # Use <> for optional, [] for required
# Optional frontmatter (only use if needed):
# allowed-tools: Read, Write, Bash  # Only if restricting Main Claude's tools
# Optional model for Main Claude (2025 options - rarely needed):
# model: claude-sonnet-4-20250514      # For complex command orchestration
# model: claude-opus-4-1-20250805      # For critical operations requiring highest capability
# NEVER include 'name:' field - it's not needed and creates inconsistency
---

# Command Title

[One-line description of the command's purpose - REQUIRED]

## Description

[Brief explanation of what this command accomplishes. Keep under 5 lines total.
Focus on WHAT the command achieves, not HOW it works.
Avoid implementation details - those belong in coordinators/agents.]

## Arguments (Optional Section)

<!-- Only include if command takes arguments -->
- **$ARGUMENTS**: [Description of expected arguments and format]
- Examples: [Show 1-2 usage examples if helpful]

## Execution

<!-- CRITICAL ARCHITECTURE COMPLIANCE RULES:
     - Commands SHOULD be <100 lines (target), but business completeness takes priority
     - If critical business context requires 97-120 lines, that's acceptable
     - Commands delegate to coordinators/agents, never implement logic
     - Use declarative "Use the X subagent to..." pattern
     - Preserve necessary workflow context for Main Claude
     - NO implementation code, but workflow instructions are OK

     TRIGGER WORD PREVENTION (v6.6):
     - ALWAYS warn Main Claude to avoid exact file names in Task prompts
     - Use descriptive language: "analyze scan data" NOT "analyze system_scan.json"
     - Include warning: "avoid trigger words that cause false Task tool errors" -->

### Simple Task Pattern (for direct execution)

<!-- Use this pattern when Main Claude can execute directly with basic tools -->
[Clear instructions for Main Claude to execute using Read/Write/Bash tools]

Example format:
```
Read the configuration from `.claude/data/context/current_project.json`
Display formatted results with project status and statistics.

# For Bash commands on Windows, use relative paths or forward slashes:
# GOOD: ls -la .claude/testing/*.json
# BAD:  ls -la "D:\testing\*.json" (backslashes fail)
```

### Complex Task Pattern (coordinator delegation) - MOST COMMON

<!-- Use this pattern for complex workflows requiring orchestration -->

**Delegating to coordinator:**

Use the [name]-coordinator subagent to [high-level goal description].

[Optional context/parameters to pass to coordinator]

Requirements:
- [Key requirement 1]
- [Key requirement 2]
- [Expected outcome]

IMPORTANT: When calling agents with Task tool, avoid using exact file names in prompts.
Use descriptive language (e.g., "process data in report directory") to prevent trigger word issues.

### Agent Delegation Pattern (simple single task)

<!-- Use this pattern for straightforward single-task operations -->

Use the [name]-agent subagent to [specific task description].

[Any specific parameters or file paths needed]

## Output

[Description of what the user will see and where files are saved.
Keep this section concise - focus on end-user visible results.]

## Success Criteria (Optional but Recommended)

<!-- Use this section for complex commands to clarify expectations -->
- [ ] [Measurable success criterion 1]
- [ ] [Measurable success criterion 2]
- [ ] [Quality/completion indicator]

## Next Steps

<!-- EXCELLENT PRACTICE - Include this section when possible -->
After successful execution:
- **Next action**: `/command:suggested-next` - [Brief description]
- **Alternative**: `/command:other-option` - [When to use this instead]
- **Quality check**: `/command:validation` - [If quality validation needed]

<!--
TEMPLATE COMPLIANCE CHECKLIST:
- Target <100 lines (FLEXIBLE - business completeness priority)
- Uses delegation pattern (not implementation)
- Preserves necessary business context
- Clean frontmatter (no 'name:' field)
- Clear one-line purpose
- Focuses on WHAT, not HOW
- Includes Next Steps when applicable

NEVER INCLUDE:
- Implementation code (belongs in agents)
- Low-level technical details
- Direct file manipulation code
- Complex conditionals in code form

OK TO INCLUDE (when necessary for business completeness):
- High-level workflow steps (for Main Claude context)
- Critical business rules and thresholds
- Quality requirements (e.g., "95+ score required")
- Parallel vs sequential execution guidance
- Large file handling requirements (>256KB files need chunked reading)

SECTION PRIORITY:
- Required: frontmatter, title, description, execution
- Recommended: output, next steps
- Optional: arguments, success criteria
- Situational: purpose (if different from description)

DELEGATION PATTERNS:
1. "Use the [name]-coordinator subagent to [goal]" - Complex workflows
2. "Use the [name]-agent subagent to [task]" - Single tasks  
3. Direct instructions - Only for simple Read/Write operations

GOOD EXAMPLES TO STUDY:
- knowledge-base-init.md (39 lines) - Perfect delegation
- next-chapter.md (45 lines) - Clean coordinator pattern
- chapter-start.md (56 lines) - Standard format

BAD EXAMPLES TO AVOID:
- bible-view.md (224 lines) - Too long, implementation details
- flow-mapping.md (216 lines) - Complex procedures in command
- status.md (130 lines) - Should delegate to coordinator
-->