# NOVELSYS-SWARM 命令工作流指南

## 完整小说创作工作流

### 1. 项目初始化流程
```bash
/novel:project-new "科幻侦探"     # 创建新项目
    ↓ (项目创建后)
/novel:bible-view                 # 查看Bible内容
    ↓ (如果Bible需要改进)
/novel:bible-create               # 增强Bible内容
    ↓ (Bible就绪后)
/novel:status                     # 检查项目状态
```

### 2. 章节创作流程
```bash
/novel:chapter-start 1            # 创建第一章
    ↓ (质量≥95)
/novel:context-sync               # 学习高质量章节
    ↓
/novel:next-chapter               # 自动生成下一章
    ↓ (质量90-94)
/novel:smart-fix 2                # 修复质量问题
    ↓ (质量≥95)
/novel:context-sync               # 更新上下文
```

### 3. 质量管理流程
```bash
/novel:quality-check-individual 3 # 检查单章质量
    ↓ (质量<95)
/novel:smart-fix 3                # 智能修复
    ↓ (多章完成后)
/novel:quality-check-cross 1-5    # 跨章节一致性检查
    ↓ (发现跨章节问题)
/novel:smart-fix-cross            # 修复连续性问题
```

### 4. 书籍完成流程
```bash
/novel:quality-check-cross all    # 全书质量检查
    ↓ (质量合格)
/novel:book-complete              # 完成当前书籍
    ↓ (继续系列)
/novel:next-book                  # 开始下一本书
    ↓ (或扩展系列)
/novel:extend-series              # 扩展系列规划
```

### 5. 项目管理流程
```bash
/novel:project-list               # 查看所有项目
    ↓ (选择项目)
/novel:project-switch "项目名"    # 切换到其他项目
    ↓ 
/novel:status                     # 查看当前状态
    ↓
/novel:next                       # 获取智能建议
```

### 6. 系统维护流程
```bash
/novel:system-check               # 系统健康检查
    ↓ (发现问题)
[Follow recommendations in report] # 按报告建议修复
    ↓
/novel:flow-mapping               # 分析系统流程
    ↓
/novel:standup                    # 项目进度报告
```

## 智能命令连接

### 条件性下一步建议

#### 章节生成后：
- **质量≥95** → `/novel:next-chapter` 继续创作
- **质量90-94** → `/novel:smart-fix` 提升质量
- **质量<90** → 重新生成或大修改

#### 质量检查后：
- **通过** → `/novel:context-sync` 学习精华
- **小问题** → `/novel:smart-fix` 快速修复
- **大问题** → 人工干预修改

#### 系统检查后：
- **分数95+** → 继续正常创作
- **分数85-94** → 按建议优化
- **分数<85** → 优先修复关键问题

#### 项目切换后：
- **有未完成章节** → `/novel:next` 获取建议
- **Bible不完整** → `/novel:bible-create` 完善
- **准备就绪** → `/novel:chapter-start` 开始创作

## 快速参考

### 常用命令序列
- 新手起步: `project-new` → `bible-view` → `chapter-start 1`
- 日常创作: `status` → `next-chapter` → `quality-check-individual`
- 质量提升: `quality-check-individual` → `smart-fix` → `context-sync`
- 完成书籍: `quality-check-cross all` → `book-complete` → `next-book`

### 智能命令
- `/novel:next` - 根据当前状态推荐最佳下一步
- `/novel:status` - 显示项目状态和建议
- `/novel:standup` - 多维度进度分析

## 工作流优化建议

1. **自动化流程**：
   - 章节生成后自动触发质量检查
   - 质量≥95自动触发context-sync
   - 多章完成自动建议cross-check

2. **批处理模式**：
   - 连续生成多章：使用 `next-chapter` 循环
   - 批量修复：`smart-fix-cross` 处理多章
   - 统一更新：`unified-update-pipeline` 

3. **质量门控**：
   - 设置最低质量标准（95分）
   - 自动阻止低质量内容进入上下文
   - 强制修复后才能继续

这个工作流确保每个命令都有清晰的下一步，形成完整的创作闭环。