"""
GitHub Integration 测试套件
测试GitHub Issues持久化功能
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, call
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.github_integration import (
    GitHubIntegration,
    GitHubRepo,
    IssueManager,
    NovelPersistence
)


class TestGitHubIntegration:
    """测试GitHub集成主类"""
    
    @pytest.fixture
    def github(self):
        """创建GitHub集成实例"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Authentication successful"
            )
            return GitHubIntegration("test-novel", token="fake-token")
    
    def test_create_novel_repo(self, github):
        """测试创建小说仓库"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Repository created: https://github.com/user/test-novel"
            )
            
            success, result = github.create_novel_repo(
                "测试小说",
                "一部测试用的小说"
            )
            
            assert success is True
            assert "github.com" in result
            mock_run.assert_called()
            
    def test_create_repo_failure(self, github):
        """测试创建仓库失败"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stderr="Repository already exists"
            )
            
            success, error = github.create_novel_repo("测试小说")
            
            assert success is False
            assert "already exists" in error
            
    def test_sync_chapter_to_issue(self, github):
        """测试同步章节到Issue"""
        chapter_data = {
            "content": "第一章内容...",
            "quality": 95,
            "metadata": {
                "word_count": 2000,
                "created_at": "2025-01-30"
            }
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Issue #1 created"
            )
            
            success = github.sync_chapter_to_issue(1, chapter_data)
            
            assert success is True
            # 验证调用了gh命令
            args = mock_run.call_args[0][0]
            assert "gh" in args[0]
            assert "issue" in args
            
    def test_get_chapter_from_issue(self, github):
        """测试从Issue恢复章节"""
        mock_issue_content = json.dumps({
            "content": "第一章内容",
            "quality": 95,
            "metadata": {"word_count": 2000}
        })
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=mock_issue_content
            )
            
            chapter = github.get_chapter_from_issue(1)
            
            assert chapter is not None
            assert chapter["content"] == "第一章内容"
            assert chapter["quality"] == 95
            
    def test_batch_sync_chapters(self, github):
        """测试批量同步章节"""
        chapters = {
            1: {"content": "第一章", "quality": 90},
            2: {"content": "第二章", "quality": 92},
            3: {"content": "第三章", "quality": 95}
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            results = github.batch_sync_chapters(chapters)
            
            assert len(results) == 3
            assert all(results.values())
            # 应该调用3次
            assert mock_run.call_count == 3


class TestIssueManager:
    """测试Issue管理器"""
    
    @pytest.fixture
    def manager(self):
        """创建Issue管理器"""
        return IssueManager("test-repo")
    
    def test_create_bible_issue(self, manager):
        """测试创建Bible Issue"""
        bible_data = {
            "title": "测试小说",
            "genre": "科幻",
            "world_setting": "未来世界",
            "characters": ["主角A", "主角B"]
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Issue #1 created"
            )
            
            issue_id = manager.create_bible_issue(bible_data)
            
            assert issue_id == 1
            args = mock_run.call_args[0][0]
            assert "--label" in args
            assert "bible" in args
            
    def test_update_issue(self, manager):
        """测试更新Issue"""
        update_data = {
            "quality": 98,
            "iteration": 3
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            success = manager.update_issue(1, update_data)
            
            assert success is True
            args = mock_run.call_args[0][0]
            assert "comment" in args
            
    def test_get_issue_comments(self, manager):
        """测试获取Issue评论"""
        mock_comments = json.dumps([
            {"body": "Stream 1 progress: 50%"},
            {"body": "Stream 2 progress: 75%"}
        ])
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=mock_comments
            )
            
            comments = manager.get_issue_comments(1)
            
            assert len(comments) == 2
            assert "Stream 1" in comments[0]["body"]
            
    def test_close_issue(self, manager):
        """测试关闭Issue"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            success = manager.close_issue(1, "Chapter completed")
            
            assert success is True
            args = mock_run.call_args[0][0]
            assert "close" in args


class TestNovelPersistence:
    """测试小说持久化管理"""
    
    @pytest.fixture
    def persistence(self):
        """创建持久化管理器"""
        return NovelPersistence("test-novel")
    
    def test_save_novel_state(self, persistence):
        """测试保存小说状态"""
        state = {
            "current_chapter": 5,
            "total_chapters": 20,
            "quality_scores": [90, 92, 95, 93, 94],
            "bible": {"title": "测试小说"},
            "dependencies": {"1": ["3", "5"]}
        }
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            success = persistence.save_state(state)
            
            assert success is True
            
    def test_restore_novel_state(self, persistence):
        """测试恢复小说状态"""
        mock_state = json.dumps({
            "current_chapter": 5,
            "bible": {"title": "测试小说"}
        })
        
        with patch('subprocess.run') as mock_run:
            # 模拟获取Issue列表和内容
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="1\n2\n3"),  # Issue列表
                MagicMock(returncode=0, stdout=mock_state),  # State Issue
                MagicMock(returncode=0, stdout="{}"),        # Bible
                MagicMock(returncode=0, stdout="{}")         # Chapter
            ]
            
            state = persistence.restore_state()
            
            assert state is not None
            assert state["current_chapter"] == 5
            
    def test_create_checkpoint(self, persistence):
        """测试创建检查点"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Release v1.0.0 created"
            )
            
            tag = persistence.create_checkpoint("First 5 chapters done")
            
            assert tag is not None
            assert "v" in tag
            
    def test_list_checkpoints(self, persistence):
        """测试列出检查点"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="v1.0.0\nv1.1.0\nv2.0.0"
            )
            
            checkpoints = persistence.list_checkpoints()
            
            assert len(checkpoints) == 3
            assert "v2.0.0" in checkpoints


class TestGitHubSync:
    """测试GitHub同步功能"""
    
    @pytest.mark.asyncio
    async def test_async_sync_multiple_chapters(self):
        """测试异步同步多个章节"""
        github = GitHubIntegration("test-novel")
        
        chapters = [
            {"num": 1, "content": "Chapter 1"},
            {"num": 2, "content": "Chapter 2"},
            {"num": 3, "content": "Chapter 3"}
        ]
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            # 异步同步
            tasks = [
                github.async_sync_chapter(ch["num"], ch)
                for ch in chapters
            ]
            results = await asyncio.gather(*tasks)
            
            assert all(results)
            assert mock_run.call_count >= 3
            
    def test_incremental_sync(self):
        """测试增量同步"""
        github = GitHubIntegration("test-novel")
        
        old_content = "Original content"
        new_content = "Original content with small changes"
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            # 应该检测到是小改动，使用patch模式
            sync_mode = github.determine_sync_mode(old_content, new_content)
            
            assert sync_mode == "patch"
            
    def test_full_sync_for_large_changes(self):
        """测试大改动时的全量同步"""
        github = GitHubIntegration("test-novel")
        
        old_content = "Short"
        new_content = "Completely different and much longer content" * 100
        
        sync_mode = github.determine_sync_mode(old_content, new_content)
        
        assert sync_mode == "full"


class TestGitHubAuthentication:
    """测试GitHub认证"""
    
    def test_check_authentication(self):
        """测试检查认证状态"""
        github = GitHubIntegration("test-novel")
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Logged in as testuser"
            )
            
            is_authed = github.check_auth()
            
            assert is_authed is True
            
    def test_authentication_failure(self):
        """测试认证失败"""
        github = GitHubIntegration("test-novel")
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stderr="Not authenticated"
            )
            
            is_authed = github.check_auth()
            
            assert is_authed is False
            
    def test_auto_login_prompt(self):
        """测试自动登录提示"""
        github = GitHubIntegration("test-novel")
        
        with patch('subprocess.run') as mock_run:
            # 第一次检查失败，第二次成功
            mock_run.side_effect = [
                MagicMock(returncode=1),  # 未认证
                MagicMock(returncode=0)   # 认证成功
            ]
            
            with patch('builtins.input', return_value='y'):
                success = github.ensure_authenticated()
                
            assert success is True
            assert mock_run.call_count == 2


class TestGitHubErrorHandling:
    """测试错误处理"""
    
    def test_network_error_handling(self):
        """测试网络错误处理"""
        github = GitHubIntegration("test-novel")
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Network error")
            
            success, error = github.create_novel_repo("test")
            
            assert success is False
            assert "Network error" in error
            
    def test_retry_on_failure(self):
        """测试失败重试机制"""
        github = GitHubIntegration("test-novel", max_retries=3)
        
        with patch('subprocess.run') as mock_run:
            # 前两次失败，第三次成功
            mock_run.side_effect = [
                MagicMock(returncode=1),
                MagicMock(returncode=1),
                MagicMock(returncode=0, stdout="Success")
            ]
            
            result = github.sync_with_retry({"test": "data"})
            
            assert result is True
            assert mock_run.call_count == 3
            
    def test_max_retries_exceeded(self):
        """测试超过最大重试次数"""
        github = GitHubIntegration("test-novel", max_retries=2)
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            
            result = github.sync_with_retry({"test": "data"})
            
            assert result is False
            assert mock_run.call_count == 2


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])