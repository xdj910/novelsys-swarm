# NOVELSYS-SWARM Complete Command System

> 基于CCMP的完整小说创作命令体系
> 版本: v2.0 Ultimate | 更新: 2025-08-29

## 创作场景分析

### 核心创作场景
```yaml
creation_scenarios:
  new_series:
    description: "全新系列小说（第一本）"
    workflow: "idea  ->  series-bible  ->  book-1  ->  chapters"
    complexity: "highest"
    
  series_continuation:
    description: "系列续集（第二本、第三本）"
    workflow: "existing-bible  ->  book-n  ->  chapters"
    complexity: "medium"
    
  standalone_novel:
    description: "独立单本小说"
    workflow: "concept  ->  book-bible  ->  chapters"
    complexity: "medium"
    
  short_story_collection:
    description: "短篇小说集"
    workflow: "theme  ->  collection-bible  ->  stories"
    complexity: "low"
    
  novel_revision:
    description: "现有小说修订和完善"
    workflow: "analysis  ->  improvement-plan  ->  revision"
    complexity: "medium"
```

## 1. 系统初始化命令

### 基础系统命令
```bash
/novel:init                    # 初始化NOVELSYS-SWARM系统
                              # - 创建目录结构
                              # - 配置Agent系统
                              # - 设置质量标准
                              # - 初始化Git worktree环境

/novel:validate               # 检查系统完整性
                              # - Agent可用性验证
                              # - 上下文系统健康检查
                              # - 质量门控功能测试

/novel:help [category]        # 显示命令帮助
                              # categories: all, bible, chapter, quality, worktree

/novel:config [setting]       # 系统配置管理
                              # - 质量阈值设定
                              # - Agent并发数限制
                              # - 成本预算控制
```

## 2. Series Bible命令（核心架构）

### Bible生命周期管理
```bash
/novel:bible-new [series-name]    # 创建全新系列Bible
                                  # 场景：新系列小说
                                  # 流程：引导式头脑风暴
                                  # 输出：.claude/bibles/[series]/bible.yaml

/novel:bible-evolve [series]      # 基于现有Bible创建续集Bible
                                  # 场景：系列第2、3本
                                  # 保留：角色、世界观、核心设定
                                  # 扩展：新角色、新地点、新冲突

/novel:bible-standalone [title]   # 创建独立小说Bible
                                  # 场景：单本小说
                                  # 简化：无系列连续性要求
                                  # 聚焦：单一故事完整性

/novel:bible-collection [theme]   # 创建短篇集合Bible
                                  # 场景：主题短篇集
                                  # 统一：风格、主题、世界观
                                  # 灵活：独立故事结构

/novel:bible-parse [name]         # 解析Bible为技术实施方案
                                  # 转换：创意概念  ->  可执行计划
                                  # 输出：.claude/epics/[name]/epic.md

/novel:bible-list                 # 列出所有Bible项目
/novel:bible-show [name]          # 显示Bible详情和状态
/novel:bible-edit [name]          # 编辑现有Bible
/novel:bible-validate [name]      # 验证Bible完整性和一致性
/novel:bible-backup [name]        # 备份Bible版本
/novel:bible-restore [name] [version]  # 恢复Bible版本
```

### Bible增强命令
```bash
/novel:bible-enhance [name] [dimension]  # 增强Bible特定维度
                                         # dimensions: characters, world, mystery, style

/novel:bible-analyze [name]              # 分析Bible质量和完整性
/novel:bible-compare [name1] [name2]     # 比较不同Bible版本
/novel:bible-merge [source] [target]     # 合并Bible内容
```

## 3. Epic命令（书籍级管理）

### Epic生命周期
```bash
/novel:epic-decompose [bible-name]    # 分解Bible为书籍Epic
                                      # 输出：章节规划、创作任务分解
                                      # 文件：.claude/epics/[name]/book-plan.md

/novel:epic-sync [name]               # 同步Epic到项目管理
                                      # 创建：进度追踪文件
                                      # 建立：任务依赖关系

/novel:epic-oneshot [name]            # 一键分解并同步
                                      # = decompose + sync

/novel:epic-start [name]              # 启动Epic的并行创作
                                      # 创建：多个worktree环境
                                      # 启动：Book和Chapter Epic协调者

/novel:epic-merge [name]              # 合并所有并行工作成果
                                      # 集成：各章节内容
                                      # 验证：整体一致性

/novel:epic-list                      # 列出所有Epic项目
/novel:epic-show [name]               # 显示Epic及其任务进度
/novel:epic-status [name]             # 检查Epic整体状态
/novel:epic-close [name]              # 标记Epic完成
/novel:epic-refresh [name]            # 从任务更新Epic进度
```

## 4. Chapter命令（章节级执行）

### 章节创作命令
```bash
/novel:chapter-new [book] [number]      # 创建新章节大纲
                                        # 基于：Book Epic规划
                                        # 输出：章节结构文档

/novel:chapter-start [book] [number]    # 启动章节并行创作
                                        # 创建：章节专用worktree
                                        # 启动：Chapter Epic协调者
                                        # 分配：6-12个Task Agent

/novel:next-chapter                     # 写下一章
                                        # 自动：找到下一章号
                                        # 调用：chapter-start

/novel:chapter-revise [book] [number]   # 修订现有章节
                                        # 分析：质量问题
                                        # 启动：目标优化Agent

/novel:chapter-status [book] [number]   # 检查章节创作状态
/novel:chapter-show [book] [number]     # 显示章节详情
/novel:chapter-validate [book] [number] # 验证章节质量
/novel:chapter-list [book]              # 列出书籍所有章节
```

### 批量章节操作
```bash
/novel:chapters-batch [book] [range]    # 批量章节操作
                                        # 例：/novel:chapters-batch book1 1-5
                                        # 启动：多worktree并行创作

/novel:chapters-sequence [book] [list]  # 序列章节创作
                                        # 例：/novel:chapters-sequence book1 3,7,12
                                        # 维护：章节间依赖关系
```

## 5. 工作流导航命令

### 智能推荐系统
```bash
/novel:next [context]         # 智能推荐下一个优先任务
                              # contexts: bible, chapter, quality, revision
                              # 分析：依赖、并行性、阻塞因素

/novel:status [scope]         # 项目仪表板
                              # scopes: all, bible, epic, chapter, quality

/novel:standup [period]       # 生成状态报告
                              # periods: daily, weekly, monthly

/novel:blocked [type]         # 显示阻塞任务
                              # types: critical, quality, resource, dependency

/novel:in-progress [filter]   # 列出进行中的工作
                              # filters: agent, chapter, epic

/novel:dashboard             # 综合创作仪表板
                              # 整合：进度、质量、资源、问题
```

### 优先级和调度
```bash
/novel:priority-set [task] [level]    # 设置任务优先级
                                      # levels: critical, high, medium, low

/novel:schedule [task] [time]         # 调度任务执行时间
/novel:deadline-set [task] [date]     # 设置任务截止时间
/novel:resource-allocate [task] [budget]  # 分配资源预算
```

## 6. Quality命令（质量管理）

### 质量验证系统
```bash
/novel:quality-check [target] [dimension]  # 运行质量检查
                                           # targets: bible, chapter, book
                                           # dimensions: all, character, plot, style

/novel:quality-gate [stage] [target]       # 执行质量门控
                                           # stages: 1-5
                                           # 阻止：低质量内容推进

/novel:quality-report [scope] [format]     # 生成质量报告
                                           # scopes: chapter, book, series
                                           # formats: summary, detailed, chart

/novel:quality-trend [period]              # 质量趋势分析
                                           # periods: week, month, project

/novel:quality-benchmark [target]          # 质量基准测试
/novel:quality-compare [source] [target]   # 质量对比分析
```

### 质量改进命令
```bash
/novel:improve [target] [focus]       # 启动质量改进
                                      # focus: character, plot, style, consistency

/novel:polish [chapter] [aspect]      # 精细化润色
                                      # aspects: dialogue, description, pacing

/novel:consistency-fix [scope]        # 修复一致性问题
                                      # scopes: character, world, timeline
```

## 7. Worktree命令（并行环境）

### Worktree环境管理
```bash
/novel:worktree-create [type] [id]    # 创建隔离工作环境
                                      # types: chapter, revision, experiment

/novel:worktree-start [range]         # 启动多章节并行worktree
                                      # 例：/novel:worktree-start 1-5

/novel:worktree-list                  # 列出所有活跃worktree
/novel:worktree-status [id]           # 检查特定worktree状态
/novel:worktree-merge [id]            # 合并worktree成果
/novel:worktree-cleanup [condition]   # 清理worktree环境
                                      # conditions: completed, failed, abandoned

/novel:worktree-switch [id]           # 切换到指定worktree
/novel:worktree-backup [id]           # 备份worktree状态
/novel:worktree-restore [id] [backup] # 恢复worktree状态
```

## 8. Agent命令（Agent管理）

### Agent协调和监控
```bash
/novel:agents-status                  # 显示所有Agent状态
/novel:agents-performance            # Agent性能分析
/novel:agents-optimize               # 优化Agent配置

/novel:agent-start [type] [task]     # 启动特定Agent
/novel:agent-stop [id]               # 停止特定Agent
/novel:agent-restart [id]            # 重启Agent
/novel:agent-debug [id]              # Agent调试模式

/novel:swarm-launch [configuration]  # 启动Agent蜂群
/novel:swarm-status                  # 蜂群整体状态
/novel:swarm-optimize                # 蜂群性能优化
```

## 9. Context命令（上下文管理）

### 上下文系统
```bash
/novel:context-sync [scope]          # 同步上下文
                                     # scopes: all, bible, chapter, agent

/novel:context-create [type] [source] # 创建上下文
                                      # types: bible, character, world

/novel:context-update [target]        # 更新上下文
/novel:context-validate [scope]       # 验证上下文一致性
/novel:context-optimize               # 优化上下文效率
/novel:context-backup                 # 备份上下文状态
/novel:context-restore [version]      # 恢复上下文版本
```

## 10. 高级工作流命令

### 快捷工作流
```bash
/novel:quickstart [type] [name]       # 快速启动项目
                                      # types: series, standalone, collection

/novel:express-chapter [book] [number] # 快速章节创作
                                       # 一键：大纲 -> 创作 -> 质检 -> 完成

/novel:batch-process [operation] [targets] # 批量处理
                                           # operations: create, revise, validate

/novel:smart-continue                 # 智能继续创作
                                      # 分析：当前状态
                                      # 推荐：最优下一步
```

### 实验和测试命令
```bash
/novel:experiment [type] [parameters]  # 创作实验
                                       # types: style, character, plot

/novel:a-b-test [variant1] [variant2]  # A/B测试对比
/novel:prototype [concept]             # 快速原型验证
/novel:sandbox [purpose]               # 沙盒环境测试
```

## 11. 数据管理命令

### 数据操作
```bash
/novel:export [format] [target]       # 导出数据
                                      # formats: pdf, epub, markdown, docx

/novel:import [source] [format]       # 导入外部内容
/novel:backup [scope] [location]      # 数据备份
/novel:restore [backup] [target]      # 数据恢复
/novel:archive [project] [location]   # 项目归档
/novel:clean [type]                   # 清理数据
                                      # types: temp, logs, cache
```

### 版本控制
```bash
/novel:version-create [name] [description] # 创建版本标记
/novel:version-list                        # 列出所有版本
/novel:version-compare [v1] [v2]           # 版本比较
/novel:version-rollback [version]          # 回滚到指定版本
```

## 12. 分析和报告命令

### 数据分析
```bash
/novel:analyze [target] [dimension]   # 深度分析
                                      # dimensions: quality, consistency, readability

/novel:metrics [scope] [period]       # 指标统计
/novel:insights [focus]               # 智能洞察生成
/novel:recommendations [context]      # 改进建议

/novel:report-generate [type] [scope] # 生成报告
                                      # types: progress, quality, performance
```

## 13. 命令组合和快捷方式

### 典型工作流
```bash
# 新系列小说完整流程
/novel:bible-new mystery-series
/novel:bible-parse mystery-series  
/novel:epic-oneshot mystery-series
/novel:worktree-start 1-3
/novel:quality-check all

# 系列续集快速启动
/novel:bible-evolve mystery-series book2
/novel:epic-start mystery-series-book2

# 单章节快速创作
/novel:express-chapter book1 5

# 质量改进循环
/novel:quality-check chapter book1-ch3
/novel:improve book1-ch3 character
/novel:quality-validate book1-ch3

# 项目健康检查
/novel:status all
/novel:blocked critical  
/novel:next bible
```

### 智能默认值
```bash
/novel:next           # 自动推荐最优任务
/novel:status         # 默认显示全项目状态  
/novel:quality-check  # 默认检查当前工作
/novel:standup        # 默认生成每日报告
```

这套命令体系特点：

- **场景覆盖完整**：新系列、续集、单本、短篇集、修订
- **渐进式工作流**：Bible  ->  Epic  ->  Chapter  ->  Quality
- **智能化操作**：自动推荐、默认参数、批量处理
- **可组合性强**：命令可串联成复杂工作流
- **容错性好**：备份、恢复、版本控制
- **可扩展性**：插件化Agent、自定义工作流

通过这套完整的命令体系，NOVELSYS-SWARM能够处理所有类型的小说创作项目！🚀

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "\u8bbe\u8ba1\u5c0f\u8bf4\u521b\u4f5c\u573a\u666f\u548c\u6d41\u7a0b", "status": "completed", "activeForm": "\u8bbe\u8ba1\u5c0f\u8bf4\u521b\u4f5c\u573a\u666f\u548c\u6d41\u7a0b"}, {"content": "\u6784\u5efa\u5b8c\u6574\u7684/novel:\u547d\u4ee4\u4f53\u7cfb", "status": "completed", "activeForm": "\u6784\u5efa\u5b8c\u6574\u7684/novel:\u547d\u4ee4\u4f53\u7cfb"}, {"content": "\u5b9e\u73b0\u6e10\u8fdb\u5f0f\u521b\u4f5c\u5de5\u4f5c\u6d41", "status": "in_progress", "activeForm": "\u5b9e\u73b0\u6e10\u8fdb\u5f0f\u521b\u4f5c\u5de5\u4f5c\u6d41"}, {"content": "\u5efa\u7acb\u667a\u80fd\u9ed8\u8ba4\u503c\u548c\u53c2\u6570\u7cfb\u7edf", "status": "pending", "activeForm": "\u5efa\u7acb\u667a\u80fd\u9ed8\u8ba4\u503c\u548c\u53c2\u6570\u7cfb\u7edf"}, {"content": "\u8bbe\u8ba1\u9519\u8bef\u6062\u590d\u548c\u6570\u636e\u4fdd\u62a4\u673a\u5236", "status": "pending", "activeForm": "\u8bbe\u8ba1\u9519\u8bef\u6062\u590d\u548c\u6570\u636e\u4fdd\u62a4\u673a\u5236"}]