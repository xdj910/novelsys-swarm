---
name: art-main-claude-execution-guide
description: Guide for Main Claude to execute workflow coordinator plans with automatic registry updates
tools: Read, Write
thinking: This is a reference guide for Main Claude to properly execute coordinator plans with the new automatic registry updates
---

## Input/Output Specification

### Input Requirements
Prompt from Main Claude:
- This is a reference document for executing art-workflow-coordinator plans
- No direct prompt input - used as reference during workflow execution

### File I/O Operations
Reads from:
- This document when executing coordinator plans
- Coordinator JSON plans from art-workflow-coordinator

Writes to:
- No direct file writes - guides Main Claude execution

### Output Format
Returns to Main Claude:
- Execution guidance and patterns
- Registry update procedures
- Error handling approaches

## Execution Guide for Main Claude

This guide explains how to properly execute art-workflow-coordinator plans with the new automatic registry update system.

### Standard Execution Pattern

When you receive a JSON execution plan from art-workflow-coordinator:

1. **Parse the Plan Structure**
   ```json
   {
     "execution_plan": {
       "agents": [...],  // Main phase work
       ...
     },
     "registry_update": {  // NEW: Automatic registry task
       "agent": "art-registry-updater",
       "task": "...",
       "inputs": {...},
       "required": true,
       "execution_order": "after_main_tasks|immediate"
     }
   }
   ```

2. **Execute Main Tasks First**
   - Execute all agents in the execution_plan section
   - Complete parallel/sequential work as specified
   - Verify all deliverables are created

3. **Execute Registry Update Automatically**
   - Check execution_order in registry_update section:
     - `"after_main_tasks"`: Execute after main work completes
     - `"immediate"`: Execute immediately (for completion phases)
   - Call the registry updater:
     ```
     Task -> art-registry-updater with:
     - Article path: {resolved from inputs.article_path}
     - Update context: {from inputs.update_context}
     ```

4. **Verify Success**
   - Confirm registry update completed successfully
   - Check that article status was updated correctly

### Registry Update Execution Examples

**Phase 3 (Research) Completion:**
```
1. Execute: art-trend-researcher, art-audience-analyst, art-competitor-scanner, art-topic-explorer
2. Verify: All research files created successfully
3. Execute: art-registry-updater with:
   - Article path: ".claude/data/articles/ai_realist/content/20250920_article"
   - Update context: "research_completed"
4. Verify: Registry shows status = "researched", phase = "writing"
```

**Phase 8 (Platform Optimization) Completion:**
```
1. Execute: art-platform-optimizer
2. Verify: All platform files (medium.md, substack.md, elevenreader.md) created
3. Execute: art-registry-updater with:
   - Article path: ".claude/data/articles/ai_realist/content/20250920_article"
   - Update context: "platform_optimization_completed"
4. Verify: Registry shows status = "ready_to_publish", phase = "publishing"
```

**Phase 9 (Publishing) Completion:**
```
1. Execute: art-registry-updater immediately with:
   - Article path: ".claude/data/articles/ai_realist/content/20250920_article"
   - Update context: "article_published"
2. Verify: Registry shows current_work cleared, statistics updated
```

### Path Resolution for Registry Updates

When executing registry updates, resolve path templates:

- `{article_dir}` -> Full path to article directory
- `{article_type_dir}` -> Full path to article type directory

**Example Resolution:**
```
Template: "{article_dir}"
Context: ai_realist article, ID 20250920_article
Resolved: ".claude/data/articles/ai_realist/content/20250920_article"
```

### Error Handling

**Registry Update Failures:**
1. **First**: Retry the registry update once
2. **If retry fails**: Report specific error details
3. **Continue workflow**: Don't block on registry failures
4. **Log issue**: Note registry inconsistency for later correction

**Missing Registry Update in Plan:**
- This should NOT happen with the new system
- If it does: Report as coordinator bug
- Manual fallback: Call art-registry-updater with appropriate context

### Benefits of Automatic System

**Before (Manual):**
- Main Claude had to remember to call registry updater
- Easy to forget, causing state inconsistencies
- Manual intervention required at each phase

**After (Automatic):**
- Registry updates built into every coordinator plan
- Zero risk of forgotten updates
- Seamless execution - no human memory required
- Real-time progress tracking guaranteed

### Validation Checklist

For each workflow execution, verify:
- [ ] Main phase tasks completed successfully
- [ ] Registry update executed as specified in plan
- [ ] Registry state matches expected phase progression
- [ ] No manual registry intervention required

### Key Success Indicators

**Working Correctly:**
- Every coordinator plan includes registry_update section
- Registry updates marked as required: true
- Execution order properly specified (after_main_tasks/immediate)
- Registry state stays consistent throughout workflow

**Needs Attention:**
- Coordinator plans missing registry_update sections
- Registry updates failing repeatedly
- Registry state inconsistent with workflow progress

This automatic system eliminates the primary source of article workflow failures: forgotten registry updates.