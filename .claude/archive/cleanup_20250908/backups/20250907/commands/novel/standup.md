---
description: Generate project status report
argument-hint: [report_type] e.g., "brief", "detailed", or "executive"
---

# Novel Standup Command  

Generate automatic intelligent status reports for NOVELSYS-SWARM: **$ARGUMENTS** (optional: 'daily', 'progress', 'blocked', 'agents')

## CCMP-Inspired Status Intelligence

### Automated Multi-Agent Status Collection
**Generate intelligent standup report:**

1. **Collect status dimensions:**
   - Agent activity summary: Get status of all agents
   - Chapter progress analysis: Analyze chapter pipeline
   - Quality metrics dashboard: Generate quality metrics
   - Blocking issues: Identify all blockers
   - Resource utilization: Assess resource usage
   - Next cycle recommendations: Predict next actions
   - Entity dictionary status: Check learning progress
   - Genre compliance: Verify genre standards
   - Learning system status: Report learning metrics

2. **Generate insights from collected data:**
   - Process all status dimensions
   - Identify critical issues
   - Find optimization opportunities
   - Determine priority actions

3. **Create comprehensive report with:**
   - Executive summary
   - Detailed status by dimension
   - Critical alerts
   - Optimization opportunities
   - Next recommended actions

### Real-Time Agent Status Matrix
```yaml
agent_status_categories:
  ACTIVE_WORKING:
    agents: ["scene-painter", "dialogue-specialist", "emotion-weaver"]
    current_tasks: ["ch03_scene_descriptions", "ch02_dialogue_polish", "ch01_emotional_layers"]
    estimated_completion: ["15 min", "25 min", "10 min"]
    quality_score: [95, 96, 97]  # [ENHANCED] All above 95 threshold
    
  WAITING_DEPENDENCIES:
    agents: ["mystery-architect", "pacing-optimizer"] 
    blocked_by: ["outline-creator completion", "scene-painter output"]
    estimated_wait: ["5 min", "15 min"]
    impact: ["critical_path", "optimization_opportunity"]
    
  QUALITY_VALIDATION:
    agents: ["quality-scorer", "consistency-guardian"]
    validating: ["ch01_final_draft", "character_consistency_ch01_ch02"]
    progress: ["80%", "60%"]
    preliminary_results: ["93/100", "inconsistency_detected"]
    
  IDLE_AVAILABLE:
    agents: ["food-culture-expert", "weather-mood-setter"]
    availability: ["immediate", "immediate"] 
    best_next_tasks: ["cultural_details_ch04", "atmosphere_ch03"]
    resource_cost: ["low", "low"]
    
  ERROR_RECOVERY:
    agents: ["voice-tuner"]
    error_type: ["context_conflict"]
    recovery_action: ["context_resync_in_progress"]
    eta: ["3 min"]
```

## Comprehensive Status Categories

### 1. Executive Dashboard

**Generate high-level status for project managers:**
    
    dashboard_metrics = {
1. **Collect overall progress metrics:**
   - Bible completeness: Check if bible.yaml exists and is complete
   - Chapters completed: Count chapters with content.md files
   - Quality average: Calculate average quality scores
   - Timeline adherence: Assess schedule status

2. **Calculate velocity metrics:**
   - Chapters per week: Track generation speed
   - Quality improvement rate: Monitor quality trends
   - Efficiency gains: Measure system improvements
   - Cost optimization: Calculate resource savings

3. **Assess system health:**
   - Agent reliability: Check agent performance
   - Context consistency: Measure context integrity
   - Parallel efficiency: Evaluate concurrent processing
   - Resource utilization: Analyze resource usage

4. **Identify risk indicators:**
   - Quality risks: Find quality issues
   - Timeline risks: Assess schedule risks
   - Resource constraints: Check resource limits
   - Technical debt: Evaluate maintenance needs

5. **Generate executive dashboard with:**
   - Key metrics summary
   - Executive status summary
   - Critical decisions needed
   - Success indicators highlighted

### 2. Technical Progress Report

**Generate detailed technical status:**

1. **Chapter pipeline status:**
   - In planning: List chapters being planned
            "in_generation": await list_chapters_in_generation(),
            "in_quality_review": await list_chapters_in_qa(),
            "completed": await list_completed_chapters(),
            "pipeline_efficiency": await calculate_pipeline_throughput()
        },
        
        "agent_performance": {
            "high_performers": await identify_top_performing_agents(),
            "performance_issues": await identify_underperforming_agents(),
            "optimization_opportunities": await suggest_agent_optimizations(),
            "resource_allocation": await analyze_agent_workload_distribution()
        },
        
        "quality_analysis": {
            "quality_trends": await track_quality_over_time(),
            "dimension_analysis": await analyze_quality_by_dimension(),
            "improvement_areas": await identify_quality_improvement_areas(),
            "quality_gate_performance": await assess_gate_pass_rates()
        },
        
        "system_performance": {
            "parallel_execution_efficiency": await measure_parallel_benefits(),
            "context_sync_performance": await analyze_context_operations(),
            "system_utilization": await assess_system_effectiveness(),
            "command_system_usage": await analyze_command_usage_patterns()
        }
    }
    
    return TechnicalProgressReport(
        detailed_metrics=technical_status,
        performance_analysis=analyze_performance_trends(technical_status),
        optimization_recommendations=generate_tech_recommendations(technical_status),
        infrastructure_status=assess_system_infrastructure(technical_status)
    )
```

### 3. Blocking Issues Intelligence

**Smart identification and prioritization of blocking issues:**

1. **Analyze critical blockers:**
   - Detect Bible inconsistencies across chapters
   - Identify failing quality gates and thresholds
   - Detect agent performance issues and malfunctions
   - Identify resource constraints and bottlenecks

2. **Assess cascading impact:**
   - Map blocked agents by specific issues
   - Calculate chapter delays caused by blockers
   - Assess quality degradation risk from issues
   - Calculate timeline impact of current blockers

3. **Develop resolution strategies:**
   - Identify immediate quick fixes available
   - Suggest temporary workaround options
   - Determine escalation requirements for complex issues
   - Recommend prevention measures for future

4. **Create priority matrix:**
   - Calculate blocking severity impact scores
   - Estimate resolution effort for each issue
   - Assess business criticality of blockers
   - Optimize resolution sequence order

5. **Return blocking issues intelligence:**
   - Compile critical_blockers analysis
   - Provide impact_assessment summary
   - Include resolution_plan strategies
   - Add priority_recommendations matrix

## Smart Insights Generation

### Automated Insight Discovery
```yaml
insight_patterns:
  performance_trends:
    - "质量分数连续3天上升  ->  系统学习效果显著"
    - "Agent协作效率提升15%  ->  上下文同步优化见效"
    - "执行效率达到85%  ->  系统运行良好"
    
  quality_patterns:
    - "角色一致性分数>95%  ->  角色设定成功，可复用模式"
    - "情节逻辑分数波动  ->  需要加强outline-creator训练"
    - "文笔风格分数稳定90+  ->  voice-tuner参数调优成功"
    
  efficiency_opportunities:
    - "3个Agent同时空闲  ->  可以启动新的并行任务"
    - "质量检查时间>15分钟  ->  可以预先并行化QA流程"
    - "上下文同步频率<80%  ->  需要优化同步触发机制"
    
  risk_indicators:
    - "连续2章质量下降  ->  可能存在系统性问题"
    - "Agent错误率>5%  ->  需要检查上下文或模型配置"
    - "资源利用率>90%  ->  需要扩容或优化"
```

### Predictive Recommendations

**Generate future-looking recommendations based on current trends:**

1. **Build prediction models:**
   - Predict quality trajectory trends
   - Predict system performance evolution
   - Predict resource requirements growth
   - Predict project completion timeline

2. **Initialize recommendation categories:**
   - immediate_actions: urgent items needing attention
   - short_term_optimizations: improvements for next sprint
   - strategic_improvements: long-term system enhancements
   - risk_mitigation_measures: preventive actions

3. **Generate model-based recommendations:**
   - For each prediction model and its results:
     * Generate specific recommendations based on model_name
     * Categorize recommendations by timeframe
     * Add recommendations to appropriate category

4. **Return predictive recommendations:**
   - Include all prediction_models results
   - Provide actionable_recommendations by category
   - Calculate confidence_scores for predictions
   - Define success_metrics for recommendations

## Status Report Formats

### Daily Standup Format
```markdown
# 📊 NOVELSYS-SWARM Daily Standup
## 2025-08-29 09:00

### 🎯 Executive Summary
- **Overall Progress**: 87% (^3% from yesterday)
- **Active Chapters**: 3 (ch01: QA, ch02: Generation, ch03: Planning)  
- **System Health**: 96% (All agents operational)
- **Quality Average**: 93.2/100 (^0.8 from yesterday)

### 🤖 Agent Status Matrix
- **ACTIVE** (8): Working on current tasks, ETA 15-45min
- **WAITING** (2): Blocked by dependencies, unblocking in progress
- **QA** (3): Quality validation in progress, 70-90% complete
- **IDLE** (4): Available for new tasks

### 🚧 Critical Issues
- **NONE** - All systems operational [x]

### 🎯 Today's Priorities  
1. Complete ch01 quality validation (15min)
2. Launch ch03 parallel generation (45min)
3. Optimize agent resource allocation (20min)

### 📈 Key Metrics
- **Parallel Efficiency**: 89% (target: 85%)
- **Context Consistency**: 98.2% (target: 95%)
- **Cost per Chapter**: $2.15 (v$0.30 from baseline)
```

### Weekly Progress Format  
```markdown
# 📊 NOVELSYS-SWARM Weekly Report  
## Week of 2025-08-25

### 🏆 Key Achievements
- Completed 5 chapters with 95+ quality scores (Learning Qualified)
- Achieved 3x speed improvement with parallel execution
- Zero critical system failures or data loss
- Reduced generation cost by 40%

### 📊 Performance Metrics
- **Quality Trend**: ^12% improvement over week
- **Velocity**: 0.8 chapters/day (target: 0.5)
- **Agent Reliability**: 97.3% uptime
- **User Satisfaction**: 9.2/10

### 🔄 System Optimizations
- Optimized chapter generation workflow
- Enhanced context persistence (50% less context recomputation)
- Optimized agent allocation (15% resource savings)

### 🎯 Next Week Focus
- Scale to 5-chapter parallel generation
- Implement advanced quality prediction
- Launch autonomous Bible evolution
```

## Usage Commands

### Basic Status Queries
```bash
# Daily standup report
/novel:standup daily

# Current progress snapshot
/novel:standup progress

# Blocking issues analysis  
/novel:standup blocked

# Agent activity report
/novel:standup agents
```

### Advanced Analytics
```bash
# Executive dashboard
/novel:standup executive

# Technical deep-dive
/novel:standup technical

# Predictive analysis
/novel:standup predict

# Performance optimization report
/novel:standup optimize
```

This intelligent status reporting system eliminates manual status gathering and provides actionable insights automatically, just like CCPM's automated progress tracking.

## Actual Implementation

### Execute Status Report

**Parse arguments and initialize:**
1. Get mode from $ARGUMENTS (default: "daily")
2. Valid modes: daily, weekly, sprint, detailed

**Get current project:**
1. Use Read tool: `.claude/data/context/current_project.json`
2. Parse JSON to get project name
3. If no project found:
   - Display: "[ ] Error: No active project. Use /novel:project-new to create one."
   - Stop execution

**Load project data:**
1. Set project path: `.claude/data/projects/{project_name}`
2. Use Read tool: `{project_path}/project.json`
3. Parse project configuration
4. If project not found:
   - Display: "[ ] Error: Project {project_name} not found"
   - Stop execution

**Gather statistics:**
1. Check if bible.yaml exists in project directory
2. Use Glob tool: `{project_path}/chapters/ch*`
3. Get list of chapter directories
4. Sort chapters by number

**Calculate progress:**
1. Get total chapters from project config (default: 30)
2. Count completed chapters:
   - For each chapter directory
   - Check if content.md exists
   - Count as completed if exists
3. Get current chapter from project progress
4. Get total word count from project progress

**Calculate quality metrics:**
1. Get last 3 chapter directories
2. For each recent chapter:
   - Check if meta.json exists
   - Use Read tool on meta.json
   - Parse JSON metadata
   - Extract quality_score if present
   - Add to scores list
3. Calculate average quality:
   - Sum all scores
   - Divide by count
   - Default to 0 if no scores

# Analyze agent status (simplified)
active_agents = []
blocked_agents = []
idle_agents = ["world-builder", "mystery-architect", "character-psychologist", "bible-architect"]

# Check for blockers
blockers = []
if not bible_exists:
    blockers.append("Bible未创建 - 阻塞所有内容生成")
if avg_quality > 0 and avg_quality < 95:
    blockers.append(f"质量未达标 ({avg_quality:.1f}/95) - 需要优化")

**Generate report based on mode:**

**Get current timestamp for report**

**If mode is "daily":**
1. Display header box:
   ```
   +===========================================================+
   |              📊 NOVELSYS-SWARM Daily Standup              |
   +===========================================================+
   ```

2. Display current date and time: "📅 {YYYY-MM-DD HH:MM}"

3. Display Executive Summary:
   - Header: "🎯 **Executive Summary**"
   - Separator line: "-------------------------"
   - Show: "Project: {project_name}"
   - Calculate progress percentage: (completed_chapters / total_chapters * 100)
   - Show: "Progress: {completed}/{total} chapters ({percentage}%)"
   - Choose quality icon: "[x]" if avg_quality >= 95, else "WARNING:️"
   - Show: "Quality Average: {avg_quality}/100 {icon}"
   - Show: "Total Words: {total_words}" (formatted with commas)

4. Display Agent Status:
   - Header: "🤖 **Agent Status**"
   - Separator line: "---------------------"
   - Show: "ACTIVE: {count} agents"
   - Show: "BLOCKED: {count} agents"
   - Show: "IDLE: {count} agents available"

5. Display Critical Issues:
   - Header: "🚧 **Critical Issues**"
   - Separator line: "---------------------"
   - If blockers list is not empty:
     * For each blocker in list:
       * Display: "-  {blocker}"
   - If blockers list is empty:
     * Display: "-  NONE - All systems operational [x]"

6. Display Today's Priorities:
   - Header: "🎯 **Today's Priorities**"
   - Separator line: "------------------------"
   - If Bible doesn't exist:
     * Display: "1. Create Series Bible (/novel:bible-create)"
   - Else if no chapters completed:
     * Display: "1. Start Chapter 1 (/novel:chapter-start 1)"
   - Else if current_chapter <= total_chapters:
     * Display: "1. Write next chapter (/novel:next-chapter)"
     * Display: "2. Quality check recent chapters (/novel:quality-check all)"
   - Else (book is complete):
     * Display: "1. Final quality review (/novel:quality-check all)"
     * Display: "2. Complete book (/novel:book-complete)"

**Else if mode is "progress":**
1. Display header box:
   ```
   +===========================================================+
   |              📈 NOVELSYS-SWARM Progress Report            |
   +===========================================================+
   ```

2. Display project overview:
   - Header: "📚 **{project_name}**"
   - Separator line: "-------------------------"
   - Calculate completion percentage: (completed_chapters / total_chapters * 100)
   - Display: "Chapters: {completed}/{total} ({percentage}%)"
   - Display: "Words: {total_words}" (formatted with commas)
   - Display: "Quality: {avg_quality}/100"

3. Display chapter status:
   - Header: "📊 **Chapter Status**"
   - Separator line: "---------------------"
   - For first 5 chapters (or all if fewer):
     * Check if {ch_dir}/content.md exists
     * If exists: status = "[x]"
     * If not exists: status = "🔄"
     * Display: "  Chapter {number}: {status}"
   - If more than 5 chapters:
     * Display: "  ... and {remaining_count} more"

**Else if mode is "blocked":**
1. Display header box:
   ```
   +===========================================================+
   |             🚧 NOVELSYS-SWARM Blocking Issues             |
   +===========================================================+
   ```

2. Display blockers section:
   - Header: "WARNING:️ Warning: **Current Blockers**"
   - Separator line: "---------------------"
   - If blockers list is not empty:
     * For each blocker with index:
       * Display: "{index}. {blocker}"
   - If blockers list is empty:
     * Display: "[x] No blocking issues detected"
    
3. Display recommended actions:
   - Header: "💡 **Recommended Actions**"
   - Separator line: "--------------------------"
   - If Bible doesn't exist:
     * Display: "-  Run: /novel:bible-create"
   - If avg_quality > 0 AND avg_quality < 95:
     * Display: "-  Run: /novel:quality-check all"

**Else if mode is "agents":**
1. Display header box:
   ```
   +===========================================================+
   |              🤖 NOVELSYS-SWARM Agent Report               |
   +===========================================================+
   ```

2. Display agent distribution:
   - Header: "📊 **Agent Distribution**"
   - Separator line: "------------------------"
   - Display: "Total Agents: 23"
   - Display: "Active: {active_count}"
   - Display: "Blocked: {blocked_count}"
   - Display: "Idle: {idle_count}"

3. Display available agents:
   - Header: "🟢 **Available Agents**"
   - Separator line: "---------------------"
   - For first 5 idle agents:
     * Display: "  -  {agent_name}"

4. Display optimization opportunities:
   - Header: "🎯 **Optimization Opportunities**"
   - Separator line: "---------------------------------"
   - Display: "-  Launch parallel chapter generation with idle agents"
   - Display: "-  Use /novel:chapter-start for efficient generation"

**Else (unknown mode):**
1. Display: "[ ] Error: Unknown mode - {mode}"
2. Display: "Available modes: daily, progress, blocked, agents"

**Display footer for all modes:**
1. Display separator line: "-" repeated 61 times
2. Display: "💡 Use /novel:next for intelligent task recommendations"
3. Display: "📊 Use /novel:status for detailed project information"