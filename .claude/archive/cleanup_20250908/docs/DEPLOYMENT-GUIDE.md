# NOVELSYS-SWARM 部署指南

> 蜂群AI小说生成系统的完整部署和操作手册
> 版本：v2.0 Enhanced | 更新：2025-08-29

## 快速开始

### 系统要求
```yaml
环境要求:
  操作系统: "Windows 11, macOS 12+, Linux"
  Python版本: "3.9+"
  Claude Code: "最新版本"
  内存: "16GB+ 推荐"
  存储: "10GB+ 可用空间"
  网络: "稳定互联网连接"
```

### 5分钟快速部署
```bash
# 1. 克隆项目
git clone https://github.com/your-org/novelsys-swarm
cd novelsys-swarm

# 2. 初始化环境
python setup.py init

# 3. 验证Agent系统
python -m swarm.test_agents

# 4. 创建第一个系列Bible
python -m swarm.create_bible "温泉推理系列"

# 5. 生成第一章
python -m swarm.generate_chapter 1
```

## 详细部署流程

### 第一步：环境准备

#### Claude Code配置
```bash
# 确认Claude Code可用
claude --version

# 设置项目为Claude Code工作目录
cd {project_root}
claude code init
```

#### Agent注册验证
```bash
# 检查所有Agent是否可用
ls .claude/agents/*/*.md | wc -l  # 应该显示18

# 验证核心Agent
python scripts/validate_agents.py
```

### 第二步：系统初始化

#### 目录结构验证
```
NOVELSYS-SWARM/
+-- .claude/
|   +-- agents/           # 18个专门Agent
|   +-- prompts/         # 系统提示词
|   +-- config.yaml      # 系统配置
+-- .claude/data/
|   +-- bibles/          # 系列Bible存储
|   +-- chapters/        # 生成的章节
|   +-- quality_reports/ # 质量报告
+-- scripts/             # 自动化脚本
+-- tests/              # 测试用例
+-- output/             # 最终输出
```

#### 配置文件设置
```yaml
# config/swarm.yaml
swarm_config:
  max_parallel_agents: 5
  quality_threshold: 90
  max_iterations: 3
  cost_budget_per_chapter: 2.0
  
  models:
    primary: "claude-3-5-sonnet"
    secondary: "claude-3-5-haiku"
    fallback: "claude-3-haiku"
    
  storage:
    bible_format: "yaml"
    chapter_format: "markdown"
    backup_enabled: true
```

### 第三步：Agent系统启动

#### 健康检查脚本
**System Health Checker specialist:**

**Initialize agent coordination system:**
1. Create an AgentCoordinator instance
2. Establish async execution context

**Perform comprehensive agent availability check:**
1. Query the coordinator for all registered agents
2. Count and display the total number of discovered agents
3. Report the agent discovery results

**Execute core agent functionality tests:**
1. Define critical agents list: ["bible-architect", "outline-creator", "quality-scorer"]
2. For each core agent:
   - Execute health status test via coordinator
   - Display agent name with success ([x]) or failure ([ ]) indicator

**Execute health check process:**
- Run the complete health check routine asynchronously
- Return system health status summary

#### Agent预热
**Agent Warmup Process specialist:**

**Execute comprehensive agent warmup:**
1. Run warmup script for all registered agents
2. Load necessary models and initialize agent states
3. Measure and report warmup timing for each agent

**Expected system warmup results:**
- bible-architect: Warmup completed (2.3s)
- character-psychologist: Warmup completed (1.8s)
- outline-creator: Warmup completed (2.1s)
- Continue for all remaining agents
- Swarm system warmup complete! Total 18 agents ready

## 使用指南

### 创建新系列Bible

#### 方法1：交互式创建
**BibleBuilder Interactive Creation specialist:**

**Initialize Bible construction system:**
1. Import and instantiate BibleBuilder from swarm module
2. Create new builder instance for interactive creation

**Execute guided Bible creation process:**
1. Launch interactive creation workflow asynchronously
2. Complete the guided construction phases:
   - Series basic settings configuration (10-15 minutes)
   - Main character development (15-20 minutes)
   - World-building and setting establishment (10-15 minutes)
   - Mystery/reasoning mechanism design (15-20 minutes)
   - Final quality validation and review (5 minutes)

**Return completed Bible structure:**
- Return fully validated Bible object ready for chapter generation

#### 方法2：从模板创建
**Template-based Bible Creation specialist:**

**Define available template options:**
- Available templates: ["cozy_mystery", "urban_fantasy", "historical_fiction"]

**Execute template-based Bible generation:**
1. Select "cozy_mystery" template as base
2. Apply custom parameters:
   - Setting: "日本温泉小镇" (Japanese hot spring town)
   - Protagonist: "30岁女性侦探" (30-year-old female detective)
   - Mystery type: "密室推理" (locked room mystery)
3. Generate Bible asynchronously using template and parameters

**Return customized Bible:**
- Return Bible object based on template with applied customizations

#### Bible质量验证
```yaml
bible_validation:
  completeness_check: 100%     # 所有必填字段完整
  consistency_score: 95%+      # 内部逻辑一致性
  character_depth: 90%+        # 角色立体程度
  world_coherence: 95%+        # 世界观连贯性
  mystery_fairness: 100%       # 推理公平性
```

### 生成章节流程

#### 标准生成流程
**ChapterGenerator Standard Process specialist:**

**Initialize chapter generation system:**
1. Import ChapterGenerator from swarm module
2. Create new generator instance

**Execute chapter 1 generation workflow:**
1. Load series Bible data for "温泉推理系列" (Hot Spring Mystery Series)
2. Configure swarm generation parameters:
   - Chapter number: 1
   - Bible reference: loaded Bible object
   - Target quality score: 90
3. Execute 6-round swarm collaborative generation process

**Process and report generation results:**
1. Display completion message with quality score
2. Report total iteration count used
3. Report total generation duration
4. Return complete result object with all metrics

**Return generation outcome:**
- Return comprehensive result object containing chapter content and metadata

#### 自定义生成参数
**Custom Parameter Generation specialist:**

**Define custom generation parameters:**
- Target word count: 8000 words
- Quality threshold requirement: 92 points
- Maximum iteration limit: 2 rounds
- Focus optimization areas: ["dialogue", "mystery"]
- Agents to skip: ["food-culture-expert"]

**Execute customized generation process:**
1. Apply custom parameter configuration to chapter 1 generation
2. Use generator with specified custom parameters
3. Process generation asynchronously with parameter constraints

**Return customized generation result:**
- Return result object matching custom parameter specifications

### 质量监控

#### 实时质量跟踪
**Quality Monitoring Dashboard specialist:**

**Launch monitoring dashboard:**
1. Execute swarm monitoring module
2. Initialize real-time tracking interface

**Monitor key system metrics:**
- Real-time quality scoring and evaluation
- Agent execution status and health monitoring
- Cost tracking and budget utilization statistics
- Error detection and reporting system

**Provide continuous system oversight:**
- Maintain active monitoring of all tracked metrics
- Alert on threshold violations or system issues

#### 质量报告解读
```yaml
质量报告示例:
  overall_score: 92           # 总分
  
  dimension_scores:
    character_depth: 94       # 人物深度
    plot_coherence: 91        # 情节连贯性
    writing_quality: 93       # 文笔质量
    emotional_impact: 89      # 情感冲击力
    consistency: 96           # 一致性
    atmosphere: 90            # 氛围营造
    
  agent_contributions:
    scene_painter: 8.5        # 各Agent贡献度
    dialogue_specialist: 9.2
    emotion_weaver: 8.8
    ...
    
  improvement_suggestions:
    - "加强第3场景的情感描述"
    - "优化主角与配角的对话节奏"
```

## 故障排除

### 常见问题及解决方案

#### Agent调用失败
```yaml
问题: "Agent timeout or connection error"
原因: 
  - 网络连接不稳定
  - Claude API限制
  - Agent负载过高
  
解决方案:
  1. 检查网络连接
  2. 降低并行Agent数量
  3. 使用重试机制
  4. 切换到备用模型
```

#### 质量分数过低
```yaml
问题: "Generated content below quality threshold"
原因:
  - Bible信息不完整
  - Agent参数配置不当
  - 复杂度超出Agent能力
  
解决方案:
  1. 完善系列Bible
  2. 调整质量阈值
  3. 增加迭代次数
  4. 使用更强大的模型
```

#### 内存或性能问题
```yaml
问题: "System running slow or out of memory"
原因:
  - 并行Agent过多
  - 上下文窗口过大
  - 缓存数据过多
  
解决方案:
  1. 减少max_parallel_agents
  2. 清理临时文件
  3. 重启系统
  4. 升级硬件配置
```

### 调试工具

#### Agent执行日志
```bash
# 查看详细执行日志
tail -f logs/swarm_execution.log

# 按Agent筛选日志
grep "scene-painter" logs/swarm_execution.log

# 查看错误日志  
grep "ERROR" logs/swarm_execution.log
```

#### 性能分析
**PerformanceAnalyzer Debug Tool specialist:**

**Initialize performance analysis system:**
1. Import PerformanceAnalyzer from swarm.debug module
2. Create analyzer instance for system diagnostics

**Execute comprehensive performance analysis:**
1. Analyze the most recent generation session
2. Generate detailed performance report

**Display critical performance metrics:**
1. Report total execution time for the session
2. Identify and report the slowest performing agent
3. Highlight system bottlenecks and performance constraints

**Return performance insights:**
- Provide actionable performance optimization recommendations

## 高级配置

### 自定义Agent

#### 创建新Agent
```markdown
# .claude/agents/custom/my-agent.md
---
name: my-agent
description: 自定义功能描述
tools:
  - Read
  - Write
---

You are a specialized agent that...

## 具体提示词内容
...
```

#### 注册新Agent
**Custom Agent Registration specialist:**

**Configure swarm agent registry:**
1. Access swarm configuration system
2. Define custom agent specifications:
   - Agent name: "my-agent"
   - Functional category: "optimization"
   - Priority level: 2
3. Register agent in custom_agents section

**Integrate new agent into swarm:**
- Add agent to active swarm configuration for future operations

### 模型选择策略

#### 动态模型分配
**Dynamic Model Allocation Strategy specialist:**

**Define agent category routing rules:**
- High reasoning tasks: ["bible-architect", "mystery-architect"]
- Creative writing tasks: ["scene-painter", "dialogue-specialist"]
- Analysis tasks: ["consistency-guardian", "plot-hole-detector"]
- Optimization tasks: ["pacing-optimizer", "voice-tuner"]

**Configure model assignments by category:**
- High reasoning category: claude-3-5-sonnet model
- Creative writing category: claude-3-5-haiku model
- Analysis category: claude-3-5-sonnet model
- Optimization category: claude-3-5-haiku model

**Implement dynamic model routing:**
- Route agents to appropriate models based on task category
- Optimize performance and cost through strategic model selection

### 成本优化

#### 预算控制
**Budget Control Configuration specialist:**

**Define comprehensive budget parameters:**
- Daily spending limit: $100.00 USD maximum
- Per-chapter generation limit: $5.00 USD maximum
- Warning threshold trigger: 80% of budget utilization
- Automatic model downgrade: Enabled when approaching limits

**Implement budget enforcement:**
1. Monitor spending against daily and chapter limits
2. Trigger warnings at 80% threshold utilization
3. Automatically downgrade to lower-cost models when necessary
4. Prevent generation if budget limits are exceeded

**Ensure cost-effective operation:**
- Maintain quality standards while respecting budget constraints

## 维护和更新

### 定期维护任务

#### 每日维护
```bash
# 清理临时文件
python scripts/cleanup_temp.py

# 备份重要数据  
python scripts/backup_bibles.py

# 检查系统健康状态
python scripts/daily_health_check.py
```

#### 每周维护
```bash
# 更新Agent提示词
git pull origin main

# 重新测试所有Agent
python scripts/test_all_agents.py

# 生成系统报告
python scripts/weekly_report.py
```

### 系统升级

#### Agent更新流程
```bash
# 1. 备份当前配置
cp -r .claude/agents .claude/agents.backup

# 2. 拉取最新Agent
git pull origin main

# 3. 验证Agent兼容性
python scripts/validate_upgrade.py

# 4. 重启系统
python -m swarm.restart
```

## 生产环境部署

### 服务器部署配置
```yaml
# docker-compose.yml
version: '3.8'
services:
  novelsys-swarm:
    build: .
    environment:
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - MAX_PARALLEL_AGENTS=3
      - QUALITY_THRESHOLD=90
    volumes:
      - ./data:/app/data
      - ./output:/app/output
    ports:
      - "8080:8080"
```

### 监控和告警
**Monitoring and Alert System specialist:**

**Define quality monitoring alert rules:**
- Alert condition: Quality score below 85 points
- Response action: Send email notification to administrator
- Severity level: Warning status

**Define budget monitoring alert rules:**
- Alert condition: Daily cost exceeds budget limit
- Response action: Pause generation operations immediately
- Severity level: Critical status

**Implement automated alert system:**
1. Continuously monitor quality scores and budget utilization
2. Trigger appropriate alerts when conditions are met
3. Execute defined response actions automatically
4. Maintain alert history and escalation procedures

**Ensure system reliability:**
- Provide proactive monitoring and rapid response to system issues

---

*遵循此部署指南，您将拥有一个完全可操作的蜂群AI小说生成系统，能够稳定产出90分以上的高质量作品！* 🐝🚀