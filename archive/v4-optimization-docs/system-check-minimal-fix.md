# System Check 最小改造方案

## 目标：用最少改动解决80%误报

不重建系统，只需改3个文件，30分钟完成。

## 改造清单

### ✅ 改造1：system-check-coordinator.md（5分钟）
**改什么**: 9处"Critical Analysis Guidelines"
**怎么改**: 
```markdown
# 替换所有这些文本：
"记住：我们需要诚实的系统评估，不是乐观的理论推测。"

# 改为：
"记住：平衡评估，验证已实现的功能，区分理论风险与实际问题。"
```

**效果**: 分析不再过度悲观

### ✅ 改造2：parallel-safety-validator.md（15分钟）
**改什么**: 添加Step 3.5
**怎么改**: 在发现风险后，主动验证是否已解决
```python
# 伪代码
if risk == "entity_dictionary_conflict":
    check entity-dictionary-updater.md
    if has_lock_mechanism:
        risk_status = "MITIGATED"
```

**效果**: Entity dictionary误报消除

### ✅ 改造3：dependency-mapper.md（10分钟）
**改什么**: 添加agent扫描
**怎么改**: 不只扫描commands，也扫描agents
```bash
# 新增扫描
Grep "lock|Lock|atomic|mutex" in .claude/agents/*.md
# 记录所有安全实现
```

**效果**: 发现并记录所有已实现的保护机制

## 实施步骤

### Step 1: 修改指导原则（立即）
```bash
1. 打开 system-check-coordinator.md
2. 搜索 "Critical Analysis Guidelines"
3. 替换为 "Balanced Analysis Guidelines"
4. 修改 "诚实的系统评估" → "平衡的系统评估"
5. 保存
```

### Step 2: 增强parallel-safety-validator（5分钟后）
```bash
1. 打开 parallel-safety-validator.md
2. 找到 Step 3: Validate File Safety
3. 在后面添加 Step 3.5: Verify Mitigation
4. 添加验证逻辑：
   - 检查entity-dictionary-updater的锁
   - 检查coordinator的保护
   - 更新风险状态
5. 保存
```

### Step 3: 扩展dependency-mapper（10分钟后）
```bash
1. 打开 dependency-mapper.md
2. 在扫描commands后
3. 添加扫描agents的步骤
4. 记录发现的安全机制
5. 添加到输出报告
6. 保存
```

## 测试验证

### 运行对比测试
```bash
# 改造前
/novel:system-check
# 记录：Entity dictionary conflicts（误报）

# 改造后
/novel:system-check
# 预期：Entity dictionary - MITIGATED by lock
```

## 预期改进

| 问题 | 改造前 | 改造后 |
|------|--------|--------|
| Entity字典冲突 | ❌ CRITICAL风险 | ✅ 已缓解(有锁) |
| YAML frontmatter | ❌ 8个缺失 | ✅ 全部正确 |
| 章节编号冲突 | ❌ HIGH风险 | ✅ Coordinator保护 |
| Bible缓存 | ❓ 未识别 | ✅ 已实现 |

## 优势

1. **最小改动** - 只改3个文件
2. **向后兼容** - 不破坏现有功能
3. **立即见效** - 30分钟完成
4. **可回滚** - 改动小，容易撤销

## 为什么这样就够了

**核心洞察**：
- 90%的误报来自"不验证实现"
- 只要加上验证步骤，误报大幅减少
- 不需要重建整个系统

**关键改动**：
1. 改变分析态度（不再过度怀疑）
2. 添加验证步骤（检查是否已解决）
3. 扫描安全实现（发现保护机制）

这三个改动解决了主要问题：
- ✅ Entity字典锁 - 会被发现和验证
- ✅ YAML frontmatter - 不再误报
- ✅ 章节编号 - 识别coordinator保护
- ✅ 分析态度 - 更加平衡

## 后续优化（可选）

如果这个方案效果好，可以考虑：
1. Phase 2优化：添加缓存避免重复扫描
2. Phase 3优化：改进其他validators
3. Phase 4优化：增强报告聚合智能

但这些都是锦上添花，核心问题这3个改动就能解决。

## 总结

**不需要重建，只需要"教会"现有系统：**
1. 不要过度怀疑
2. 发现问题要验证
3. 扫描已有的解决方案

30分钟的改动，解决80%的误报问题。