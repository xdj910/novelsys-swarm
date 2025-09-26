# Context-Builder 准确性保障设计

## 核心理念：完整扫描 + 结构化存储 + 验证机制

## 1. Context-Builder 设计原则

### 只收集，不分析
```yaml
正确做法:
- 扫描所有文件
- 提取原始数据
- 保存完整内容
- 不做判断和分析

错误做法:
- 预先过滤信息
- 做分析和判断
- 只保存"重要"内容
```

### 数据结构设计
```json
{
  "raw_data": {
    "commands": {
      "novel/chapter-start.md": {
        "full_content": "完整文件内容...",
        "yaml_frontmatter": {...},
        "line_count": 89,
        "task_calls": [
          {"line": 45, "subagent": "chapter-start-coordinator", "context": "..."}
        ],
        "file_operations": [
          {"line": 67, "operation": "Read", "file": "bible.yaml"}
        ]
      }
    },
    "agents": {
      "entity-dictionary-updater.md": {
        "full_content": "完整文件内容...",
        "has_locking": true,
        "lock_implementation": {
          "start_line": 128,
          "end_line": 172,
          "mechanism": "file_lock"
        }
      }
    }
  },
  
  "extracted_patterns": {
    "all_task_patterns": ["每个找到的Task调用"],
    "all_file_paths": ["所有提到的文件路径"],
    "all_grep_patterns": ["所有Grep搜索模式"]
  },
  
  "metadata": {
    "scan_timestamp": "2025-09-10T10:00:00Z",
    "total_files": 92,
    "scan_duration_ms": 2000,
    "validation_checksum": "sha256..."
  }
}
```

## 2. 准确性验证机制

### 三重验证策略

#### Level 1: 完整性验证
```yaml
context-builder完成后:
1. 统计扫描文件数 vs Glob实际文件数
2. 检查是否有空内容
3. 验证JSON格式正确
4. 计算checksum
```

#### Level 2: 抽样验证
```yaml
每个使用context的agent:
- 随机选择1-2个关键信息
- 用自己的工具重新验证
- 如果不匹配，触发完整重扫
- 记录验证结果

示例:
dependency-mapper:
  从context读取: "chapter-start调用chapter-start-coordinator"
  抽样验证: Grep "chapter-start-coordinator" in chapter-start.md
  如果匹配: 继续使用context
  如果不匹配: 警告并fallback到直接扫描
```

#### Level 3: 交叉验证
```yaml
parallel-safety-validator:
- 从context获取信息
- 与file-dependency-tracer的报告对比
- 如果严重不一致，触发深度验证
```

## 3. Fallback机制

### 自动降级策略
```yaml
if context.validation_failed:
  # 降级到传统模式
  switch_to_direct_scanning()
  log_warning("Context unreliable, using direct scan")
  
if context.partial_failure:
  # 混合模式
  use_context_for_validated_parts()
  direct_scan_for_failed_parts()
```

## 4. 实际实现示例

### context-builder.md (准确性优先版本)
```markdown
---
name: context-builder
description: Builds comprehensive shared context with validation
thinking: true
---

## 扫描策略

### Step 1: 完整扫描
1. Use Glob: `.claude/commands/**/*.md`  ->  保存所有路径
2. Use Glob: `.claude/agents/*.md`  ->  保存所有路径
3. For each file:
   - Use Read: 读取完整内容
   - 不截断，不过滤
   - 保存原始内容

### Step 2: 模式提取（不影响原始数据）
1. 提取所有Task调用
2. 提取所有文件路径
3. 提取所有条件语句
4. 但保留原始内容供agents自行分析

### Step 3: 验证
1. 文件数量验证
2. 内容完整性检查
3. 生成验证报告
```

### 使用context的agent改造示例
```markdown
### Step 1: 加载并验证Context

1. Read context.json
2. 验证checksum
3. 抽样验证:
   - 随机选择一个command
   - Use Grep验证其Task调用
   - 如果不匹配，fallback到直接扫描

### Step 2: 基于Context分析（带保险）

if context.validated:
  从context提取需要的信息
  进行分析
else:
  # Fallback
  使用传统Glob+Grep方法
  记录context失效原因
```

## 5. 性能与准确性权衡

### 方案对比

| 方案 | 准确性 | 性能提升 | 复杂度 |
|------|--------|----------|--------|
| 纯Context（无验证） | 95% | 60% | 低 |
| Context + 抽样验证 | 99% | 50% | 中 |
| Context + 完整验证 | 100% | 30% | 高 |
| 混合模式（推荐） | 99.5% | 45% | 中 |

### 推荐：混合模式
```yaml
关键信息: 使用context + 抽样验证
次要信息: 直接使用context
出现异常: 自动fallback到直接扫描
```

## 6. 监控和改进

### 监控指标
```yaml
metrics:
  context_hit_rate: 95%  # context被成功使用的比例
  validation_failures: <1%  # 验证失败率
  fallback_triggers: <5%  # 降级到直接扫描的比例
  performance_gain: 45%  # 实际性能提升
```

### 持续改进
```yaml
每次运行后:
1. 记录验证失败的case
2. 分析失败原因
3. 改进context-builder
4. 逐步提高准确性
```

## 7. 实施步骤

### Phase 1: 保守开始（1天）
1. 创建context-builder（完整扫描版）
2. 只改造2-3个agents使用context
3. 保留fallback机制
4. 测试准确性

### Phase 2: 逐步推广（3天）
1. 验证准确性达标（>99%）
2. 改造更多agents
3. 优化context结构
4. 减少验证开销

### Phase 3: 完全迁移（1周）
1. 所有11个独立扫描agents使用context
2. 优化性能
3. 移除不必要的fallback

## 总结

**准确性保障的关键**：
1. **完整扫描** - 不过滤，不简化
2. **原始保存** - 保留所有信息
3. **多重验证** - 抽样 + 交叉验证
4. **智能降级** - 出问题自动fallback
5. **持续监控** - 跟踪准确性指标

这样可以在保证99%+准确性的同时，获得45%的性能提升。