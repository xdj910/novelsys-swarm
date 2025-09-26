# NOVELSYS-SWARM 项目结构说明

## 目录组织

```
D:/NOVELSYS-SWARM/
|
+-- .claude/                    # Claude Code 配置和文档系统
|   +-- agents/                 # Agent定义文档
|   |   +-- bible/             # Bible创建相关Agent
|   |   +-- coordination/      # 协调类Agent
|   |   +-- detail/           # 细节处理Agent
|   |   +-- generation/       # 内容生成Agent
|   |   +-- memory/           # 记忆管理Agent
|   |   +-- optimization/     # 优化类Agent
|   |   +-- quality/          # 质量控制Agent
|   |   +-- validation/       # 验证类Agent
|   |
|   +-- commands/              # 自定义命令定义
|   |   +-- novel/            # /novel:* 命令系列
|   |       +-- bible-*.md    # Bible相关命令
|   |       +-- chapter-*.md  # 章节相关命令
|   |       +-- *.md          # 其他命令
|   |
|   +-- context/              # 持久化上下文
|   |   +-- series-bible.md  # 系列Bible
|   |   +-- character-*.md   # 角色档案
|   |   +-- world-*.md       # 世界观设定
|   |
|   +-- books/               # 书籍级管理
|   |   +-- [series-name]/  # 各系列目录
|   |
|   +-- docs/               # 项目文档
|       +-- CCMP-*.md      # CCPM集成文档
|       +-- ERROR-*.md     # 错误恢复文档
|       +-- *.md          # 其他系统文档
|
+-- src/                    # Python实现代码
|   +-- core/              # 核心架构
|   |   +-- agent_base.py  # Agent基类
|   +-- agents/            # Agent实现
|   |   +-- bible_creator.py
|   |   +-- chapter_generator.py
|   +-- commands/          # 命令路由
|   |   +-- command_router.py
|   +-- main.py           # 主程序入口
|
+-- bibles/               # 生成的Bible文件（JSON）
+-- chapters/             # 生成的章节文件（JSON）
+-- archived/             # 归档的旧版本
|
+-- test_system.py        # 系统测试
+-- requirements.txt      # Python依赖
+-- package.json         # 项目配置
+-- start.bat           # Windows启动脚本
+-- start.sh            # Linux/Mac启动脚本
```

## 文件类型说明

### 1. `.claude/` - Claude Code配置
- **用途**: Claude Code的配置、Agent定义、命令定义
- **格式**: Markdown文档，YAML配置
- **特点**: 这是Claude Code理解和执行的"大脑"

### 2. `src/` - Python实现
- **用途**: 实际运行的Python代码
- **格式**: Python源文件
- **特点**: 可执行的系统实现

### 3. `bibles/` 和 `chapters/` - 数据输出
- **用途**: 存储生成的小说内容
- **格式**: JSON文件
- **特点**: 结构化的创作成果

## 工作流程

1. **Claude Code读取**: `.claude/` 目录的配置和Agent定义
2. **Python执行**: `src/` 目录的代码实现功能
3. **数据生成**: 输出到 `bibles/` 和 `chapters/`
4. **上下文持久化**: 更新 `.claude/context/`

## 关键文件

### 配置和文档
- `.claude/commands/novel/*.md` - 命令定义
- `.claude/agents/*/**.md` - Agent定义
- `.claude/context/*.md` - 持久化上下文
- `.claude/docs/*.md` - 系统文档

### 代码实现
- `src/main.py` - 程序入口
- `src/core/agent_base.py` - Agent基础架构
- `src/commands/command_router.py` - 命令路由系统

### 测试和运行
- `test_system.py` - 完整系统测试
- `start.bat/start.sh` - 快速启动脚本

## 使用指南

1. **查看文档**: 进入 `.claude/docs/` 了解系统设计
2. **运行系统**: 执行 `python src/main.py` 或 `start.bat`
3. **测试功能**: 运行 `python test_system.py`
4. **查看Agent**: 浏览 `.claude/agents/` 了解各Agent职责
5. **查看命令**: 浏览 `.claude/commands/novel/` 了解可用命令

## 开发指南

- **添加新Agent**: 
  1. 在 `.claude/agents/` 添加定义文档
  2. 在 `src/agents/` 添加Python实现

- **添加新命令**:
  1. 在 `.claude/commands/novel/` 添加命令定义
  2. 在 `src/commands/command_router.py` 添加路由

- **修改Bible结构**:
  1. 更新 `.claude/context/series-bible.md`
  2. 修改 `src/agents/bible_creator.py`

这样的结构保持了Claude Code的配置系统和Python实现的清晰分离，同时确保两者协同工作。