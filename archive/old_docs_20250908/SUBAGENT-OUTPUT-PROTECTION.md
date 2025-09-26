# Subagent输出保护系统

## 问题背景

Subagent在生成文件时可能出现的问题：
- 📄 文件被截断（特别是长内容）
- 🔧 JSON/YAML格式错误
- ❌ 缺少必要字段或结构
- 📝 内容不完整或格式混乱
- 🔤 编码问题导致的乱码

## 三层保护机制

### 第一层：实时验证 (subagent-output-validator.sh)

**触发时机**：文件写入后立即执行
**功能**：
- 验证JSON/YAML语法
- 检查必要字段存在性
- 验证数据范围合理性
- 检测文件截断
- 生成验证报告

**验证规则**：
```yaml
JSON文件:
  - 语法必须有效
  - meta.json必须有: chapter_number, word_count, last_modified
  - quality_check.json的分数必须在0-100之间

YAML文件:
  - 语法必须有效
  - bible.yaml必须有: title, characters, universe
  - entity_dictionary必须有基本结构

Markdown文件:
  - content.md必须有章节标题
  - 内容不能为空
  - 字数应大于50
```

### 第二层：自动修复 (auto-output-fixer.sh)

**触发时机**：验证后自动执行
**修复能力**：

#### JSON修复
- ✅ 移除尾随逗号
- ✅ 修复未闭合引号
- ✅ 添加缺失的必要字段
- ✅ 修正数据类型

#### YAML修复
- ✅ 修复缩进问题
- ✅ 替换制表符为空格
- ✅ 添加缺失的顶级结构
- ✅ 修复基本语法错误

#### Markdown修复
- ✅ 添加缺失的章节标题
- ✅ 修复编码问题（如智能引号）
- ✅ 清理多余空行
- ✅ 添加截断警告标记

### 第三层：人工介入提醒

当自动修复失败时：
- 🚨 生成失败报告到 `.claude/validation/`
- 📝 记录到 `.claude/logs/validation.log`
- ⚠️ 标记关键文件需要立即修复
- 💾 保留原始文件备份

## 文件截断检测

特别针对Subagent容易出现的截断问题：

```bash
检测方法:
1. 检查文件结尾是否正常
2. 检查是否有未完成的句子
3. 检查JSON/YAML是否完整闭合
4. 检查章节是否有结尾标记

处理方式:
- 轻微截断 → 自动添加标记
- 严重截断 → 生成警告报告
- JSON截断 → 尝试补全结构
- 内容截断 → 添加 [TRUNCATED] 标记
```

## 实际案例

### 案例1：JSON尾随逗号
```json
// Subagent生成的错误JSON
{
  "chapter": 1,
  "title": "Beginning",  // ← 错误的逗号
}

// 自动修复后
{
  "chapter": 1,
  "title": "Beginning"
}
```

### 案例2：章节内容截断
```markdown
# Subagent生成的截断内容
Sarah walked into the room and suddenly

// 自动修复后
Sarah walked into the room and suddenly

*[Chapter appears incomplete - pending continuation]*
```

### 案例3：缺失必要字段
```json
// Subagent生成的不完整meta.json
{
  "chapter_number": 5
}

// 自动修复后
{
  "chapter_number": 5,
  "word_count": 0,
  "status": "draft",
  "last_modified": "2025-09-03T12:00:00",
  "auto_fixed": true
}
```

## 监控和报告

### 验证日志
`~/.claude/logs/validation.log`
```
[2025-09-03 12:00:00] Validating Chapter Meta: ch001/meta.json
[2025-09-03 12:00:00] ✓ Validation passed: ch001/meta.json
[2025-09-03 12:00:01] ✗ Validation failed: ch002/content.md
  Errors: Content too short: 45 words
```

### 修复日志
`~/.claude/logs/auto-fixes.log`
```
[2025-09-03 12:00:02] Auto-fixed JSON: ch002/quality_check.json
  Fixes: Removed trailing commas; Added missing fields
```

### 失败报告
`~/.claude/validation/failure_*.txt`
- 详细的错误描述
- 文件内容预览
- 修复建议

## 性能影响

- ✅ **异步执行**：不阻塞主流程
- ✅ **静默运行**：不干扰用户
- ✅ **轻量级**：只验证关键文件
- ✅ **智能判断**：只修复明确的问题

## 配置选项

在 `.claude/hooks/config.yaml` 中可配置：
```yaml
validation:
  enabled: true
  strict_mode: false  # true = 阻塞式验证
  auto_fix: true
  backup_before_fix: true
  
thresholds:
  min_chapter_words: 50
  max_quality_score: 100
  json_depth_limit: 10
```

## 最佳实践

1. **定期检查验证日志**
   - 每日查看 `validation.log`
   - 关注反复出现的问题

2. **保留修复历史**
   - 不要删除 `.broken` 备份文件
   - 用于分析Subagent的问题模式

3. **优化Subagent提示词**
   - 根据常见错误优化agent指令
   - 添加格式验证要求到agent描述中

4. **人工复查关键文件**
   - Bible和entity_dictionary需要人工确认
   - 自动修复只是应急措施

## 总结

这个三层保护系统确保：
- 🛡️ **验证层**：立即发现问题
- 🔧 **修复层**：自动解决常见问题  
- 👀 **提醒层**：需要人工介入时及时通知
- 📊 **学习层**：积累问题模式，持续改进

让Subagent的输出更可靠，减少人工干预！