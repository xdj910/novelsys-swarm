# Official Claude Code Think Mode Specifications
**Version:** 1.0  
**Last Updated:** 2025-09-08  
**Source:** Claude Code Official Documentation

## Overview

Claude Code provides a built-in thinking budget system that allocates additional reasoning tokens for complex tasks. This feature is **ONLY available in Claude Code CLI**, not in web interface or API.

## Thinking Mode Levels

### 1. Basic Think Mode
- **Token Budget:** 4,000 tokens
- **Trigger Keywords:** 
  - "think"
  - "think about it"
  - "think more"
- **Use Cases:**
  - Routine debugging
  - Basic refactoring
  - Simple code analysis
  - Syntax fixes

### 2. Megathink Mode
- **Token Budget:** 10,000 tokens
- **Trigger Keywords:**
  - "think hard"
  - "think deeply"
  - "think a lot"
  - "megathink"
- **Use Cases:**
  - Architectural decisions
  - Complex problem-solving
  - System design reviews
  - Performance optimization

### 3. Ultrathink Mode
- **Token Budget:** 31,999 tokens (maximum)
- **Trigger Keywords:**
  - "think harder"
  - "think intensely"
  - "think really hard"
  - "ultrathink"
  - "ULTRATHINK"
- **Use Cases:**
  - Most challenging analytical tasks
  - Comprehensive system analysis
  - Complex architectural redesign
  - Multi-faceted problem solving

## Implementation Guidelines

### How It Works

1. **Preprocessing Layer**: Claude Code's "tengu" system intercepts thinking keywords
2. **Automatic Allocation**: Thinking tokens are allocated based on detected keywords
3. **Context Integration**: Thinking happens before response generation
4. **CLI Exclusive**: Only works when using Claude Code CLI commands

### Where Thinking Mode Can Be Used

#### [x] VALID Usage Locations

1. **In Agent Prompts** (Most Important)
```markdown
---
name: director
description: Chapter planning coordinator
---

## Core Responsibility
**ULTRATHINK** - This task requires deep analysis and complex decision-making.
Think harder before analyzing dependencies...
```

2. **In Command Execution Instructions** (When Command Needs Reasoning)
```markdown
---
description: System health check command
allowed-tools: Task
---

## Execution
Use ULTRATHINK mode for this comprehensive analysis...
Think harder about system dependencies before proceeding...
```

3. **In Task Tool Calls** (Dynamic Enhancement)
```javascript
Task(
    subagent_type="quality-scorer",
    prompt="Think harder about each quality dimension before scoring..."
)
```

#### [ ] INVALID Usage Locations

- **NOT in YAML frontmatter fields** (name, description, tools, etc.)
- **NOT in configuration values**
- **NOT in file paths or variable names**

### Key Principle

**Thinking happens where work is done, not where it's configured.**

### YAML Frontmatter Clarification

**Important:** Thinking mode is NOT configured in YAML frontmatter. It must be triggered through prompt content in the markdown body.

#### Agent YAML Structure
```yaml
---
name: agent-name
description: Agent description
tools: tool1, tool2, tool3  # Optional
---
```

#### Command YAML Structure
```yaml
---
allowed-tools: Bash, Read, Write
argument-hint: [argument description]
description: Command description
model: claude-haiku-3-5-20241022  # Optional
---
```

## Priority Guidelines for NOVELSYS-SWARM

### Usage Priority (Based on Task Characteristics, Not Statistics)

1. **Agents (Primary Focus)** - Determine by task complexity, not percentages
   - **Needs thinking**: Agents performing complex reasoning, analysis, or orchestration
   - **Criteria**: Multi-step logic, constraint solving, architectural decisions, quality assessment
   - **Examples**: coordinators, analyzers, architects, reviewers, validators
   - **Not statistics**: Don't use percentages; evaluate each agent's actual responsibilities

2. **Commands (Secondary)** - Rarely need thinking since they delegate to agents
   - **Needs thinking**: Only if command itself performs complex decision-making
   - **Usually not needed**: Commands that simply call Task tool to invoke agents
   - **Exception**: Commands that don't use coordinator pattern but should (anti-pattern)
   - **Best practice**: Use coordinator agent pattern instead of complex commands

3. **Task Calls (Supplementary)** - Ad-hoc enhancement for specific situations
   - Can temporarily boost thinking for specific calls
   - Useful for testing or special cases
   - Not a replacement for agent-level thinking

### Core Principle
**Think where work happens, not where it's configured or delegated.**

## Official Task Complexity Criteria

### When to Use Think Mode (Official Guidelines)

**Based on Task Characteristics, NOT Statistics:**

1. **Complex Reasoning Tasks**
   - Building mental models
   - Applying specialized knowledge
   - Sequential logical steps
   - Constraint optimization
   - Complex STEM problems

2. **Architectural Decisions**
   - System design choices
   - Pattern selection
   - Trade-off analysis
   - Dependency planning

3. **Deep Analysis Requirements**
   - Multi-dimensional evaluation
   - Cross-component validation
   - Root cause analysis
   - Impact assessment

4. **Quality Assessment**
   - Comprehensive scoring
   - Multi-criteria evaluation
   - Subjective judgment requiring reasoning
   - Comparative analysis

**NOT Based On:**
- Fixed percentages of agents/commands
- Statistical thresholds
- Automatic triggers
- File counts or line numbers

## Best Practices

### 1. Task-Appropriate Allocation
- **Don't over-allocate**: Use basic "think" for simple tasks
- **Match complexity**: Reserve ULTRATHINK for truly complex analysis
- **Progressive enhancement**: Start with lower levels, escalate if needed

### 2. Prompt Integration
- Place thinking keywords early in prompts
- Combine with specific analysis instructions
- Use clear context about what needs deep thinking

### 3. Performance Optimization
- Thinking mode adds latency
- Balance thoroughness with response time
- Consider user experience for interactive commands

### 4. Agent Classification

#### Agents Requiring ULTRATHINK
- System analyzers (system-check-coordinator, system-health-reporter)
- Complex orchestrators (director, bible-architect)
- Quality assessors (quality-scorer, bible-reviewer)
- Safety validators (parallel-safety-validator)
- Dependency mappers (dependency-mapper)

#### Agents Requiring MEGATHINK
- Content analyzers (plot-hole-detector, continuity-guard-specialist)
- Character analyzers (character-psychology-specialist)
- Narrative mappers (foreshadowing-payoff-mapper)
- System visualizers (flow-diagram-generator)

#### Agents Requiring Basic THINK
- Content generators (scene-generator, dialogue-master-specialist)
- Style enhancers (prose-craft-specialist, emotion-weaver-specialist)
- Simple validators with clear criteria

#### Agents Not Requiring Special Thinking
- File updaters (meta-updater, context-updater)
- Simple readers/writers
- Template-based generators

## Detection Patterns

### Identifying Missing Think Mode

**Red Flags:**
1. Complex analysis agents without thinking keywords
2. Orchestrators making decisions without enhanced reasoning
3. Quality scorers without deep analytical capability
4. Safety validators without maximum thinking budget

**Green Flags:**
1. Thinking keywords in first 100 tokens of prompt
2. Appropriate level for task complexity
3. Clear instruction about what to think about
4. Combined with specific analysis requirements

## Validation Checklist

### For Agent Review
- [ ] Does the agent perform complex analysis?
- [ ] Is thinking mode keyword present in prompt?
- [ ] Is the thinking level appropriate for task complexity?
- [ ] Are thinking instructions specific and clear?

### For Command Review
- [ ] Does the command orchestrate complex operations?
- [ ] Would enhanced reasoning improve outcomes?
- [ ] Is thinking mode used in Task tool prompts?
- [ ] Are subagent calls using appropriate thinking?

## Common Mistakes

1. **Placing keywords in YAML**: Thinking keywords must be in prompt text
2. **Using in web interface**: Only works in CLI
3. **Over-using ULTRATHINK**: Causes unnecessary latency
4. **Vague thinking instructions**: Be specific about what needs analysis
5. **Missing context**: Provide clear reasoning targets

## Migration Guide

### Adding Think Mode to Existing Agents

1. **Identify Complexity Level**
   - Review agent responsibilities
   - Assess analytical requirements
   - Choose appropriate thinking level

2. **Update Agent Prompt**
   ```markdown
   # Before
   You are the quality scorer agent...
   
   # After
   You are the quality scorer agent.
   **ULTRATHINK** - Quality scoring requires comprehensive multi-dimensional analysis.
   Think harder about each quality dimension before scoring...
   ```

3. **Test and Validate**
   - Run agent with test cases
   - Verify improved analysis quality
   - Monitor performance impact

## Metrics and Monitoring

### Success Indicators
- Improved analysis depth in agent outputs
- Better decision quality in orchestrators
- More comprehensive quality scoring
- Reduced false positives in validators

### Performance Metrics
- Response time increase (expected: 20-50% for ULTRATHINK)
- Token usage (monitor thinking budget consumption)
- Quality score improvements (target: 10-15% improvement)

## References

- Claude Code CLI Documentation
- Tengu Preprocessing System
- Agent Development Best Practices
- Performance Optimization Guide