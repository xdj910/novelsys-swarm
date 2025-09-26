---
description: Scan all components for potential trigger word issues
---

# Validate Trigger Words

Scans all commands, coordinators, and agents for potential trigger word patterns that could cause Task tool failures.

## Purpose

Proactively identify and report potential trigger word issues before they cause runtime failures.

## Execution

1. Scan all coordinator JSON plans for dangerous patterns
2. Check command files for unsafe Task prompts
3. Verify agents handle inputs defensively
4. Generate report of findings

## Validation Checks

- File names in prompts (e.g., "system_scan.json")
- Direct .claude/ path references
- Large file references without chunking mention
- Missing defensive input handling

## Expected Output

- **trigger_word_report.md**: List of components with potential issues
- **Severity levels**: Critical (will fail), Warning (might fail), Info (could be improved)