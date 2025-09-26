# NOVELSYS-SWARM 命令手册

> 完整的命令参考文档  
> Version: 2.5.0 | Updated: 2025-01-30

## 📋 命令分类

### 🎬 创作命令

#### /novel:init
初始化NOVELSYS-SWARM系统
```bash
/novel:init
```

#### /novel:project-new
创建新小说项目
```bash
/novel:project-new "项目名称"
```

#### /novel:concept-new
创建故事概念
```bash
/novel:concept-new "故事标题"
# 示例: /novel:concept-new "量子觉醒"
```

#### /novel:bible-create
创建小说Bible（世界观设定）
```bash
/novel:bible-create "类型"
# 示例: /novel:bible-create "科幻悬疑"
```

#### /novel:chapter-decompose
分解章节大纲
```bash
/novel:chapter-decompose
```

#### /novel:chapter-start
生成单个章节
```bash
/novel:chapter-start [章节号]
# 示例: /novel:chapter-start 1
```

#### /novel:parallel-chapter ⚡
并行生成多个章节（新功能）
```bash
/novel:parallel-chapter [章节号列表]
# 示例: /novel:parallel-chapter 1 2 3
```

### 🔧 管理命令

#### /novel:status
查看实时状态
```bash
/novel:status
```
显示：
- 当前进度
- Agent状态
- 质量分数
- 依赖关系

#### /novel:github-init
初始化GitHub项目
```bash
/novel:github-init "项目名"
# 示例: /novel:github-init "my-awesome-novel"
```

#### /novel:sync
同步到GitHub
```bash
/novel:sync [章节号]
# 示例: /novel:sync 1
```

#### /novel:dependency-add
添加依赖关系
```bash
/novel:dependency-add [源章节] [目标章节] [类型]
# 示例: /novel:dependency-add 1 3 plot
```
类型：
- plot: 情节依赖
- character: 角色依赖
- setting: 设定依赖

#### /novel:dependency-check
检查依赖关系
```bash
/novel:dependency-check
```

#### /novel:foreshadowing-add
添加伏笔
```bash
/novel:foreshadowing-add "名称" [设置章节] [回收章节]
# 示例: /novel:foreshadowing-add "神秘徽章" 1 5
```

#### /novel:foreshadowing-status
查看伏笔状态
```bash
/novel:foreshadowing-status
```

### 📊 质量命令

#### /novel:quality-check
质量检查
```bash
/novel:quality-check [章节号]
# 示例: /novel:quality-check 1
```
评估维度：
- 角色深度 (≥95分)
- 情节连贯 (≥99分)
- 文字表达 (≥95分)
- 设定一致 (≥98分)
- 情感共鸣 (≥95分)
- 对话自然 (≥95分)
- 伏笔完整 (=100分)
- 创新性 (≥90分)

#### /novel:iterate
迭代优化
```bash
/novel:iterate [章节号] [迭代次数]
# 示例: /novel:iterate 1 3
```
迭代流程：
1. 初稿 (85分)
2. 优化 (92分)
3. 精雕 (98分)

#### /novel:consistency-check
一致性检查
```bash
/novel:consistency-check
```

### 📤 导出命令

#### /novel:export
导出作品
```bash
/novel:export [格式] [章节范围]
# 示例: /novel:export markdown 1-10
# 示例: /novel:export epub all
```
支持格式：
- markdown
- html
- epub
- pdf
- docx

#### /novel:preview
预览章节
```bash
/novel:preview [章节号]
```

### 🛠️ 系统命令

#### /novel:config
配置系统
```bash
/novel:config [选项] [值]
# 示例: /novel:config parallel_workers 8
```

#### /novel:reset
重置系统
```bash
/novel:reset [--hard]
```

#### /novel:backup
备份数据
```bash
/novel:backup [备份名]
```

#### /novel:restore
恢复数据
```bash
/novel:restore [备份名]
```

## 🎯 工作流示例

### 完整创作流程
```bash
# 1. 初始化
/novel:init
/novel:github-init "my-novel"

# 2. 概念设计
/novel:concept-new "量子觉醒"
/novel:bible-create "科幻悬疑"

# 3. 章节规划
/novel:chapter-decompose

# 4. 并行生成
/novel:parallel-chapter 1 2 3

# 5. 质量检查
/novel:quality-check 1
/novel:iterate 1 2

# 6. 同步发布
/novel:sync 1
/novel:export epub all
```

### 伏笔管理流程
```bash
# 添加伏笔
/novel:foreshadowing-add "神秘信件" 2 8
/novel:foreshadowing-add "失踪的项链" 3 10

# 检查状态
/novel:foreshadowing-status

# 验证回收
/novel:consistency-check
```

### 依赖管理流程
```bash
# 添加依赖
/novel:dependency-add 1 3 plot
/novel:dependency-add 2 5 character

# 检查依赖图
/novel:dependency-check

# 自动排序执行
/novel:parallel-chapter --respect-dependencies
```

## ⚙️ 高级选项

### 并行执行控制
```bash
# 设置并行数
/novel:config parallel_workers 8

# 设置Stream权重
/novel:config stream_weights "character:1.2,plot:1.0"

# 启用/禁用Context Firewall
/novel:config use_firewall true
```

### GitHub集成
```bash
# 设置Issue标签
/novel:config github_labels "novel,chapter,wip"

# 自动同步
/novel:config auto_sync true

# 增量同步模式
/novel:config sync_mode incremental
```

### Agent配置
```bash
# 查看活跃Agent
/novel:agent-list

# 调整Agent权重
/novel:agent-weight "emotion-weaver" 1.5

# 启用特定Agent
/novel:agent-enable "action-choreographer"
```

## 🔍 调试命令

#### /novel:debug
启用调试模式
```bash
/novel:debug [on|off]
```

#### /novel:trace
追踪执行过程
```bash
/novel:trace [章节号]
```

#### /novel:profile
性能分析
```bash
/novel:profile [命令]
```

## 📊 监控命令

#### /novel:monitor
实时监控面板
```bash
/novel:monitor
```
显示：
- CPU/内存使用
- Agent活动
- Token消耗
- 执行时间

#### /novel:stats
统计信息
```bash
/novel:stats [时间范围]
# 示例: /novel:stats today
# 示例: /novel:stats 7d
```

## ⚠️ 注意事项

1. **并行执行限制**
   - 建议同时不超过8个章节
   - 复杂章节建议降低并行数

2. **GitHub同步**
   - 需要先运行 `gh auth login`
   - 确保有仓库写入权限

3. **质量控制**
   - 初次生成建议至少2轮迭代
   - 关键章节建议3轮迭代

4. **依赖管理**
   - 避免循环依赖
   - 依赖链不宜过长

## 🆘 常见问题

### Q: 并行生成失败？
```bash
# 减少并行数
/novel:config parallel_workers 4
# 或单章节生成
/novel:chapter-start 1
```

### Q: GitHub同步失败？
```bash
# 重新认证
gh auth login
# 检查权限
gh auth status
```

### Q: 质量分数低？
```bash
# 增加迭代次数
/novel:iterate [章节] 3
# 或调整Agent权重
/novel:agent-weight "prose-craftsman" 1.5
```

---

*最后更新: 2025-01-30 | 详细文档: [docs/index.md](index.md)*