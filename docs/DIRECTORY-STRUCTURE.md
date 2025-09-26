# 项目目录结构说明

> NOVELSYS-SWARM 2.5 完整目录结构文档  
> Version: 2.5.0 | Updated: 2025-01-30

## 📂 根目录结构

```
D:\NOVELSYS-SWARM\
├── src/                    # 源代码
├── tests/                  # 测试文件
├── docs/                   # 文档
├── data/                   # 数据存储
├── .claude/archives/       # 归档文件（统一）
├── .claude/                # Claude配置
├── README.md               # 项目主页
├── SYSTEM-ARCHITECTURE-COMPLETE.md  # 架构文档
├── CONTRIBUTING.md         # 贡献指南
├── CHANGELOG.md           # 变更日志
├── CLAUDE.md              # Claude配置
└── requirements.txt       # Python依赖
```

## 📦 源代码目录 (src/)

### 核心模块 (src/core/)
**状态**: ✅ 已实现v2.5全部功能

| 文件 | 功能 | 状态 | 说明 |
|-----|------|------|------|
| **context_firewall.py** | Context防火墙 | ✅ 新增 | v2.5核心功能 |
| **github_integration.py** | GitHub集成 | ✅ 新增 | Issues持久化 |
| **parallel_coordinator.py** | 并行协调器 | ✅ 新增 | 8-Stream并行 |
| **agent_type_mapper.py** | Agent映射 | ✅ 新增 | 动态分配 |
| **execution_status.py** | 执行状态 | ✅ 新增 | 实时监控 |
| **git_worktree_manager.py** | Worktree管理 | ✅ 新增 | 多分支并行 |
| **five_stage_workflow.py** | 5阶段流程 | ✅ 新增 | 标准化流程 |
| **dependency_manager.py** | 依赖管理 | ✅ 新增 | 伏笔追踪 |
| **incremental_sync.py** | 增量同步 | ✅ 新增 | 智能同步 |
| agent_base.py | Agent基类 | ✅ 保留 | 基础框架 |
| agent_dispatcher.py | Agent调度 | ✅ 更新 | 支持动态分配 |
| agent_executor.py | Agent执行 | ✅ 更新 | 支持并行 |
| bible_evolution.py | Bible演化 | ✅ 保留 | 设定管理 |
| command_executor.py | 命令执行 | ✅ 更新 | 新增命令 |
| data_persistence.py | 数据持久化 | ⚠️ 待更新 | 需集成GitHub |
| decomposer.py | 章节分解 | ✅ 保留 | 大纲生成 |
| iterative_generator.py | 迭代生成 | ✅ 保留 | 质量优化 |
| parallel_generator.py | 并行生成器 | ⚠️ 废弃 | 被parallel_coordinator替代 |
| project_manager.py | 项目管理 | ✅ 保留 | 项目组织 |
| scene_analyzer.py | 场景分析 | ✅ 保留 | 场景识别 |
| stream_integrator.py | Stream集成 | ⚠️ 废弃 | 被ultimate_stream_integrator替代 |
| ultimate_stream_integrator.py | 终极Stream集成 | ✅ 保留 | 8-Stream核心 |
| global_optimizer.py | 全局优化 | ✅ 保留 | 质量控制 |
| context_sync.py | 上下文同步 | ⚠️ 待更新 | 需集成Firewall |

### Stream实现 (src/streams/)
**状态**: ✅ 8个Stream已实现

- character_psychology.py - 角色心理
- narrative_structure.py - 叙事结构
- world_building.py - 世界构建
- prose_craft.py - 文笔工艺
- continuity_guard.py - 连贯性
- foreshadowing.py - 伏笔管理
- dialogue_master.py - 对话艺术
- emotion_weaver.py - 情感编织

### 其他模块
- **src/agents/** - Agent实现
- **src/commands/** - 命令处理
- **src/config/** - 配置管理
- **src/utils/** - 工具函数
- **src/validation/** - 验证逻辑
- **src/optimization/** - 优化算法
- **src/continuity/** - 连贯性检查

## 📚 文档目录 (docs/)

| 文件 | 说明 | 更新频率 |
|-----|------|---------|
| index.md | 文档索引 | 按需 |
| MAINTENANCE.md | 维护指南 | 季度 |
| COMMANDS.md | 命令手册 | 新增命令时 |
| API-REFERENCE.md | API文档 | API变更时 |
| AGENTS.md | Agent说明 | Agent变更时 |
| DIRECTORY-STRUCTURE.md | 本文档 | 结构变更时 |

**待创建**:
- TROUBLESHOOTING.md - 故障排除
- PERFORMANCE.md - 性能报告
- TESTING.md - 测试指南
- modules/*.md - 模块文档

## 🗃️ 归档目录 (.claude/archives/)

**已统一合并**（原archived/已合并）

```
.claude/archives/
├── analysis/              # CCPM分析文档 ✅
├── status/               # 项目状态文档 ✅
├── outdated/             # 过时文件 ✅
│   ├── PROJECT-STRUCTURE.md
│   ├── QUICK-START-OLD.md
│   ├── series_bible_template.yaml
│   ├── IMPLEMENTATION-TRACKER.yaml
│   └── test_integration.py
├── implementation/       # 实现记录
├── implementation-complete/ # 完整实现
├── planning/             # 规划文档
├── reviews/              # 审查记录
├── docs/                 # 旧文档
├── old-structure/        # 旧结构
├── v1.0/                # v1.0版本
├── v1.0-original/       # v1.0原始
├── v2.0/                # v2.0版本
├── deprecated/          # 废弃功能
├── experiments/         # 实验功能
└── README.md           # 归档说明
```

## 💾 数据目录 (data/)

```
data/
├── bible_templates/     # Bible模板
├── bibles/             # 生成的Bible
├── chapters/           # 章节内容
├── completed/          # 完成作品
├── context/            # 上下文缓存
├── logs/               # 运行日志
├── memory/             # 记忆存储
├── projects/           # 项目数据
├── tasks/              # 任务队列
└── workspace/          # 工作空间
```

## 🔧 Claude配置 (.claude/)

```
.claude/
├── agents/             # 29个Agent定义
├── commands/           # 15个命令定义
├── books/              # 示例小说
├── context/            # 上下文配置
├── docs/              
│   └── ARCHITECTURE.md # 技术架构
└── README.md          # Claude说明
```

## 🧪 测试目录 (tests/)

**当前状态**: ⚠️ 需要更新

```
tests/
├── test_project_manager.py    # 项目管理测试
├── test_stream_integration.py # Stream集成测试
├── test_stream_simple.py      # Stream简单测试
└── test_system.py             # 系统测试
```

**需要添加**:
- test_context_firewall.py
- test_github_integration.py
- test_parallel_coordinator.py
- test_dependency_manager.py
- integration/ (集成测试)
- e2e/ (端到端测试)

## 📊 文件统计

| 目录 | 文件数 | 状态 | 说明 |
|------|--------|------|------|
| src/core/ | 25 | ⚠️ | 9个新增，部分待更新 |
| src/streams/ | 8 | ✅ | 全部实现 |
| docs/ | 6 | 🚧 | 需要补充更多文档 |
| tests/ | 4 | ⚠️ | 需要添加新功能测试 |
| .claude/archives/ | 15+ | ✅ | 已整理归档 |

## 🔄 需要的操作

### 立即执行
1. ✅ 合并archived到archives（已完成）
2. ✅ 整理归档文件（已完成）
3. ⚠️ 更新过时的core模块
4. ⚠️ 创建缺失的测试文件

### 后续计划
1. 创建缺失的文档
2. 更新测试覆盖
3. 清理废弃代码
4. 优化目录结构

## ⚠️ 注意事项

1. **废弃文件处理**
   - parallel_generator.py → 使用parallel_coordinator.py
   - stream_integrator.py → 使用ultimate_stream_integrator.py
   - data_persistence.py → 需要集成github_integration.py

2. **命名一致性**
   - 使用snake_case命名Python文件
   - 使用UPPER-CASE命名Markdown文档
   - 模块名与功能对应

3. **版本控制**
   - 重要变更前创建备份
   - 使用Git标签标记版本
   - 保持.claude/archives/整洁有序

---

*最后更新: 2025-01-30*  
*维护者: NOVELSYS-SWARM团队*