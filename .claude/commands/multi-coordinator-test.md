---
description: Test multi-coordinator collaboration in complex scenarios
argument-hint: '<complexity> <data-size>'
---

# Multi-Coordinator Test Command

Test a Command calling multiple Coordinators in collaboration, validating complex multi-phase task processing.

## Description

This command tests the Command -> Multi-Coordinator real collaboration pattern, validating:
- Sequential calling of multiple Coordinators
- Phase dependency handling
- Data passing between Coordinators
- Parallel Coordinator execution

## Arguments

- **$ARGUMENTS**:
  - Complexity: simple/complex/advanced (default: complex)
  - Data size: 50-500 (default: 100)

## Execution

### Real Multi-Coordinator Test

Use Task tool to call multiple coordinators in sequence, demonstrating Command -> Multi-Coordinator pattern:

1. **Phase 1: Data Analysis**
   - Use test-data-analysis-coordinator subagent
   - Analyzes requirements and creates execution plan
   - Outputs: phase1_analysis_plan.json

2. **Phase 2: Content Generation**
   - Use test-content-generation-coordinator subagent
   - Based on Phase 1 results
   - Outputs: phase2_content_plan.json

3. **Phase 3: Result Integration**
   - Main Claude integrates both coordinator outputs
   - Verifies phase dependencies
   - Generates final report

Test parameters:
- Complexity: ${ARGUMENTS[0]:-complex}
- Data size: ${ARGUMENTS[1]:-100}

The test requires the following coordinators to be present:
- test-data-analysis-coordinator
- test-content-generation-coordinator

These coordinators must be created first before running the multi-coordinator test.

Main Claude will execute real multi-coordinator collaboration:

**Phase 1: Data Analysis Coordination**
1. Use Task to call test-data-analysis-coordinator
2. Receive JSON plan specifying agents to execute
3. Execute the plan by calling agents with Task:
   - Task -> test-data-parser-agent (process input data)
   - Task -> test-data-analyzer-agent (analyze processed data)
4. Verify Phase 1 deliverables are created

**Phase 2: Content Generation Coordination**
5. Use Task to call test-content-generation-coordinator (with Phase 1 results)
6. Receive JSON plan specifying content generation agents
7. Execute the plan by calling agents with Task:
   - Task -> test-report-generator-agent (generate comprehensive report)
   - Task -> test-summary-generator-agent (create executive summary)
8. Verify Phase 2 deliverables are created

**Phase 3: Collaboration Validation**
9. Verify that Phase 2 agents successfully consumed Phase 1 results
10. Confirm that real work was performed by agents under coordinator management
11. Generate final multi-coordinator collaboration assessment

## Success Criteria

**Phase 1 Success Criteria:**
- [ ] test-data-analysis-coordinator returns agent execution plan
- [ ] test-data-parser-agent successfully processes input data
- [ ] test-data-analyzer-agent generates statistical insights
- [ ] Phase 1 deliverables created: parsed_data.json, analysis_results.json

**Phase 2 Success Criteria:**
- [ ] test-content-generation-coordinator validates Phase 1 completion
- [ ] test-report-generator-agent creates comprehensive report from real analysis
- [ ] test-summary-generator-agent generates executive summary
- [ ] Phase 2 deliverables created: test_report.md, executive_summary.json

**Multi-Coordinator Collaboration Validation:**
- [ ] Coordinators successfully managed actual agents (not just planning)
- [ ] Phase 2 agents consumed real results from Phase 1 agents
- [ ] True inter-coordinator collaboration demonstrated
- [ ] File-based communication enabled seamless multi-phase workflow
- [ ] Architecture pattern validated for complex workflows

## Next Steps

After successful execution:
- **Verify phase dependencies**: Check `.claude/testing/multi_coordinator_test/` for phase outputs
- **Run full test suite**: Use `/architecture-test full` for comprehensive validation
- **Review collaboration**: Analyze how Phase 1 data was used in Phase 2
- **Create custom coordinators**: Use this pattern for your own multi-phase workflows

## Notes

### Test Description
- This command simulates real multi-Coordinator collaboration scenarios
- Uses file system for inter-Coordinator communication
- Validates Phase dependencies and data passing

### Cleanup Strategy
- Test files saved in `.claude/testing/multi_coordinator_test/`
- No impact on production environment files
- Test files can be manually cleaned or retained for analysis after completion