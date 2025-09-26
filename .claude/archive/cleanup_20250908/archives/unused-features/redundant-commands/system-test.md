---
name: system-test
description: Test and validate the CCMP-enhanced NOVELSYS-SWARM system
tools:
  - Read
  - Write
  - Task
  - TodoWrite
  - Bash
---

# System Test Command

Test and validate the CCMP-enhanced NOVELSYS-SWARM system: **$ARGUMENTS** (test scope: 'full', 'context', 'agents', 'commands')

## Test Framework

### Comprehensive System Validation
Execute multi-layer testing to verify CCMP integration effectiveness:

**Layer 1: Context System Test**
- Validate persistent context architecture
- Test context synchronization across agents
- Verify conflict detection and resolution
- Check context inheritance chain integrity

**Layer 2: Agent Coordination Test**
- Test Issue-driven parallel execution
- Validate Director orchestration capabilities
- Check real-time context propagation
- Verify agent memory persistence

**Layer 3: Command System Test**
- Test all /novel:* slash commands
- Validate command parameter handling
- Check workflow automation
- Verify error handling and recovery

**Layer 4: Quality Integration Test**
- Test 30-minute validation cycles
- Validate 5-stage quality gates
- Check CCMP-style progress tracking
- Verify quality score consistency

**Layer 5: [ENHANCED] Entity & Genre System Test**
- Test entity dictionary loading and usage
- Validate genre detection and application
- Check variation vs error distinction
- Verify 95+ quality threshold enforcement

## Test Execution Plan

### Phase 1: Context System Validation
```python
async def test_context_system():
    """Test CCMP-style context persistence and synchronization"""
    
    test_cases = [
        {
            "name": "Context Loading Test",
            "action": "Load all context files and verify completeness",
            "expected": "All context files accessible with proper structure"
        },
        
        {
            "name": "Context Synchronization Test", 
            "action": "Update character profile and verify propagation",
            "expected": "Changes immediately visible to all agents"
        },
        
        {
            "name": "Conflict Detection Test",
            "action": "Create conflicting character information",
            "expected": "Automatic conflict detection and Bible-based resolution"
        },
        
        {
            "name": "Context Inheritance Test",
            "action": "Test Project -> Book -> Chapter -> Issue context flow",
            "expected": "Proper inheritance with no information loss"
        }
    ]
    
    results = []
    for test_case in test_cases:
        result = await execute_test_case(test_case)
        results.append(result)
        
        # Immediate failure handling
        if not result.passed:
            await escalate_test_failure(test_case, result)
    
    return ContextSystemTestResult(
        passed_tests=len([r for r in results if r.passed]),
        total_tests=len(test_cases),
        critical_failures=len([r for r in results if r.severity == "critical"]),
        system_health="healthy" if all(r.passed for r in results) else "needs_attention"
    )
```

### Phase 2: Agent Coordination Test
```python
async def test_agent_coordination():
    """Test CCMP Issue-driven parallel execution"""
    
    coordination_tests = [
        {
            "name": "Issue Decomposition Test",
            "action": "Test Director's ability to break chapter into parallel Issues",
            "validation": "Verify 8-12 Issues created with proper dependencies"
        },
        
        {
            "name": "Parallel Execution Test",
            "action": "Launch multiple agents simultaneously on independent Issues",
            "validation": "Verify agents work independently without conflicts"
        },
        
        {
            "name": "Context Sync Test",
            "action": "Test real-time context updates during parallel execution",
            "validation": "Verify agent sees updates from other agents immediately"
        },
        
        {
            "name": "Conflict Resolution Test",
            "action": "Create deliberate agent conflicts and test resolution",
            "validation": "Verify Director resolves conflicts using Bible authority"
        }
    ]
    
    # Execute coordination tests with real agents
    coordination_results = await execute_coordination_tests(coordination_tests)
    
    return AgentCoordinationTestResult(
        parallel_efficiency=coordination_results.parallel_execution_score,
        conflict_resolution_speed=coordination_results.avg_resolution_time,
        context_sync_reliability=coordination_results.sync_success_rate,
        director_effectiveness=coordination_results.director_decision_quality
    )
```

### Phase 3: Command System Test
```python
async def test_command_system():
    """Test /novel:* command functionality"""
    
    command_tests = [
        {
            "command": "/novel:bible-create",
            "args": "test-mystery-series",
            "expected_outputs": [
                "series_bible.yaml created",
                "context files updated", 
                "quality validation passed"
            ]
        },
        
        {
            "command": "/novel:chapter-start",
            "args": "1",
            "expected_outputs": [
                "Issue decomposition completed",
                "Parallel agents launched",
                "Chapter generated successfully"
            ]
        },
        
        {
            "command": "/novel:context-sync",
            "args": "",
            "expected_outputs": [
                "Context conflicts resolved",
                "Agent memories synchronized",
                "Consistency scores updated"
            ]
        },
        
        {
            "command": "/novel:quality-check",
            "args": "1",
            "expected_outputs": [
                "Quality validation completed",
                "Stage gate compliance verified",
                "Improvement recommendations generated"
            ]
        }
    ]
    
    command_results = []
    for test in command_tests:
        result = await execute_command_test(test)
        command_results.append(result)
        
        # Log command performance metrics
        await log_command_performance(test["command"], result)
    
    return CommandSystemTestResult(
        commands_tested=len(command_tests),
        success_rate=len([r for r in command_results if r.success]) / len(command_tests),
        average_execution_time=sum(r.duration for r in command_results) / len(command_results),
        error_recovery_effectiveness=calculate_error_recovery_rate(command_results)
    )
```

### Phase 4: Quality Integration Test
```python
async def test_quality_integration():
    """Test CCMP-style quality gates and validation cycles"""
    
    # [ENHANCED] Load entity dictionary and genre
    entity_dict_path = ".claude/agents/shared/entity_dictionary.yaml"
    project_genre = detect_current_project_genre()
    
    quality_tests = [
        {
            "name": "30-Minute Cycle Test",
            "action": "Execute complete validation cycle",
            "validation": "Verify all 4 phases complete within time limit"
        },
        
        {
            "name": "Stage Gate Test",
            "action": "Test 5-stage progression with 80% thresholds",
            "validation": "Verify gates prevent progression below thresholds"
        },
        
        {
            "name": "Quality Scoring Test",
            "action": "Generate content and verify 95+ quality target",
            "validation": "Verify consistent quality assessment"
        },
        
        {
            "name": "Continuous Improvement Test",
            "action": "Test system learning from quality feedback",
            "validation": "Verify quality scores improve over iterations"
        }
    ]
    
    quality_results = await execute_quality_tests(quality_tests)
    
    return QualityIntegrationTestResult(
        cycle_completion_rate=quality_results.cycle_success_rate,
        stage_gate_enforcement=quality_results.gate_compliance_rate,
        quality_target_achievement=quality_results.score_achievement_rate,
        continuous_improvement_trend=quality_results.improvement_slope
    )
```

## Performance Benchmarking

### CCMP Integration Metrics
```yaml
performance_benchmarks:
  context_system:
    - "Context load time: <2 seconds"
    - "Sync propagation time: <5 seconds"
    - "Conflict resolution time: <30 seconds"
    - "Context consistency: >98%"
    
  agent_coordination:
    - "Issue decomposition time: <3 minutes"
    - "Parallel execution efficiency: >85%"  
    - "Agent communication latency: <1 second"
    - "Director decision speed: <10 seconds"
    
  command_system:
    - "Command response time: <30 seconds"
    - "Workflow completion time: <2 hours"
    - "Error recovery success rate: >95%"
    - "User experience satisfaction: >90%"
    
  quality_integration:
    - "Cycle completion time: 30±5 minutes"
    - "Quality target achievement: >90%"
    - "Stage gate compliance: 100%"
    - "Improvement trend: positive slope"
```

## Test Reporting

### Comprehensive Test Report
Generate detailed report covering:

**System Health Dashboard**
- Overall system functionality: [PASS/FAIL]
- CCMP integration effectiveness: [Score 0-100] 
- Performance against benchmarks: [Percentage]
- Critical issues requiring attention: [List]

**Component Analysis**
- Context System: [Detailed status and metrics]
- Agent Coordination: [Parallel efficiency and reliability]
- Command System: [Functionality and user experience]
- Quality Integration: [Standards compliance and improvement]

**Recommendations**
- Immediate fixes required: [Priority list]
- Performance optimization opportunities: [Improvement suggestions]
- System enhancement recommendations: [Future development]
- Success criteria validation: [Achievement assessment]

## Test Execution Instructions

### Running the Tests
```bash
# Full system test
/novel:system-test full

# Specific component tests
/novel:system-test context
/novel:system-test agents  
/novel:system-test commands
/novel:system-test quality

# Performance benchmark only
/novel:system-test benchmark
```

### Success Criteria
The system passes testing if:
- All critical functionality works as designed
- CCMP integration patterns are properly implemented
- Performance meets or exceeds benchmark targets
- Quality standards are consistently achieved
- User experience meets design requirements

Execute comprehensive testing to validate that NOVELSYS-SWARM successfully integrates CCMP patterns for industrial-grade novel generation.