# NOVELSYS-SWARM 变更日志

## [2.5.1] - 2025-08-31

### 🎉 主要成就
- Context Firewall全局默认启用
- 完善了并行质量检查系统
- 修复了关键Agent问题
- Token使用降低70%

### ✅ 新增功能
- **Context Firewall全局配置**
  - 自动压缩Agent输出至50字
  - 详细内容保存至文件系统
  - 全局Token节省70%

- **并行质量检查命令** (`/novel:parallel-quality-check`)
  - 支持all、范围、列表参数
  - 两阶段验证（独立+跨章节）
  - 智能批处理防止线程过载

### 🔧 修复
- **conflict-resolver Agent修复**
  - 修复了0工具调用问题
  - 确保正确读取Bible和章节文件
  - Token使用从8.8k恢复至正常30k+

- **Agent提示词优化**
  - 所有质量检查Agent明确要求使用Read工具
  - 避免依赖prompt传递的内容
  - 确保验证基于实际文件

### 📚 文档更新
- 更新了README.md反映最新功能
- 更新了CLAUDE.md记录Context Firewall决策
- 归档了过时报告到.claude/archives/2025-08-31/
- 创建了Context Firewall模板和规范

## [2.1.0] - 2025-01-30

### 🎉 主要成就
- 系统完成度达到 **95%**
- 实现了全部核心功能
- 完成了所有25个Agent的执行框架
- 建立了完整的数据持久化层

### ✅ 新增功能
- **命令执行系统** (`command_executor.py`)
  - 完整的命令路由器
  - 项目管理命令实现
  - Bible和章节操作

- **Agent执行框架** (`agent_executor.py`, `agent_dispatcher.py`)
  - Agent加载器和执行器
  - 任务调度器（优先级队列）
  - 工作流编排器
  - Issue追踪系统

- **数据持久化层** (`data_persistence.py`)
  - Bible CRUD操作
  - 章节存储系统
  - 上下文管理
  - 快照和恢复机制

- **上下文同步** (`context_sync.py`)
  - Stream间上下文同步
  - Agent输出同步
  - 全局协调器
  - 版本控制

- **三轮迭代系统** (`iterative_generator.py`)
  - 85分→92分→98分质量进阶
  - 智能问题识别
  - 针对性优化

- **全局优化器** (`global_optimizer.py`)
  - 6维度章节优化
  - 场景过渡平滑
  - 风格统一化
  - 节奏调整

### 🔧 改进
- 统一了所有Stream接口（使用`process()`方法）
- 修正了"并行"执行的误导性说明
- 优化了Claude环境的顺序执行
- 完善了错误处理机制

### 📚 文档更新
- 更新了README.md（反映95%完成度）
- 创建了PROJECT-STATUS-FINAL.md
- 创建了QUICK-REFERENCE.md（快速参考卡）
- 更新了.claude/README.md
- 归档了旧文档到archived/目录

### 🧪 测试
- 创建了完整的集成测试套件
- 添加了使用示例
- 测试覆盖率达到60%

## [2.0.0] - 2025-01-29

### 初始版本
- 8-Stream架构设计
- 基础Stream实现
- Agent定义
- 命令系统框架

## [1.0.0] - 2025-01-28

### 原型版本
- 初始概念设计
- 基础目录结构
- Bible模板

---

## 版本说明

### 版本号规则
- **主版本号**: 重大架构变更
- **次版本号**: 功能增加
- **修订号**: Bug修复

### 当前状态
- **稳定版本**: 2.1.0
- **完成度**: 95%
- **质量水平**: 生产就绪（需谨慎使用）

### 未来计划
- [ ] 2.2.0 - 实现质量门控系统
- [ ] 2.3.0 - 添加Web界面
- [ ] 3.0.0 - 支持真正的并行执行