# Agent 详细说明

> NOVELSYS-SWARM 29个Agent完整文档  
> Version: 2.5.0 | Updated: 2025-01-30

## 📋 Agent分类

### 系统架构
- **8个核心Stream Agent** - 始终运行
- **2个协调Agent** - 管理和协调
- **10个生成Agent** - 内容创作
- **9个特化Agent** - 动态分配

## 🌊 核心Stream Agent (8个)

### 1. character-psychology-stream
**角色心理深度分析器**
- **职责**: 深度挖掘角色心理，确保人物立体
- **质量目标**: 95分
- **关注点**:
  - 心理动机合理性
  - 情感变化逻辑
  - 内心冲突深度
  - 性格一致性

### 2. narrative-structure-stream
**叙事结构管理器**
- **职责**: 管理故事节奏和结构
- **质量目标**: 92分
- **关注点**:
  - 三幕式结构
  - 冲突升级曲线
  - 悬念设置
  - 高潮安排

### 3. world-building-stream
**世界构建感官增强器**
- **职责**: 构建沉浸式世界观
- **质量目标**: 93分
- **关注点**:
  - 五感描写
  - 环境氛围
  - 文化背景
  - 物理规则

### 4. prose-craft-stream
**文笔工艺优化器**
- **职责**: 提升文字表达质量
- **质量目标**: 91分
- **关注点**:
  - 词汇选择
  - 句式变化
  - 修辞运用
  - 节奏控制

### 5. continuity-guard-stream
**连贯性守护者**
- **职责**: 确保前后一致性
- **质量目标**: 99分
- **关注点**:
  - 时间线准确
  - 设定一致
  - 逻辑连贯
  - 细节对应

### 6. foreshadowing-stream
**伏笔生命周期管理器**
- **职责**: 管理伏笔设置和回收
- **质量目标**: 100分
- **关注点**:
  - 伏笔设置自然
  - 回收时机恰当
  - 呼应完整
  - 惊喜但合理

### 7. dialogue-master-stream
**对话艺术大师**
- **职责**: 优化角色对话
- **质量目标**: 94分
- **关注点**:
  - 个性化语言
  - 潜台词
  - 信息密度
  - 自然流畅

### 8. emotion-weaver-stream
**情感编织器**
- **职责**: 编织情感线索
- **质量目标**: 90分
- **关注点**:
  - 情感递进
  - 共鸣点设置
  - 张力营造
  - 情绪转换

## 🎯 协调Agent (2个)

### 9. parallel-coordinator
**并行执行协调器**
- **职责**: 协调8-Stream并行执行
- **功能**:
  - 任务分配
  - 进度同步
  - 结果汇总
  - 冲突解决
- **配置**:
  **Parallel coordinator configuration:**
  1. Set maximum parallel streams to 8
  2. Configure timeout to 300 seconds
  3. Set retry count to 3 attempts

### 10. quality-controller
**质量控制器**
- **职责**: 监控和保证输出质量
- **功能**:
  - 8维度评分
  - 迭代决策
  - 质量报告
  - 改进建议
- **评分标准**:
  - <85分: 需要重写
  - 85-92分: 需要优化
  - 92-98分: 可以接受
  - >98分: 优秀

## ✍️ 生成Agent (10个)

### 11. scene-generator
**场景生成器**
- **职责**: 生成具体场景
- **输出**: 1000-2000字场景
- **特点**: 注重画面感和细节

### 12. dialogue-generator
**对话生成器**
- **职责**: 生成角色对话
- **输出**: 自然的对话交流
- **特点**: 个性化、有潜台词

### 13. description-generator
**描写生成器**
- **职责**: 生成环境和人物描写
- **输出**: 生动的描写段落
- **特点**: 感官丰富、画面感强

### 14. action-generator
**动作生成器**
- **职责**: 生成动作场景
- **输出**: 紧张刺激的动作序列
- **特点**: 节奏快、动感强

### 15. emotion-generator
**情感生成器**
- **职责**: 生成情感场景
- **输出**: 细腻的情感描写
- **特点**: 深入内心、引发共鸣

### 16. transition-generator
**过渡生成器**
- **职责**: 生成章节过渡
- **输出**: 流畅的过渡段落
- **特点**: 承上启下、自然流畅

### 17. opening-generator
**开篇生成器**
- **职责**: 生成章节开头
- **输出**: 吸引人的开篇
- **特点**: 钩子强、节奏好

### 18. climax-generator
**高潮生成器**
- **职责**: 生成高潮场景
- **输出**: 激动人心的高潮
- **特点**: 张力足、冲击强

### 19. ending-generator
**结尾生成器**
- **职责**: 生成章节结尾
- **输出**: 回味无穷的结尾
- **特点**: 悬念或满足感

### 20. flashback-generator
**回忆生成器**
- **职责**: 生成回忆场景
- **输出**: 过去时态的回忆
- **特点**: 时间转换自然

## 🎭 特化Agent (9个)

### 21. action-choreographer
**动作编排师**
- **激活条件**: 动作场景
- **专长**: 打斗、追逐、爆炸
- **提升**: 动作流畅度+30%

### 22. pacing-specialist
**节奏专家**
- **激活条件**: 需要节奏控制
- **专长**: 快慢切换、张弛有度
- **提升**: 阅读体验+25%

### 23. tension-maximizer
**张力最大化器**
- **激活条件**: 冲突场景
- **专长**: 制造紧张感
- **提升**: 紧张度+40%

### 24. subtext-weaver
**潜台词编织者**
- **激活条件**: 对话场景
- **专长**: 言外之意
- **提升**: 对话深度+35%

### 25. sensory-detail
**感官细节师**
- **激活条件**: 描写场景
- **专长**: 五感描写
- **提升**: 沉浸感+30%

### 26. atmosphere-builder
**氛围营造师**
- **激活条件**: 环境描写
- **专长**: 气氛渲染
- **提升**: 氛围感+35%

### 27. mystery-keeper
**悬念保持者**
- **激活条件**: 悬疑情节
- **专长**: 信息控制
- **提升**: 悬念感+40%

### 28. romance-specialist
**浪漫专家**
- **激活条件**: 感情场景
- **专长**: 情感细腻
- **提升**: 浪漫度+35%

### 29. humor-injector
**幽默注入器**
- **激活条件**: 轻松场景
- **专长**: 幽默对话
- **提升**: 趣味性+30%

## 📊 动态分配策略

### 章节类型映射

| 章节类型 | 基础Agent | 特化Agent | 总数 |
|---------|-----------|-----------|------|
| action | 8 Stream + 2协调 | 3 (21,22,23) | 13 |
| dialogue | 8 Stream + 2协调 | 2 (24,25) | 12 |
| description | 8 Stream + 2协调 | 2 (25,26) | 12 |
| emotional | 8 Stream + 2协调 | 2 (28,24) | 12 |
| mystery | 8 Stream + 2协调 | 2 (27,23) | 12 |
| romance | 8 Stream + 2协调 | 2 (28,24) | 12 |
| humor | 8 Stream + 2协调 | 1 (29) | 11 |
| transition | 8 Stream + 2协调 | 1 (22) | 11 |
| climax | 8 Stream + 2协调 | 3 (21,22,23) | 13 |
| mixed | 8 Stream + 2协调 | 2-4 (动态) | 12-14 |

## 🔧 Agent配置

### 全局配置
```yaml
agents:
  max_concurrent: 15
  timeout: 300
  retry_on_failure: true
  
stream_agents:
  always_active: true
  parallel_execution: true
  
specialized_agents:
  dynamic_allocation: true
  max_per_chapter: 5
```

### 权重配置
**Agent weight configuration specialist:**
- Character psychology stream: Weight 1.2
- Continuity guard stream: Weight 1.5  
- Foreshadowing stream: Weight 2.0 (highest priority)
- Prose craft stream: Weight 0.9
- Emotion weaver stream: Weight 1.1

## 📈 性能指标

| Agent类型 | 平均耗时 | Token使用 | 成功率 |
|----------|---------|-----------|--------|
| Stream Agent | 30s | 2K | 98% |
| 协调Agent | 5s | 500 | 99.5% |
| 生成Agent | 45s | 3K | 95% |
| 特化Agent | 20s | 1.5K | 97% |

## 🔍 调试和监控

### 查看Agent状态
```bash
/novel:agent-status
```

### 查看Agent日志
```bash
/novel:agent-logs [agent-id]
```

### 调整Agent权重
```bash
/novel:agent-weight [agent-id] [weight]
```

### 禁用特定Agent
```bash
/novel:agent-disable [agent-id]
```

## ⚠️ 注意事项

1. **Stream Agent不可禁用** - 它们是核心架构的一部分
2. **特化Agent按需分配** - 不要手动强制启用所有Agent
3. **权重调整谨慎** - 过高的权重可能导致偏向性
4. **监控Token使用** - 某些Agent可能消耗较多Token

---

*详细实现请查看 `.claude/agents/` 目录*  
*最后更新: 2025-01-30*