# NOVELSYS-SWARM Documentation System Index v6.6
*Last Updated: 2025-09-15*

## Documentation Hierarchy & Purpose

This index provides the complete map of the NOVELSYS-SWARM documentation system, showing how all components work together to create a recursion-safe, production-ready Claude Code architecture.

```
┌─────────────────────────────────────────────────┐
│            SYSTEM_INDEX.md (You are here)       │
│         Master Index & Navigation Guide          │
└────────────────────┬────────────────────────────┘
                     │
     ┌───────────────┴───────────────┐
     │                               │
┌────┴──────────────┐    ┌──────────┴──────────────┐
│    CLAUDE.md      │    │  .claude/templates/     │
│ System Authority  │    │  Implementation Kit     │
│ (Core Rules)      │    │  (How to Build)         │
└───────┬───────────┘    └───────────┬─────────────┘
        │                            │
        │                ┌───────────┴─────────────┐
        │                │                         │
┌───────┴─────────┐     │     ┌───────────────────┴──────────┐
│ claude-code-    │     │     │  Component Templates:        │
│ expert.md       │     │     │  - TEMPLATE_command.md       │
│ (Live Expert)   │     │     │  - TEMPLATE_coordinator.md   │
└─────────────────┘     │     │  - TEMPLATE_agent.md         │
                        │     └──────────────────────────────┘
                        │
                        │     ┌──────────────────────────────┐
                        │     │  Architecture & Reference:   │
                        └─────┤  - README.md                 │
                              │  - QUICK_REFERENCE.md        │
                              │  - ARCHITECTURE_data_layer.md│
                              │  - ARCHITECTURE_GOLD_STANDARD.md│
                              └──────────────────────────────┘
                                            │
                              ┌─────────────┴────────────┐
                              │ NOVEL_SYSTEM_PATTERNS.md │
                              │ (Application Patterns)   │
                              └──────────────────────────┘
```

## Document Roles & Relationships

### 1. **CLAUDE.md** - System Constitution
- **Location**: `/CLAUDE.md`
- **Role**: Single Source of Truth for all system rules
- **Contains**:
  - Five-Layer Architecture definition
  - 18 Golden Rules (including trigger word avoidance)
  - 6 Tested execution patterns
  - Task Tool Trigger Word Discovery (NEW v6.6)
  - Large File Handling Patterns
  - Python Script Integration best practices
  - Windows compatibility guidelines
  - System validation status
- **Authority Level**: HIGHEST - All other documents must comply
- **Version**: v6.6

### 2. **claude-code-expert.md** - Living Expert Agent
- **Location**: `/.claude/agents/claude-code-expert.md`
- **Role**: Executable expert that enforces CLAUDE.md rules
- **Contains**:
  - Real-time architecture validation
  - Problem-solving patterns
  - Community best practices
  - Continuous learning protocol
- **References**: CLAUDE.md for authority
- **Version**: v6.5

### 3. **Template System** - Implementation Standards
- **Location**: `/.claude/templates/`
- **Role**: Practical implementation guides and templates

#### Core Templates (Required):
- **TEMPLATE_command.md**: Create user-facing commands
  - Target: <100 lines (50-120 acceptable)
  - Pattern: Pure delegation

- **TEMPLATE_coordinator.md**: Create planning coordinators
  - Target: <250 lines
  - Pattern: Return JSON plans only

- **TEMPLATE_agent.md**: Create execution agents
  - Target: <500 lines
  - Pattern: Single responsibility

#### Reference Documents (Essential):
- **README.md**: Template system overview
  - Explains how templates work together
  - Usage guide for each template

- **QUICK_REFERENCE.md**: Rapid lookup guide
  - One-line rules
  - Common patterns
  - Quick validation

- **ARCHITECTURE_data_layer.md**: Deep architecture understanding
  - Why file system prevents recursion
  - I/O patterns and best practices
  - Communication mechanisms

- **ARCHITECTURE_GOLD_STANDARD.md**: Universal system design
  - Authority: Implementation Guide (subordinate to CLAUDE.md)
  - Contains: 7-part gold standard from 6 proven tests
  - Scope: ANY Claude Code system, not just novels
  - Version: 1.0

### 4. **Application Patterns** - Novel-Specific Implementation
- **Location**: `/.claude/`
- **Role**: Apply universal patterns to novel generation system

- **NOVEL_SYSTEM_PATTERNS.md**: Novel-specific patterns
  - Authority: Application Guide (subordinate to CLAUDE.md and ARCHITECTURE_GOLD_STANDARD.md)
  - Contains: Production patterns for novel generation
  - Scope: Novel system implementation
  - Version: 1.0

## Navigation Guide

### For New Developers
1. Start with **QUICK_REFERENCE.md** - Get oriented quickly
2. Read **CLAUDE.md** sections 1-3 - Understand core rules
3. Study **README.md** in templates - Learn the system
4. Use templates to create components

### For Creating Components
1. Choose template: Command, Coordinator, or Agent
2. Check **QUICK_REFERENCE.md** for rules
3. Copy appropriate **TEMPLATE_*.md**
4. Validate against **CLAUDE.md** rules

### For Troubleshooting
1. **claude-code-expert.md** - Ask the expert agent
2. **CLAUDE.md** "Common Errors" section
3. **ARCHITECTURE_data_layer.md** for I/O issues

### For System Validation
1. Run tests listed in **CLAUDE.md** section "System Test Validation Status"
2. Use **claude-code-expert.md** for architecture audits
3. Check **QUICK_REFERENCE.md** for rapid validation

## Version Control & Updates

### Current System Version: v6.6
- **Release Date**: 2025-09-15
- **Status**: Production Ready + Trigger-Word-Safe
- **Validation**: 100% recursion-safe, Windows compatible, trigger word protection validated
- **New Features**: Task tool trigger word discovery and prevention, 5-layer protection architecture, automated validation script

### Document Versioning Rules
1. **CLAUDE.md** version = System version
2. All documents sync to CLAUDE.md version
3. Updates cascade: CLAUDE.md → Templates → Expert

### Change Management
When updating any document:
1. Update CLAUDE.md first (if rule change)
2. Update templates to match
3. Update claude-code-expert.md
4. Update this INDEX
5. Test all patterns still work

## Quick Links Reference

### Essential Commands
- Test architecture: `/architecture-test`
- Test patterns: `/parallel-test`, `/io-patterns-test`
- Test pipeline: `/python-pipeline-test`
- Test coordinators: `/multi-coordinator-test`
- Test human-in-loop: `/human-in-loop-test`
- System health check: `/novel:system-check` (NEW)

### Key Sections
- [CLAUDE.md#golden-rules](CLAUDE.md#golden-rules) - 18 core principles (includes trigger word rule)
- [CLAUDE.md#task-tool-trigger-word-discovery](CLAUDE.md#task-tool-trigger-word-discovery) - Trigger word prevention (NEW v6.6)
- [CLAUDE.md#execution-patterns](CLAUDE.md#execution-patterns) - Tested patterns
- [CLAUDE.md#large-file-handling-patterns](CLAUDE.md#large-file-handling-patterns) - Chunked reading
- [QUICK_REFERENCE.md#recursion-prevention](QUICK_REFERENCE.md#recursion-prevention)
- [ARCHITECTURE_data_layer.md#io-patterns](ARCHITECTURE_data_layer.md#io-patterns)

### Template Sections
- [TEMPLATE_command.md#execution](TEMPLATE_command.md#execution)
- [TEMPLATE_coordinator.md#json-plan](TEMPLATE_coordinator.md#step-3-return-structured-plan)
- [TEMPLATE_agent.md#atomic-operations](TEMPLATE_agent.md#step-3-atomic-output-generation)

## System Health Indicators

### ✅ All Green Status
- **Architecture**: Five-layer model implemented
- **Recursion Safety**: 0 agents/coordinators with Task tool
- **Windows Compatibility**: Path handling documented
- **Testing**: All 6 patterns verified
- **Documentation**: Fully synchronized v6.6

### Critical Compliance Points
1. NO Unicode in any component
2. Only Main Claude has Task tool
3. Coordinators return JSON plans only
4. Agents execute single tasks only
5. File system for all communication
6. Atomic writes prevent corruption
7. Use chunked reading for large files (>256KB)
8. Use simple 1/2 choices for Human-in-Loop workflows
9. AVOID trigger words in Task prompts (use descriptive language)
10. Implement defensive input handling in agents

## Maintenance Notes

### Regular Audits
- Weekly: Run `/architecture-test`
- On changes: Update all cross-references
- Monthly: Review with claude-code-expert

### Documentation Standards
- Use ASCII only (no Unicode)
- Maintain cross-references
- Keep examples tested and working
- Update version numbers together

---

## Quick Decision Tree

**"I need to..."**

### Create something new:
→ Go to `/.claude/templates/` and choose template

### Fix an error:
→ Check CLAUDE.md "Common Errors and Fixes"

### Understand architecture:
→ Read ARCHITECTURE_data_layer.md

### Look up a rule quickly:
→ See QUICK_REFERENCE.md

### Validate my component:
→ Use claude-code-expert.md

### Understand the big picture:
→ Read CLAUDE.md completely

### Handle large files (>256KB):
→ Use CLAUDE.md "Large File Handling Patterns"

---

*This index is the navigation hub for the NOVELSYS-SWARM documentation system. All paths lead from here.*

**Remember**: When in doubt, CLAUDE.md is the ultimate authority.