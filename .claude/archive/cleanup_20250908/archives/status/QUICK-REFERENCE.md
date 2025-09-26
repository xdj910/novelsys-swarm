# NOVELSYS-SWARM 快速参考卡

## 🚀 快速命令

```bash
# 项目管理
/novel:init                        # 初始化系统
/novel:project-new "名称" "类型"    # 创建项目
/novel:status                      # 查看状态

# 内容生成
/novel:bible-create                # 创建Bible
/novel:chapter-start 1             # 生成第1章
/novel:quality-check               # 质量检查
```

## 📊 质量等级选择

| 场景类型 | 推荐配置 | 质量分数 | 时间 | 成本 |
|---------|---------|---------|------|------|
| 草稿 | 4-Stream | 80-85 | 2分钟 | $0.30 |
| 标准 | 8-Stream+1轮 | 88-90 | 4分钟 | $0.60 |
| 精品 | 8-Stream+2轮 | 92-94 | 8分钟 | $1.50 |
| 极致 | 全系统+3轮 | 95-98 | 15分钟 | $3.00 |

## 🎯 Python API

```python
# 基础用法
from src.core.command_executor import CommandExecutor
executor = CommandExecutor()
await executor.execute("chapter-start", ["1"])

# 高级用法
from src.core.agent_orchestrator import AgentOrchestrator
orchestrator = AgentOrchestrator()
result = await orchestrator.execute_chapter_generation(
    chapter_number=1,
    bible=bible_data,
    context=context_data
)

# 数据管理
from src.core.data_persistence import DataManager
manager = DataManager()
bible_id = manager.initialize_project(project_data)
manager.save_chapter_with_context(1, chapter_data)
```

## 📁 关键文件位置

```
代码实现: src/core/
Agent定义: .claude/agents/
命令定义: .claude/commands/
数据存储: data/bibles/
测试文件: test_integration.py
使用示例: examples/quick_start.py
```

## 🔧 常见操作

### 创建新小说项目
```bash
/novel:project-new "星际迷航" "科幻"
/novel:bible-create
/novel:chapter-start 1
```

### 提升章节质量
```python
# 使用迭代优化
from src.core.iterative_generator import IterativeGenerator
generator = IterativeGenerator()
result = await generator.generate_with_iterations(
    scene, context, max_rounds=3
)
```

### 检查项目状态
```python
from src.core.data_persistence import DataManager
manager = DataManager()
status = manager.get_project_status()
print(f"章节数: {status['chapters_count']}")
print(f"总字数: {status['total_words']}")
print(f"平均质量: {status['average_quality']}")
```

## 💡 性能优化技巧

1. **批处理**: 相似场景一起处理
2. **缓存**: Bible和上下文缓存
3. **跳过**: 低重要度场景简化
4. **复用**: 角色模型复用

## WARNING:️ 注意事项

- Claude环境顺序执行
- 高质量需要更多时间
- 定期保存和备份
- 使用context-sync保持一致性

## 📞 获取帮助

- 查看完整文档: [README.md](README.md)
- 运行测试: `python test_integration.py`
- 查看示例: `python examples/quick_start.py`

---
*Version 2.1 | 95%完成度 | 2025-01-30*