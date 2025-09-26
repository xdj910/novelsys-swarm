# Parallel Execution Checklist
*Lessons from ccpm-original to prevent execution errors*

## Pre-Execution Validation
- [ ] Read command specification completely
- [ ] Count required components (e.g., 4 agents)
- [ ] Verify all files/paths exist
- [ ] Check arguments are valid

## During Execution
- [ ] Follow spec exactly - don't optimize prematurely
- [ ] Launch all required components
- [ ] Track what has been launched
- [ ] Verify count matches requirement

## Specific to parallel-quality-check
Required agents per chapter (MUST be 4):
1. ✓ continuity-guard-specialist
2. ✓ plot-hole-detector  
3. ✓ conflict-resolver (checks Bible compliance)
4. ✓ quality-scorer

## Post-Execution Validation
- [ ] Confirm all components ran
- [ ] Check results match expected count
- [ ] Verify no components were skipped

## Error Prevention
- Don't batch/optimize until basic requirement met
- Count launched tasks vs required tasks
- Use TodoWrite to track progress systematically
- Validate against spec, not memory

## Recovery Pattern
If error detected:
1. Stop immediately
2. Document what was completed
3. Identify what was missed
4. Restart with complete set

---
*Created after analyzing ccpm-original patterns to prevent future parallel execution errors*