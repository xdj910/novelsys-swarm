# System Check v4.0 设计方案

## 当前v3.1的核心问题

### 1. 信息孤岛
- 15个agents各自独立工作
- 11个agents重复扫描同样的文件
- 信息不在phases间流动
- 没有知识积累和共享

### 2. 缺乏验证链
- 发现问题 → 直接报告
- 没有验证步骤
- 不检查是否已有解决方案
- 静态分析无法理解动态行为

### 3. 重复工作
- 每个agent都从零开始
- 不利用前面的分析结果
- 效率低下，容易矛盾

## v4.0 架构设计

### 核心理念：渐进式深化 + 智能验证

```
Phase 1: 扫描构建知识图谱
    ↓ (传递知识图谱)
Phase 2: 基于图谱深化分析
    ↓ (传递图谱+深化结果)
Phase 3: 智能验证和纠偏
    ↓ (传递验证后的事实)
Phase 4: 对标最佳实践
    ↓ (综合所有已验证信息)
Phase 5: 生成可信报告
```

### Phase 1: 构建知识图谱（新设计）

**单一超级扫描器**：system-knowledge-builder
```yaml
职责:
  - 一次性扫描所有文件
  - 构建完整的系统知识图谱
  - 输出结构化知识库

知识图谱内容:
  components:
    commands:
      - name, path, complexity, delegates_to
    agents:  
      - name, path, type, has_thinking, has_locking
    coordinators:
      - name, path, orchestrates
      
  relationships:
    - command → coordinator → agents
    - agent → files (read/write)
    - file → lock_mechanism (if any)
    
  implementations:
    verified_features:
      - entity_locking: {path, line, mechanism}
      - bible_caching: {path, line, performance}
      - yaml_frontmatter: {count: 70/70}
```

### Phase 2: 智能分析（基于图谱）

不再重复扫描，而是分析知识图谱：

**dependency-analyzer-v4**:
```yaml
输入: knowledge_graph.json
分析:
  - 从图谱中提取依赖关系
  - 识别循环依赖
  - 计算组件耦合度
输出: 依赖分析报告
```

**safety-analyzer-v4**:
```yaml
输入: knowledge_graph.json
分析:
  - 检查file写入冲突
  - 但先查看implementations.entity_locking
  - 如果已实现锁 → 标记为SAFE
  - 如果没有锁 → 标记为RISK
输出: 安全分析报告（更准确）
```

### Phase 3: 主动验证（新增）

**implementation-verifier**:
```yaml
输入: 
  - Phase 2报告的所有风险
  - knowledge_graph.json
  
工作流:
  for each reported_risk:
    1. 识别风险类型
    2. 查找对应的解决方案位置
    3. 深度检查实现代码
    4. 运行验证测试（如可能）
    5. 更新风险状态：
       - VERIFIED_SAFE (有完整解决方案)
       - PARTIALLY_SAFE (有部分缓解)
       - CONFIRMED_RISK (确实有问题)
       
输出: 验证后的风险报告
```

### Phase 4: 最佳实践对标（改进）

**claude-code-validator-v4**:
```yaml
输入:
  - verified_knowledge_graph.json
  - Phase 3验证报告
  
不再重复扫描，而是:
  - 基于已验证的事实对标
  - 只报告确认的违规
  - 提供具体的改进建议
```

### Phase 5: 智能报告生成（改进）

**smart-health-reporter**:
```yaml
输入: 所有phases的报告

智能特性:
  1. 去重: 多个报告提到同一问题只报一次
  2. 验证优先: 已验证安全的不再报告为风险
  3. 置信度加权: 
     - 多方确认的问题 = 高置信度
     - 单一报告的问题 = 需要验证
  4. 历史对比:
     - 与上次报告对比
     - 识别改进和退化
  5. 智能分类:
     - 真实问题 vs 理论风险
     - 已解决 vs 待解决
     - 紧急 vs 可延迟
```

## 实施步骤

### Step 1: 创建知识图谱构建器
```bash
# 新建agent
.claude/agents/system-knowledge-builder.md

职责：
- 一次扫描所有文件
- 提取所有信息
- 构建知识图谱
- 识别已实现的功能
```

### Step 2: 改造现有analyzers
```bash
# 修改为基于图谱分析
- dependency-mapper → dependency-analyzer-v4
- consistency-validator → consistency-analyzer-v4
- 等等...

改变：
- 不再扫描源文件
- 读取knowledge_graph.json
- 基于结构化数据分析
```

### Step 3: 添加验证层
```bash
# 新建验证器
.claude/agents/implementation-verifier.md

功能：
- 主动验证所有报告的问题
- 深入检查实现代码
- 更新问题状态
```

### Step 4: 升级报告生成器
```bash
# 增强智能
system-health-reporter → smart-health-reporter

新增：
- 去重逻辑
- 置信度权重
- 历史对比
- 智能分类
```

## 预期效果

### 性能提升
- 扫描时间：减少70%（只扫描一次）
- 分析速度：提升5倍（基于结构化数据）
- 内存使用：减少50%（避免重复加载）

### 准确性提升
- 误报率：从30%降至5%
- 漏报率：从10%降至2%
- 置信度：平均提升30%

### 可维护性提升
- 知识可复用
- 分析可追溯
- 结果可验证

## 对比示例

### 当前v3.1流程
```
dependency-mapper: 扫描所有文件 → "可能有entity字典冲突"
parallel-safety: 读dependency报告 → "确认有冲突风险"
最终报告: "⚠️ 严重：Entity字典写入冲突"
实际情况: 已实现完整的锁机制（误报）
```

### 新v4.0流程
```
knowledge-builder: 扫描一次 → 发现entity-dictionary-updater有锁实现
dependency-analyzer: 基于图谱 → "entity字典有多写入者"
implementation-verifier: 验证 → "已实现锁机制，标记为SAFE"
最终报告: "✅ Entity字典：已实现锁保护"
实际情况: 匹配（正确）
```

## 实施优先级

1. **紧急**：创建knowledge-builder（1天）
2. **重要**：添加implementation-verifier（1天）
3. **改进**：升级analyzers使用图谱（2天）
4. **优化**：增强报告生成器（1天）

## 总结

v4.0设计解决了当前的核心问题：
1. ✅ 信息孤岛 → 知识图谱共享
2. ✅ 缺乏验证 → 主动验证层
3. ✅ 重复工作 → 一次扫描多次使用
4. ✅ 静态局限 → 实现代码验证

这将使System Check成为真正可信赖的健康监控系统。