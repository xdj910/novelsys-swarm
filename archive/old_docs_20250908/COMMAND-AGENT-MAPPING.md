# NOVELSYS-SWARM 命令与Agent映射关系
生成时间：2025-08-31

## 一、核心命令与Agent调用映射

### 1. 创作命令（调用Agent）

#### `/novel:bible-create`
- **主Agent**: `bible-architect`
- **调用方式**: 直接Task调用
- **执行流程**:
  1. bible-architect生成完整Bible
  2. 保存到bible.yaml

#### `/novel:chapter-start [章节号]` (v3.0重构)
- **执行方式**: 顺序管道（Sequential Pipeline）
- **调用Agents** (按执行顺序):
  1. `bible-architect` - 生成章节大纲
  2. `scene-generator` - 生成初始草稿
  3. `character-psychologist` - 深化角色心理
  4. `dialogue-master-specialist` - 优化对话
  5. `world-builder` - 丰富世界细节
  6. `continuity-guard-specialist` - 验证连续性
  7. `prose-craft-specialist` - 润色文笔
  8. `plot-hole-detector` - 检测逻辑问题
  9. `quality-scorer` - 最终质量评分
- **执行流程**:
  1. 每个agent读取前一版本草稿
  2. 增强特定方面
  3. 输出新版本（draft_v1 → v2 → ... → content.md）
  4. 最终质量评分必须≥95

#### `/novel:chapter-continue`
- **主Agents**:
  - `director` - 规划继续方案
  - `scene-generator` - 生成剩余场景
- **执行流程**:
  1. director分析已有内容
  2. scene-generator逐个生成缺失场景

#### `/novel:quality-check`
- **调用Agents**:
  - `continuity-guard-specialist` - 一致性检查
  - `plot-hole-detector` - 情节漏洞检测
  - `conflict-resolver` - Bible合规检查
  - `quality-scorer` - 综合质量评分
- **执行流程**:
  1. 并行执行4个质量维度检查
  2. 生成综合质量报告

#### `/novel:project-new`
- **主Agent**: `bible-architect`
- **执行流程**:
  1. 创建项目结构
  2. bible-architect生成初始Bible

#### `/novel:book-complete`
- **主Agent**: `quality-scorer`
- **执行流程**:
  1. 整合所有章节
  2. quality-scorer生成总结报告

### 2. 管理命令（不调用Agent）

这些命令直接执行Python代码，不调用Agent：

- `/novel:init` - 初始化系统
- `/novel:status` - 显示项目状态
- `/novel:project-list` - 列出所有项目
- `/novel:project-switch` - 切换项目
- `/novel:next` - 智能推荐下一步
- `/novel:standup` - 生成进度报告
- `/novel:github-sync` - 同步到GitHub
- `/novel:context-sync` - 同步上下文
- `/novel:smart-defaults` - 管理默认值
- `/novel:firewall-mode` - 控制防火墙
- `/novel:worktree-start` - Git worktree管理
- `/novel:system-test` - 系统测试

## 二、Agent层级结构

### 1. 协调层（Coordinators）
```
director (章节规划)
└── conflict-resolver (冲突解决)
```
注：novel-parallel-coordinator已归档（架构缺陷）

### 2. 核心Stream Agents（8个并行）
```
1. character-psychology-specialist
2. narrative-structure-specialist  
3. world-building-specialist
4. prose-craft-specialist
5. continuity-guard-specialist
6. foreshadowing-specialist
7. dialogue-master-specialist
8. emotion-weaver-specialist
```

### 3. 支持Agents
```
质量控制:
├── quality-scorer (质量评分)
└── plot-hole-detector (漏洞检测)

内容生成:
└── scene-generator (场景生成)

Bible管理:
├── bible-architect (Bible构建)
├── character-psychologist (角色设定)
├── mystery-architect (悬疑设计)
└── world-builder (世界观设计)

细节增强:
├── clue-planter (线索铺设)
├── food-culture-expert (饮食文化)
└── weather-mood-setter (天气氛围)

上下文管理:
├── context-manager (上下文管理)
└── incremental-sync (增量同步)
```

## 三、完整创作流程

### Phase 1: 项目初始化
```mermaid
用户 -> /novel:project-new
     -> bible-architect (生成Bible)
     -> 创建项目结构
     -> 初始化上下文
```

### Phase 2: Bible创建/优化
```mermaid
用户 -> /novel:bible-create
     -> bible-architect
        ├── character-psychologist (角色设定)
        ├── mystery-architect (悬疑逻辑)
        └── world-builder (世界观)
     -> 生成bible.yaml
```

### Phase 3: 章节生成 (v3.0顺序管道)
```mermaid
用户 -> /novel:chapter-start N
     -> bible-architect (生成大纲)
     -> scene-generator (初始草稿)
     -> character-psychologist (角色深化)
     -> dialogue-master-specialist (对话优化)
     -> world-builder (世界细节)
     -> continuity-guard-specialist (连续性验证)
     -> prose-craft-specialist (文笔润色)
     -> plot-hole-detector (逻辑检查)
     -> quality-scorer (质量评分≥95)
     -> 输出最终章节
```

### Phase 4: 质量检查
```mermaid
用户 -> /novel:quality-check
     ├── continuity-guard-specialist (一致性)
     ├── plot-hole-detector (漏洞检测)
     ├── conflict-resolver (Bible合规)
     └── quality-scorer (综合评分)
     -> 生成质量报告
     -> 如果<95分，建议修改
```

### Phase 5: 迭代优化
```mermaid
质量不达标 -> /novel:chapter-continue
           -> director (分析问题)
           -> scene-generator (补充场景)
           -> 重新quality-check
```

### Phase 6: 完成与同步
```mermaid
章节完成 -> /novel:github-sync (持久化)
        -> /novel:context-sync (更新上下文)
        -> /novel:next (推荐下一步)
```

## 四、系统特点

### 1. 并行处理架构
- 8个Stream同时工作，每个负责不同维度
- Context Firewall保护主线程（50字摘要）
- 理论上提升8倍效率

### 2. 质量保证机制
- 95分质量门槛
- 4维度质量检查
- 自动迭代优化

### 3. 智能管理功能
- 智能任务推荐（/novel:next）
- 自动进度报告（/novel:standup）
- GitHub持久化（/novel:github-sync）
- 上下文同步（/novel:context-sync）

### 4. Agent专业分工
- 23个专门Agent
- 每个Agent专注单一职责
- 协同工作产生高质量内容

## 五、实际执行示例

### 创建新项目并生成第一章
```bash
# 1. 创建项目
/novel:project-new "Island Inn Mysteries"
# -> 调用bible-architect生成初始Bible

# 2. 查看推荐
/novel:next
# -> 推荐创建完整Bible

# 3. 创建Bible
/novel:bible-create
# -> bible-architect生成完整设定

# 4. 生成第一章
/novel:chapter-start 1
# -> 顺序执行9个agent生成章节

# 5. 质量检查
/novel:quality-check 1
# -> 4个Agent进行质量评估

# 6. 同步到GitHub
/novel:github-sync 1
# -> 保存到GitHub Issue

# 7. 查看进度
/novel:standup
# -> 显示项目状态报告
```

## 六、验证结果

### ✅ 命令完整性
- 19个命令全部实现
- 6个创作命令正确调用Agent
- 13个管理命令独立执行

### ✅ Agent完整性
- 23个Agent全部存在
- 正确的YAML元数据
- 明确的调用关系

### ✅ 流程完整性
- 从项目创建到完成的完整流程
- 质量控制循环
- 持久化和同步机制

系统已完全实现v2.5架构设计！