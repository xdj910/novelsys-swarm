# NOVELSYS-SWARM 归档文档库

> 历史文档、废弃功能和实验性内容的集中存档
> Version: 3.0 | Updated: 2025-01-06

## 📂 目录结构总览

```
archives/
+-- deprecated-agents/      # 废弃的Agent（功能已整合）
+-- old-python-implementation/  # 旧Python实现（已被Subagent系统替代）
+-- unused-features/        # 未使用的功能
+-- context-firewall-design/   # 上下文防火墙设计文档
+-- outdated/              # 过时文件
+-- analysis/              # CCPM分析文档
+-- status/                # 项目状态历史文档
+-- v1.0-original/         # 1.0版本原始文档
+-- v2.0/                  # 2.0版本文档
```

## 📋 归档内容详情

### 1. 废弃的Agents (deprecated-agents/)

#### narrative-structure-specialist
- **废弃日期**: 2025-01-06
- **原因**: 从未在命令中使用，功能与其他agents重叠
- **功能整合到**:
  - `scene-generator.md` - 章节结构要求（开场钩子、发展、高潮、结尾）
  - `quality-scorer.md` - 叙事结构评分维度（15分）
  - `prose-craft-specialist.md` - 叙事技巧（节奏控制、张力构建）

### 2. 旧Python实现 (old-python-implementation/)

- **归档日期**: 2025-09-03
- **包含文件**:
  - chapter_generator.py - 基础章节生成器
  - enhanced_chapter_generator.py - 增强版生成器
  - smart_chapter_generator.py - 智能生成器
  - validated_chapter_generator.py - 带验证的生成器
  - force_save_generator.py - 强制保存版本

**被替代原因**:
- 硬编码的9步生成流程
- Python脚本依赖
- 缺乏灵活性
- 无法利用Claude Code原生能力

**新系统优势**:
- Subagent系统：38个专门的Markdown定义agents
- Hook系统：自动化流程控制
- 原生集成：直接使用Claude Code的Task工具
- 智能并行：性能优化的Hook执行

### 3. 未使用功能 (unused-features/)

#### redundant-commands/
包含已被更好方案替代的命令：
- 冗余的质量检查命令
- 旧版本的上下文同步命令
- 实验性但未采用的功能

### 4. 上下文防火墙设计 (context-firewall-design/)

早期的上下文隔离设计文档，核心概念已整合到：
- Hook系统的上下文管理
- 项目级context目录结构
- entity_dictionary的命名空间隔离

### 5. 过时文件 (outdated/)

- **IMPLEMENTATION-TRACKER.yaml** - 旧的实现跟踪文件
- **test_integration.py** - 旧的集成测试
- **series_bible_template.yaml** - 被新的bible-architect替代

### 6. CCPM分析文档 (analysis/)

从CCPM项目学习的分析文档：
- **CCPM-VS-NOVELSYS-CONTEXT-ANALYSIS.md** - 上下文管理对比分析
- **CCPM-DEEP-ANALYSIS.md** - 深度技术分析
- **CCPM-COMPLETE-TECHNICAL-DOCUMENTATION.md** - 完整技术文档

关键学习点已应用到：
- 30分钟验证循环
- 5阶段质量门控
- 并行执行优化

### 7. 项目状态文档 (status/)

- **PROJECT-STATUS-FINAL.md** - 最终项目状态
- **QUICK-REFERENCE.md** - 快速参考指南

### 8. 版本历史 (v1.0-original/, v2.0/)

#### v1.0 特点
- 线性9步流程
- 基础Agent系统
- 90分质量标准

#### v2.0 升级
- Director-Stream架构
- 4-Stream并行执行
- 95分质量标准
- CCPM验证循环集成

## 🔍 查找指南

| 寻找内容 | 查看位置 |
|---------|---------|
| 废弃的Agent代码 | deprecated-agents/ |
| Python旧代码 | old-python-implementation/ |
| 设计文档 | context-firewall-design/ |
| 技术分析 | analysis/ |
| 版本差异 | v1.0-original/ vs v2.0/ |

## 📝 归档原则

1. **保留价值内容**: 有用的概念整合到活跃代码中
2. **记录废弃原因**: 明确为什么某功能被废弃
3. **指明替代方案**: 说明新系统如何替代旧功能
4. **保持可追溯性**: 保留历史文件供参考

## WARNING:️ 注意事项

- 归档文件仅供历史参考，不应在生产中使用
- 新功能开发应基于当前活跃的系统
- 如需恢复某功能，应先评估其必要性并进行现代化改造

---

*最后更新: 2025-01-06 | 维护者: Claude Code System*