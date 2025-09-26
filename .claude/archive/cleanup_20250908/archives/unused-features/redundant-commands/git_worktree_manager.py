"""
Git Worktree Manager for Multi-Chapter Parallel
多章节并行创作的Git Worktree管理
借鉴CCPM的worktree架构
"""

import os
import subprocess
import shutil
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)


class GitWorktreeManager:
    """
    Git Worktree管理器
    实现多章节并行创作
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).absolute()
        self.worktrees_dir = self.base_dir.parent / "novelsys-worktrees"
        self.active_worktrees = {}
        
        # 确保是git仓库
        if not (self.base_dir / ".git").exists():
            logger.warning(f"{self.base_dir}不是git仓库")
    
    def _run_git_command(self, args: List[str], cwd: Path = None) -> Tuple[bool, str]:
        """执行git命令"""
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                cwd=cwd or self.base_dir,
                encoding='utf-8'
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def create_chapter_worktree(self, chapter_num: int) -> Tuple[bool, Path]:
        """
        为章节创建独立的worktree
        """
        branch_name = f"chapter/{chapter_num}"
        worktree_path = self.worktrees_dir / f"chapter-{chapter_num}"
        
        # 检查worktree是否已存在
        if worktree_path.exists():
            logger.info(f"Worktree已存在: {worktree_path}")
            self.active_worktrees[chapter_num] = worktree_path
            return True, worktree_path
        
        # 创建worktrees目录
        self.worktrees_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查分支是否存在
        success, output = self._run_git_command(["branch", "--list", branch_name])
        branch_exists = branch_name in output if success else False
        
        if not branch_exists:
            # 创建新分支
            logger.info(f"创建新分支: {branch_name}")
            success, output = self._run_git_command(["checkout", "-b", branch_name])
            if not success:
                # 如果创建失败，可能是因为已在其他worktree中
                logger.info(f"尝试基于main创建分支")
                success, output = self._run_git_command(
                    ["branch", branch_name, "main"]
                )
            
            # 切回主分支
            self._run_git_command(["checkout", "main"])
        
        # 创建worktree
        logger.info(f"创建worktree: {worktree_path}")
        success, output = self._run_git_command([
            "worktree", "add", 
            str(worktree_path),
            branch_name
        ])
        
        if success:
            self.active_worktrees[chapter_num] = worktree_path
            logger.info(f"成功创建worktree: {worktree_path}")
            
            # 初始化章节结构
            self._initialize_chapter_structure(worktree_path, chapter_num)
            
            return True, worktree_path
        else:
            logger.error(f"创建worktree失败: {output}")
            return False, None
    
    def _initialize_chapter_structure(self, worktree_path: Path, chapter_num: int):
        """
        初始化章节目录结构
        """
        # 创建章节特定的目录
        dirs = [
            worktree_path / "data" / "chapters" / f"ch{chapter_num}",
            worktree_path / "data" / "analysis" / f"ch{chapter_num}",
            worktree_path / "data" / "streams" / f"ch{chapter_num}",
            worktree_path / "data" / "context" / f"ch{chapter_num}"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 创建章节元数据
        metadata = {
            "chapter_num": chapter_num,
            "branch": f"chapter/{chapter_num}",
            "worktree": str(worktree_path),
            "created_at": datetime.now().isoformat(),
            "status": "initialized"
        }
        
        metadata_file = worktree_path / "data" / "chapters" / f"ch{chapter_num}" / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"初始化章节{chapter_num}结构完成")
    
    def remove_chapter_worktree(self, chapter_num: int) -> bool:
        """
        移除章节worktree
        """
        if chapter_num not in self.active_worktrees:
            logger.warning(f"章节{chapter_num}的worktree不存在")
            return False
        
        worktree_path = self.active_worktrees[chapter_num]
        
        # 移除worktree
        success, output = self._run_git_command([
            "worktree", "remove", str(worktree_path), "--force"
        ])
        
        if success:
            del self.active_worktrees[chapter_num]
            logger.info(f"成功移除worktree: {worktree_path}")
            return True
        else:
            logger.error(f"移除worktree失败: {output}")
            return False
    
    def list_worktrees(self) -> List[Dict]:
        """
        列出所有worktree
        """
        success, output = self._run_git_command(["worktree", "list", "--porcelain"])
        
        if not success:
            return []
        
        worktrees = []
        current = {}
        
        for line in output.strip().split('\n'):
            if line.startswith("worktree "):
                if current:
                    worktrees.append(current)
                current = {"path": line[9:]}
            elif line.startswith("branch "):
                current["branch"] = line[7:]
            elif line.startswith("HEAD "):
                current["head"] = line[5:]
            elif line == "":
                if current:
                    worktrees.append(current)
                    current = {}
        
        if current:
            worktrees.append(current)
        
        return worktrees
    
    def sync_worktree_to_main(self, chapter_num: int) -> bool:
        """
        将worktree的更改合并回主分支
        """
        if chapter_num not in self.active_worktrees:
            logger.warning(f"章节{chapter_num}的worktree不存在")
            return False
        
        worktree_path = self.active_worktrees[chapter_num]
        branch_name = f"chapter/{chapter_num}"
        
        # 在worktree中提交更改
        logger.info(f"提交章节{chapter_num}的更改")
        
        # 添加所有更改
        success, output = self._run_git_command(
            ["add", "."],
            cwd=worktree_path
        )
        
        # 提交
        commit_message = f"完成第{chapter_num}章内容"
        success, output = self._run_git_command(
            ["commit", "-m", commit_message],
            cwd=worktree_path
        )
        
        if not success and "nothing to commit" not in output:
            logger.error(f"提交失败: {output}")
            return False
        
        # 切换到主分支并合并
        logger.info(f"合并章节{chapter_num}到主分支")
        
        # 在主仓库中操作
        self._run_git_command(["checkout", "main"])
        
        # 合并分支
        success, output = self._run_git_command([
            "merge", branch_name, "--no-ff",
            "-m", f"合并第{chapter_num}章内容"
        ])
        
        if success:
            logger.info(f"成功合并章节{chapter_num}")
            return True
        else:
            logger.error(f"合并失败: {output}")
            # 尝试解决冲突或回滚
            self._run_git_command(["merge", "--abort"])
            return False
    
    def create_parallel_chapters(self, chapter_nums: List[int]) -> Dict[int, Path]:
        """
        批量创建并行章节worktree
        """
        results = {}
        
        for chapter_num in chapter_nums:
            success, path = self.create_chapter_worktree(chapter_num)
            if success:
                results[chapter_num] = path
                logger.info(f"创建章节{chapter_num}的worktree: {path}")
            else:
                logger.error(f"创建章节{chapter_num}的worktree失败")
        
        return results
    
    def execute_in_worktree(self, chapter_num: int, command: str) -> Tuple[bool, str]:
        """
        在特定worktree中执行命令
        """
        if chapter_num not in self.active_worktrees:
            return False, f"章节{chapter_num}的worktree不存在"
        
        worktree_path = self.active_worktrees[chapter_num]
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=worktree_path,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def get_worktree_status(self, chapter_num: int) -> Optional[Dict]:
        """
        获取worktree状态
        """
        if chapter_num not in self.active_worktrees:
            return None
        
        worktree_path = self.active_worktrees[chapter_num]
        
        # 获取git状态
        success, output = self._run_git_command(
            ["status", "--porcelain"],
            cwd=worktree_path
        )
        
        if not success:
            return None
        
        # 解析状态
        modified_files = []
        new_files = []
        deleted_files = []
        
        for line in output.strip().split('\n'):
            if line:
                status = line[:2]
                file_path = line[3:]
                
                if 'M' in status:
                    modified_files.append(file_path)
                elif 'A' in status or '?' in status:
                    new_files.append(file_path)
                elif 'D' in status:
                    deleted_files.append(file_path)
        
        return {
            "chapter_num": chapter_num,
            "worktree_path": str(worktree_path),
            "branch": f"chapter/{chapter_num}",
            "modified": modified_files,
            "new": new_files,
            "deleted": deleted_files,
            "clean": len(modified_files) == 0 and len(new_files) == 0
        }
    
    def cleanup_all_worktrees(self):
        """
        清理所有worktree
        """
        for chapter_num in list(self.active_worktrees.keys()):
            self.remove_chapter_worktree(chapter_num)
        
        # 删除worktrees目录
        if self.worktrees_dir.exists():
            shutil.rmtree(self.worktrees_dir)
            logger.info(f"清理worktrees目录: {self.worktrees_dir}")


class ParallelChapterManager:
    """
    并行章节管理器
    结合Worktree和并行执行
    """
    
    def __init__(self):
        self.worktree_manager = GitWorktreeManager()
        self.active_chapters = {}
    
    async def start_parallel_chapters(self, chapter_ranges: List[Tuple[int, int]]) -> Dict:
        """
        启动多个章节的并行创作
        
        Args:
            chapter_ranges: [(1, 3), (5, 7)] 表示1-3章和5-7章并行
        """
        results = {}
        
        for start, end in chapter_ranges:
            for chapter_num in range(start, end + 1):
                # 创建worktree
                success, worktree_path = self.worktree_manager.create_chapter_worktree(
                    chapter_num
                )
                
                if success:
                    # 记录活跃章节
                    self.active_chapters[chapter_num] = {
                        "worktree": worktree_path,
                        "status": "ready",
                        "start_time": datetime.now()
                    }
                    
                    results[chapter_num] = "initialized"
                    logger.info(f"章节{chapter_num}准备就绪: {worktree_path}")
                else:
                    results[chapter_num] = "failed"
        
        return results
    
    def get_parallel_status(self) -> str:
        """
        获取并行状态报告
        """
        report = []
        report.append("## 📚 并行章节状态")
        report.append("")
        
        # 获取所有worktree
        worktrees = self.worktree_manager.list_worktrees()
        
        for wt in worktrees:
            if "chapter/" in wt.get("branch", ""):
                chapter_num = int(wt["branch"].split("/")[1])
                status = self.worktree_manager.get_worktree_status(chapter_num)
                
                if status:
                    emoji = "✅" if status["clean"] else "📝"
                    report.append(f"{emoji} 第{chapter_num}章")
                    report.append(f"   路径: {wt['path']}")
                    report.append(f"   修改: {len(status['modified'])}个文件")
                    report.append(f"   新增: {len(status['new'])}个文件")
                    report.append("")
        
        if not worktrees:
            report.append("暂无并行章节")
        
        return "\n".join(report)


# 使用示例
from datetime import datetime

if __name__ == "__main__":
    # 创建管理器
    manager = GitWorktreeManager()
    
    # 创建多个章节的worktree
    chapters = manager.create_parallel_chapters([1, 2, 3])
    print(f"创建了{len(chapters)}个章节worktree")
    
    # 在各个worktree中工作
    for chapter_num, path in chapters.items():
        print(f"\n章节{chapter_num}: {path}")
        
        # 模拟在worktree中创建内容
        content_file = path / "data" / "chapters" / f"ch{chapter_num}" / "content.md"
        content_file.write_text(f"# 第{chapter_num}章内容\n\n这是第{chapter_num}章的内容...")
        
        # 获取状态
        status = manager.get_worktree_status(chapter_num)
        print(f"状态: {status}")
    
    # 合并回主分支
    for chapter_num in chapters.keys():
        success = manager.sync_worktree_to_main(chapter_num)
        print(f"合并章节{chapter_num}: {'成功' if success else '失败'}")
    
    # 清理
    # manager.cleanup_all_worktrees()