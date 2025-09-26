# 测试指南

> NOVELSYS-SWARM 2.5 测试策略和执行指南  
> Version: 2.5.0 | Updated: 2025-01-30

## 📋 目录

- [测试架构](#测试架构)
- [测试分类](#测试分类)
- [运行测试](#运行测试)
- [编写测试](#编写测试)
- [测试覆盖率](#测试覆盖率)
- [持续集成](#持续集成)

## 🏗️ 测试架构

### 测试层级

```
测试金字塔
    ╱╲
   ╱E2E╲      (5%) - 端到端测试
  ╱──────╲
 ╱集成测试╲    (15%) - 模块集成
╱──────────╲
╱ 单元测试 ╲  (80%) - 函数级测试
──────────────
```

### 测试目录结构

```
tests/
├── unit/                 # 单元测试
│   ├── test_context_firewall.py
│   ├── test_github_integration.py
│   ├── test_parallel_coordinator.py
│   └── test_dependency_manager.py
├── integration/         # 集成测试
│   └── test_full_workflow.py
├── e2e/                # 端到端测试
│   └── test_novel_generation.py
├── fixtures/           # 测试固件
├── mocks/             # 模拟对象
└── conftest.py        # pytest配置
```

## 📊 测试分类

### 1. 单元测试

测试单个函数或类的功能。

**核心模块测试**:
- ✅ `test_context_firewall.py` - Context防火墙测试
- ✅ `test_github_integration.py` - GitHub集成测试
- ✅ `test_parallel_coordinator.py` - 并行协调器测试
- ✅ `test_dependency_manager.py` - 依赖管理测试

**测试内容**:
- 正常路径
- 边界条件
- 错误处理
- 性能要求

### 2. 集成测试

测试多个模块的协作。

**工作流测试**:
- ✅ `test_full_workflow.py` - 完整工作流测试
- 5阶段流程测试
- 依赖驱动执行测试
- GitHub持久化测试

### 3. 端到端测试

测试完整的用户场景。

**场景测试**:
- 小说创建到导出
- 故障恢复流程
- 并行生成性能

## 🚀 运行测试

### 运行所有测试

```bash
# 基础运行
pytest

# 详细输出
pytest -v

# 显示打印输出
pytest -s

# 并行运行
pytest -n auto
```

### 运行特定测试

```bash
# 运行单个文件
pytest tests/test_context_firewall.py

# 运行单个测试
pytest tests/test_context_firewall.py::TestContextFirewall::test_filter_agent_response

# 运行某类测试
pytest tests/unit/
pytest tests/integration/
```

### 运行带标记的测试

```bash
# 只运行快速测试
pytest -m "not slow"

# 只运行异步测试
pytest -m asyncio

# 跳过需要网络的测试
pytest -m "not network"
```

### 测试覆盖率

```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 显示未覆盖的行
pytest --cov=src --cov-report=term-missing

# 设置覆盖率阈值
pytest --cov=src --cov-fail-under=80
```

## ✍️ 编写测试

### 测试命名规范

**Test file naming specialist:**
• Use pattern: `test_<module_name>.py`
• Example: `test_context_firewall.py`

**Test class naming specialist:**
• Use pattern: `class Test<ClassName>:`
• Example: `class TestContextFirewall:`

**Test method naming specialist:**
1. Use descriptive pattern: `test_<what_is_being_tested>()`
2. Use scenario pattern: `test_<method>_<scenario>_<expected_result>()`
3. Examples:
   • `test_filter_agent_response()`
   • `test_execute_chapter_with_valid_data_returns_result()`

### 测试结构 (AAA模式)

**AAA pattern test structure specialist:**
1. **Arrange (准备)**: Set up test data and dependencies
   • Create ContextFirewall instance
   • Prepare test data dictionary with "content": "test"
   
2. **Act (执行)**: Execute the function being tested
   • Call firewall.filter_response() with test data
   • Store the result
   
3. **Assert (断言)**: Verify expected outcomes
   • Confirm result is not None
   • Verify "summary" key exists in result

### 使用Fixtures

**Pytest fixture specialist:**
1. Import pytest module
2. Create coordinator fixture:
   • Add @pytest.fixture decorator
   • Define function that creates and returns NovelParallelCoordinator instance
   • Add docstring: "创建协调器实例"

**Fixture-based test specialist:**
1. Create test function accepting coordinator parameter
2. Execute coordinator.execute_chapter() with parameters (1, "outline", {})
3. Assert result is not None
4. Add docstring: "使用fixture的测试"

### 异步测试

**Async test specialist:**
1. Import required modules (pytest, asyncio)
2. Create async test function:
   • Add @pytest.mark.asyncio decorator
   • Define async function with "test_" prefix
   • Add docstring: "异步函数测试"
3. Execute async operation:
   • Await async_function() call
   • Store result
4. Assert result is not None

### Mock使用

**Mock testing specialist:**
1. Import Mock and patch from unittest.mock
2. Create mock test function:
   • Add docstring: "使用Mock的测试"
3. Set up patch context:
   • Use patch('module.function') as mock_func
   • Set mock_func.return_value to "mocked"
4. Execute test:
   • Call function_under_test()
   • Store result
5. Verify behavior:
   • Assert result equals "expected"
   • Assert mock_func.assert_called_once()

## 📈 测试覆盖率

### 当前覆盖率目标

| 模块 | 目标 | 当前 | 状态 |
|-----|------|------|------|
| core/context_firewall | 90% | 95% | ✅ |
| core/github_integration | 85% | 88% | ✅ |
| core/parallel_coordinator | 85% | 87% | ✅ |
| core/dependency_manager | 90% | 92% | ✅ |
| streams/* | 80% | 75% | ⚠️ |
| agents/* | 75% | 70% | ⚠️ |
| **总体** | **80%** | **82%** | ✅ |

### 覆盖率报告

```bash
# 生成HTML报告
pytest --cov=src --cov-report=html
# 打开 htmlcov/index.html

# 生成XML报告（用于CI）
pytest --cov=src --cov-report=xml
```

## 🔄 持续集成

### GitHub Actions配置

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

### 测试环境矩阵

| Python | OS | 状态 |
|--------|-----|------|
| 3.8 | Ubuntu | ✅ |
| 3.9 | Ubuntu | ✅ |
| 3.10 | Ubuntu | ✅ |
| 3.9 | Windows | ✅ |
| 3.9 | macOS | ✅ |

## 🎯 测试最佳实践

### 1. 测试独立性

**Independent test specialist:**

**First independent test:**
1. Create new MyClass instance
2. Call obj.method()
3. Assert result equals expected value

**Second independent test:**
1. Create fresh MyClass instance (new instance, not shared)
2. Call obj.other_method()
3. Assert result equals expected value

**Key principle**: Each test creates its own objects to ensure complete isolation

### 2. 明确的断言

**Clear assertion specialist:**

**Good practices:**
• Assert specific values: response.status_code == 200
• Assert absence of errors: "error" not in response.json()

**Avoid:**
• Vague assertions like "assert response" (太模糊)
• Use specific, meaningful assertions that clearly indicate what is being tested

### 3. 测试数据管理

**Test data fixture specialist:**
1. Create sample_bible fixture:
   • Add @pytest.fixture decorator
   • Return dictionary with test data:
     - "title": "测试小说"
     - "genre": "科幻"
     - "characters": ["A", "B", "C"]

**Data-driven test specialist:**
1. Accept sample_bible fixture as parameter
2. Call process_bible() with sample_bible data
3. Assert result is not None

### 4. 参数化测试

**Parametrized test specialist:**
1. Add @pytest.mark.parametrize decorator with:
   • Parameter names: "input,expected"
   • Test cases list:
     - (1, "one")
     - (2, "two")
     - (3, "three")
2. Create test function accepting input and expected parameters
3. Assert number_to_word(input) equals expected value

**Result**: This will run 3 separate test cases automatically

## 🐛 调试测试

### 使用pdb调试

**Debug test specialist:**
1. Create test function for debugging
2. Add debugging breakpoint:
   • Import pdb module
   • Call pdb.set_trace() to start debugger
3. Execute the function under test
4. Assert result equals expected value

**Usage**: Test will pause at breakpoint for interactive debugging

### 查看详细失败信息

```bash
# 显示完整的断言失败信息
pytest --tb=long

# 显示本地变量
pytest --showlocals

# 失败时进入pdb
pytest --pdb
```

## 📊 性能测试

### 基准测试

**Performance benchmark specialist:**
1. Import pytest module
2. Create benchmark test:
   • Add @pytest.mark.benchmark decorator
   • Accept benchmark fixture parameter
3. Execute benchmarked function:
   • Call benchmark(function_to_test, arg1, arg2)
   • Store result
4. Assert result equals expected value

**Purpose**: Measures function execution time and performance

### 超时测试

**Timeout test specialist:**
1. Add timeout decorator:
   • Use @pytest.mark.timeout(5) for 5-second timeout
2. Create test function
3. Execute potentially slow function:
   • Call slow_function()
   • Store result
4. Assert result is not None

**Behavior**: Test will fail if execution takes longer than specified timeout

## 🔍 测试检查清单

### PR提交前检查

- [ ] 所有测试通过 `pytest`
- [ ] 覆盖率达标 `pytest --cov=src --cov-fail-under=80`
- [ ] 无lint错误 `flake8 src tests`
- [ ] 类型检查通过 `mypy src`
- [ ] 文档更新
- [ ] 新功能有测试
- [ ] 测试有意义的场景

## 🆘 常见问题

### Q: 测试运行很慢？
```bash
# 并行运行
pytest -n auto

# 只运行快速测试
pytest -m "not slow"

# 使用缓存
pytest --cache-show
```

### Q: Mock不生效？

**Mock path troubleshooting specialist:**
• Ensure correct patch path format
• Use full module path: 'src.module.function'
• Avoid shortened path: 'module.function' (incorrect)
• Verify the import path matches where the function is actually used

### Q: 异步测试失败？

**Async test troubleshooting specialist:**
1. Install pytest-asyncio plugin
2. Create async test function:
   • Add @pytest.mark.asyncio decorator
   • Define async function with "test_" prefix
3. Properly await async operations:
   • Use "await" keyword before async_function() call

**Common issue**: Missing @pytest.mark.asyncio decorator or not awaiting async calls

---

*最后更新: 2025-01-30*