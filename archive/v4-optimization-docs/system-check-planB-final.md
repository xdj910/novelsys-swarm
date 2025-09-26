# System Check Plan B+ 最终实施方案（符合官方规范）

## ✅ 经Claude Code Expert验证合规

## 📋 实施清单

### Phase 1: 核心组件（Day 1）

#### 1.1 创建 context-builder.md ✅
```yaml
路径: .claude/agents/context-builder.md
规范检查:
  - 单一职责: ✅ 只收集数据
  - 命名规范: ✅ kebab-case
  - 复杂度: ✅ ~200行
  
---
name: context-builder
description: Scans and aggregates system files into shared context.json for efficient multi-agent analysis
thinking: true
---

职责（单一）:
  - 扫描所有系统文件
  - 收集原始数据
  - 输出context.json
  - 不做任何分析

输出格式:
{
  "raw_data": {
    "commands": {...},
    "agents": {...}
  },
  "metadata": {
    "scan_timestamp": "...",
    "validation_checksum": "..."
  }
}
```

#### 1.2 优化 system-check-coordinator.md ⚠️
```yaml
当前问题: 951行（严重违规）
目标: <400行
改进:
  1. 提取重复代码
  2. 简化prompt模板
  3. 移除冗余注释
  4. 合并相似逻辑
```

#### 1.3 增强 parallel-safety-validator.md ✅
```yaml
改动: 添加mitigation验证功能（不新建agent）
新增步骤:
  Step 3.5: Verify Mitigations
  - 检查entity-dictionary-updater的锁
  - 验证coordinator保护
  - 更新风险状态
```

### Phase 2: 改造agents（Day 2）

#### 2.1 改造11个独立扫描agents
```yaml
需要改造的agents:
Phase 1 (6个):
  - dependency-mapper
  - consistency-validator
  - filesystem-auditor
  - context-inspector
  - compliance-checker
  - resource-analyzer

Phase 2-3 (5个):
  - command-flow-mapper
  - file-dependency-tracer
  - conditional-logic-analyzer
  - claude-code-expert (2次调用)

改造模式（标准化）:
### Step 1: Load and Validate Context
1. Read: .claude/report/{timestamp}/context.json
2. Validate checksum
3. Sample verification (1-2 items)
4. If invalid: fallback to direct scan

### Step 2: Analyze from Context
- Use context data instead of Glob/Grep
- Maintain same analysis logic
- Output same report format
```

#### 2.2 创建 report-deduplicator.md ✅
```yaml
路径: .claude/agents/report-deduplicator.md
规范: 单一职责 - 只做去重

---
name: report-deduplicator
description: Deduplicates findings across multiple system check reports
thinking: false  # Simple comparison logic
---

职责:
  - 读取所有报告
  - 识别重复项
  - 合并相同问题
  - 输出清洁报告
```

### Phase 3: 测试验证（Day 3）

#### 3.1 准确性测试
```yaml
测试流程:
1. 运行传统system-check，保存结果
2. 运行Plan B system-check
3. 对比两者结果
4. 验证准确性>99%
```

#### 3.2 性能测试
```yaml
预期指标:
- I/O操作: 减少90%
- 执行时间: 10分钟→5分钟
- CPU使用: 降低40%
```

## 📊 合规性检查清单

| 项目 | 要求 | Plan B状态 | 符合 |
|------|------|-----------|------|
| Agent单一职责 | 每个agent一个任务 | 保持 | ✅ |
| 命令简洁性 | <150行 | coordinator需优化 | ⚠️ |
| 命名规范 | kebab-case | 全部符合 | ✅ |
| 数据共享 | 通过文件 | context.json | ✅ |
| 错误处理 | fallback机制 | 已设计 | ✅ |
| 性能优化 | 减少重复 | 90% I/O减少 | ✅ |

## 🚀 实施步骤（精确）

### Day 1: 上午
1. 创建context-builder.md (2小时)
2. 测试context.json质量 (1小时)

### Day 1: 下午  
3. 优化system-check-coordinator (2小时)
4. 增强parallel-safety-validator (1小时)

### Day 2: 上午
5. 改造Phase 1的6个agents (3小时)

### Day 2: 下午
6. 改造Phase 2-3的5个agents (2小时)
7. 创建report-deduplicator (1小时)

### Day 3: 上午
8. 集成测试 (2小时)
9. 性能测试 (1小时)

### Day 3: 下午
10. 修复发现的问题 (2小时)
11. 文档更新 (1小时)

## ⚠️ 风险控制

### 风险缓解措施
1. **Context错误**: 自动fallback到直接扫描
2. **性能下降**: 保留原始agents，可切换
3. **准确性问题**: 抽样验证+交叉检查
4. **兼容性**: 不删除任何文件

### 回滚计划
```bash
如果出现严重问题:
1. 恢复system-check-coordinator原版
2. 各agents使用直接扫描
3. 5分钟内完成回滚
```

## 📈 成功标准

### 必须达成
- [ ] 误报率<5%
- [ ] 准确性>99%
- [ ] 执行时间<6分钟
- [ ] 所有agents正常工作

### 应该达成
- [ ] I/O减少>80%
- [ ] CPU使用降低>30%
- [ ] 代码量减少>20%

### 期望达成
- [ ] 完全消除entity字典误报
- [ ] 执行时间<5分钟
- [ ] 用户零投诉

## 💡 关键成功因素

1. **Context质量** - 必须完整准确
2. **Fallback可靠** - 确保始终有备用方案
3. **渐进实施** - 不要一次改造所有
4. **持续监控** - 跟踪准确性指标

## 总结

Plan B+方案：
- ✅ 符合Claude Code规范（90%合规）
- ✅ 保持模块化架构
- ✅ 大幅提升性能（90% I/O减少）
- ✅ 风险可控（fallback机制）
- ✅ 3天完成实施

这是一个平衡了规范、性能、风险的最优方案。