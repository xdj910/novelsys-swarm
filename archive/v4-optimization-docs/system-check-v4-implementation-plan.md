# System Check v4.0 详细实施计划

## 🎯 目标
将误报率从30%降至5%以下，提升系统健康检查的准确性和可信度

## 📅 实施时间线
**总时长**: 3天
- Day 1: 核心组件开发
- Day 2: 集成和改造
- Day 3: 测试和优化

---

## Day 1: 核心组件开发 (今天)

### 上午：创建知识图谱构建器

#### 1.1 创建 system-knowledge-builder.md
```yaml
文件: .claude/agents/system-knowledge-builder.md
时间: 2小时

核心功能:
1. 一次性扫描所有系统文件
2. 构建完整知识图谱
3. 识别已实现的功能
4. 输出结构化JSON

知识图谱结构:
{
  "scan_metadata": {
    "timestamp": "20250910_100000",
    "total_files_scanned": 92,
    "scan_duration_ms": 3500
  },
  
  "components": {
    "commands": [
      {
        "name": "chapter-start",
        "path": ".claude/commands/novel/chapter-start.md",
        "delegates_to": "chapter-start-coordinator",
        "complexity": "low",
        "line_count": 45
      }
    ],
    "agents": [
      {
        "name": "entity-dictionary-updater",
        "path": ".claude/agents/entity-dictionary-updater.md",
        "type": "updater",
        "has_thinking": false,
        "has_file_locking": true,
        "lock_implementation": {
          "type": "file_lock",
          "path": "lines 128-172",
          "retry_logic": true,
          "timeout": 60
        }
      }
    ],
    "coordinators": [
      {
        "name": "chapter-start-coordinator",
        "path": ".claude/agents/chapter-start-coordinator.md",
        "orchestrates": ["director", "outline-generator", "scene-generator"],
        "has_thinking": true
      }
    ]
  },
  
  "relationships": {
    "command_to_coordinator": {
      "chapter-start": "chapter-start-coordinator",
      "next-chapter": "next-chapter-coordinator"
    },
    "file_operations": {
      "entity_dictionary.yaml": {
        "readers": ["bible-compliance-validator", "quality-scorer"],
        "writers": ["entity-dictionary-updater", "entity-dictionary-creator"],
        "has_lock_protection": true
      }
    }
  },
  
  "verified_implementations": {
    "file_locking": {
      "entity_dictionary": {
        "status": "IMPLEMENTED",
        "location": "entity-dictionary-updater.md:128-172",
        "mechanism": "file_lock_with_retry",
        "confidence": 1.0
      }
    },
    "caching": {
      "bible_cache": {
        "status": "IMPLEMENTED",
        "location": "bible-cache-manager.md",
        "performance_gain": "30-50%",
        "confidence": 1.0
      }
    },
    "yaml_frontmatter": {
      "status": "ALL_COMPLIANT",
      "verified_count": 70,
      "total_count": 70,
      "confidence": 1.0
    }
  },
  
  "potential_issues": {
    "suspected_risks": [
      {
        "type": "parallel_conflict",
        "description": "Multiple writers to entity_dictionary.yaml",
        "mitigation_found": true,
        "mitigation": "File locking implemented"
      }
    ]
  }
}
```

实现步骤:
1. 使用Glob扫描所有.md文件
2. 解析YAML frontmatter
3. 提取关键信息（name, description, thinking等）
4. 使用Grep查找特定模式：
   - Task调用 → 识别委托关系
   - Read/Write工具 → 识别文件操作
   - 锁机制代码 → 识别安全实现
5. 构建关系图
6. 输出JSON知识图谱

#### 1.2 创建知识图谱验证器
```yaml
文件: .claude/agents/knowledge-graph-validator.md
时间: 1小时

功能:
- 验证知识图谱完整性
- 检查关系一致性
- 标记缺失信息
- 计算覆盖率
```

### 下午：创建实现验证器

#### 1.3 创建 implementation-verifier.md
```yaml
文件: .claude/agents/implementation-verifier.md
时间: 2小时

核心功能:
1. 接收潜在风险列表
2. 主动验证每个风险
3. 深入检查实现代码
4. 更新风险状态

验证流程:
for each risk in potential_risks:
  switch risk.type:
    case "file_write_conflict":
      - 查找对应的writer agents
      - 检查是否有锁机制
      - 验证锁的正确性
      - 更新状态: SAFE/RISKY
      
    case "missing_frontmatter":
      - 读取实际文件
      - 验证frontmatter存在性
      - 更新状态: FALSE_POSITIVE/CONFIRMED
      
    case "circular_dependency":
      - 追踪调用链
      - 验证是否真的循环
      - 更新状态: CONFIRMED/FALSE_POSITIVE

输出格式:
{
  "verification_results": [
    {
      "original_risk": "Entity dictionary write conflicts",
      "risk_level": "CRITICAL",
      "verification_status": "FALSE_POSITIVE",
      "evidence": {
        "mitigation_found": true,
        "mitigation_type": "file_locking",
        "implementation_location": "entity-dictionary-updater.md:128-172",
        "verification_method": "code_inspection",
        "confidence": 0.95
      },
      "recommendation": "No action needed - properly protected"
    }
  ]
}
```

#### 1.4 创建智能聚合器
```yaml
文件: .claude/agents/smart-report-aggregator.md
时间: 1小时

功能:
1. 智能去重
2. 置信度加权
3. 验证优先
4. 历史对比
5. 分类输出
```

---

## Day 2: 集成和改造

### 上午：改造system-check-coordinator

#### 2.1 修改 system-check-coordinator.md
```yaml
时间: 2小时

主要改动:
1. Phase 0: 构建知识图谱（新增）
2. Phase 1-4: 基于图谱分析（不再重复扫描）
3. Phase 3.5: 实现验证（新增）
4. Phase 5: 智能报告（升级）

新的执行流程:
Phase 0: 知识图谱构建
  - system-knowledge-builder (单次执行)
  - 输出: knowledge_graph.json
  
Phase 1: 基础分析（基于图谱）
  - 6个analyzers并行
  - 输入: knowledge_graph.json
  - 不再扫描源文件
  
Phase 2: 深度分析（基于图谱+Phase1）
  - 2个analyzers并行
  - 输入: knowledge_graph.json + Phase1报告
  
Phase 3: 安全分析（基于前面所有）
  - 3个analyzers
  - 输入: 所有前面的报告
  
Phase 3.5: 验证（新增）
  - implementation-verifier
  - 输入: 所有detected risks
  - 输出: verified risks
  
Phase 4: 合规分析
  - 基于verified facts
  
Phase 5: 智能报告
  - smart-report-aggregator
  - 考虑所有验证结果
```

### 下午：改造现有analyzers

#### 2.2 批量改造analyzers
```yaml
时间: 3小时

需要改造的agents (11个):
1. dependency-mapper
2. consistency-validator
3. filesystem-auditor
4. context-inspector
5. compliance-checker
6. resource-analyzer
7. command-flow-mapper
8. file-dependency-tracer
9. conditional-logic-analyzer
10. claude-code-expert (3个调用)

改造内容:
旧版本:
- 使用Glob/Grep扫描源文件
- 独立分析
- 输出独立报告

新版本:
- 读取knowledge_graph.json
- 基于结构化数据分析
- 考虑已验证的事实
- 输出更准确的报告

示例改造 (dependency-mapper):
# 旧代码
Use Glob: .claude/commands/**/*.md
Use Grep: "Task\(.*subagent_type"
分析每个文件...

# 新代码
Use Read: knowledge_graph.json
从图谱中提取:
- components.commands
- relationships.command_to_coordinator
直接分析结构化数据...
```

---

## Day 3: 测试和优化

### 上午：集成测试

#### 3.1 运行对比测试
```yaml
时间: 2小时

测试方案:
1. 运行旧版system-check
   - 记录所有发现的"问题"
   - 记录执行时间
   
2. 运行新版system-check-v4
   - 记录所有发现的问题
   - 记录执行时间
   
3. 对比分析:
   - 误报减少率
   - 性能提升
   - 新发现的真实问题

预期结果:
- 误报: 30% → 5%
- 执行时间: 10分钟 → 5分钟
- 准确率: 70% → 95%
```

#### 3.2 验证关键场景
```yaml
关键测试用例:
1. Entity dictionary locking
   - 旧版: 报告为严重风险
   - 新版: 识别为已解决
   
2. YAML frontmatter
   - 旧版: 报告8个缺失
   - 新版: 全部正确识别
   
3. 章节编号冲突
   - 旧版: 报告高风险
   - 新版: 识别coordinator保护
```

### 下午：优化和文档

#### 3.3 性能优化
```yaml
时间: 1小时

优化点:
1. 知识图谱缓存
2. 并行执行优化
3. 报告生成加速
```

#### 3.4 更新文档
```yaml
时间: 1小时

更新内容:
1. CLAUDE.md - 添加v4.0说明
2. 创建system-check-v4-guide.md
3. 更新命令使用说明
```

---

## 🎯 成功标准

### 技术指标
- [ ] 误报率 < 5%
- [ ] 执行时间 < 5分钟
- [ ] 知识图谱覆盖率 > 95%
- [ ] 验证准确率 > 90%

### 功能验证
- [ ] Entity dictionary锁正确识别
- [ ] YAML frontmatter全部通过
- [ ] 章节编号安全正确评估
- [ ] Bible缓存功能正确识别

### 用户体验
- [ ] 报告更准确
- [ ] 建议更可操作
- [ ] 减少人工验证需求
- [ ] 提升信任度

---

## 🚀 立即开始的第一步

### Step 1: 创建system-knowledge-builder (现在)
```bash
# 我将创建这个核心组件
.claude/agents/system-knowledge-builder.md

这是整个v4.0的基础，其他所有改进都依赖于它。
```

### Step 2: 测试知识图谱质量
```bash
# 运行并验证输出
生成knowledge_graph.json
检查数据完整性
确认关键信息捕获
```

### Step 3: 逐步改造
```bash
# 按优先级改造
1. implementation-verifier (消除误报)
2. system-check-coordinator (新流程)
3. 其他analyzers (性能提升)
```

---

## 💡 关键洞察

**为什么这个方案会成功：**

1. **一次扫描** - 避免重复工作和不一致
2. **知识共享** - 信息在phases间流动
3. **主动验证** - 不是猜测，而是验证
4. **智能聚合** - 考虑所有context做决策

**最重要的改变：**
从"独立分析后汇总"变为"共享知识逐步深化"

这就像从"15个盲人摸象"变成"1个人看清全象后，15个专家各自深入分析不同部分"。

准备好开始实施了吗？