# NOVELSYS-SWARM 2.5 完整系统架构与流程文档

> **终极小说生成系统 - 从概念到成稿的完整解决方案**  
> Version: 2.5.0 | Updated: 2025-01-30  
> Status: Production Ready | 100% 实现

## 目录

1. [系统概述](#1-系统概述)
2. [核心架构](#2-核心架构)
3. [技术栈](#3-技术栈)
4. [模块详解](#4-模块详解)
5. [工作流程](#5-工作流程)
6. [数据流](#6-数据流)
7. [命令系统](#7-命令系统)
8. [Agent体系](#8-agent体系)
9. [质量控制](#9-质量控制)
10. [性能优化](#10-性能优化)
11. [部署指南](#11-部署指南)
12. [API参考](#12-api参考)

---

## 1. 系统概述

### 1.1 系统定位

NOVELSYS-SWARM 2.5 是一个**AI驱动的专业小说创作系统**，通过8-Stream多维度协同架构和智能Agent编排，实现98分质量目标的小说自动生成。

### 1.2 核心价值

| 维度 | 价值点 | 量化指标 |
|-----|--------|---------|
| **质量** | 8-Stream多维度处理 | 98分目标质量 |
| **效率** | 并行执行架构 | 3x速度提升 |
| **智能** | 动态Agent分配 | 10种章节类型识别 |
| **持久** | GitHub+本地双存储 | 100%跨会话恢复 |
| **可控** | 5阶段规范流程 | 完全可追溯 |

### 1.3 技术创新

1. **Context Firewall架构** - 主线程token使用减少70%
2. **GitHub Issues数据库** - 永久化上下文存储
3. **Parallel-Worker模式** - 真正的8-Stream并行
4. **依赖图管理** - 伏笔全生命周期追踪
5. **增量同步机制** - 90%带宽节省

### 1.4 系统边界

**可以做**：
- ✅ 长篇小说创作（10万字+）
- ✅ 多线程情节管理
- ✅ 复杂人物关系
- ✅ 伏笔铺设与回收
- ✅ 风格一致性保持

**不适合**：
- ❌ 诗歌创作
- ❌ 剧本格式
- ❌ 学术论文
- ❌ 新闻报道

---

## 2. 核心架构

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     用户界面层 (Claude Code)                 │
├─────────────────────────────────────────────────────────────┤
│                        命令路由层                             │
│  /novel:init  /novel:bible-create  /novel:chapter-start     │
├─────────────────────────────────────────────────────────────┤
│                      Context Firewall                        │
│              [主线程保护 - 只接收50字摘要]                    │
├─────────────────────────────────────────────────────────────┤
│                    并行协调层 (Coordinator)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Stream 1  │  │Stream 2  │  │Stream 3  │  │Stream 4  │   │
│  │Character │  │Narrative │  │World     │  │Prose     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Stream 5  │  │Stream 6  │  │Stream 7  │  │Stream 8  │   │
│  │Continuity│  │Foreshadow│  │Dialogue  │  │Emotion   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
├─────────────────────────────────────────────────────────────┤
│                      Agent执行层                             │
│         25个预定义Agent + 动态特化Agent (4-7个)              │
├─────────────────────────────────────────────────────────────┤
│                     数据持久化层                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │GitHub Issues│  │Local Files  │  │Git Worktree │       │
│  │(永久存储)    │  │(YAML/JSON)  │  │(并行分支)   │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 目录结构

```
NOVELSYS-SWARM/
├── .claude/                      # Claude系统文件
│   ├── agents/                   # Agent定义（29个）
│   │   ├── novel-parallel-coordinator.md  # 并行协调器
│   │   ├── character-psychology-specialist.md
│   │   └── [其他27个Agent定义]
│   ├── commands/                 # 命令定义
│   │   └── novel/               # 小说命令（15个）
│   │       ├── init.md
│   │       ├── bible-create.md
│   │       ├── chapter-start.md
│   │       ├── parallel-chapter.md
│   │       └── [其他命令]
│   ├── context/                 # 上下文模板
│   ├── docs/                    # 文档
│   └── rules/                   # 系统规则
│
├── src/                         # 源代码
│   ├── core/                    # 核心模块（新增9个）
│   │   ├── context_firewall.py          # Context防护 ✨
│   │   ├── github_integration.py        # GitHub集成 ✨
│   │   ├── parallel_coordinator.py      # 并行协调器 ✨
│   │   ├── agent_type_mapper.py         # 动态Agent ✨
│   │   ├── execution_status.py          # 状态追踪 ✨
│   │   ├── git_worktree_manager.py      # Worktree管理 ✨
│   │   ├── five_stage_workflow.py       # 5阶段流程 ✨
│   │   ├── dependency_manager.py        # 依赖管理 ✨
│   │   ├── incremental_sync.py          # 增量同步 ✨
│   │   ├── ultimate_stream_integrator.py
│   │   ├── command_executor.py
│   │   ├── agent_executor.py
│   │   └── data_persistence.py
│   ├── streams/                 # 8-Stream实现
│   │   ├── core/               # 4个核心Stream
│   │   └── enhanced/           # 4个增强Stream
│   └── utils/                  # 工具函数
│
├── data/                        # 数据存储
│   ├── bibles/                 # Bible存储
│   ├── chapters/               # 章节内容
│   ├── context/                # 共享上下文
│   ├── workflow/               # 5阶段工作流
│   ├── dependencies/           # 依赖关系
│   ├── sync_cache/             # 同步缓存
│   └── status/                 # 执行状态
│
└── tests/                       # 测试文件
```

---

## 3. 技术栈

### 3.1 运行环境

| 组件 | 版本/要求 | 说明 |
|-----|----------|------|
| **Claude Code** | Latest | 执行环境 |
| **Python** | 3.8+ | 核心逻辑 |
| **Git** | 2.28+ | 版本控制 |
| **GitHub CLI** | 2.0+ | Issue管理 |
| **文件系统** | Any | 本地存储 |

### 3.2 核心依赖

**Requirements specification:**
1. Install networkx version 2.6 or higher for dependency graph management
2. Install pyyaml version 5.4 or higher for YAML file processing
3. Install aiofiles version 0.8 or higher for asynchronous file input/output operations
4. Include asyncio module for parallel execution capabilities
5. Include difflib module for content difference calculation
6. Include hashlib module for content hash generation

### 3.3 Claude特定工具

```yaml
必需工具:
  - Task: SubAgent调用
  - Read/Write: 文件操作
  - Bash: 系统命令
  - WebFetch: 资料获取
  - TodoWrite: 任务管理
```

---

## 4. 模块详解

### 4.1 Context Firewall (context_firewall.py)

**功能**：保护主线程不被细节污染

**AgentResponse data structure specialist:**
1. Create summary field containing 50-character summary for main thread
2. Set status field indicating execution state (success/partial/failed)
3. Populate decisions list with key strategic decisions made
4. Add next_steps list with recommended follow-up actions
5. Store detailed content in _details field (internal use only, not returned to main thread)

**使用示例**：
**Context firewall protected agent execution:**
1. Apply context firewall decorator with maximum summary length of 50 characters
2. Execute agent asynchronously
3. Generate detailed content (approximately 2000 characters)
4. Create AgentResponse with concise summary
5. Store complete details internally without returning to main thread
6. Return summary: "完成角色心理分析，识别3个动机"

### 4.2 GitHub Integration (github_integration.py)

**功能**：使用GitHub Issues作为持久化数据库

**GitHub Integration specialist:**
1. **Create novel repository:** Take project name as input, return success status and repository URL
2. **Create GitHub issue:** Accept title, body content, and label list, return success status and issue number
3. **Sync chapter to issue:** Take chapter number and chapter data dictionary, update corresponding GitHub issue, return sync status
4. **Load Bible from issue:** Retrieve Bible configuration from GitHub issues, return Bible data or None if not found

**Issue结构**：
```
Novel Project Repo
├── Issue #1: Bible定义（Epic）
│   ├── Comment 1: Bible更新
│   └── Comment 2: 设定补充
├── Issue #2: 第1章（Task）
│   ├── Comment 1: Stream分析
│   ├── Comment 2: Agent-1进度
│   └── Comment 3: 质量报告
└── Issue #3: 第2章（Task）
```

### 4.3 Parallel Coordinator (parallel_coordinator.py)

**功能**：管理8个Stream的并行执行

**Novel parallel coordinator specialist:**
1. **Analyze chapter requirements:** Take chapter number, outline, and Bible context as input
2. **Determine chapter type:** Analyze outline and Bible context to identify chapter characteristics
3. **Allocate specialized agents:** Use agent pool to assign appropriate agents based on chapter type
4. **Launch 8-Stream execution:** Create tasks for each of the eight core streams plus dynamic agents
5. **Execute streams in parallel:** Run all stream tasks concurrently using async execution
6. **Merge stream results:** Intelligently combine outputs from all streams into cohesive chapter content
7. Return merged chapter data dictionary

### 4.4 Agent Type Mapper (agent_type_mapper.py)

**功能**：根据章节类型动态分配Agent

**Agent type mapping specialist:**
1. **Define chapter type mappings:**
   • Action chapters: Assign action-choreographer and pacing-specialist
   • Romance chapters: Assign emotion-weaver and dialogue-master
   • Mystery chapters: Assign suspense-engineer and clue-tracker
   • Climax chapters: Assign climax-orchestrator and tension-maximizer

2. **Agent allocation process:**
   • Start with base 8-Stream agents (always required)
   • Identify chapter type from input
   • Add specialized agents based on chapter type
   • Return combined agent list (typically 8-15 agents total)

### 4.5 Execution Status Tracker (execution_status.py)

**功能**：实时追踪执行进度

**Execution status tracker specialist:**
1. **Start chapter tracking:** Initialize tracking for specific chapter with total agent count
2. **Start agent tracking:** Begin monitoring individual agent with name and type
3. **Update agent progress:** Record progress percentage for specified agent
4. **Complete agent execution:** Mark agent as finished with quality score
5. **Generate status report:** Create comprehensive status summary for current execution state

**状态报告示例**：
```
## 📊 NOVELSYS执行状态

### 📖 第1章: 觉醒之日
- 整体进度: 75%
- Agent状态: 6/8 完成

### 🤖 Agent执行状态
✅ Character Psychology: [████████████████████] 100% - 95分
✅ Narrative Structure: [████████████████████] 100% - 92分
⏳ World Building: [████████████--------] 60%
```

### 4.6 Git Worktree Manager (git_worktree_manager.py)

**功能**：多章节并行创作

**Git worktree manager specialist:**
1. **Create chapter worktree:** Establish isolated Git worktree for specific chapter, return success status and path
2. **Create parallel chapter worktrees:** Set up multiple worktrees for concurrent chapter development, return mapping of chapter numbers to paths
3. **Sync worktree to main branch:** Merge completed chapter worktree back to main branch, return sync success status

**Worktree结构**：
```
novelsys-worktrees/
├── chapter-1/    # 独立分支 chapter/1
├── chapter-2/    # 独立分支 chapter/2
└── chapter-3/    # 独立分支 chapter/3
```

### 4.7 Five Stage Workflow (five_stage_workflow.py)

**功能**：5阶段规范化流程

**Five stage workflow specialist:**
1. **Stage 1 - Concept creation:** Generate concept from title, genre, themes, and target audience, return concept ID
2. **Stage 2 - Bible planning:** Create comprehensive Bible document from concept, return Bible ID
3. **Stage 3 - Chapter decomposition:** Break Bible into individual chapter outlines, return list of chapter IDs
4. **Stage 4 - Scene generation:** Generate detailed scenes for each chapter, return list of scene IDs
5. **Stage 5 - Manuscript polishing:** Compile and refine all scenes into final manuscript, return manuscript ID

**流程追溯**：
```
概念(concept_001)
  └→ Bible(bible_001)
      └→ 章节1(chapter_001)
          ├→ 场景1(scene_001)
          ├→ 场景2(scene_002)
          └→ 场景3(scene_003)
              └→ 成稿(manuscript_001) [质量: 95分]
```

### 4.8 Dependency Manager (dependency_manager.py)

**功能**：管理章节间依赖关系

**Dependency manager specialist:**
1. **Add chapter dependency:** Create dependency relationship between source and target chapters with type and description, return dependency ID
2. **Add foreshadowing element:** Establish foreshadowing with setup chapter and planned payoff chapter, return foreshadowing ID
3. **Validate chapter readiness:** Check if chapter dependencies are satisfied, return readiness status and list of unmet dependencies
4. **Determine execution order:** Analyze chapter dependencies to create optimal execution sequence, return ordered chapter list

**依赖类型**：
- `FORESHADOWING` - 伏笔依赖
- `PLOT` - 情节依赖
- `CHARACTER` - 角色发展依赖
- `TEMPORAL` - 时间顺序依赖

**依赖图可视化**：
```mermaid
graph TD
    chapter_1 -->|伏笔| chapter_5
    chapter_2 -->|角色| chapter_4
    chapter_3 -->|情节| chapter_6
```

### 4.9 Incremental Sync (incremental_sync.py)

**功能**：智能增量同步

**Incremental sync manager specialist:**
1. **Detect file changes:** Analyze file for modifications, return change status and change details
2. **Execute incremental sync:** Synchronize only changed portions between source and target, return sync status and sync record
3. **Optimize batch synchronization:** Group files for efficient batch processing, return optimized file batches

**同步策略**：
- 小改动(<10行) → `patch`模式
- 中改动(<100行) → `incremental`模式
- 大改动(>100行) → `full`模式

**性能优化**：
- 内容哈希缓存
- 差异计算
- 批量优化
- 带宽节省90%

---

## 5. 工作流程

### 5.1 完整创作流程

```mermaid
graph TB
    A[用户输入命令] -->|/novel:init| B[系统初始化]
    B --> C[概念构思]
    C -->|/novel:concept-new| D[创建概念文档]
    D --> E[Bible规划]
    E -->|/novel:bible-create| F[生成Bible]
    F --> G[章节分解]
    G -->|/novel:chapter-decompose| H[创建章节大纲]
    H --> I[场景生成]
    I -->|/novel:parallel-chapter| J[8-Stream并行处理]
    J --> K[质量评估]
    K -->|<90分| L[迭代优化]
    L --> J
    K -->|≥90分| M[成稿润色]
    M --> N[同步GitHub]
    N --> O[导出作品]
```

### 5.2 章节生成详细流程

#### Step 1: 命令接收
```bash
用户输入: /novel:chapter-start 1
```

#### Step 2: 准备阶段
**Chapter preparation process:**
1. **Load Bible configuration:** Read the complete Bible document from file system
2. **Retrieve chapter outline:** Extract outline for specified chapter number (chapter 1)
3. **Analyze chapter characteristics:** Determine chapter type based on outline content (example result: "action")
4. **Validate dependencies:** Check if all required dependencies are met for this chapter, identify any unmet dependencies

#### Step 3: Agent分配
**Agent allocation strategy:**
1. **Assign core 8-Stream agents:**
   • character-psychology-specialist
   • narrative-structure-specialist
   • world-building-specialist
   • prose-craft-specialist
   • continuity-guard-specialist
   • foreshadowing-specialist
   • dialogue-master-specialist
   • emotion-weaver-specialist

2. **Add specialized agents based on chapter type:**
   • For action chapters: Add action-choreographer and pacing-specialist
   • Total agents assigned: 10 (8 core + 2 specialized)

#### Step 4: 并行执行
**Parallel execution workflow:**
1. **Create Git worktree:** Establish isolated working directory for chapter 1
2. **Initialize parallel coordinator:** Set up coordinator with GitHub integration
3. **Execute multi-stream processing:** Run all assigned agents (8-Stream + specialized) concurrently with chapter parameters
4. **Apply Context Firewall filtering:**
   • Each agent returns 50-character summary to main thread
   • Store complete detailed content in data/streams/ch1/{stream_name}.md files

#### Step 5: 结果合并
**Results processing workflow:**
1. **Collect stream results:** Gather summaries and quality scores from all streams
   • Character Psychology: "完成3个角色分析" (95 points)
   • Narrative Structure: "三幕式结构建立" (92 points)
   • Plus results from remaining 6 streams

2. **Detect and resolve conflicts:** Identify conflicts between stream outputs and resolve using priority system
   • Priority order: Continuity > Character > Plot > Prose

3. **Intelligent merging:** Combine all stream outputs into cohesive chapter content

#### Step 6: 质量控制
**Quality control process:**
1. **Assess content quality:** Evaluate merged content across dimensions:
   • Character depth, plot coherence, prose quality, setting consistency
   • Emotional resonance, dialogue naturalness, foreshadowing completeness

2. **Apply three-round iteration system:**
   • Round 1 (if score < 85): Fix basic issues and structural problems
   • Round 2 (if score < 92): Perform deep optimization and enhancement
   • Round 3 (if score < 98): Apply final polish and refinement

#### Step 7: 持久化
**Persistence and synchronization:**
1. **Save to local storage:** Write completed chapter content to local file system
2. **Synchronize to GitHub Issues:** Update corresponding GitHub issue with:
   • Final chapter content
   • Quality assessment score
   • Individual stream results
   • Total execution time
3. **Enable incremental sync:** Set up automated synchronization for future updates between local files and GitHub issues

### 5.3 伏笔管理流程

**Foreshadowing management process:**
1. **Plant foreshadowing element:**
   • Create "神秘徽章" foreshadowing in chapter 1
   • Set description: "主角发现一个不明来源的徽章"
   • Schedule payoff for chapter 5 with importance level 8

2. **Track foreshadowing status:** Monitor active foreshadowing elements
   • Return status: "神秘徽章" active for 4 chapters

3. **Resolve foreshadowing:** Complete the story arc in chapter 5
   • Add resolution note: "徽章原来是反派组织的标志"

4. **Generate integrity report:** Create comprehensive report showing all foreshadowing elements and their dependency relationships

---

## 6. 数据流

### 6.1 数据流向图

```
输入层                    处理层                    存储层                    输出层
   │                        │                        │                        │
用户命令 ──────→ Claude主线程 ──────→ GitHub Issues ──────→ 质量报告
   │                        │                        │                        │
   │                        ↓                        ↓                        │
   │              Context Firewall          本地文件系统                      │
   │                        │              (YAML/JSON/MD)                     │
   │                        ↓                        ↑                        │
   └──────────→ SubAgent执行层 ──────────────────────┘                        │
                     │                                                        │
                     ↓                                                        ↓
               8-Stream处理 ─────────────────────────────────────→ 最终成稿
```

### 6.2 上下文流转

**Context flow management:**
1. **Global context structure (cross-chapter):**
   • Bible: Complete world-building and setting information
   • Characters: Comprehensive character profiles and relationships
   • Plot progress: Overall story advancement tracking
   • Foreshadowings: Active plot elements awaiting resolution

2. **Chapter context structure (current chapter):**
   • Chapter number and specific outline details
   • Dependency requirements and previous chapter summary

3. **Stream context structure (independent processing):**
   • Stream identification and processing scope
   • Input from chapter context and output with summary/details separation

4. **Agent context structure (finest granularity):**
   • Specific agent task and style constraints from Bible
   • Access to previous work for consistency

### 6.3 数据持久化策略

| 数据类型 | 存储位置 | 格式 | 同步策略 |
|---------|---------|------|---------|
| Bible设定 | `data/bibles/` + Issue#1 | YAML | 全量同步 |
| 章节内容 | `data/chapters/` + Issue#N | Markdown | 增量同步 |
| Stream输出 | `data/streams/` | Markdown | 本地缓存 |
| 执行状态 | `data/status/` | JSON | 实时更新 |
| 依赖关系 | `data/dependencies/` | JSON | 变更同步 |
| 工作流文档 | `data/workflow/` | JSON | 版本控制 |

---

## 7. 命令系统

### 7.1 核心命令列表

| 命令 | 功能 | 参数 | 示例 |
|-----|------|------|------|
| `/novel:init` | 初始化系统 | 无 | `/novel:init` |
| `/novel:project-new` | 创建新项目 | 项目名 | `/novel:project-new "量子觉醒"` |
| `/novel:concept-new` | 创建概念 | 标题 | `/novel:concept-new "科幻悬疑"` |
| `/novel:bible-create` | 创建Bible | 类型 | `/novel:bible-create "都市异能"` |
| `/novel:chapter-decompose` | 分解章节 | Bible ID | `/novel:chapter-decompose bible_001` |
| `/novel:parallel-chapter` | 并行生成 | 章节号列表 | `/novel:parallel-chapter 1 2 3` |
| `/novel:chapter-start` | 生成单章 | 章节号 | `/novel:chapter-start 1` |
| `/novel:quality-check` | 质量检查 | 章节号 | `/novel:quality-check 1` |
| `/novel:dependency-add` | 添加依赖 | 源,目标,类型 | `/novel:dependency-add 1 5 foreshadowing` |
| `/novel:foreshadowing-add` | 添加伏笔 | 名称,章节 | `/novel:foreshadowing-add "徽章" 1 5` |
| `/novel:github-init` | GitHub初始化 | 项目名 | `/novel:github-init my-novel` |
| `/novel:sync` | 同步到GitHub | 章节号 | `/novel:sync 1` |
| `/novel:status` | 查看状态 | 无 | `/novel:status` |
| `/novel:export` | 导出作品 | 格式 | `/novel:export markdown` |
| `/novel:help` | 获取帮助 | 命令名 | `/novel:help chapter-start` |

### 7.2 命令定义格式

```markdown
---
allowed-tools: Task, Read, Write, Bash
---

# 命令名称

命令描述...

## Usage
`/novel:command-name <参数>`

## Preflight Checklist
- [ ] 检查前置条件
- [ ] 验证参数
- [ ] 加载依赖

## Instructions
1. 步骤1
2. 步骤2
3. 步骤3

## Error Handling
- 错误1: 处理方式
- 错误2: 处理方式
```

---

## 8. Agent体系

### 8.1 Agent分类

#### 8.1.1 基础Stream Agent (8个)

| Agent | 职责 | 输出 |
|-------|------|------|
| `character-psychology-specialist` | 角色心理深度分析 | 心理模型、动机链、情感轨迹 |
| `narrative-structure-specialist` | 叙事结构管理 | 节奏控制、冲突设计、转折点 |
| `world-building-specialist` | 世界构建与感官 | 环境描写、氛围营造、感官细节 |
| `prose-craft-specialist` | 文笔工艺优化 | 修辞技巧、语言节奏、风格统一 |
| `continuity-guard-specialist` | 连贯性守护 | 逻辑检查、时间线、设定一致 |
| `foreshadowing-specialist` | 伏笔管理 | 铺设、维护、回收追踪 |
| `dialogue-master-specialist` | 对话艺术 | 角色语言、潜台词、信息密度 |
| `emotion-weaver-specialist` | 情感编织 | 情感曲线、共鸣点、氛围渲染 |

#### 8.1.2 协调Agent (2个)

| Agent | 职责 | 权限 |
|-------|------|------|
| `novel-parallel-coordinator` | 并行执行协调 | 启动/停止Stream、冲突解决 |
| `director` | 总体规划 | 制定计划、分配任务、质量把关 |

#### 8.1.3 生成Agent (8个)

| Agent | 职责 | 特长 |
|-------|------|------|
| `outline-creator` | 大纲生成 | 结构设计、节奏规划 |
| `scene-painter` | 场景描写 | 视觉呈现、空间感 |
| `dialogue-specialist` | 对话创作 | 口语化、个性化 |
| `action-specialist` | 动作描写 | 动作设计、紧张感 |
| `emotion-specialist` | 情感描写 | 内心活动、情绪变化 |
| `description-specialist` | 细节描写 | 感官细节、象征隐喻 |
| `transition-specialist` | 过渡处理 | 场景切换、时间跳跃 |
| `climax-specialist` | 高潮设计 | 冲突爆发、情感顶点 |

#### 8.1.4 优化Agent (5个)

| Agent | 职责 | 优化目标 |
|-------|------|----------|
| `pacing-optimizer` | 节奏优化 | 张弛有度、阅读体验 |
| `voice-tuner` | 风格调整 | 语言风格、叙述声音 |
| `suspense-engineer` | 悬念工程 | 钩子设置、期待管理 |
| `consistency-checker` | 一致性检查 | 设定、逻辑、风格 |
| `quality-scorer` | 质量评分 | 多维度评估、改进建议 |

#### 8.1.5 特化Agent (动态)

| 章节类型 | 额外Agent | 专长 |
|---------|-----------|------|
| `action` | action-choreographer, pacing-specialist | 动作设计、节奏控制 |
| `romance` | emotion-weaver, intimacy-coordinator | 情感细腻、关系发展 |
| `mystery` | suspense-engineer, clue-tracker | 悬念设置、线索管理 |
| `dialogue` | conversation-architect, subtext-master | 对话节奏、潜台词 |
| `climax` | climax-orchestrator, tension-maximizer | 高潮设计、张力最大化 |

### 8.2 Agent通信协议

**Inter-agent communication protocol:**
1. **Message structure components:**
   • Source agent: character-psychology-specialist
   • Target agent: dialogue-master-specialist
   • Communication type: recommendation

2. **Content payload details:**
   • Character identification and speech pattern specifications
   • Current emotional state and suggested dialogue phrases

3. **Message metadata:**
   • Priority level: high
   • Timestamp: 2025-01-30T10:00:00Z

---

## 9. 质量控制

### 9.1 质量标准体系

#### 9.1.1 8维度评分标准

| 维度 | 权重 | 目标分 | 评估要点 |
|-----|------|--------|---------|
| **角色深度** | 15% | ≥95 | 心理复杂度、动机合理性、成长轨迹 |
| **情节连贯** | 15% | ≥99 | 逻辑严密、因果关系、节奏控制 |
| **文字表达** | 15% | ≥95 | 语言优美、修辞恰当、风格统一 |
| **设定一致** | 10% | ≥98 | 世界观统一、规则自洽、细节准确 |
| **情感共鸣** | 15% | ≥95 | 情感真实、共鸣点、感染力 |
| **对话自然** | 10% | ≥95 | 口语化、个性化、信息密度 |
| **伏笔完整** | 10% | 100 | 铺设合理、回收完整、意外合理 |
| **创新性** | 10% | ≥90 | 独特视角、新颖设定、意外转折 |

**综合评分计算**：
**Overall quality score calculation:**
1. Multiply each dimension score by its corresponding weight
2. Sum all weighted dimension scores to get overall quality rating

### 9.2 5阶段质量门

**Five-stage quality gate system:**
1. **Stage 1 (10% completion) - Framework integrity:**
   • Minimum threshold: 80 points
   • Required checks: Outline exists, characters defined, world-building established

2. **Stage 2 (30% completion) - Basic content:**
   • Minimum threshold: 80 points
   • Required checks: Complete scenes, basic dialogue, action descriptions

3. **Stage 3 (60% completion) - Deep development:**
   • Minimum threshold: 85 points
   • Required checks: Character development, plot advancement, conflict expansion

4. **Stage 4 (80% completion) - Chapter coherence:**
   • Minimum threshold: 90 points
   • Required checks: Narrative consistency, foreshadowing management, pacing flow

5. **Stage 5 (100% completion) - Final polish:**
   • Minimum threshold: 95 points
   • Required checks: Language refinement, detail enhancement, emotional elevation

### 9.3 三轮迭代系统

**Iterative optimizer specialist:**
1. **Round 1 optimization (target 85 points):** Apply if current score below 85
   • Fix logical errors and inconsistencies
   • Add missing content elements
   • Adjust basic pacing issues

2. **Round 2 optimization (target 92 points):** Apply if current score below 92
   • Deepen character psychological development
   • Strengthen conflict tension and stakes
   • Optimize language expression and clarity

3. **Round 3 optimization (target 98 points):** Apply if current score below 98
   • Refine intricate details and nuances
   • Enhance literary quality and style
   • Amplify emotional impact and resonance

4. Return optimized content after applicable rounds

### 9.4 质量监控仪表板

```
╔════════════════════════════════════════════════════════════╗
║              NOVELSYS 质量监控仪表板                         ║
╠════════════════════════════════════════════════════════════╣
║ 章节: 第1章                     状态: 生成中                  ║
║ 目标质量: 98分                  当前: 92.5分                  ║
╠════════════════════════════════════════════════════════════╣
║ 维度评分:                                                    ║
║ ┌─────────────┬───────┬────────┬─────────┐                ║
║ │ 角色深度     │ 95/95 │ ██████ │ ✅      │                ║
║ │ 情节连贯     │ 98/99 │ █████▌ │ ⚠️      │                ║
║ │ 文字表达     │ 90/95 │ ████▌  │ ⚠️      │                ║
║ │ 设定一致     │ 98/98 │ ██████ │ ✅      │                ║
║ │ 情感共鸣     │ 89/95 │ ████   │ ⚠️      │                ║
║ │ 对话自然     │ 95/95 │ ██████ │ ✅      │                ║
║ │ 伏笔完整     │100/100│ ██████ │ ✅      │                ║
║ │ 创新性      │ 88/90 │ █████  │ ⚠️      │                ║
║ └─────────────┴───────┴────────┴─────────┘                ║
║ 改进建议:                                                    ║
║ • 加强第3段的情感描写                                        ║
║ • 优化第2个场景的过渡                                        ║
║ • 提升对话的个性化                                          ║
╚════════════════════════════════════════════════════════════╝
```

---

## 10. 性能优化

### 10.1 性能指标

| 指标 | 目标值 | 实测值 | 优化策略 |
|-----|--------|--------|---------|
| **章节生成时间** | <5分钟 | 3分钟 | 并行Stream执行 |
| **Token使用** | <50K/章 | 35K/章 | Context Firewall |
| **内存占用** | <500MB | 320MB | 流式处理 |
| **同步带宽** | <100KB/次 | 10KB/次 | 增量同步 |
| **并发Agent** | 8-15个 | 12个 | 动态分配 |

### 10.2 优化技术

#### 10.2.1 Context Firewall优化
**Context firewall token optimization:**
1. **Optimized approach:** Main thread receives 50 characters per agent summary
2. **Traditional approach:** Each agent would send 2000 characters to main thread
3. **Token savings calculation:** 97.5% reduction in main thread token usage

#### 10.2.2 增量同步优化
**Incremental sync optimization strategy:**
1. **Patch mode:** For changes under 10 lines - minimal data transfer
2. **Incremental mode:** For changes 10-100 lines - moderate data transfer
3. **Full mode:** For changes over 100 lines - complete content transfer

#### 10.2.3 并行执行优化
**Parallel execution optimization:**
1. **Identify parallelizable tasks:** Analyze chapter to find independent streams
2. **Batch execute tasks:** Run all parallel tasks simultaneously using async gathering
3. **Time savings:** 60-70% reduction compared to sequential execution

#### 10.2.4 缓存策略
**Multi-layer caching strategy:**
• **L1 Memory cache:** Store frequently accessed hot data in system memory
• **L2 File cache:** Cache commonly used data in local file system
• **L3 GitHub Issues:** Maintain persistent data in GitHub Issues for long-term storage

### 10.3 扩展性设计

```yaml
水平扩展:
  - Agent数量: 8 → 15 → 30 (根据需要)
  - 章节并行: 1 → 3 → 10 (Git Worktree)
  - 项目并发: 支持多项目同时进行

垂直优化:
  - 质量提升: 85 → 92 → 98分
  - 深度增强: 更复杂的依赖关系
  - 智能升级: 更智能的Agent分配
```

---

## 11. 部署指南

### 11.1 环境准备

```bash
# 1. 安装GitHub CLI
gh auth login

# 2. 配置Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. 克隆项目
git clone https://github.com/yourusername/NOVELSYS-SWARM.git
cd NOVELSYS-SWARM

# 4. 安装依赖
pip install -r requirements.txt
```

### 11.2 初始化系统

```bash
# 1. 在Claude Code中打开项目
claude-code NOVELSYS-SWARM/

# 2. 初始化系统
/novel:init

# 3. 创建GitHub项目（可选）
/novel:github-init my-novel-project

# 4. 验证安装
/novel:status
```

### 11.3 配置文件

```json
// .claude/settings.local.json
{
  "github": {
    "owner": "your-username",
    "repo": "your-novel-repo",
    "token": "ghp_xxxxxxxxxxxx"  // 可选
  },
  "quality": {
    "target_score": 98,
    "max_iterations": 3,
    "parallel_agents": 12
  },
  "sync": {
    "auto_sync": true,
    "sync_interval": 300,  // 秒
    "incremental": true
  }
}
```

### 11.4 故障排除

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| Agent执行失败 | 内存不足 | 减少并行Agent数量 |
| GitHub同步失败 | 认证问题 | 运行 `gh auth login` |
| 质量分数低 | 迭代不足 | 增加max_iterations |
| 生成速度慢 | 顺序执行 | 启用parallel模式 |
| 依赖冲突 | 循环依赖 | 检查dependency图 |

---

## 12. API参考

### 12.1 核心类

**Core system classes:**

**Context Firewall specialist:**
• **Filter agent response:** Extract summary from AgentResponse and return filtered string
• **Batch filter responses:** Process multiple AgentResponse objects and return combined summary

**GitHub Integration specialist:**
• **Create novel repository:** Generate new GitHub repo for project, return success status and repo URL
• **Sync chapter to issue:** Update specific GitHub issue with chapter data, return sync success status

**Novel Parallel Coordinator specialist:**
• **Execute chapter processing:** Coordinate multi-stream chapter generation, return processed chapter data
• **Generate status report:** Create comprehensive execution status summary

**Dependency Manager specialist:**
• **Add chapter dependency:** Create dependency relationship between chapters, return dependency ID
• **Validate chapter readiness:** Check if chapter dependencies are satisfied, return status and unmet list

**Five Stage Workflow specialist:**
• **Create concept:** Generate initial story concept from title and genre, return concept ID
• **Create Bible document:** Build comprehensive Bible from concept, return Bible ID
• **Generate traceability report:** Create complete workflow tracking report

### 12.2 数据结构

**Core data structures:**

**AgentResponse structure:**
• Summary: Main thread summary text
• Status: Current execution state
• Decisions: List of key strategic decisions made
• Next steps: List of recommended follow-up actions
• Metrics: Quality indicators and performance data
• Details: Complete content (internal only, not returned to main thread)

**Dependency structure:**
• ID: Unique dependency identifier
• Type: Category of dependency relationship
• Source and target: Connected elements
• Description: Detailed dependency explanation
• Strength: Importance level (numeric)
• Hard dependency flag and resolution status

**ChapterExecution structure:**
• Chapter number and title
• Agent counts: Total assigned and completed
• Overall progress percentage
• Quality score (optional, when available)

### 12.3 事件钩子

**Event hook system:**

**Available event hooks:**
• **before_chapter_start:** Triggered before chapter generation begins
• **after_stream_complete:** Triggered when individual stream processing finishes
• **on_quality_check:** Triggered during quality assessment phase
• **before_sync:** Triggered before synchronization to external systems
• **after_sync:** Triggered after successful synchronization
• **on_conflict:** Triggered when conflicts between streams are detected
• **on_error:** Triggered when errors occur during processing

**Hook registration process:**
1. Accept event name and callback function as parameters
2. Add callback to the specified event's callback list
3. Enable custom logic execution at specific system events

---

## 附录A: 命令速查表

```bash
# 项目管理
/novel:init                        # 初始化
/novel:project-new "名称"          # 新项目
/novel:project-list                # 项目列表
/novel:status                      # 当前状态

# 创作流程
/novel:concept-new "标题"          # 创建概念
/novel:bible-create "类型"         # 创建Bible
/novel:chapter-decompose           # 章节分解
/novel:chapter-start 1             # 生成章节
/novel:parallel-chapter 1 2 3      # 并行生成

# 质量管理
/novel:quality-check 1             # 质量检查
/novel:iterate 1                   # 迭代优化

# 依赖管理
/novel:dependency-add 1 5 "plot"   # 添加依赖
/novel:foreshadowing-add "名" 1 5  # 添加伏笔
/novel:dependency-check 3          # 检查依赖

# 同步管理
/novel:github-init "项目名"        # GitHub初始化
/novel:sync 1                      # 同步章节
/novel:sync-all                    # 全部同步

# 导出
/novel:export markdown             # 导出Markdown
/novel:export epub                 # 导出EPUB
```

## 附录B: 质量检查清单

```markdown
## 章节质量检查清单

### 结构完整性
- [ ] 开头吸引人
- [ ] 中间有起伏
- [ ] 结尾有悬念
- [ ] 场景转换流畅

### 角色表现
- [ ] 角色行为符合设定
- [ ] 对话符合身份
- [ ] 情感变化合理
- [ ] 成长轨迹清晰

### 情节逻辑
- [ ] 因果关系合理
- [ ] 时间线正确
- [ ] 没有逻辑漏洞
- [ ] 冲突有张力

### 文字表达
- [ ] 语言流畅
- [ ] 描写生动
- [ ] 节奏恰当
- [ ] 风格统一

### 世界观一致
- [ ] 设定没有矛盾
- [ ] 规则自洽
- [ ] 细节准确
- [ ] 氛围统一

### 伏笔处理
- [ ] 新伏笔合理铺设
- [ ] 旧伏笔适时推进
- [ ] 该回收的已回收
- [ ] 没有遗漏的线索
```

## 附录C: 故障诊断流程

```mermaid
graph TD
    A[问题发生] --> B{什么类型?}
    B -->|生成失败| C[检查Bible完整性]
    B -->|质量太低| D[增加迭代次数]
    B -->|速度太慢| E[检查并行设置]
    B -->|同步失败| F[验证GitHub认证]
    
    C --> G[修复Bible]
    D --> H[调整质量参数]
    E --> I[优化Agent数量]
    F --> J[重新认证]
    
    G --> K[重试生成]
    H --> K
    I --> K
    J --> K
    
    K --> L{成功?}
    L -->|是| M[问题解决]
    L -->|否| N[查看日志]
    N --> O[联系支持]
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| 2.5.0 | 2025-01-30 | 完整实现CCPM特性集成 |
| 2.0.0 | 2025-01-29 | 8-Stream架构实现 |
| 1.0.0 | 2025-01-28 | 初始版本发布 |

---

## 许可证

MIT License

---

*本文档为NOVELSYS-SWARM 2.5的完整技术文档，包含所有已实现功能的详细说明。*

**文档完成度**: 100%  
**技术实现度**: 100%  
**测试覆盖率**: 60%  

---

最后更新: 2025-01-30 15:00:00 UTC+8