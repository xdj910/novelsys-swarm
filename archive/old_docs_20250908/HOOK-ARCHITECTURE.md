# Hook系统架构文档 - 项目隔离版

## 核心理念：每本书独立的上下文和学习系统

每本书都是独立的创作项目，应该有自己的：
- 📚 独立的上下文记忆
- 🧠 独立的学习历史
- 📊 独立的质量追踪
- 🎯 独立的写作模式

## 目录结构

```
.claude/
├── hooks/                          # 全局Hook脚本
│   ├── master-hook.sh              # 主分发器
│   ├── subagent-context-enhancer.sh # Subagent上下文增强
│   ├── subagent-output-learner.sh  # Subagent输出学习
│   └── ... (其他7个hooks)
│
├── data/
│   └── projects/
│       ├── Island_Inn_Mysteries/   # 书籍1
│       │   ├── bible.yaml          # 本书的Bible
│       │   ├── chapters/           # 章节内容
│       │   ├── shared/             # 共享资源
│       │   │   └── entity_dictionary.yaml
│       │   │
│       │   ├── context/            # 🆕 本书专属上下文
│       │   │   ├── current_context.md
│       │   │   ├── memory_director.json
│       │   │   ├── memory_scene-generator.json
│       │   │   └── memory_*.json   # 各agent记忆
│       │   │
│       │   ├── learning/           # 🆕 本书专属学习数据
│       │   │   ├── writing_patterns.json
│       │   │   ├── quality_history.json
│       │   │   └── entity_changes.log
│       │   │
│       │   └── logs/               # 🆕 本书专属日志
│       │       └── daily_agent_report_*.md
│       │
│       └── Quantum_Shadows/        # 书籍2
│           ├── bible.yaml
│           ├── chapters/
│           ├── context/            # 独立的上下文
│           ├── learning/           # 独立的学习
│           └── logs/               # 独立的日志
```

## Hook工作流程

### 1. PreToolUse: subagent-context-enhancer.sh

当调用Subagent时：
1. **自动检测当前活动书籍**
2. **加载该书的特定上下文**：
   - 从 `projects/BookName/context/` 读取
   - 包含该书的章节、角色、写作风格
3. **注入该书的历史记忆**：
   - 读取 `memory_${agent_type}.json`
   - 包含该agent在这本书中的工作历史

### 2. PostToolUse: 现有7个Hook

文件写入时触发，都在书籍目录内操作：
- meta-updater.sh → 更新章节元数据
- session-tracker.sh → 记录写作会话
- smart-backup.sh → 智能备份
- 等等...

### 3. SubagentStop: subagent-output-learner.sh

Subagent完成后：
1. **保存到书籍特定的学习目录**：
   - `projects/BookName/learning/`
2. **更新书籍特定的记忆**：
   - `projects/BookName/context/memory_*.json`
3. **生成书籍特定的报告**：
   - `projects/BookName/logs/daily_*.md`

## 优势

### 📚 完全的项目隔离
- 每本书有独立的写作风格学习
- 不同书的质量标准可以不同
- 角色记忆不会混淆

### 🎯 精准的上下文
- Director为《Island Inn》生成悬疑风格
- Director为《Quantum Shadows》生成科幻风格
- 不会混淆不同书的设定

### 💾 持久的项目记忆
- 即使几个月后回来继续写
- 所有上下文和学习都还在
- 可以无缝继续创作

### 🔄 可移植性
- 整个书籍目录可以打包
- 包含所有上下文和学习
- 可以在其他环境继续

## 使用示例

```bash
# 当前活动项目：Island_Inn_Mysteries
# 调用scene-generator

# Hook自动：
1. 读取 Island_Inn_Mysteries/context/memory_scene-generator.json
2. 加载 Island_Inn_Mysteries 的最新章节
3. 使用 Island_Inn_Mysteries 的角色设定
4. 生成符合该书风格的内容
5. 保存学习到 Island_Inn_Mysteries/learning/

# 切换到另一本书：Quantum_Shadows
# 调用同样的scene-generator

# Hook自动：
1. 读取 Quantum_Shadows/context/memory_scene-generator.json
2. 加载 Quantum_Shadows 的最新章节
3. 使用 Quantum_Shadows 的角色设定
4. 生成符合该书风格的内容
5. 保存学习到 Quantum_Shadows/learning/
```

## 配置激活

确保 `.claude/settings.json` 包含：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Task",
      "hooks": [{
        "type": "command",
        "command": "bash .claude/hooks/subagent-context-enhancer.sh"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "bash .claude/hooks/subagent-output-learner.sh"
      }]
    }]
  }
}
```

## 总结

这个架构确保：
- ✅ 每本书都有独立的"大脑"
- ✅ 不同项目之间完全隔离
- ✅ 长期项目的记忆持久化
- ✅ 自动化的上下文管理
- ✅ 智能的模式学习和优化