# System Check v4.0 完整文件改动清单

## 📊 改动统计
- **新建**: 4个文件
- **修改**: 16个文件  
- **归档**: 0个文件（保留向后兼容）
- **删除**: 0个文件

---

## 🆕 新建文件（4个）

### 1. system-knowledge-builder.md
```yaml
路径: .claude/agents/system-knowledge-builder.md
类型: 核心组件
功能: 一次扫描构建完整知识图谱
优先级: P0（必须第一个创建）

主要内容:
---
name: system-knowledge-builder
description: Builds comprehensive system knowledge graph in single scan
thinking: true
---

职责:
1. 扫描所有系统文件（commands, agents, data）
2. 提取组件信息和关系
3. 识别已实现的功能（锁、缓存等）
4. 构建knowledge_graph.json
5. 输出到.claude/report/{timestamp}/

输出格式:
{
  "components": {...},
  "relationships": {...},
  "implementations": {...},
  "potential_issues": {...}
}
```

### 2. implementation-verifier.md
```yaml
路径: .claude/agents/implementation-verifier.md
类型: 验证层
功能: 主动验证所有报告的风险
优先级: P0（第二个创建）

主要内容:
---
name: implementation-verifier
description: Verifies reported risks against actual implementations
thinking: true
---

职责:
1. 读取所有Phase 1-3的风险报告
2. 对每个风险进行深度验证
3. 检查是否有缓解措施
4. 更新风险状态（MITIGATED/CONFIRMED）
5. 输出验证报告
```

### 3. smart-health-reporter.md
```yaml
路径: .claude/agents/smart-health-reporter.md
类型: 智能聚合器
功能: 替代system-health-reporter
优先级: P1

主要内容:
---
name: smart-health-reporter
description: Intelligent health report aggregator with deduplication
thinking: true
---

新增功能:
1. 智能去重（相同问题只报一次）
2. 验证优先（已解决的不报为风险）
3. 置信度加权
4. 历史对比
5. 分类输出（真实问题 vs 理论风险）
```

### 4. knowledge-graph-cache.md
```yaml
路径: .claude/agents/knowledge-graph-cache.md
类型: 性能优化
功能: 缓存知识图谱避免重复扫描
优先级: P2（可选）

主要内容:
管理知识图谱缓存:
1. 检查系统文件是否变化
2. 如果没变化，使用缓存
3. 如果变化，触发重新扫描
4. 类似bible-cache-manager的机制
```

---

## ✏️ 修改文件（16个）

### 核心改动（3个）- 必须修改

#### 1. system-check-coordinator.md
```yaml
改动类型: 重大修改
改动内容:
1. 添加Phase 0: 知识图谱构建
2. 修改Phase 1-4: 传递knowledge_graph.json给所有agents
3. 添加Phase 3.5: 实现验证
4. 替换Phase 5的reporter为smart-health-reporter
5. 修改所有"Critical Analysis Guidelines"为"Balanced Analysis"

具体改动:
### Step 1.5: Build Knowledge Graph (NEW)
Display: "🔍 Phase 0: Building system knowledge graph..."
Execute Task:
  subagent_type: "system-knowledge-builder"
  prompt: "Scan entire system and build knowledge graph.
          Save to .claude/report/{TIMESTAMP}/knowledge_graph.json"

### Step 2: Execute Phase 1 (MODIFIED)
每个agent的prompt添加:
  "Use the knowledge graph at .claude/report/{TIMESTAMP}/knowledge_graph.json
   instead of scanning source files directly."
```

#### 2. parallel-safety-validator.md
```yaml
改动类型: 重要添加
改动内容:
1. 添加Step 1.5: 读取knowledge_graph.json
2. 添加Step 3.5: 验证缓解措施
3. 修改风险评估逻辑

具体改动:
### Step 1.5: Load Knowledge Graph (NEW)
- Read: .claude/report/{TIMESTAMP}/knowledge_graph.json
- Extract implementations.file_locking
- Extract implementations.caching
- Use for validation

### Step 3.5: Verify Mitigations (NEW)
For each identified risk:
  if risk.type == "file_conflict":
    check knowledge_graph.implementations
    if has_lock_protection:
      risk.status = "MITIGATED"
      risk.evidence = implementation_location
```

#### 3. dependency-mapper.md
```yaml
改动类型: 重构
改动内容:
从扫描源文件改为分析知识图谱

旧逻辑:
- Use Glob: .claude/commands/**/*.md
- Use Grep: 搜索Task调用
- 构建依赖关系

新逻辑:
- Use Read: knowledge_graph.json
- 从components.commands提取
- 从relationships提取依赖
- 不再需要扫描
```

### Phase 1 Agents改动（6个）- 全部改为使用图谱

#### 4. consistency-validator.md
```yaml
改动: 读取knowledge_graph而非扫描
旧: Glob + Grep扫描所有文件
新: 从knowledge_graph.components分析
```

#### 5. filesystem-auditor.md
```yaml
改动: 基于图谱审计
旧: 扫描目录结构
新: 从knowledge_graph.file_structure分析
```

#### 6. context-inspector.md
```yaml
改动: 从图谱提取依赖
旧: 扫描识别依赖
新: 从knowledge_graph.relationships分析
```

#### 7. compliance-checker.md
```yaml
改动: 基于已验证的组件检查
旧: 扫描检查合规性
新: 从knowledge_graph.components检查
```

#### 8. resource-analyzer.md
```yaml
改动: 从图谱分析资源
旧: 扫描统计使用
新: 从knowledge_graph.usage_stats分析
```

### Phase 2 Agents改动（2个）

#### 9. command-flow-mapper.md
```yaml
改动: 基于图谱映射流程
旧: 扫描所有命令文件
新: 从knowledge_graph.commands分析流程
```

#### 10. flow-diagram-generator.md
```yaml
改动: 输入增加knowledge_graph
旧: 只读Phase 1报告
新: 读knowledge_graph + Phase 1报告
```

### Phase 3 Agents改动（2个）

#### 11. file-dependency-tracer.md
```yaml
改动: 从图谱提取文件依赖
旧: 扫描识别I/O操作
新: 从knowledge_graph.file_operations提取
```

#### 12. conditional-logic-analyzer.md
```yaml
改动: 基于图谱分析条件
旧: 扫描条件逻辑
新: 从knowledge_graph.conditional_flows分析
```

### Phase 4 Agents改动（3个claude-code-expert调用）

#### 13-15. claude-code-expert (3次调用)
```yaml
改动: 每次调用都传入knowledge_graph
prompt修改:
添加: "Reference knowledge_graph.json for verified implementations.
       Don't report as issues if already marked as IMPLEMENTED in graph."
```

### Phase 5 Agent改动（1个）

#### 16. system-health-reporter.md → 归档
```yaml
改动: 不修改，保留兼容性
说明: 新系统使用smart-health-reporter
     但保留旧的以防需要回滚
```

---

## 📁 归档文件（0个）

**策略**: 不归档任何文件，保持向后兼容
- 所有旧agents继续可用
- 可以运行旧版system-check对比
- 降低风险

---

## 🗂️ 文件组织结构

```
.claude/agents/
├── 【新增】system-knowledge-builder.md
├── 【新增】implementation-verifier.md  
├── 【新增】smart-health-reporter.md
├── 【新增】knowledge-graph-cache.md
├── 【修改】system-check-coordinator.md
├── 【修改】dependency-mapper.md
├── 【修改】consistency-validator.md
├── 【修改】filesystem-auditor.md
├── 【修改】context-inspector.md
├── 【修改】compliance-checker.md
├── 【修改】resource-analyzer.md
├── 【修改】command-flow-mapper.md
├── 【修改】flow-diagram-generator.md
├── 【修改】parallel-safety-validator.md
├── 【修改】file-dependency-tracer.md
├── 【修改】conditional-logic-analyzer.md
├── 【保留】system-health-reporter.md (不改，兼容用)
└── ... (其他agents不变)

.claude/report/{timestamp}/
├── 【新增】knowledge_graph.json (核心数据)
├── 【新增】verification_report.json
├── dependency-mapper_report.json
├── ... (其他报告照常)
└── 【新增】smart_health_report.md (替代旧的)
```

---

## 🎯 实施顺序（关键）

### Day 1: 核心基础
1. **创建system-knowledge-builder.md** (2h)
   - 这是一切的基础
   - 必须第一个完成
   - 测试生成的knowledge_graph.json质量

2. **修改system-check-coordinator.md** (1h)
   - 添加Phase 0调用knowledge-builder
   - 修改各Phase传递knowledge_graph

3. **创建implementation-verifier.md** (1h)
   - 读取风险报告
   - 验证是否已解决

### Day 2: 批量改造
4. **批量修改Phase 1 agents** (2h)
   - 6个agents改为读图谱
   - 使用相同的改造模式

5. **修改Phase 2-3 agents** (2h)
   - 4个agents改造
   - 测试信息流

6. **修改parallel-safety-validator** (1h)
   - 添加验证逻辑
   - 这是消除误报的关键

### Day 3: 完善优化
7. **创建smart-health-reporter.md** (2h)
   - 智能聚合
   - 去重和验证

8. **集成测试** (2h)
   - 运行完整流程
   - 对比新旧结果

9. **性能优化** (1h)
   - 添加knowledge-graph-cache
   - 优化慢速操作

---

## ⚠️ 风险控制

### 回滚策略
1. 保留所有原始文件
2. system-check-coordinator可切换新旧模式
3. 分阶段部署，每步验证

### 测试计划
```bash
# Phase 0测试
运行system-knowledge-builder
验证knowledge_graph.json完整性

# Phase 1测试  
运行单个改造后的agent
对比新旧输出

# 集成测试
运行完整v4.0流程
对比v3.1结果
```

### 兼容性保证
- 所有改动向后兼容
- 可以并行运行新旧版本
- 数据格式保持一致

---

## 📈 预期效果

### 性能提升
- 扫描次数: 15次 → 1次
- 执行时间: 10分钟 → 5分钟
- CPU使用: 降低50%

### 准确性提升
- 误报率: 30% → <5%
- 漏报率: 10% → <2%
- 置信度: 提升40%

### 维护性提升
- 新增analyzer无需重复扫描
- 知识可复用
- 调试更容易

---

## 💡 关键洞察

**最少的新建文件**（只有4个）:
1. knowledge-builder - 核心引擎
2. implementation-verifier - 验证器
3. smart-reporter - 智能聚合
4. cache-manager - 性能优化

**最大的复用**:
- 16个agents只需要改输入源
- 逻辑基本不变
- 风险最小

**最好的兼容性**:
- 不删除任何文件
- 可以随时回滚
- 新旧可并存

这就是完整的v4.0改动计划，每个文件都有明确的改动内容和原因。