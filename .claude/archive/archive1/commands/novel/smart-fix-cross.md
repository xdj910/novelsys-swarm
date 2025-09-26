---
description: Fix cross-chapter consistency issues with intelligent analysis
---

# Smart Fix Cross-Chapter Command

Intelligently analyze and fix consistency issues across multiple chapters in proper sequence.

## Command Usage

- `/novel:smart-fix-cross` - Analyze and fix cross-chapter consistency issues

## Implementation

This command uses the smart-fix-cross-coordinator subagent to orchestrate comprehensive cross-chapter consistency fixes with:

- **Cross-Chapter Analysis**: Identify consistency issues across all chapters
- **Dependency Sequencing**: Fix issues in proper order to prevent cascading problems
- **Intelligent Prioritization**: Address most critical consistency issues first
- **Systematic Validation**: Ensure fixes maintain overall narrative coherence
- **Context Integration**: Update project understanding with consistency improvements

## Execution Steps

### Step 1: Cross-Chapter Consistency Analysis

Use the smart-fix-cross-coordinator to:
1. Analyze all completed chapters for consistency issues
2. Identify character, plot, and world-building inconsistencies
3. Map dependency relationships between consistency fixes

### Step 2: Intelligent Fix Orchestration

The coordinator will manage systematic consistency improvement covering:

**Analysis Phase**
- Scan all chapters for character voice, timeline, and continuity issues
- Identify priority consistency problems affecting narrative coherence
- Plan fix sequence to prevent cascading consistency problems

**Sequential Fix Phase**
- Apply fixes in dependency-aware sequence
- Address character consistency before plot consistency
- Ensure timeline and world-building coherence throughout

**Validation Phase**
- Verify consistency improvements across all affected chapters
- Validate overall narrative coherence and flow
- Update project context with improved consistency patterns

### Step 3: Consistency Validation

Ensure comprehensive consistency through:
- Cross-chapter validation of character voices and development
- Timeline and plot consistency verification
- World-building and setting coherence confirmation

## Expected Output

The smart-fix-cross-coordinator will provide:

1. **Consistency Analysis Report** identifying cross-chapter issues
2. **Fix Implementation Summary** showing improvements made across chapters
3. **Validation Results** confirming consistency achievement
4. **Context Updates** integrating improved consistency understanding

## Features

- **Comprehensive Analysis**: Full cross-chapter consistency evaluation
- **Intelligent Sequencing**: Dependency-aware fix application order
- **Narrative Coherence**: Maintain overall story flow and consistency
- **Systematic Validation**: Thorough verification of consistency improvements
- **Learning Integration**: Enhance future consistency maintenance

## Notes

- Cross-chapter fixes require careful sequencing to prevent consistency conflicts
- Comprehensive analysis ensures all consistency issues are identified and addressed
- Systematic validation maintains narrative coherence throughout fix process

## Data I/O

### File Operations
- **Reads from**:
  - `.claude/data/context/current_project.json`
  - [Project-specific configuration files]

- **Writes to**:
  - [Output files based on operation]
  - `.claude/data/logs/command_log.json`

- Context integration improves future consistency maintenance capabilities