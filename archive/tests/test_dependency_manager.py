"""
Dependency Manager 测试套件
测试依赖图管理和伏笔追踪功能
"""

import pytest
import networkx as nx
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.dependency_manager import (
    DependencyManager,
    Foreshadowing,
    DependencyType,
    ExecutionOrder
)


class TestDependencyManager:
    """测试依赖管理器主类"""
    
    @pytest.fixture
    def manager(self):
        """创建依赖管理器实例"""
        return DependencyManager()
    
    def test_add_simple_dependency(self, manager):
        """测试添加简单依赖"""
        manager.add_dependency(1, 3, DependencyType.PLOT)
        
        assert manager.has_dependency(1, 3)
        assert manager.get_dependency_type(1, 3) == DependencyType.PLOT
        
    def test_add_multiple_dependencies(self, manager):
        """测试添加多个依赖"""
        manager.add_dependency(1, 3, DependencyType.PLOT)
        manager.add_dependency(2, 3, DependencyType.CHARACTER)
        manager.add_dependency(3, 5, DependencyType.SETTING)
        
        # 章节3依赖1和2
        deps_of_3 = manager.get_dependencies(3)
        assert 1 in deps_of_3
        assert 2 in deps_of_3
        
        # 章节5依赖3
        deps_of_5 = manager.get_dependencies(5)
        assert 3 in deps_of_5
        
    def test_detect_circular_dependency(self, manager):
        """测试检测循环依赖"""
        manager.add_dependency(1, 2)
        manager.add_dependency(2, 3)
        manager.add_dependency(3, 1)  # 形成循环
        
        cycles = manager.check_circular_dependency()
        
        assert len(cycles) > 0
        assert set(cycles[0]) == {1, 2, 3}
        
    def test_no_circular_dependency(self, manager):
        """测试无循环依赖"""
        manager.add_dependency(1, 2)
        manager.add_dependency(2, 3)
        manager.add_dependency(1, 3)  # 不形成循环
        
        cycles = manager.check_circular_dependency()
        
        assert len(cycles) == 0
        
    def test_get_execution_order(self, manager):
        """测试获取执行顺序"""
        # 构建依赖图：1->3, 2->3, 3->4, 3->5
        manager.add_dependency(1, 3)
        manager.add_dependency(2, 3)
        manager.add_dependency(3, 4)
        manager.add_dependency(3, 5)
        
        order = manager.get_execution_order([1, 2, 3, 4, 5])
        
        # 1和2必须在3之前，3必须在4和5之前
        assert order.index(1) < order.index(3)
        assert order.index(2) < order.index(3)
        assert order.index(3) < order.index(4)
        assert order.index(3) < order.index(5)
        
    def test_execution_order_with_independent(self, manager):
        """测试包含独立节点的执行顺序"""
        manager.add_dependency(2, 4)
        manager.add_dependency(3, 4)
        
        # 1和5是独立的
        order = manager.get_execution_order([1, 2, 3, 4, 5])
        
        assert len(order) == 5
        assert order.index(2) < order.index(4)
        assert order.index(3) < order.index(4)
        # 1和5可以在任何位置
        
    def test_remove_dependency(self, manager):
        """测试移除依赖"""
        manager.add_dependency(1, 3)
        manager.add_dependency(2, 3)
        
        manager.remove_dependency(1, 3)
        
        assert not manager.has_dependency(1, 3)
        assert manager.has_dependency(2, 3)


class TestForeshadowing:
    """测试伏笔管理"""
    
    @pytest.fixture
    def manager(self):
        """创建管理器实例"""
        return DependencyManager()
    
    def test_add_foreshadowing(self, manager):
        """测试添加伏笔"""
        manager.add_foreshadowing(
            name="神秘徽章",
            setup_chapter=1,
            payoff_chapter=5,
            description="主角发现的徽章将揭示真相"
        )
        
        foreshadowing = manager.get_foreshadowing("神秘徽章")
        
        assert foreshadowing is not None
        assert foreshadowing.setup_chapter == 1
        assert foreshadowing.payoff_chapter == 5
        assert foreshadowing.status == "setup"
        
    def test_foreshadowing_lifecycle(self, manager):
        """测试伏笔生命周期"""
        manager.add_foreshadowing("线索A", 1, 5)
        
        # 初始状态
        assert manager.get_foreshadowing_status("线索A") == "setup"
        
        # 标记为已设置
        manager.mark_foreshadowing_setup("线索A")
        assert manager.get_foreshadowing_status("线索A") == "planted"
        
        # 标记为已回收
        manager.mark_foreshadowing_payoff("线索A")
        assert manager.get_foreshadowing_status("线索A") == "resolved"
        
    def test_get_pending_foreshadowings(self, manager):
        """测试获取待处理伏笔"""
        manager.add_foreshadowing("伏笔1", 1, 5)
        manager.add_foreshadowing("伏笔2", 2, 6)
        manager.add_foreshadowing("伏笔3", 3, 7)
        
        manager.mark_foreshadowing_payoff("伏笔1")
        
        pending = manager.get_pending_foreshadowings()
        
        assert len(pending) == 2
        assert "伏笔2" in pending
        assert "伏笔3" in pending
        assert "伏笔1" not in pending
        
    def test_get_foreshadowings_for_chapter(self, manager):
        """测试获取特定章节的伏笔"""
        manager.add_foreshadowing("伏笔A", 1, 5)
        manager.add_foreshadowing("伏笔B", 1, 7)
        manager.add_foreshadowing("伏笔C", 2, 5)
        
        # 第1章设置的伏笔
        setup_in_1 = manager.get_foreshadowings_for_chapter(1, "setup")
        assert len(setup_in_1) == 2
        assert "伏笔A" in setup_in_1
        assert "伏笔B" in setup_in_1
        
        # 第5章回收的伏笔
        payoff_in_5 = manager.get_foreshadowings_for_chapter(5, "payoff")
        assert len(payoff_in_5) == 2
        assert "伏笔A" in payoff_in_5
        assert "伏笔C" in payoff_in_5
        
    def test_validate_foreshadowing_chain(self, manager):
        """测试验证伏笔链"""
        # 创建伏笔链
        manager.add_foreshadowing("线索1", 1, 3)
        manager.add_foreshadowing("线索2", 3, 5)
        manager.add_foreshadowing("线索3", 5, 8)
        
        # 添加依赖确保顺序
        manager.add_dependency(1, 3)
        manager.add_dependency(3, 5)
        manager.add_dependency(5, 8)
        
        is_valid = manager.validate_foreshadowing_chain(["线索1", "线索2", "线索3"])
        
        assert is_valid is True
        
    def test_invalid_foreshadowing_chain(self, manager):
        """测试无效伏笔链"""
        manager.add_foreshadowing("线索1", 1, 3)
        manager.add_foreshadowing("线索2", 5, 2)  # 回收在设置之前
        
        is_valid = manager.validate_foreshadowing_chain(["线索1", "线索2"])
        
        assert is_valid is False


class TestDependencyType:
    """测试依赖类型"""
    
    def test_dependency_types(self):
        """测试依赖类型枚举"""
        assert DependencyType.PLOT == "plot"
        assert DependencyType.CHARACTER == "character"
        assert DependencyType.SETTING == "setting"
        assert DependencyType.THEME == "theme"
        assert DependencyType.FORESHADOWING == "foreshadowing"
        
    def test_add_typed_dependencies(self):
        """测试添加不同类型的依赖"""
        manager = DependencyManager()
        
        manager.add_dependency(1, 2, DependencyType.PLOT)
        manager.add_dependency(1, 3, DependencyType.CHARACTER)
        manager.add_dependency(2, 4, DependencyType.SETTING)
        
        assert manager.get_dependency_type(1, 2) == DependencyType.PLOT
        assert manager.get_dependency_type(1, 3) == DependencyType.CHARACTER
        assert manager.get_dependency_type(2, 4) == DependencyType.SETTING


class TestExecutionOrder:
    """测试执行顺序计算"""
    
    @pytest.fixture
    def manager(self):
        return DependencyManager()
    
    def test_topological_sort(self, manager):
        """测试拓扑排序"""
        # 创建DAG: 1->2->3, 1->4->5, 3->5
        manager.add_dependency(1, 2)
        manager.add_dependency(2, 3)
        manager.add_dependency(1, 4)
        manager.add_dependency(4, 5)
        manager.add_dependency(3, 5)
        
        order = manager.get_execution_order([1, 2, 3, 4, 5])
        
        # 验证所有依赖都被满足
        for i, chapter in enumerate(order):
            deps = manager.get_dependencies(chapter)
            for dep in deps:
                assert order.index(dep) < i
                
    def test_parallel_groups(self, manager):
        """测试获取可并行执行的组"""
        # 1和2独立，都指向3和4
        manager.add_dependency(1, 3)
        manager.add_dependency(1, 4)
        manager.add_dependency(2, 3)
        manager.add_dependency(2, 4)
        
        groups = manager.get_parallel_groups([1, 2, 3, 4])
        
        # 应该有两组：[1,2] 和 [3,4]
        assert len(groups) == 2
        assert set(groups[0]) == {1, 2}
        assert set(groups[1]) == {3, 4}
        
    def test_complex_parallel_groups(self, manager):
        """测试复杂的并行分组"""
        # 1独立，2和3依赖1，4依赖2和3，5独立
        manager.add_dependency(1, 2)
        manager.add_dependency(1, 3)
        manager.add_dependency(2, 4)
        manager.add_dependency(3, 4)
        
        groups = manager.get_parallel_groups([1, 2, 3, 4, 5])
        
        # 组1: [1, 5], 组2: [2, 3], 组3: [4]
        assert len(groups) == 3
        assert 1 in groups[0] and 5 in groups[0]
        assert 2 in groups[1] and 3 in groups[1]
        assert 4 in groups[2]


class TestDependencyPersistence:
    """测试依赖持久化"""
    
    @pytest.fixture
    def manager(self):
        return DependencyManager()
    
    def test_export_to_json(self, manager):
        """测试导出为JSON"""
        manager.add_dependency(1, 3, DependencyType.PLOT)
        manager.add_dependency(2, 3, DependencyType.CHARACTER)
        manager.add_foreshadowing("伏笔1", 1, 5, "测试伏笔")
        
        json_data = manager.export_to_json()
        data = json.loads(json_data)
        
        assert "dependencies" in data
        assert "foreshadowings" in data
        assert len(data["dependencies"]) == 2
        assert len(data["foreshadowings"]) == 1
        
    def test_import_from_json(self, manager):
        """测试从JSON导入"""
        json_data = '''
        {
            "dependencies": [
                {"source": 1, "target": 3, "type": "plot"},
                {"source": 2, "target": 3, "type": "character"}
            ],
            "foreshadowings": [
                {
                    "name": "伏笔1",
                    "setup_chapter": 1,
                    "payoff_chapter": 5,
                    "description": "测试",
                    "status": "setup"
                }
            ]
        }
        '''
        
        manager.import_from_json(json_data)
        
        assert manager.has_dependency(1, 3)
        assert manager.has_dependency(2, 3)
        assert manager.get_foreshadowing("伏笔1") is not None
        
    def test_save_and_load(self, manager, tmp_path):
        """测试保存和加载"""
        # 创建测试数据
        manager.add_dependency(1, 2)
        manager.add_foreshadowing("test", 1, 3)
        
        # 保存到文件
        file_path = tmp_path / "dependencies.json"
        manager.save_to_file(str(file_path))
        
        # 创建新管理器并加载
        new_manager = DependencyManager()
        new_manager.load_from_file(str(file_path))
        
        assert new_manager.has_dependency(1, 2)
        assert new_manager.get_foreshadowing("test") is not None


class TestDependencyVisualization:
    """测试依赖可视化"""
    
    @pytest.fixture
    def manager(self):
        manager = DependencyManager()
        # 创建示例依赖图
        manager.add_dependency(1, 3, DependencyType.PLOT)
        manager.add_dependency(2, 3, DependencyType.CHARACTER)
        manager.add_dependency(3, 4, DependencyType.SETTING)
        manager.add_dependency(3, 5, DependencyType.THEME)
        return manager
    
    def test_generate_dot_graph(self, manager):
        """测试生成DOT格式图"""
        dot_string = manager.generate_dot_graph()
        
        assert "digraph" in dot_string
        assert "1 -> 3" in dot_string
        assert "2 -> 3" in dot_string
        assert "3 -> 4" in dot_string
        assert "3 -> 5" in dot_string
        
    def test_get_graph_statistics(self, manager):
        """测试获取图统计信息"""
        stats = manager.get_graph_statistics()
        
        assert stats["total_nodes"] == 5
        assert stats["total_edges"] == 4
        assert stats["max_in_degree"] == 2  # 节点3
        assert stats["max_out_degree"] == 2  # 节点3
        assert stats["has_cycles"] is False
        
    def test_find_critical_path(self, manager):
        """测试查找关键路径"""
        path = manager.find_critical_path(1, 5)
        
        assert path is not None
        assert path[0] == 1
        assert path[-1] == 5
        assert 3 in path  # 必须经过3


class TestDependencyValidation:
    """测试依赖验证"""
    
    def test_validate_no_orphan_nodes(self):
        """测试验证无孤立节点"""
        manager = DependencyManager()
        manager.add_dependency(1, 2)
        manager.add_dependency(2, 3)
        # 4是孤立的
        
        orphans = manager.find_orphan_nodes([1, 2, 3, 4])
        
        assert 4 in orphans
        assert 1 not in orphans
        
    def test_validate_foreshadowing_coverage(self):
        """测试验证伏笔覆盖"""
        manager = DependencyManager()
        manager.add_foreshadowing("A", 1, 5)
        manager.add_foreshadowing("B", 2, 6)
        manager.add_foreshadowing("C", 3, 7)
        
        manager.mark_foreshadowing_payoff("A")
        manager.mark_foreshadowing_payoff("B")
        # C未回收
        
        unresolved = manager.get_unresolved_foreshadowings()
        
        assert len(unresolved) == 1
        assert "C" in unresolved
        
    def test_validate_dependency_completeness(self):
        """测试验证依赖完整性"""
        manager = DependencyManager()
        manager.add_dependency(1, 3)
        manager.add_dependency(2, 3)
        
        # 检查章节3的所有依赖是否在列表中
        chapters = [1, 3]  # 缺少2
        missing = manager.check_missing_dependencies(chapters)
        
        assert 2 in missing
        assert 1 not in missing


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])