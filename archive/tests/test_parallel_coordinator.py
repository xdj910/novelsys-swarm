"""
Parallel Coordinator 测试套件
测试8-Stream并行执行协调功能
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.parallel_coordinator import (
    NovelParallelCoordinator,
    StreamExecutor,
    ParallelConfig,
    ExecutionResult
)


class TestNovelParallelCoordinator:
    """测试并行协调器主类"""
    
    @pytest.fixture
    def coordinator(self):
        """创建协调器实例"""
        config = ParallelConfig(
            max_workers=8,
            timeout=30,
            enable_logging=True
        )
        return NovelParallelCoordinator(config)
    
    @pytest.mark.asyncio
    async def test_execute_single_chapter(self, coordinator):
        """测试单章节执行"""
        bible = {"title": "测试小说", "genre": "科幻"}
        outline = "第一章：觉醒"
        
        with patch.object(coordinator, '_execute_streams') as mock_execute:
            mock_execute.return_value = {
                'character': {'score': 95, 'content': 'character analysis'},
                'narrative': {'score': 92, 'content': 'narrative structure'},
                'world': {'score': 93, 'content': 'world building'},
                'prose': {'score': 91, 'content': 'prose craft'},
                'continuity': {'score': 99, 'content': 'continuity check'},
                'foreshadowing': {'score': 100, 'content': 'foreshadowing'},
                'dialogue': {'score': 94, 'content': 'dialogue'},
                'emotion': {'score': 90, 'content': 'emotion'}
            }
            
            result = await coordinator.execute_chapter(
                chapter_num=1,
                outline=outline,
                bible=bible
            )
            
            assert result['success'] is True
            assert 'content' in result
            assert 'quality' in result
            assert result['quality'] >= 90
            assert 'streams' in result
            assert len(result['streams']) == 8
            
    @pytest.mark.asyncio
    async def test_execute_multiple_chapters(self, coordinator):
        """测试多章节并行执行"""
        bible = {"title": "测试小说"}
        outlines = {
            1: "第一章大纲",
            2: "第二章大纲",
            3: "第三章大纲"
        }
        
        with patch.object(coordinator, '_execute_streams') as mock_execute:
            mock_execute.return_value = self._get_mock_stream_results()
            
            results = await coordinator.execute_parallel(
                chapters=[1, 2, 3],
                outlines=outlines,
                bible=bible
            )
            
            assert len(results) == 3
            assert all(results[i]['success'] for i in [1, 2, 3])
            # 验证并行执行
            assert mock_execute.call_count >= 3
            
    @pytest.mark.asyncio
    async def test_stream_timeout_handling(self, coordinator):
        """测试Stream超时处理"""
        async def slow_stream():
            await asyncio.sleep(100)  # 模拟超时
            return {"score": 90}
        
        coordinator.config.timeout = 1  # 1秒超时
        
        with patch.object(coordinator, '_execute_stream', side_effect=slow_stream):
            result = await coordinator.execute_chapter(1, "outline", {})
            
            # 应该处理超时，但不失败
            assert result['success'] is True
            assert result.get('warnings', [])
            assert 'timeout' in str(result.get('warnings', [])).lower()
            
    def _get_mock_stream_results(self):
        """获取模拟的Stream结果"""
        return {
            'character': {'score': 95, 'content': 'mock'},
            'narrative': {'score': 92, 'content': 'mock'},
            'world': {'score': 93, 'content': 'mock'},
            'prose': {'score': 91, 'content': 'mock'},
            'continuity': {'score': 99, 'content': 'mock'},
            'foreshadowing': {'score': 100, 'content': 'mock'},
            'dialogue': {'score': 94, 'content': 'mock'},
            'emotion': {'score': 90, 'content': 'mock'}
        }


class TestStreamExecutor:
    """测试Stream执行器"""
    
    @pytest.fixture
    def executor(self):
        """创建执行器实例"""
        return StreamExecutor(max_workers=8)
    
    @pytest.mark.asyncio
    async def test_execute_all_streams(self, executor):
        """测试执行所有Stream"""
        context = {
            'chapter_num': 1,
            'outline': '测试大纲',
            'bible': {}
        }
        
        # Mock所有8个Stream
        with patch.object(executor, 'character_stream', new_callable=AsyncMock) as mock_char, \
             patch.object(executor, 'narrative_stream', new_callable=AsyncMock) as mock_narr, \
             patch.object(executor, 'world_stream', new_callable=AsyncMock) as mock_world, \
             patch.object(executor, 'prose_stream', new_callable=AsyncMock) as mock_prose, \
             patch.object(executor, 'continuity_stream', new_callable=AsyncMock) as mock_cont, \
             patch.object(executor, 'foreshadowing_stream', new_callable=AsyncMock) as mock_fore, \
             patch.object(executor, 'dialogue_stream', new_callable=AsyncMock) as mock_dial, \
             patch.object(executor, 'emotion_stream', new_callable=AsyncMock) as mock_emot:
            
            # 设置返回值
            mock_char.process.return_value = {'score': 95}
            mock_narr.process.return_value = {'score': 92}
            mock_world.process.return_value = {'score': 93}
            mock_prose.process.return_value = {'score': 91}
            mock_cont.process.return_value = {'score': 99}
            mock_fore.process.return_value = {'score': 100}
            mock_dial.process.return_value = {'score': 94}
            mock_emot.process.return_value = {'score': 90}
            
            results = await executor.execute_all(context)
            
            assert len(results) == 8
            assert results['character']['score'] == 95
            assert results['continuity']['score'] == 99
            assert results['foreshadowing']['score'] == 100
            
    @pytest.mark.asyncio
    async def test_stream_failure_handling(self, executor):
        """测试Stream失败处理"""
        context = {'chapter_num': 1}
        
        with patch.object(executor, 'character_stream', new_callable=AsyncMock) as mock_stream:
            mock_stream.process.side_effect = Exception("Stream failed")
            
            results = await executor.execute_all(context)
            
            # 单个Stream失败不应导致整体失败
            assert 'character' in results
            assert results['character'].get('error') is not None
            
    @pytest.mark.asyncio
    async def test_parallel_execution_timing(self, executor):
        """测试并行执行时间"""
        async def slow_process(duration):
            await asyncio.sleep(duration)
            return {'score': 90}
        
        # 8个Stream各需要0.5秒
        with patch.object(executor, 'character_stream', new_callable=AsyncMock) as mock_char, \
             patch.object(executor, 'narrative_stream', new_callable=AsyncMock) as mock_narr:
            
            mock_char.process.side_effect = lambda _: slow_process(0.5)
            mock_narr.process.side_effect = lambda _: slow_process(0.5)
            
            start = time.time()
            await executor.execute_all({})
            elapsed = time.time() - start
            
            # 并行执行应该在1秒内完成（不是1秒）
            assert elapsed < 1.0


class TestParallelConfig:
    """测试并行配置"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ParallelConfig()
        
        assert config.max_workers == 8
        assert config.timeout == 300
        assert config.enable_logging is True
        assert config.retry_on_failure is True
        
    def test_custom_config(self):
        """测试自定义配置"""
        config = ParallelConfig(
            max_workers=16,
            timeout=60,
            enable_logging=False,
            retry_on_failure=False
        )
        
        assert config.max_workers == 16
        assert config.timeout == 60
        assert config.enable_logging is False
        
    def test_config_validation(self):
        """测试配置验证"""
        with pytest.raises(ValueError):
            # 工作线程不能为0
            ParallelConfig(max_workers=0)
            
        with pytest.raises(ValueError):
            # 超时不能为负
            ParallelConfig(timeout=-1)


class TestExecutionResult:
    """测试执行结果类"""
    
    def test_create_success_result(self):
        """测试创建成功结果"""
        result = ExecutionResult.success(
            content="生成的内容",
            quality=95,
            metadata={'tokens': 2000}
        )
        
        assert result.is_success() is True
        assert result.content == "生成的内容"
        assert result.quality == 95
        
    def test_create_failure_result(self):
        """测试创建失败结果"""
        result = ExecutionResult.failure(
            error="执行失败",
            partial_content="部分内容"
        )
        
        assert result.is_success() is False
        assert result.error == "执行失败"
        assert result.partial_content == "部分内容"
        
    def test_merge_results(self):
        """测试合并多个结果"""
        results = [
            ExecutionResult.success("Content 1", 90),
            ExecutionResult.success("Content 2", 95),
            ExecutionResult.success("Content 3", 92)
        ]
        
        merged = ExecutionResult.merge(results)
        
        assert merged.is_success() is True
        assert "Content 1" in merged.content
        assert "Content 2" in merged.content
        assert merged.quality == pytest.approx(92.33, 0.1)


class TestParallelPerformance:
    """测试并行性能"""
    
    @pytest.mark.asyncio
    async def test_scaling_performance(self):
        """测试扩展性能"""
        configs = [
            ParallelConfig(max_workers=1),
            ParallelConfig(max_workers=4),
            ParallelConfig(max_workers=8)
        ]
        
        timings = []
        
        for config in configs:
            coordinator = NovelParallelCoordinator(config)
            
            with patch.object(coordinator, '_execute_streams') as mock:
                mock.return_value = {'test': {'score': 90}}
                
                start = time.time()
                await coordinator.execute_parallel(
                    chapters=list(range(1, 9)),
                    outlines={i: f"Chapter {i}" for i in range(1, 9)},
                    bible={}
                )
                elapsed = time.time() - start
                timings.append(elapsed)
        
        # 更多工作线程应该更快
        assert timings[2] <= timings[1] <= timings[0]
        
    @pytest.mark.asyncio
    async def test_memory_efficiency(self):
        """测试内存效率"""
        import tracemalloc
        tracemalloc.start()
        
        coordinator = NovelParallelCoordinator()
        
        snapshot1 = tracemalloc.take_snapshot()
        
        # 执行大量章节
        with patch.object(coordinator, '_execute_streams') as mock:
            mock.return_value = {'test': {'score': 90}}
            
            await coordinator.execute_parallel(
                chapters=list(range(1, 101)),
                outlines={i: f"Chapter {i}" for i in range(1, 101)},
                bible={}
            )
        
        snapshot2 = tracemalloc.take_snapshot()
        stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        # 内存增长应该是线性的，不是指数的
        total_diff = sum(stat.size_diff for stat in stats if stat.size_diff > 0)
        assert total_diff < 100 * 1024 * 1024  # 小于100MB
        
        tracemalloc.stop()


class TestDependencyHandling:
    """测试依赖处理"""
    
    @pytest.mark.asyncio
    async def test_execute_with_dependencies(self):
        """测试带依赖的执行"""
        coordinator = NovelParallelCoordinator()
        
        # 章节3依赖章节1和2
        dependencies = {
            3: [1, 2],
            5: [3, 4]
        }
        
        with patch.object(coordinator, '_execute_streams') as mock:
            mock.return_value = {'test': {'score': 90}}
            
            # 应该按依赖顺序执行
            execution_order = []
            
            async def track_execution(chapter_num, *args, **kwargs):
                execution_order.append(chapter_num)
                return {'success': True}
            
            with patch.object(coordinator, 'execute_chapter', side_effect=track_execution):
                await coordinator.execute_with_dependencies(
                    chapters=[1, 2, 3, 4, 5],
                    dependencies=dependencies,
                    outlines={i: f"Chapter {i}" for i in range(1, 6)},
                    bible={}
                )
                
                # 验证执行顺序
                assert execution_order.index(1) < execution_order.index(3)
                assert execution_order.index(2) < execution_order.index(3)
                assert execution_order.index(3) < execution_order.index(5)
                assert execution_order.index(4) < execution_order.index(5)


class TestErrorRecovery:
    """测试错误恢复"""
    
    @pytest.mark.asyncio
    async def test_retry_on_failure(self):
        """测试失败重试"""
        coordinator = NovelParallelCoordinator(
            ParallelConfig(retry_on_failure=True, max_retries=3)
        )
        
        call_count = 0
        
        async def flaky_execution(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return {'success': True}
        
        with patch.object(coordinator, '_execute_streams', side_effect=flaky_execution):
            result = await coordinator.execute_chapter(1, "outline", {})
            
            assert result['success'] is True
            assert call_count == 3  # 重试了2次
            
    @pytest.mark.asyncio
    async def test_partial_failure_recovery(self):
        """测试部分失败恢复"""
        coordinator = NovelParallelCoordinator()
        
        # 模拟部分Stream失败
        def mixed_results():
            return {
                'character': {'score': 95},
                'narrative': {'error': 'Failed'},
                'world': {'score': 93},
                'prose': {'score': 91},
                'continuity': {'score': 99},
                'foreshadowing': {'score': 100},
                'dialogue': {'error': 'Failed'},
                'emotion': {'score': 90}
            }
        
        with patch.object(coordinator, '_execute_streams', return_value=mixed_results()):
            result = await coordinator.execute_chapter(1, "outline", {})
            
            # 即使部分Stream失败，也应该返回结果
            assert result['success'] is True
            assert result['quality'] > 0  # 基于成功的Stream计算质量
            assert 'warnings' in result
            assert len(result['warnings']) == 2  # 两个失败的Stream


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])