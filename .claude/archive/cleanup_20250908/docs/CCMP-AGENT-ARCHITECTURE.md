# CCMP Agent Architecture for NOVELSYS-SWARM

> 基于CCMP三层Agent架构的小说创作系统重构
> 版本: v2.0 Ultimate | 更新: 2025-08-29

## 三层Agent架构体系

### 架构层级图
```
+---------------------------------------------+
|           Director (创作总监)                |
|   战略决策、全局协调、质量把控                |
+--------------+------------------------------+
               |
    +----------+----------+
    |                     |
+---v--------+    +------v--------+
| Book-Epic  |    | Chapter-Epic  |  （史诗级协调者）
| Coordinator|    | Coordinator   |
+---+--------+    +------+--------+
    |                    |
+---+-----------------+  +----------------+
|                     |                   |
v       v       v     v       v     v     v
Bible  World  Character  Scene  Dialogue  Quality  Task
Agent  Agent    Agent    Agent   Agent    Agent    Agent
      (专业执行者)
```

## 第一层：Director (创作总监)

### Director职责定义
**Novel Director specialist:**

**Core responsibilities:**
- Strategic vision: Maintain overall creative vision and quality standards
- Epic coordination: Coordinate Book-Epic and Chapter-Epic coordinators
- Resource allocation: Distribute agent resources and task priorities
- Quality governance: Enforce 95-point quality standards
- Conflict resolution: Resolve cross-Epic conflicts
- Timeline management: Monitor project progress and milestones

**Novel creation orchestration process:**
1. Analyze high-level series requirements and develop creation strategy
2. Decompose strategy into manageable Epic components
3. Launch Epic coordinators for each identified Epic
4. Monitor and coordinate Epic execution:
   - Coordinate between active Epics
   - Resolve any cross-Epic conflicts
   - Validate adherence to quality standards
   - Continue until all Epics are completed
5. Integrate final results from all Epic coordinators

Return Novel Creation Result containing:
- Overall quality score
- Total number of Epics managed
- Total agents utilized across all Epics
- Complete creation timeline

### Director上下文优化
```yaml
director_context_budget: 2000_tokens_max
strategic_focus_areas:
  series_vision: 
    - "核心主题和读者定位"
    - "整体故事弧线"
    - "质量和商业目标"
    token_allocation: 400
    
  epic_coordination:
    - "各Epic的进度状态"
    - "跨Epic依赖关系" 
    - "资源分配决策"
    token_allocation: 500
    
  quality_governance:
    - "当前质量仪表板"
    - "风险和改进机会"
    - "成功指标追踪"
    token_allocation: 300
    
  decision_context:
    - "待决策问题"
    - "影响分析和选项"
    - "历史决策参考"
    token_allocation: 500
    
  coordination_state:
    - "活跃Epic状态"
    - "阻塞问题识别"
    - "下一步行动计划"
    token_allocation: 300
```

## 第二层：Epic Coordinators (史诗级协调者)

### Book-Epic Coordinator
**Book-Epic Coordinator specialist:**

**Scope:** Manage entire book architecture and consistency

**Managed agent responsibilities:**
- bible-architect: Series Bible construction and maintenance
- character-psychologist: Main character deep development
- world-builder: World-building and consistency
- mystery-architect: Mystery logic and clue distribution
- continuity-guardian: Cross-chapter consistency guarantee

**Book creation coordination process:**
1. Launch foundation agents in parallel:
   - bible-architect for series Bible construction
   - world-builder for world framework establishment
   - mystery-architect for mystery structure design
2. Wait for all foundation agents to complete their tasks
3. Launch character-psychologist for deep character development, using foundation results as dependencies
4. Maintain continuous consistency monitoring throughout the process

Return Book Epic Result containing:
- Bible completeness score
- World consistency score
- Character depth score
- Mystery logic score

### Chapter-Epic Coordinator  
**Chapter-Epic Coordinator specialist:**

**Scope:** Manage complete creation process for individual chapters

**Base agent configuration:**
- outline-creator: Chapter structure design
- scene-painter: Scene description creation
- dialogue-specialist: Dialogue creation and optimization
- emotion-weaver: Emotional layer weaving
- pacing-optimizer: Rhythm and tension control
- quality-validator: Chapter quality verification

**Conditional agents (dynamically added based on chapter characteristics):**
- action-choreographer: Specialized for action scenes
- suspense-engineer: Specialized for suspense climax
- food-culture-expert: Specialized for cultural scenes
- weather-mood-setter: Specialized for atmosphere-critical chapters

**Chapter creation coordination process:**
1. **Phase 1 - Structure Design (Single Agent):**
   - Launch outline-creator for chapter structure design

2. **Phase 2 - Base Creation (Parallel):**
   - Launch scene-painter for scene descriptions using structure context
   - Launch dialogue-specialist for dialogue creation using structure context
   - Conditionally add action-choreographer if structure has action scenes
   - Conditionally add food-culture-expert if cultural elements are needed
   - Wait for all base creation tasks to complete

3. **Phase 3 - Emotional and Pacing Optimization (Sequential):**
   - Launch emotion-weaver for emotional weaving using base results
   - Launch pacing-optimizer for rhythm optimization using emotional content

4. **Phase 4 - Quality Validation:**
   - Launch quality-validator with 95-point quality threshold using paced content

Return Chapter Epic Result containing:
- Chapter number
- Total agents utilized
- Final quality score
- Number of creation phases
- Parallel efficiency calculation

## 第三层：Task Agents (专业执行者)

### 专业化Task Agent体系
**Task Agent Registry specialist:**

**Agent catalog organization:**

**Foundation Layer - Infrastructure Agents:**
- bible-architect:
  - Specialization: Series Bible construction
  - Context focus: Series requirements, genre conventions
  - Output type: Structured Bible
  - Parallel safe: No (requires exclusive execution)
  - Resource cost: High

- world-builder:
  - Specialization: World-building
  - Context focus: Setting requirements, cultural background
  - Output type: World documentation
  - Parallel safe: Yes
  - Resource cost: Medium

**Content Creation Layer - Content Creation Agents:**
- scene-painter:
  - Specialization: Scene description and environment depiction
  - Context focus: World building, atmosphere requirements
  - Output type: Scene descriptions
  - Parallel safe: Yes
  - Resource cost: Medium
  - Can collaborate with: weather-mood-setter

- dialogue-specialist:
  - Specialization: Dialogue creation and character voice
  - Context focus: Character profiles, relationship dynamics
  - Output type: Dialogue content
  - Parallel safe: Yes
  - Resource cost: Medium
  - Depends on: character-psychologist

**Enhancement Layer - Optimization Enhancement Agents:**
- emotion-weaver:
  - Specialization: Emotional depth and psychological layers
  - Context focus: Character psychology, emotional arcs
  - Output type: Emotional enhancement
  - Parallel safe: No (requires integration of all content)
  - Resource cost: High
  - Execution phase: Post-creation

- pacing-optimizer:
  - Specialization: Rhythm control and tension adjustment
  - Context focus: Story structure, tension curves
  - Output type: Pacing optimization
  - Parallel safe: No
  - Resource cost: Medium
  - Execution phase: Post-creation

**Quality Assurance Layer - Quality Assurance Agents:**
- quality-validator:
  - Specialization: Multi-dimensional quality assessment
  - Context focus: Quality standards, assessment criteria
  - Output type: Quality report
  - Parallel safe: Yes
  - Resource cost: Low
  - Execution phase: Validation

- consistency-guardian:
  - Specialization: Consistency verification and repair
  - Context focus: Bible standards, continuity rules
  - Output type: Consistency analysis
  - Parallel safe: Yes
  - Resource cost: Medium
  - Execution phase: Validation

**Optimal agent combination selection process:**
1. Initialize required and optional agent lists
2. Analyze task requirements:
   - If needs world building: Add world-builder to required agents
   - If has character interactions: Add character-psychologist and dialogue-specialist to required agents
   - If needs atmosphere: Add weather-mood-setter to optional agents
3. Calculate optimal parallel execution groups for all selected agents

Return Agent Combination containing:
- Required agents list
- Optional agents list
- Parallel execution groups
- Estimated total agent count
- Total resource requirements

### Agent间智能协作协议
**Agent Collaboration Protocol specialist:**

**Collaboration pattern definitions:**

**Parallel Independent Pattern:**
- Description: Completely parallel execution with no dependencies
- Suitable agents: scene-painter, weather-mood-setter, food-culture-expert
- Communication method: Context files only
- Conflict resolution: Director arbitration

**Sequential Dependency Pattern:**
- Description: Clear dependency order execution
- Execution pattern: outline-creator  ->  dialogue-specialist  ->  emotion-weaver
- Communication method: Direct output handoff
- Quality gates: Validation at each step

**Collaborative Review Pattern:**
- Description: Mutual review and optimization
- Agent interaction: scene-painter ↔ dialogue-specialist (bidirectional)
- Communication method: Bidirectional feedback
- Iteration criteria: Continue until consensus reached

**Swarm Integration Pattern:**
- Description: Multi-agent result integration
- Coordinator: chapter-epic-coordinator
- Integration method: Weighted merge
- Quality threshold: 95 points

**Agent collaboration orchestration process:**
1. Retrieve collaboration pattern configuration
2. Execute based on pattern type:

   **For Parallel Independent:**
   - Create independent execution tasks for all agents
   - Execute all tasks in parallel
   - Gather results simultaneously

   **For Sequential Dependency:**
   - Initialize empty results list and context
   - For each agent in sequence:
     - Execute agent with current context
     - Add result to results list
     - Update context with new result

   **For Collaborative Review:**
   - Execute iterative collaboration process between agents

   **For Swarm Integration:**
   - Execute all agents in parallel
   - Apply intelligent integration to combine individual results

Return Collaboration Result containing:
- Pattern used for collaboration
- List of agents involved
- Total execution time
- Quality achieved
- Collaboration efficiency score

## 动态Agent扩展机制

### 智能Agent调度系统
**Dynamic Agent Scheduler specialist:**

**Capacity limits configuration:**
- Maximum concurrent agents: 15
- Maximum agents per Epic: 8
- Resource budget per agent: 4000 tokens

**Scheduling strategies available:**
- Load balancing: Evenly distribute agent workload
- Priority first: Prioritize high-priority tasks
- Resource optimization: Optimize resource utilization
- Deadline driven: Schedule based on deadlines

**Dynamic agent scheduling process:**
1. **System Analysis:**
   - Analyze current system load

2. **Schedule Calculation:**
   - Calculate optimal schedule using:
     - Task queue
     - Current system load
     - Available resources

3. **Initial Agent Launch:**
   - Launch agents for immediate tasks from optimal schedule
   - Add launched agents to active agents list

4. **Dynamic Monitoring and Adjustment:**
   - Continue while active agents exist:
     - Check completion status of all active agents
     - For each completed agent:
       - Release agent resources
       - Remove from active agents list
     - If system can launch more agents:
       - Get next batch of tasks from schedule
       - Launch new agent for each task
       - Add new agents to active agents list

Return Dynamic Scheduling Result containing:
- Total agents utilized
- Peak concurrent agents count
- Resource utilization efficiency
- Total completion time

这个三层Agent架构完美地适配了CCMP的精髓，让NOVELSYS-SWARM能够：

1. **战略级协调**：Director保持高层视角，不被细节污染
2. **Epic级管理**：Book和Chapter协调者处理中层协调
3. **专业化执行**：Task Agent专注具体创作任务
4. **动态扩展**：根据复杂度智能调整Agent数量
5. **智能协作**：多种协作模式应对不同场景

这将是AI小说创作领域的架构革命！🚀

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "\u5b9e\u73b0CCMP\u4e09\u5c42Agent\u67b6\u6784\u4f53\u7cfb", "status": "completed", "activeForm": "\u5b9e\u73b0CCMP\u4e09\u5c42Agent\u67b6\u6784\u4f53\u7cfb"}, {"content": "\u5efa\u7acb\u52a8\u6001Agent\u6269\u5c55\u673a\u5236", "status": "completed", "activeForm": "\u5efa\u7acb\u52a8\u6001Agent\u6269\u5c55\u673a\u5236"}, {"content": "\u521b\u5efaAgent\u95f4\u667a\u80fd\u534f\u4f5c\u7cfb\u7edf", "status": "completed", "activeForm": "\u521b\u5efaAgent\u95f4\u667a\u80fd\u534f\u4f5c\u7cfb\u7edf"}, {"content": "\u8bbe\u8ba1Agent\u751f\u547d\u5chu\u671f\u7ba1\u7406", "status": "pending", "activeForm": "\u8bbe\u8ba1Agent\u751f\u547d\u5chu\u671f\u7ba1\u7406"}, {"content": "\u6784\u5efa\u51b2\u7a81\u89e3\u51b3\u548c\u5408\u5e76\u673a\u5236", "status": "pending", "activeForm": "\u6784\u5efa\u51b2\u7a81\u89e3\u51b3\u548c\u5408\u5e76\u673a\u5236"}]