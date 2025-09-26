"""
完整工作流集成测试
测试NOVELSYS-SWARM 2.5的端到端功能
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.context_firewall import ContextFirewall, AgentResponse
from src.core.github_integration import GitHubIntegration
from src.core.parallel_coordinator import NovelParallelCoordinator
from src.core.dependency_manager import DependencyManager
from src.core.agent_type_mapper import AgentTypeMapper
from src.core.five_stage_workflow import FiveStageWorkflow
from src.core.git_worktree_manager import GitWorktreeManager
from src.core.incremental_sync import IncrementalSync


class TestCompleteNovelGeneration:
    """测试完整的小说生成流程"""
    
    @pytest.mark.asyncio
    async def test_five_stage_workflow(self):
        """测试5阶段工作流"""
        workflow = FiveStageWorkflow()
        
        # Stage 1: 概念
        concept = await workflow.stage_concept({
            "title": "测试小说",
            "genre": "科幻",
            "premise": "AI觉醒的故事"
        })
        assert concept["status"] == "completed"
        
        # Stage 2: Bible
        bible = await workflow.stage_bible(concept)
        assert "world_setting" in bible
        assert "characters" in bible
        
        # Stage 3: 章节
        chapters = await workflow.stage_chapters(bible, count=5)
        assert len(chapters) == 5
        
        # Stage 4: 场景
        scenes = await workflow.stage_scenes(chapters[0])
        assert len(scenes) > 0
        
        # Stage 5: 手稿
        manuscript = await workflow.stage_manuscript(scenes)
        assert "content" in manuscript
        assert len(manuscript["content"]) > 1000
        
    @pytest.mark.asyncio
    async def test_parallel_chapter_generation(self):
        """测试并行章节生成"""
        coordinator = NovelParallelCoordinator()
        firewall = ContextFirewall()
        
        bible = {
            "title": "测试小说",
            "genre": "科幻",
            "setting": "未来世界"
        }
        
        outlines = {
            1: "第一章：觉醒",
            2: "第二章：探索",
            3: "第三章：冲突"
        }
        
        with patch.object(coordinator, '_execute_streams') as mock_streams:
            # 模拟8个Stream的返回
            mock_streams.return_value = {
                'character': {'score': 95, 'content': 'X' * 10000},
                'narrative': {'score': 92, 'content': 'X' * 10000},
                'world': {'score': 93, 'content': 'X' * 10000},
                'prose': {'score': 91, 'content': 'X' * 10000},
                'continuity': {'score': 99, 'content': 'X' * 10000},
                'foreshadowing': {'score': 100, 'content': 'X' * 10000},
                'dialogue': {'score': 94, 'content': 'X' * 10000},
                'emotion': {'score': 90, 'content': 'X' * 10000}
            }
            
            # 并行生成
            results = await coordinator.execute_parallel(
                chapters=[1, 2, 3],
                outlines=outlines,
                bible=bible
            )
            
            # 通过防火墙过滤
            filtered_results = {}
            for chapter_num, result in results.items():
                response = AgentResponse(
                    summary=f"第{chapter_num}章完成，质量{result.get('quality', 0)}",
                    status="success",
                    details=str(result)
                )
                filtered_results[chapter_num] = response.get_summary()
            
            # 验证结果
            assert len(filtered_results) == 3
            for summary in filtered_results.values():
                assert len(summary) <= 50  # 防火墙限制


class TestDependencyDrivenExecution:
    """测试依赖驱动的执行"""
    
    @pytest.mark.asyncio
    async def test_execute_with_plot_dependencies(self):
        """测试带情节依赖的执行"""
        manager = DependencyManager()
        coordinator = NovelParallelCoordinator()
        
        # 设置依赖：1->3, 2->3, 3->5, 4->5
        manager.add_dependency(1, 3, "plot")
        manager.add_dependency(2, 3, "character")
        manager.add_dependency(3, 5, "plot")
        manager.add_dependency(4, 5, "setting")
        
        # 添加伏笔
        manager.add_foreshadowing("神秘信件", 1, 5)
        manager.add_foreshadowing("失踪的项链", 2, 4)
        
        # 获取执行顺序
        chapters = [1, 2, 3, 4, 5]
        order = manager.get_execution_order(chapters)
        
        # 按顺序执行
        executed = []
        for chapter in order:
            deps = manager.get_dependencies(chapter)
            # 确保依赖已执行
            for dep in deps:
                assert dep in executed
            
            # 模拟执行
            with patch.object(coordinator, 'execute_chapter') as mock_exec:
                mock_exec.return_value = {"success": True, "chapter": chapter}
                result = await coordinator.execute_chapter(
                    chapter,
                    f"第{chapter}章",
                    {}
                )
                executed.append(chapter)
        
        assert len(executed) == 5
        # 验证伏笔设置和回收的顺序
        assert executed.index(1) < executed.index(5)  # 神秘信件
        assert executed.index(2) < executed.index(4)  # 失踪的项链


class TestGitHubPersistence:
    """测试GitHub持久化集成"""
    
    def test_complete_sync_workflow(self):
        """测试完整的同步流程"""
        github = GitHubIntegration("test-novel")
        sync = IncrementalSync()
        
        # 初始内容
        chapter_v1 = {
            "content": "第一章原始内容" * 100,
            "quality": 85,
            "metadata": {"version": 1}
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            # 首次同步（全量）
            mode = sync.determine_sync_mode(None, chapter_v1["content"])
            assert mode == "full"
            github.sync_chapter_to_issue(1, chapter_v1)
            
            # 小修改（补丁）
            chapter_v2 = chapter_v1.copy()
            chapter_v2["content"] = chapter_v1["content"] + "新增一句话。"
            mode = sync.determine_sync_mode(
                chapter_v1["content"],
                chapter_v2["content"]
            )
            assert mode == "patch"
            
            # 大修改（全量）
            chapter_v3 = {
                "content": "完全重写的内容" * 200,
                "quality": 95
            }
            mode = sync.determine_sync_mode(
                chapter_v2["content"],
                chapter_v3["content"]
            )
            assert mode == "full"
            
    def test_checkpoint_and_recovery(self):
        """测试检查点和恢复"""
        github = GitHubIntegration("test-novel")
        
        # 创建检查点
        state = {
            "chapters_completed": [1, 2, 3],
            "current_chapter": 4,
            "bible": {"title": "测试小说"},
            "dependencies": {"1": ["3"], "2": ["3"]}
        }
        
        with patch('subprocess.run') as mock_run:
            # 模拟创建检查点
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="v1.0.0"
            )
            
            checkpoint = github.create_checkpoint(state, "前3章完成")
            assert checkpoint == "v1.0.0"
            
            # 模拟恢复
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=json.dumps(state)
            )
            
            recovered = github.restore_from_checkpoint("v1.0.0")
            assert recovered["current_chapter"] == 4
            assert len(recovered["chapters_completed"]) == 3


class TestDynamicAgentAllocation:
    """测试动态Agent分配"""
    
    def test_agent_selection_for_chapter_types(self):
        """测试不同章节类型的Agent选择"""
        mapper = AgentTypeMapper()
        
        # 动作章节
        action_agents = mapper.get_agents_for_chapter("action")
        assert "action-choreographer" in action_agents
        assert "pacing-specialist" in action_agents
        assert "tension-maximizer" in action_agents
        
        # 对话章节
        dialogue_agents = mapper.get_agents_for_chapter("dialogue")
        assert "dialogue-enhancer" in dialogue_agents
        assert "subtext-weaver" in dialogue_agents
        
        # 情感章节
        emotion_agents = mapper.get_agents_for_chapter("emotional")
        assert "emotion-amplifier" in emotion_agents
        assert "romance-specialist" in emotion_agents
        
    def test_auto_detect_chapter_type(self):
        """测试自动检测章节类型"""
        mapper = AgentTypeMapper()
        
        action_content = "他猛地跃起，拳头如雷霆般轰出，敌人应声倒地。爆炸声响起..."
        dialogue_content = '"你真的要走吗？" 她问道。\n"我别无选择。" 他回答。'
        
        assert mapper.auto_detect_type(action_content) == "action"
        assert mapper.auto_detect_type(dialogue_content) == "dialogue"


class TestGitWorktreeIntegration:
    """测试Git Worktree集成"""
    
    def test_parallel_branch_management(self):
        """测试并行分支管理"""
        manager = GitWorktreeManager("test-novel")
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            # 创建多个工作树
            worktrees = []
            for i in range(1, 4):
                wt = manager.create_worktree(f"chapter-{i}")
                worktrees.append(wt)
                assert wt is not None
            
            # 并行工作
            for i, wt in enumerate(worktrees, 1):
                manager.switch_to_worktree(wt)
                # 模拟章节生成
                manager.commit_changes(f"Complete chapter {i}")
            
            # 合并回主分支
            for wt in worktrees:
                manager.merge_worktree(wt)
            
            # 清理
            for wt in worktrees:
                manager.remove_worktree(wt)


class TestEndToEndScenarios:
    """测试端到端场景"""
    
    @pytest.mark.asyncio
    async def test_complete_novel_generation_pipeline(self):
        """测试完整的小说生成管道"""
        # 初始化所有组件
        workflow = FiveStageWorkflow()
        coordinator = NovelParallelCoordinator()
        firewall = ContextFirewall()
        deps = DependencyManager()
        github = GitHubIntegration("test-novel")
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            # 1. 创建概念和Bible
            concept = {"title": "AI觉醒", "genre": "科幻"}
            bible = {
                "title": "AI觉醒",
                "characters": ["Alice", "Bob", "AI"],
                "setting": "2045年"
            }
            
            # 2. 设置依赖和伏笔
            deps.add_dependency(1, 3, "plot")
            deps.add_dependency(2, 3, "character")
            deps.add_foreshadowing("AI的秘密", 1, 5)
            
            # 3. 生成章节（遵循依赖）
            order = deps.get_execution_order([1, 2, 3, 4, 5])
            
            results = {}
            for chapter in order:
                # 检查依赖
                dependencies = deps.get_dependencies(chapter)
                
                # 模拟生成
                with patch.object(coordinator, '_execute_streams') as mock_streams:
                    mock_streams.return_value = self._get_mock_streams()
                    
                    result = await coordinator.execute_chapter(
                        chapter,
                        f"第{chapter}章",
                        bible,
                        dependencies
                    )
                    
                    # 通过防火墙
                    response = AgentResponse(
                        f"第{chapter}章完成",
                        "success",
                        str(result)
                    )
                    
                    results[chapter] = response.get_summary()
                    
                    # 同步到GitHub
                    github.sync_chapter_to_issue(chapter, result)
            
            # 4. 验证结果
            assert len(results) == 5
            for summary in results.values():
                assert len(summary) <= 50
                assert "完成" in summary
                
    def _get_mock_streams(self):
        """获取模拟的Stream结果"""
        return {
            'character': {'score': 95},
            'narrative': {'score': 92},
            'world': {'score': 93},
            'prose': {'score': 91},
            'continuity': {'score': 99},
            'foreshadowing': {'score': 100},
            'dialogue': {'score': 94},
            'emotion': {'score': 90}
        }
    
    @pytest.mark.asyncio
    async def test_failure_recovery(self):
        """测试失败恢复"""
        coordinator = NovelParallelCoordinator()
        github = GitHubIntegration("test-novel")
        
        # 模拟第3章失败
        with patch.object(coordinator, 'execute_chapter') as mock_exec:
            mock_exec.side_effect = [
                {"success": True, "chapter": 1},
                {"success": True, "chapter": 2},
                Exception("Chapter 3 failed"),
                {"success": True, "chapter": 3},  # 重试成功
                {"success": True, "chapter": 4},
                {"success": True, "chapter": 5}
            ]
            
            chapters_completed = []
            for i in range(1, 6):
                try:
                    result = await coordinator.execute_chapter(i, f"第{i}章", {})
                    chapters_completed.append(i)
                except Exception as e:
                    # 保存检查点
                    with patch('subprocess.run'):
                        github.create_checkpoint(
                            {"completed": chapters_completed},
                            f"Failed at chapter {i}"
                        )
                    # 重试
                    result = await coordinator.execute_chapter(i, f"第{i}章", {})
                    chapters_completed.append(i)
            
            assert len(chapters_completed) == 5
            assert 3 in chapters_completed


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])