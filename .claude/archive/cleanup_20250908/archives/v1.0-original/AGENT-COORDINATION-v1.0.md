# Agent协调执行协议

> 蜂群Agent系统的精确协作规范
> 最后更新：2025-08-29

## 一、Agent调用语法

### 基础调用格式
```python
# 串行调用 - 后续Agent需要前一个的完整输出
result = await call_agent("agent-name", {
    "input_data": previous_result,
    "quality_target": 90,
    "bible_reference": "series_bible.yaml"
})

# 并行调用 - 多个Agent可以独立工作
results = await parallel_agents([
    ("scene-painter", outline_data),
    ("dialogue-specialist", outline_data),  
    ("action-choreographer", outline_data)
])

# 迭代调用 - 直到满足质量标准
final_result = await iterative_agent("quality-scorer", {
    "content": generated_content,
    "threshold": 90,
    "max_iterations": 3
})
```

### Agent任务包装格式
```yaml
agent_task:
  agent_name: "scene-painter"
  instruction: "基于提供的章节大纲，创建生动的场景描写"
  input_data:
    chapter_outline: {...}
    series_bible: {...}
    quality_requirements: {...}
  output_requirements:
    format: "markdown"
    length: "2000-3000字"
    quality_target: 90
  context_preservation: 
    - "保持与前面章节的一致性"
    - "遵循既定的叙述风格"
```

## 二、6轮协作流程详解

### 第1轮：结构设计
```python
async def round_1_structure_design(chapter_num):
    """架构设计阶段"""
    
    # 主Agent：outline-creator
    outline = await call_agent("outline-creator", {
        "chapter_number": chapter_num,
        "series_bible": load_bible(),
        "previous_chapters": load_chapters(chapter_num - 1),
        "target_word_count": 7500,
        "quality_target": 90
    })
    
    # 验证结构完整性
    if outline.quality_score < 90:
        raise QualityException("大纲质量不达标")
    
    return outline
```

### 第2轮：基础生成（并行）
```python  
async def round_2_base_generation(outline):
    """基础内容并行生成"""
    
    agents = [
        ("scene-painter", "创建场景描写"),
        ("dialogue-specialist", "编写对话内容"),
        ("action-choreographer", "编排动作场景")
    ]
    
    # 并行执行，提高效率
    base_results = await asyncio.gather(*[
        call_agent(agent, {
            "outline": outline,
            "focus": description,
            "quality_target": 85
        }) for agent, description in agents
    ])
    
    return integrate_base_content(base_results)
```

### 第3轮：情感深化（并行）
```python
async def round_3_emotional_enhancement(base_content):
    """情感和氛围增强"""
    
    enhancement_agents = [
        ("emotion-weaver", "编织情感层次"),
        ("weather-mood-setter", "营造氛围"),
        ("suspense-engineer", "构建悬念")
    ]
    
    enhanced_results = await parallel_execution(
        enhancement_agents, 
        base_content,
        quality_target=88
    )
    
    return merge_enhancements(enhanced_results)
```

### 第4轮：细节丰富（并行）
```python
async def round_4_detail_enrichment(enhanced_content):
    """专业细节添加"""
    
    detail_agents = [
        ("food-culture-expert", "添加美食文化细节"),
        ("clue-planter", "植入推理线索")
    ]
    
    detailed_content = await parallel_execution(
        detail_agents,
        enhanced_content,
        quality_target=90
    )
    
    return detailed_content
```

### 第5轮：优化调整（串行）
```python
async def round_5_optimization(detailed_content):
    """串行优化，每步基于前一步结果"""
    
    # 节奏优化
    paced_content = await call_agent("pacing-optimizer", {
        "content": detailed_content,
        "target_rhythm": "cozy_mystery_pace",
        "quality_target": 92
    })
    
    # 声音调优
    tuned_content = await call_agent("voice-tuner", {
        "content": paced_content,
        "voice_profile": load_voice_profile(),
        "quality_target": 92
    })
    
    return tuned_content
```

### 第6轮：质量检验（并行）
```python
async def round_6_quality_assurance(optimized_content):
    """多维度质量检验"""
    
    qa_agents = [
        ("consistency-guardian", "一致性验证"),
        ("plot-hole-detector", "逻辑漏洞检测"),
        ("quality-scorer", "综合评分")
    ]
    
    quality_reports = await parallel_execution(
        qa_agents,
        optimized_content,
        strict_mode=True
    )
    
    final_score = quality_reports["quality-scorer"]["overall_score"]
    
    if final_score >= 90:
        return {
            "status": "APPROVED",
            "content": optimized_content,
            "score": final_score,
            "reports": quality_reports
        }
    else:
        # 返回具体问题，准备重新生成
        return {
            "status": "NEEDS_REVISION", 
            "issues": extract_issues(quality_reports),
            "recommendations": generate_fixes(quality_reports)
        }
```

## 三、Agent间通信协议

### 数据传递格式
```yaml
inter_agent_data:
  metadata:
    source_agent: "outline-creator"
    target_agent: "scene-painter"
    timestamp: "2025-08-29T10:30:00Z"
    quality_score: 90
    
  content:
    primary_data: {...}  # 主要内容
    context_data: {...}  # 上下文信息
    constraints: {...}   # 约束条件
    
  quality_metrics:
    current_score: 90
    dimension_scores: {...}
    improvement_areas: [...]
```

### 错误处理机制
```python
class AgentCoordinationError(Exception):
    """Agent协调异常处理"""
    
    def __init__(self, agent_name, error_type, details):
        self.agent_name = agent_name
        self.error_type = error_type
        self.details = details
        
async def handle_agent_failure(agent_name, error):
    """Agent失败处理流程"""
    
    if error.type == "QUALITY_BELOW_THRESHOLD":
        # 质量不达标，重试
        return await retry_with_feedback(agent_name, error.feedback)
        
    elif error.type == "TIMEOUT":
        # 超时，使用备用策略
        return await fallback_generation(agent_name)
        
    elif error.type == "RESOURCE_LIMIT":
        # 资源限制，调整参数
        return await adjusted_generation(agent_name, reduced_complexity=True)
```

## 四、质量保证机制

### 三级质量验证
```python
class QualityAssuranceFramework:
    """三级质量保证体系"""
    
    async def level_1_basic_check(self, content):
        """L1: 基础合规性检查"""
        checks = [
            ("bible_compliance", self.check_bible_compliance),
            ("format_validation", self.validate_format),
            ("length_check", self.check_length)
        ]
        
        for name, check_func in checks:
            if not await check_func(content):
                raise QualityException(f"L1检查失败: {name}")
    
    async def level_2_logic_verification(self, content):
        """L2: 逻辑一致性验证"""
        return await call_agent("plot-hole-detector", {
            "content": content,
            "strict_mode": True,
            "threshold": 95
        })
    
    async def level_3_comprehensive_scoring(self, content):
        """L3: 综合质量评分"""
        return await call_agent("quality-scorer", {
            "content": content,
            "target_score": 90,
            "detailed_analysis": True
        })
```

### 质量门控系统
```python
async def quality_gate_check(content, stage):
    """质量门控检查"""
    
    gates = {
        "outline": {"min_score": 85, "critical_dims": ["structure"]},
        "draft": {"min_score": 87, "critical_dims": ["character", "plot"]},  
        "refined": {"min_score": 90, "critical_dims": ["all"]},
        "final": {"min_score": 92, "critical_dims": ["all"]}
    }
    
    gate_config = gates[stage]
    score = await comprehensive_quality_check(content)
    
    if score.overall < gate_config["min_score"]:
        return QualityGateResult(
            passed=False,
            required_fixes=score.get_critical_issues(),
            recommendations=score.get_improvements()
        )
    
    return QualityGateResult(passed=True, score=score.overall)
```

## 五、成本控制策略

### 模型选择策略
```python
MODEL_SELECTION_RULES = {
    # 结构设计 - 需要强推理能力
    "outline-creator": "claude-3-5-sonnet",
    "mystery-architect": "claude-3-5-sonnet",
    
    # 内容生成 - 平衡质量和成本
    "scene-painter": "claude-3-5-haiku", 
    "dialogue-specialist": "claude-3-5-haiku",
    
    # 质量检查 - 需要最高精度
    "consistency-guardian": "claude-3-5-sonnet",
    "quality-scorer": "claude-3-5-sonnet",
    
    # 细节优化 - 可用快速模型
    "weather-mood-setter": "claude-3-5-haiku",
    "food-culture-expert": "claude-3-5-haiku"
}
```

### 成本监控
```python
class CostMonitor:
    """成本监控和预算控制"""
    
    def __init__(self, budget_limit=50.0):
        self.budget_limit = budget_limit
        self.current_cost = 0.0
        self.cost_breakdown = {}
    
    async def estimate_agent_cost(self, agent_name, input_size):
        """预估Agent调用成本"""
        base_costs = {
            "claude-3-5-sonnet": 0.015,  # per 1k tokens
            "claude-3-5-haiku": 0.0025   # per 1k tokens  
        }
        
        model = MODEL_SELECTION_RULES[agent_name]
        estimated_tokens = input_size * 1.5  # 考虑输出
        
        return base_costs[model] * (estimated_tokens / 1000)
    
    def check_budget_remaining(self, required_cost):
        """检查预算是否充足"""
        return (self.current_cost + required_cost) <= self.budget_limit
```

## 六、监控和调试

### 实时监控指标
```yaml
monitoring_metrics:
  performance:
    - agent_response_time
    - parallel_execution_efficiency  
    - queue_wait_time
    - memory_usage
    
  quality:
    - average_quality_score
    - first_pass_success_rate
    - iteration_count_average
    - consistency_score
    
  cost:
    - tokens_per_chapter
    - cost_per_quality_point
    - budget_utilization
    - model_usage_distribution
```

### 调试工具
```python
class SwarmDebugger:
    """蜂群系统调试工具"""
    
    def trace_agent_flow(self, chapter_generation_id):
        """追踪Agent调用流程"""
        return {
            "execution_path": self.get_execution_trace(chapter_generation_id),
            "agent_outputs": self.get_all_outputs(chapter_generation_id),
            "quality_progression": self.track_quality_changes(chapter_generation_id),
            "bottlenecks": self.identify_bottlenecks(chapter_generation_id)
        }
    
    def analyze_quality_failures(self):
        """分析质量失败模式"""
        failures = self.get_failed_generations()
        return {
            "common_failure_types": self.categorize_failures(failures),
            "problematic_agents": self.identify_problem_agents(failures),
            "improvement_suggestions": self.generate_suggestions(failures)
        }
```

## 七、故障恢复机制

### 自动恢复策略
```python
async def recovery_strategies():
    """故障自动恢复机制"""
    
    strategies = {
        "agent_timeout": retry_with_shorter_context,
        "quality_failure": iterative_improvement_cycle,
        "resource_exhaustion": graceful_degradation,
        "consistency_violation": bible_reconciliation
    }
    
    return strategies

async def graceful_degradation(failed_agent, context):
    """优雅降级处理"""
    
    # 使用更简单的Agent替代
    fallback_agents = {
        "emotion-weaver": "basic-emotion-enhancer",
        "suspense-engineer": "simple-tension-builder"
    }
    
    if failed_agent in fallback_agents:
        return await call_agent(
            fallback_agents[failed_agent], 
            simplified_context(context)
        )
```

## 八、性能优化建议

### 并行化最佳实践
1. **最大并行度**: 同时运行最多5个Agent
2. **资源分配**: 为每个Agent预留足够内存
3. **负载均衡**: 避免所有Agent同时请求相同模型
4. **缓存策略**: 缓存Bible和角色设定等静态数据

### 质量效率平衡
1. **快速失败**: 早期检测质量问题
2. **智能重试**: 基于具体问题调整重试策略  
3. **渐进优化**: 先满足基本要求，再追求完美
4. **预测性调度**: 根据历史数据预估Agent需求

---

*通过精确的协调机制，18个Agent将如蜂群般高效协作，确保每一章都达到90分以上的卓越品质！* 🐝ALERT: