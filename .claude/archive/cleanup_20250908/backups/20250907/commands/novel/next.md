---
description: Recommend next priority tasks
argument-hint: [filter] e.g., "quality", "content", or none for all
---

# Novel Next Command - Intelligent Multi-Level Task Recommendation System

Intelligently recommend optimal next tasks based on comprehensive project analysis: **$ARGUMENTS** (optional: 'chapter', 'quality', 'context', 'series', or 'all')

## Intelligent Priority Analysis

### CCMP-Inspired Smart Recommendations

**Analyze current state and recommend optimal next action:**

1. **Load context for intelligent recommendations:**
   - Use Bash tool: `mkdir -p .claude/data/projects/{project}/shared`
   - Set entity_dict_path: `.claude/data/projects/{project}/shared/entity_dictionary.yaml`
   - Detect project genre from Bible
   - Set quality_threshold: 95 (learning eligibility threshold)

2. **Analyze multiple dimensions:**
   
   **Dependency Analysis:**
   - Identify blocked tasks awaiting prerequisites
   - Identify ready tasks with all dependencies met
   - Map prerequisite chains for optimization
   
   **Parallel Opportunities:**
   - Find independent tasks safe for parallel execution
   - Assess agent availability for task distribution
   - Check system capacity for concurrent operations
   
   **Progress Bottlenecks:**
   - Identify failing quality gates blocking progress
   - Detect context inconsistencies causing conflicts
   - Analyze agent performance bottlenecks
   
   **Strategic Priorities:**
   - Assess Bible completeness status
   - Evaluate chapter generation pipeline
   - Estimate reader value impact of tasks

3. **Calculate priority matrix:**
   - Combine all analysis dimensions
   - Apply weighted scoring algorithm
   - Generate priority scores for each task

4. **Return smart recommendation result:**
   - top_recommendation: highest impact task
   - parallel_opportunities: tasks for concurrent execution
   - blocking_issues: critical blockers to resolve
   - efficiency_gain: expected improvement percentage

### Multi-Dimensional Priority Matrix
```yaml
priority_calculation_factors:
  impact_weight: 40%      # 对整体项目的影响度
  urgency_weight: 25%     # 任务的紧急程度
  effort_weight: 15%      # 完成任务的工作量
  dependency_weight: 10%  # 解除阻塞的价值
  parallel_weight: 10%    # 并行化的可能性

priority_scoring_algorithm:
  high_impact_low_effort:
    score: 90-100
    examples: ["修复关键Bible冲突", "完成阻塞其他任务的前置条件"]
    
  high_impact_medium_effort:
    score: 70-89
    examples: ["生成核心章节", "建立重要角色关系"]
    
  parallel_optimization:
    score: 60-79
    examples: ["启动多个独立章节", "并行优化不同维度"]
    
  maintenance_tasks:
    score: 30-59
    examples: ["上下文清理", "文档更新"]
    
  low_priority:
    score: 0-29
    examples: ["非关键细节优化", "未来功能规划"]
```

## Smart Task Categories

### 1. Critical Path Tasks

**Identify tasks on the critical path blocking overall progress:**

1. **Define critical indicators:**
   
   **Bible Incomplete:**
   - Condition: bible_incomplete
   - Impact: "阻塞所有后续创作"
   - Recommendation:
     * Task: `/novel:bible-create [series-name]`
     * Priority: CRITICAL
     * Estimated time: 30-45 minutes
     * Blocking agents: ALL
   
   **Context Conflicts:**
   - Condition: context_conflicts_detected
   - Impact: "Agent产生不一致内容"
   - Recommendation:
     * Task: `/novel:context-sync all`
     * Priority: HIGH
     * Estimated time: 5-10 minutes
     * Blocking agents: content-generators
   
   **Quality Gate Failures:**
   - Condition: quality_gate_failures
   - Impact: "无法推进到下一阶段"
   - Recommendation:
     * Task: `/novel:quality-check [failing-chapter]`
     * Priority: HIGH
     * Estimated time: 15-20 minutes
     * Blocking agents: quality-validators

2. **Assess current project state:**
   - Load project metadata
   - Check Bible status
   - Analyze quality reports
   - Detect context issues

3. **Check active critical tasks:**
   - For each critical indicator:
     * Check if condition matches current state
     * If match found, add recommendation to active_critical_tasks

4. **Return critical path analysis:**
   - critical_tasks: list of active critical tasks
   - total_blocking_impact: calculated blocking severity
   - recommended_sequence: optimized task execution order

### 2. Parallel Optimization Opportunities

**Find tasks that can be executed in parallel for maximum efficiency:**

1. **Define parallel analysis opportunities:**
   
   **Independent Chapters:**
   - Condition: multiple_chapters_ready_for_generation
   - Opportunity: batch_generation
   - Potential gain: 300-500% speed improvement
   - Resources required: sequential processing
   
   **Cross-Dimensional Optimization:**
   - Condition: existing_content_needs_enhancement
   - Opportunity: parallel_quality_improvement
   - Tasks available:
     * dialogue_enhancement
     * atmosphere_enrichment
     * character_deepening
     * plot_tightening
   
   **Bible Expansion:**
   - Condition: core_bible_stable_but_incomplete
   - Opportunity: parallel_bible_development
   - Tasks available:
     * character_backstory_expansion
     * world_detail_enrichment
     * mystery_logic_refinement
     * cultural_authenticity_research

2. **Assess system capacity:**
   - Check available resources
   - Evaluate current workload
   - Determine parallel execution limits

3. **Check opportunity feasibility:**
   - For each opportunity:
     * Verify condition is met
     * Check resource availability
     * If feasible, add to available_opportunities

4. **Return parallel opportunity analysis:**
   - opportunities: list of available parallel tasks
   - max_efficiency_combination: optimal task combination
   - resource_constraints: system limitations

### 3. Quality Improvement Tasks

**Identify quality improvement tasks with highest ROI:**

1. **Perform comprehensive quality assessment:**
   - Analyze character depth scores
   - Evaluate plot coherence metrics
   - Assess atmospheric richness levels
   - Review all quality dimensions

2. **Identify improvement opportunities:**
   
   **Character Depth:**
   - Current score from quality analysis
   - Calculate improvement potential
   - Effort required: medium
   - Reader impact: high
   
   **Plot Coherence:**
   - Current score from quality analysis
   - Calculate improvement potential
   - Effort required: high
   - Reader impact: very_high
   
   **Atmospheric Richness:**
   - Current score from quality analysis
   - Calculate improvement potential
   - Effort required: low
   - Reader impact: medium

3. **Prioritize by ROI:**
   - Calculate ROI = (reader_impact x improvement_potential) / effort
   - Sort opportunities by ROI descending
   - Identify quick wins (low effort tasks)
   - Identify high impact projects

4. **Return quality improvement analysis:**
   - prioritized_tasks: sorted by ROI
   - quick_wins: low effort, good return
   - high_impact_projects: maximum reader value

## Smart Recommendation Engine

### Contextual Recommendations
```yaml
recommendation_contexts:
  empty_project:
    top_recommendation: "/novel:bible-create [series-name]"
    reasoning: "没有Bible就无法进行任何创作"
    next_steps: ["bible创建", "角色设定", "世界构建"]
    
  bible_complete_no_chapters:
    top_recommendation: "/novel:chapter-start 1" 
    reasoning: "Bible完备，可以开始第一章创作"
    # 可以按顺序生成多个章节
    
  chapters_in_progress:
    top_recommendation: "/novel:quality-check [章节号]"
    reasoning: "确保现有章节质量后再继续"
    optimization_option: "/novel:context-sync"
    
  quality_issues_detected:
    top_recommendation: "解决最严重的质量问题"
    reasoning: "质量问题会影响后续所有工作"
    specific_actions: ["修复一致性冲突", "提升不达标维度"]
    
  system_ready_for_scaling:
    top_recommendation: "/novel:chapter-start [下一章节]" 
    reasoning: "系统状态良好，可以继续生成章节"
    efficiency_gain: "保持稳定"
```

### Recommendation Confidence Scoring

**Calculate confidence score for recommendations:**

1. **Assess confidence factors:**
   
   **Data Completeness (30% weight):**
   - Assess available data quality
   - Check for missing information
   - Verify data consistency
   
   **System Stability (25% weight):**
   - Evaluate system health metrics
   - Check for recent errors
   - Verify agent availability
   
   **Historical Accuracy (20% weight):**
   - Analyze past recommendation success
   - Review completion rates
   - Track effectiveness metrics
   
   **Resource Availability (15% weight):**
   - Check resource constraints
   - Verify capacity limits
   - Assess workload balance
   
   **External Dependencies (10% weight):**
   - Verify external readiness
   - Check integration points
   - Validate prerequisites

2. **Calculate weighted score:**
   - Sum up (weight x score) for each factor
   - Divide by total weight sum
   - Determine confidence level:
     * HIGH if score > 80
     * MEDIUM if score > 60
     * LOW otherwise

3. **Return recommendation confidence:**
   - confidence_score: weighted average
   - confidence_level: HIGH/MEDIUM/LOW
   - contributing_factors: detailed breakdown
   - reliability_estimate: percentage confident

## Usage Examples

### Basic Next Task Query
```bash
# 获取下一个最优任务推荐
/novel:next

# 示例输出:
# 🎯 TOP RECOMMENDATION: /novel:bible-create "mystery-series"
# 📊 Confidence: 95% (HIGH)
# ⏱️ Estimated Time: 30-45 minutes  
# 🚧 Currently Blocking: ALL content generation
# 📈 Impact: Unlocks entire creation pipeline
```

### Specific Context Analysis
```bash
# 分析特定方面的优化机会
/novel:next chapter     # 章节相关任务
/novel:next quality     # 质量改进机会  
/novel:next context     # 上下文优化建议
/novel:next parallel    # 并行化机会

# 获取全面分析
/novel:next all
```

### Advanced Recommendations
```bash
# 获取并行化建议
/novel:next parallel

# 示例输出:
# 🔄 PARALLEL OPPORTUNITIES:
# 1. Launch sequential chapter generation
# 2. Cross-dimensional quality enhancement (4 parallel streams)
# 3. Bible expansion in 6 independent areas
# 
# 💡 OPTIMAL STRATEGY: Sequential generation + quality validation
# 🎯 Expected Outcome: 3 chapters + improved quality in 90 minutes
```

This intelligent task prioritization system eliminates guesswork and maximizes productivity by always recommending the highest-impact next action based on comprehensive project analysis.

## Actual Implementation

### Execute Analysis

**Analyze project state and generate recommendations:**

1. **Get current project:**
   - Use Read tool: `.claude/data/context/current_project.json`
   - If no project found:
     * Display: "[ ] Error: No active project"
     * Display: "🎯 Recommended: /novel:project-new '项目名称'"
     * Stop execution
   - Extract project_name

2. **Load project metadata and detect structure:**
   - Use Read tool: `.claude/data/projects/{project_name}/project.json`
   - Extract progress information
   - Extract current_book from project["metadata"]["current_book"] (default: 1)
   - Use Glob tool: `.claude/data/projects/{project_name}/book_*/` to detect series structure
   - If multiple books found: Set is_series = True

3. **Intelligent multi-level Bible status check:**
   - Check current book Bible: `.claude/data/projects/{project_name}/book_{current_book}/bible.yaml`
   - Check series Bible if exists: `.claude/data/projects/{project_name}/series_bible.yaml`
   - For series, scan all books: `book_*/bible.yaml`
   - Store comprehensive Bible status map

4. **Smart chapter status check with backward compatibility:**
   
   **Try current book structure first (new standard):**
   - Use Glob tool: `.claude/data/projects/{project_name}/book_{current_book}/chapters/*/content.md`
   - Store as: current_book_chapters (list of chapter files)
   - Count: current_book_chapter_count = number of chapters found
   
   **Fallback to legacy project-level structure if needed:**
   - If current_book_chapter_count equals 0:
     * Use Glob tool: `.claude/data/projects/{project_name}/chapters/*/content.md`
     * Store as: legacy_chapters (list of chapter files)
     * If legacy_chapters count > 0:
       - Display: "⚠️ Warning: Using legacy project structure - consider migration"
       - Set: use_legacy_structure = True
   
   **For series, analyze all books:**
   - If is_series is True:
     * For each book_N directory in book_dirs:
       - Use Glob tool: `.claude/data/projects/{project_name}/book_N/chapters/*/content.md`
       - Check existence: `.claude/data/projects/{project_name}/book_N/bible.yaml`
       - Calculate completion percentage based on chapters found vs expected
       - Store book_status for book_N with:
         * chapters: count of chapter files found
         * bible: whether bible.yaml exists (true/false)
         * completion: calculated percentage (chapters_found / total_expected * 100)

5. **Comprehensive quality analysis across levels:**
   - Current book quality: Last 3 chapters in current_book
   - Series quality: Average scores across all books
   - Identify chapters below 95 threshold needing improvement
   - Track quality trends and patterns

6. **Generate multiple prioritized recommendations:**
   
   **Generate recommendation list based on comprehensive analysis:**
   
   **Initialize recommendations list to build prioritized tasks**
   
   **Check for critical tasks (blocking everything):**
   - If current_book_bible_exists is False:
     * Add to recommendations:
       - priority: "🔴 CRITICAL"
       - scope: "Current Book"
       - task: `/novel:bible-create`
       - reason: "Book [current_book_number] lacks Bible - blocking all creation"
       - impact: "Unblocks chapter generation for current book"
   
   **Check for high priority tasks:**
   - If current_book_bible_exists is True AND no_chapters_in_current_book:
     * Add to recommendations:
       - priority: "🟠 HIGH"
       - scope: "Current Book"
       - task: `/novel:chapter-start 1`
       - reason: "Bible ready, no chapters started"
       - impact: "Begin content generation"
   
   **If no chapters completed:**
   - Priority: "🟠 HIGH"
   - Task: `/novel:chapter-start 1`
   - Reason: "开始第一章创作"
   - Impact: "启动内容生成"
   
   **If current chapter in progress:**
   - Check chapter status:
     * Recommend `/novel:next-chapter`
   
   **If quality issues:**
   - If avg_quality < 95:
     * Add to recommendations:
       - priority: "🟡 MEDIUM"
       - task: `/novel:quality-check [current_chapter]`
       - reason: "质量([avg_quality_value])低于目标(95)"
       - impact: "提升质量"
   
   **If all chapters completed:**
   - If completed >= total:
     * Add to recommendations:
       - priority: "🟢 LOW"
       - task: "/novel:book-complete"
       - reason: "所有章节已完成"
       - impact: "完成作品"
   
   **Default status check:**
   - If no other conditions met:
     * Add to recommendations:
       - priority: "🔵 INFO"
       - task: "/novel:status"
       - reason: "查看详细状态"
       - impact: "了解进度"

7. **Output multi-level recommendations:**

   **Display project overview header:**
   ```
   ╔═══════════════════════════════════════════════════════════╗
   ║         📚 NOVELSYS Intelligent Task Recommendations       ║
   ╚═══════════════════════════════════════════════════════════╝
   
   📊 **Project Overview**
   ─────────────────────
   ```
   
   **Display project details:**
   - Project: [project_name from step 1]
   - Structure: "Series ([num_books] books)" if is_series, else "Single Book"
   - Current Book: [current_book from metadata]
   - Overall Progress: [completed]/[total] chapters ([percentage]%)
   - Average Quality: [avg_quality]/100 (Target: 95+)
   - Total Words: [total_words with comma formatting]
   
   **Display prioritized recommendations:**
   ```
   🎯 **Prioritized Task Recommendations**
   ───────────────────────────────────────
   ```
   
   **For each recommendation in list (show top 5):**
   - Display number (1-5)
   - Display: [priority] [scope] [task]
   - Display: Reason: [reason]
   - Display: Impact: [impact]

8. **Identify parallel opportunities across levels:**

   **Initialize parallel tasks list**
   
   **Add current book parallel tasks:**
   - If current_book_bible_exists AND current_book_chapters > 0:
     * For each chapter in low_quality_chapters:
       - Add task: "/novel:quality-check-individual [chapter_number] - Check specific chapter"
   
   **Add cross-book parallel tasks (for series):**
   - If is_series AND multiple_books_have_content:
     * Add task: "/novel:quality-check-cross - Cross-chapter consistency"
     * Add task: "/novel:smart-fix-cross - Fix cross-book issues"
   
   **Add maintenance tasks (always available):**
   - If has_any_content:
     * Add task: "/novel:context-sync - Update entity dictionary"
     * Add task: "/novel:github-sync all - Backup to GitHub"
     * Add task: "/novel:standup - Generate progress report"
   
   **Display parallel opportunities if any exist:**
   - If parallel tasks list is not empty:
     * Display header:
       ```
       🚀 **Parallel Opportunities** (Can run simultaneously)
       ──────────────────────────────────────────────────
       ```
     * For each task in parallel list (show top 5):
       - Display: * [task]

9. **Display contextual tips based on project state:**

   **Display tips header:**
   ```
   💡 **Smart Tips Based on Your Project**
   ───────────────────────────────────
   ```
   
   **Conditional tips based on project analysis:**
   
   - If is_series:
     * Display: "* Series detected: Use `/novel:next-book` when ready for next book"
   
   - If use_legacy_structure:
     * Display: "* ⚠️ Warning: Legacy structure detected - Consider migrating to book_N structure"
   
   - If avg_quality < 95:
     * Display: "* Quality below target ([avg_quality]<95): Focus on quality improvement"
   
   - If completed > 10 AND not recent_backup:
     * Display: "* No recent backup: Use `/novel:github-sync` to protect your work"
   
   - If is_series AND current_book_complete AND not next_book_started:
     * Display: "* Book [current_book] complete: Ready to start Book [next_book_number] with `/novel:next-book`"

10. **Display filter options:**
   
   ```
   📝 **Filter Options**
   ──────────────────
   * `/novel:next chapter` - Chapter-specific recommendations
   * `/novel:next quality` - Quality improvement focus
   * `/novel:next context` - Context and consistency tasks
   * `/novel:next series` - Series-level recommendations
   * `/novel:next all` - Comprehensive analysis
   ```