"""
Context Firewall 测试套件
测试主线程保护和摘要生成功能
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.context_firewall import (
    ContextFirewall,
    AgentResponse,
    FirewallConfig,
    ContextProtector
)


class TestAgentResponse:
    """测试Agent响应封装类"""
    
    def test_create_response_with_summary(self):
        """测试创建带摘要的响应"""
        response = AgentResponse(
            summary="章节生成完成，质量95分",
            status="success",
            details="[完整的章节内容，包含大量文字...]" * 100
        )
        
        assert response.get_summary() == "章节生成完成，质量95分"
        assert response.is_success() is True
        assert len(response._details) > 50  # 详细内容很长
        
    def test_summary_truncation(self):
        """测试摘要自动截断到50字符"""
        long_summary = "这是一个非常长的摘要" * 10
        response = AgentResponse(
            summary=long_summary,
            status="success"
        )
        
        summary = response.get_summary()
        assert len(summary) <= 50
        assert summary == long_summary[:50]
        
    def test_response_status_types(self):
        """测试不同的响应状态"""
        success = AgentResponse("成功", "success")
        partial = AgentResponse("部分完成", "partial")
        failed = AgentResponse("失败", "failed")
        
        assert success.is_success() is True
        assert partial.is_success() is False
        assert failed.is_success() is False
        assert failed.status == "failed"
        
    def test_response_with_metadata(self):
        """测试带元数据的响应"""
        response = AgentResponse(
            summary="处理完成",
            status="success",
            metadata={
                "token_used": 1500,
                "time_elapsed": 2.5,
                "quality_score": 95
            }
        )
        
        assert response.metadata["token_used"] == 1500
        assert response.metadata["quality_score"] == 95


class TestContextFirewall:
    """测试Context防火墙主类"""
    
    @pytest.fixture
    def firewall(self):
        """创建防火墙实例"""
        config = FirewallConfig(
            max_summary_length=50,
            enable_filtering=True,
            log_blocked_content=True
        )
        return ContextFirewall(config)
    
    def test_filter_agent_response(self, firewall):
        """测试过滤Agent响应"""
        # 模拟Agent返回大量内容
        raw_response = {
            "content": "X" * 10000,  # 10000字符
            "status": "success",
            "metadata": {"tokens": 5000}
        }
        
        filtered = firewall.filter_response(raw_response)
        
        # 应该只返回摘要
        assert "summary" in filtered
        assert "content" not in filtered  # 原始内容被过滤
        assert len(filtered["summary"]) <= 50
        
    def test_batch_filter_responses(self, firewall):
        """测试批量过滤响应"""
        responses = [
            {"content": "Response 1" * 1000, "status": "success"},
            {"content": "Response 2" * 1000, "status": "success"},
            {"content": "Response 3" * 1000, "status": "failed"}
        ]
        
        filtered_list = firewall.batch_filter(responses)
        
        assert len(filtered_list) == 3
        for filtered in filtered_list:
            assert "summary" in filtered
            assert len(filtered.get("summary", "")) <= 50
            
    def test_firewall_logging(self, firewall):
        """测试防火墙日志记录"""
        with patch('logging.Logger.info') as mock_log:
            response = {"content": "Test content" * 100}
            firewall.filter_response(response)
            
            # 应该记录过滤操作
            mock_log.assert_called()
            
    def test_firewall_statistics(self, firewall):
        """测试防火墙统计功能"""
        # 处理多个响应
        for i in range(10):
            firewall.filter_response({
                "content": f"Content {i}" * 100,
                "status": "success" if i < 8 else "failed"
            })
        
        stats = firewall.get_statistics()
        
        assert stats["total_filtered"] == 10
        assert stats["total_blocked_chars"] > 0
        assert stats["success_rate"] == 0.8


class TestContextProtector:
    """测试上下文保护器"""
    
    def test_protect_main_thread(self):
        """测试主线程保护"""
        protector = ContextProtector()
        
        # 模拟大量Agent响应
        agent_responses = [
            AgentResponse(f"Agent {i} 完成", "success", "详细内容" * 1000)
            for i in range(10)
        ]
        
        # 保护主线程，只获取摘要
        protected_data = protector.protect(agent_responses)
        
        # 验证只返回摘要
        assert len(protected_data) == 10
        for item in protected_data:
            assert len(item) <= 50  # 只有摘要
            
    def test_emergency_cutoff(self):
        """测试紧急截断功能"""
        protector = ContextProtector(emergency_cutoff=True)
        
        # 创建超大响应
        huge_response = AgentResponse(
            "摘要",
            "success",
            "X" * 1000000  # 1MB文本
        )
        
        # 应该触发紧急截断
        with patch('logging.Logger.warning') as mock_warn:
            protected = protector.protect([huge_response])
            mock_warn.assert_called_with(pytest.stringcontaining("Emergency cutoff"))


class TestFirewallIntegration:
    """测试防火墙集成场景"""
    
    @pytest.mark.asyncio
    async def test_parallel_agent_filtering(self):
        """测试并行Agent执行时的过滤"""
        firewall = ContextFirewall()
        
        async def mock_agent_execution(agent_id):
            """模拟Agent执行"""
            await asyncio.sleep(0.1)
            return {
                "agent_id": agent_id,
                "content": f"Agent {agent_id} generated content" * 100,
                "status": "success"
            }
        
        # 并行执行多个Agent
        tasks = [mock_agent_execution(i) for i in range(8)]
        raw_results = await asyncio.gather(*tasks)
        
        # 通过防火墙过滤
        filtered_results = firewall.batch_filter(raw_results)
        
        # 验证结果
        assert len(filtered_results) == 8
        for result in filtered_results:
            assert "summary" in result
            assert len(result["summary"]) <= 50
            
    def test_memory_efficiency(self):
        """测试内存效率"""
        import tracemalloc
        tracemalloc.start()
        
        firewall = ContextFirewall()
        
        # 创建大量数据
        large_responses = [
            {"content": "X" * 10000, "status": "success"}
            for _ in range(100)
        ]
        
        # 获取初始内存
        snapshot1 = tracemalloc.take_snapshot()
        
        # 过滤响应
        filtered = firewall.batch_filter(large_responses)
        
        # 获取过滤后内存
        snapshot2 = tracemalloc.take_snapshot()
        
        # 计算内存差异
        stats = snapshot2.compare_to(snapshot1, 'lineno')
        total_diff = sum(stat.size_diff for stat in stats)
        
        # 过滤后应该使用更少内存（因为丢弃了详细内容）
        assert total_diff < len(large_responses) * 10000
        
        tracemalloc.stop()


class TestFirewallConfig:
    """测试防火墙配置"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = FirewallConfig()
        
        assert config.max_summary_length == 50
        assert config.enable_filtering is True
        assert config.log_blocked_content is False
        
    def test_custom_config(self):
        """测试自定义配置"""
        config = FirewallConfig(
            max_summary_length=100,
            enable_filtering=False,
            log_blocked_content=True,
            emergency_cutoff=True,
            cutoff_threshold=5000
        )
        
        assert config.max_summary_length == 100
        assert config.enable_filtering is False
        assert config.emergency_cutoff is True
        
    def test_config_validation(self):
        """测试配置验证"""
        with pytest.raises(ValueError):
            # 摘要长度不能为负
            FirewallConfig(max_summary_length=-1)
            
        with pytest.raises(ValueError):
            # 摘要长度不能超过1000
            FirewallConfig(max_summary_length=1001)


class TestFirewallPerformance:
    """测试防火墙性能"""
    
    def test_filtering_speed(self):
        """测试过滤速度"""
        import time
        
        firewall = ContextFirewall()
        
        # 创建1000个响应
        responses = [
            {"content": f"Content {i}" * 100, "status": "success"}
            for i in range(1000)
        ]
        
        start_time = time.time()
        filtered = firewall.batch_filter(responses)
        elapsed = time.time() - start_time
        
        # 应该在1秒内完成
        assert elapsed < 1.0
        assert len(filtered) == 1000
        
    @pytest.mark.asyncio
    async def test_concurrent_filtering(self):
        """测试并发过滤"""
        firewall = ContextFirewall()
        
        async def filter_task(task_id):
            responses = [
                {"content": f"Task {task_id} Response {i}" * 50}
                for i in range(100)
            ]
            return firewall.batch_filter(responses)
        
        # 并发执行10个过滤任务
        tasks = [filter_task(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # 验证所有任务都成功完成
        assert len(results) == 10
        for result in results:
            assert len(result) == 100


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])