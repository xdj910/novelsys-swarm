---
description: Test automatic registry update integration
argument-hint: 'no arguments needed'
---

# Test Automatic Registry Updates

This command validates that the new automatic registry update system works correctly.

## Test Strategy

Use the art-workflow-coordinator subagent to generate a sample execution plan and verify:

1. **Coordinator Integration**: Plans include registry_update sections
2. **Execution Order**: Registry updates specified as "after_main_tasks" or "immediate"
3. **Required Flag**: All registry updates marked as required: true
4. **Context Passing**: Proper article path and update context provided

## Test Execution

Ask the coordinator to return a sample execution plan for Phase 3 (Research Collection) with these parameters:

**Test Context:**
- Article path: ".claude/data/articles/ai_realist/content/test_article_20250920"
- Phase: Research phase (should trigger registry update)
- Current status: "initiated" -> should update to "researched"

**Expected Plan Structure:**
```json
{
  "execution_plan": {
    "agents": [...],
  },
  "registry_update": {
    "agent": "art-registry-updater",
    "task": "Update article status to researched and phase to writing",
    "inputs": {
      "article_path": "{article_dir}",
      "update_context": "research_completed"
    },
    "required": true,
    "execution_order": "after_main_tasks"
  }
}
```

## Validation Criteria

**PASS conditions:**
- [ ] Plan includes registry_update section
- [ ] Registry update marked as required: true
- [ ] Execution order properly specified
- [ ] Article path and context correctly provided
- [ ] Update context matches phase completion

**FAIL conditions:**
- [ ] No registry_update in plan (old manual system)
- [ ] Registry update not marked as required
- [ ] Missing execution order specification
- [ ] Incorrect article path or context

This test confirms the automatic registry update system eliminates manual intervention requirements.