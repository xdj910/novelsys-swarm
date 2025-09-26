# 贡献指南

> 欢迎为NOVELSYS-SWARM贡献代码！  
> Version: 2.5.0 | Updated: 2025-01-30

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [文档要求](#文档要求)
- [测试要求](#测试要求)
- [审核流程](#审核流程)

## 🤝 行为准则

我们致力于提供友好、安全、欢迎的环境。所有参与者都应该：

- ✅ 使用友好和包容的语言
- ✅ 尊重不同的观点和经验
- ✅ 优雅地接受建设性批评
- ✅ 关注对社区最有利的事情
- ✅ 对其他社区成员表示同情

## 🚀 如何贡献

### 1. 报告Bug

创建Issue时请包含：
- 问题的清晰描述
- 复现步骤
- 期望行为
- 实际行为
- 系统环境信息
- 相关日志或截图

### 2. 建议新功能

- 先搜索是否已有类似建议
- 创建详细的功能提案
- 说明使用场景和价值
- 考虑实现复杂度

### 3. 提交代码

#### 首次贡献
```bash
# 1. Fork项目
# 2. 克隆你的Fork
git clone https://github.com/your-username/NOVELSYS-SWARM.git
cd NOVELSYS-SWARM

# 3. 添加上游仓库
git remote add upstream https://github.com/original/NOVELSYS-SWARM.git

# 4. 创建开发分支
git checkout -b feature/your-feature-name
```

#### 开发流程
```bash
# 1. 保持与上游同步
git fetch upstream
git checkout main
git merge upstream/main

# 2. 创建功能分支
git checkout -b feature/your-feature

# 3. 进行开发...

# 4. 提交更改
git add .
git commit -m "feat: add amazing feature"

# 5. 推送到你的Fork
git push origin feature/your-feature

# 6. 创建Pull Request
```

## 📝 代码规范

### Python代码规范

**NovelGenerator specialist:**
1. Follow PEP 8 style guidelines strictly
2. Import required type hints: Dict, List, Optional
3. Define class attributes:
   - config: Configuration dictionary
   - agents: List of Agent instances
4. Initialize generator with configuration:
   - Accept config dictionary containing all necessary parameters
   - Create empty agents list for later population
5. Implement chapter generation function:
   - Accept chapter number, outline, and optional bible
   - Validate chapter number (must be >= 1)
   - Raise ValueError for invalid chapter numbers
   - Process generation logic
   - Return dictionary containing chapter content
6. Include comprehensive docstrings for all methods
7. Use type hints for all parameters and return values

### 命名规范

| 类型 | 规范 | 示例 |
|-----|------|------|
| 类名 | PascalCase | `NovelGenerator` |
| 函数名 | snake_case | `generate_chapter` |
| 常量 | UPPER_SNAKE_CASE | `MAX_AGENTS` |
| 私有成员 | 前缀下划线 | `_internal_state` |
| 文件名 | snake_case | `context_firewall.py` |

### 目录结构

```
src/
├── core/           # 核心模块
│   ├── __init__.py
│   └── *.py       # 模块文件
├── streams/        # Stream实现
├── agents/         # Agent实现
├── utils/          # 工具函数
└── tests/          # 测试文件
```

## 📋 提交规范

### Commit Message格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

| Type | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | `feat(agent): add emotion analyzer` |
| fix | 修复Bug | `fix(sync): resolve GitHub sync issue` |
| docs | 文档更新 | `docs(readme): update installation guide` |
| style | 代码格式 | `style: format with black` |
| refactor | 重构 | `refactor(core): simplify parallel logic` |
| perf | 性能优化 | `perf: reduce token usage by 50%` |
| test | 测试 | `test: add unit tests for firewall` |
| chore | 构建/工具 | `chore: update dependencies` |

### 示例

```bash
git commit -m "feat(parallel): implement 8-stream architecture

- Add parallel coordinator for concurrent execution
- Implement stream isolation with context firewall
- Support dynamic agent allocation

Closes #123"
```

## 📚 文档要求

### 代码必须包含

1. **类文档字符串**
   - 类的用途说明
   - 主要属性说明
   - 使用示例（复杂类）

2. **函数文档字符串**
   - 函数功能说明
   - 参数说明（类型和用途）
   - 返回值说明
   - 异常说明（如果有）

3. **模块文档字符串**
   - 模块功能概述
   - 主要类和函数列表
   - 使用示例

### 文档更新

修改代码时必须同步更新：
- 相关的.md文档
- API文档
- 命令说明
- 配置示例

## 🧪 测试要求

### 测试覆盖

- 核心功能测试覆盖率 > 80%
- 所有公共API必须有测试
- 边界条件必须测试
- 错误处理必须测试

### 测试结构

**TestNovelGenerator specialist:**
1. Import testing framework: pytest and Mock, patch from unittest.mock
2. Create test fixture for generator:
   - Configure test environment with {"test": True}
   - Return NovelGenerator instance for testing
3. Test successful chapter generation:
   - Call generate_chapter with valid parameters (1, "test outline")
   - Assert result status equals "success"
   - Verify "content" key exists in result
4. Test invalid chapter number handling:
   - Call generate_chapter with invalid number (0)
   - Expect ValueError to be raised
   - Use pytest.raises context manager
5. Test GitHub synchronization with mocking:
   - Mock src.core.github_integration.GitHubAPI
   - Configure mock to return True for create_issue
   - Call sync_to_github method
   - Assert result is True
   - Verify create_issue was called exactly once
6. Include descriptive docstrings for all test methods

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/test_core.py

# 运行并显示覆盖率
pytest --cov=src --cov-report=html

# 运行并行测试
pytest -n auto
```

## 🔍 审核流程

### PR要求

1. **代码质量**
   - 通过所有测试
   - 符合代码规范
   - 无明显性能问题
   - 有适当的错误处理

2. **文档完整**
   - 代码有充分注释
   - 更新相关文档
   - 包含使用示例

3. **测试充分**
   - 新功能有测试
   - 测试覆盖边界情况
   - 测试可重复执行

### 审核检查清单

- [ ] 代码符合项目规范
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] 没有破坏性变更
- [ ] commit message规范
- [ ] 没有包含敏感信息
- [ ] 性能影响可接受
- [ ] 向后兼容（或有迁移方案）

### 合并策略

- 小改动：Squash and merge
- 功能分支：Create a merge commit
- 紧急修复：可以直接合并

## 🎯 贡献优先级

### 高优先级
- 🔴 安全漏洞修复
- 🔴 数据丢失问题
- 🔴 系统崩溃问题

### 中优先级
- 🟡 性能优化
- 🟡 新功能开发
- 🟡 用户体验改进

### 低优先级
- 🟢 代码重构
- 🟢 文档改进
- 🟢 测试补充

## 💡 开发技巧

### 本地开发环境

```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装pre-commit hooks
pre-commit install

# 运行代码检查
black src/
flake8 src/
mypy src/
```

### 调试技巧

**Debugging specialist:**
1. Use proper logging instead of print statements:
   - Import logging module
   - Create logger with __name__ identifier
   - Log debug information with chapter processing details
2. Implement breakpoint debugging:
   - Import pdb module
   - Set trace point at critical execution locations
   - Use pdb.set_trace() for interactive debugging
3. Perform performance analysis:
   - Import cProfile module
   - Profile specific function calls like generate_chapter
   - Analyze execution time and resource usage
4. Return diagnostic information for troubleshooting

## 📮 获取帮助

- 查看[文档索引](docs/index.md)
- 在[Issues](https://github.com/yourusername/NOVELSYS-SWARM/issues)中提问
- 加入[Discord社区](https://discord.gg/novelsys)
- 发送邮件至: dev@novelsys-swarm.io

## 🙏 致谢

感谢所有贡献者的努力！你们的贡献使NOVELSYS-SWARM变得更好。

特别感谢：
- 所有提交PR的开发者
- 报告问题的用户
- 提供建议的社区成员
- 编写文档的志愿者

---

*最后更新: 2025-01-30*