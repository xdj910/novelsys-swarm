"""
命令执行器
处理和执行所有 /novel:* 命令
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
import os
from pathlib import Path
import yaml
import asyncio
from datetime import datetime

@dataclass
class CommandResult:
    """命令执行结果"""
    success: bool
    command: str
    message: str
    data: Optional[Dict] = None
    errors: List[str] = None


class CommandExecutor:
    """
    命令执行器
    负责解析和执行所有小说生成命令
    """
    
    def __init__(self, base_path: str = "D:\\NOVELSYS-SWARM"):
        """
        初始化命令执行器
        
        Args:
            base_path: 项目根目录
        """
        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data"
        self.commands_path = self.base_path / ".claude" / "commands"
        
        # 确保必要目录存在
        self._ensure_directories()
        
        # 加载命令定义
        self.command_registry = self._load_command_definitions()
        
        # 初始化组件
        self.bible_manager = BibleManager(self.data_path / "bibles")
        self.project_manager = ProjectManager(self.data_path / "projects")
        self.context_manager = ContextManager(self.data_path / "context")
        
    def _ensure_directories(self):
        """确保必要的目录结构存在"""
        directories = [
            self.data_path / "bibles",
            self.data_path / "chapters",
            self.data_path / "context",
            self.data_path / "projects",
            self.data_path / "logs",
            self.data_path / "memory"
        ]
        
        for dir_path in directories:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _load_command_definitions(self) -> Dict:
        """加载命令定义"""
        registry = {}
        
        # 扫描命令目录
        if self.commands_path.exists():
            for cmd_file in self.commands_path.glob("**/*.md"):
                # 从文件名提取命令名
                cmd_name = cmd_file.stem
                registry[cmd_name] = {
                    'file': cmd_file,
                    'category': cmd_file.parent.name
                }
        
        return registry
    
    async def execute(self, command: str, args: List[str] = None) -> CommandResult:
        """
        执行命令
        
        Args:
            command: 命令名称（如 'project-new'）
            args: 命令参数
            
        Returns:
            命令执行结果
        """
        # 移除 /novel: 前缀（如果有）
        if command.startswith('/novel:'):
            command = command[7:]
        
        # 路由到对应的执行器
        if command == 'init':
            return await self._execute_init()
        elif command == 'project-new':
            return await self._execute_project_new(args)
        elif command == 'project-switch':
            return await self._execute_project_switch(args)
        elif command == 'project-list':
            return await self._execute_project_list()
        elif command == 'status':
            return await self._execute_status()
        elif command == 'bible-create':
            return await self._execute_bible_create(args)
        elif command == 'bible-view':
            return await self._execute_bible_view()
        elif command == 'chapter-start':
            return await self._execute_chapter_start(args)
        elif command == 'quality-check':
            return await self._execute_quality_check(args)
        elif command == 'context-sync':
            return await self._execute_context_sync()
        else:
            return CommandResult(
                success=False,
                command=command,
                message=f"未知命令: {command}",
                errors=[f"命令 '{command}' 未定义"]
            )
    
    # ==================== 命令实现 ====================
    
    async def _execute_init(self) -> CommandResult:
        """执行初始化命令"""
        try:
            # 初始化系统结构
            self._ensure_directories()
            
            # 创建默认配置
            config = {
                'version': '2.0',
                'initialized_at': datetime.now().isoformat(),
                'default_quality_target': 90,
                'default_iteration_rounds': 2
            }
            
            config_path = self.data_path / "config.yaml"
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True)
            
            return CommandResult(
                success=True,
                command='init',
                message="系统初始化成功",
                data={'config_path': str(config_path)}
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='init',
                message="初始化失败",
                errors=[str(e)]
            )
    
    async def _execute_project_new(self, args: List[str]) -> CommandResult:
        """执行创建新项目命令"""
        if not args or len(args) < 1:
            return CommandResult(
                success=False,
                command='project-new',
                message="缺少项目名称",
                errors=["用法: /novel:project-new <项目名称>"]
            )
        
        project_name = args[0]
        
        try:
            # 创建项目
            project_data = await self.project_manager.create_project(project_name)
            
            # 触发头脑风暴（集成设计）
            brainstorm_result = await self._brainstorm_project(project_name)
            
            # 自动创建Bible
            bible_result = await self.bible_manager.create_bible(
                project_name,
                brainstorm_result.get('bible_template', {})
            )
            
            # 设置为当前项目
            await self.context_manager.set_current_project(project_name)
            
            return CommandResult(
                success=True,
                command='project-new',
                message=f"项目 '{project_name}' 创建成功",
                data={
                    'project': project_data,
                    'bible': bible_result,
                    'brainstorm': brainstorm_result
                }
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='project-new',
                message=f"创建项目失败",
                errors=[str(e)]
            )
    
    async def _execute_project_switch(self, args: List[str]) -> CommandResult:
        """执行切换项目命令"""
        if not args:
            return CommandResult(
                success=False,
                command='project-switch',
                message="缺少项目名称",
                errors=["用法: /novel:project-switch <项目名称>"]
            )
        
        project_name = args[0]
        
        try:
            # 检查项目是否存在
            if not await self.project_manager.project_exists(project_name):
                return CommandResult(
                    success=False,
                    command='project-switch',
                    message=f"项目 '{project_name}' 不存在",
                    errors=[f"请先创建项目: /novel:project-new {project_name}"]
                )
            
            # 切换项目
            await self.context_manager.set_current_project(project_name)
            
            # 加载项目context
            context = await self.context_manager.load_project_context(project_name)
            
            return CommandResult(
                success=True,
                command='project-switch',
                message=f"已切换到项目 '{project_name}'",
                data={'context': context}
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='project-switch',
                message="切换项目失败",
                errors=[str(e)]
            )
    
    async def _execute_project_list(self) -> CommandResult:
        """执行列出所有项目命令"""
        try:
            projects = await self.project_manager.list_projects()
            current = await self.context_manager.get_current_project()
            
            return CommandResult(
                success=True,
                command='project-list',
                message=f"找到 {len(projects)} 个项目",
                data={
                    'projects': projects,
                    'current': current
                }
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='project-list',
                message="获取项目列表失败",
                errors=[str(e)]
            )
    
    async def _execute_status(self) -> CommandResult:
        """执行状态查询命令"""
        try:
            current_project = await self.context_manager.get_current_project()
            
            if not current_project:
                return CommandResult(
                    success=True,
                    command='status',
                    message="当前没有活动项目",
                    data={'current_project': None}
                )
            
            # 获取项目状态
            project_status = await self.project_manager.get_project_status(current_project)
            
            # 获取Bible状态
            bible_status = await self.bible_manager.get_bible_status(current_project)
            
            # 获取章节进度
            chapter_progress = await self._get_chapter_progress(current_project)
            
            return CommandResult(
                success=True,
                command='status',
                message=f"项目 '{current_project}' 状态",
                data={
                    'project': project_status,
                    'bible': bible_status,
                    'chapters': chapter_progress
                }
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='status',
                message="获取状态失败",
                errors=[str(e)]
            )
    
    async def _execute_bible_create(self, args: List[str]) -> CommandResult:
        """执行创建Bible命令"""
        try:
            current_project = await self.context_manager.get_current_project()
            
            if not current_project:
                return CommandResult(
                    success=False,
                    command='bible-create',
                    message="没有活动项目",
                    errors=["请先创建或切换到项目"]
                )
            
            # 获取Bible模板
            template_name = args[0] if args else 'default'
            
            # 创建Bible
            bible_data = await self.bible_manager.create_bible(
                current_project,
                template=template_name
            )
            
            return CommandResult(
                success=True,
                command='bible-create',
                message=f"Bible创建成功",
                data={'bible': bible_data}
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='bible-create',
                message="创建Bible失败",
                errors=[str(e)]
            )
    
    async def _execute_bible_view(self) -> CommandResult:
        """执行查看Bible命令"""
        try:
            current_project = await self.context_manager.get_current_project()
            
            if not current_project:
                return CommandResult(
                    success=False,
                    command='bible-view',
                    message="没有活动项目",
                    errors=["请先创建或切换到项目"]
                )
            
            # 加载Bible
            bible = await self.bible_manager.load_bible(current_project)
            
            if not bible:
                return CommandResult(
                    success=False,
                    command='bible-view',
                    message="项目还没有Bible",
                    errors=["请先创建Bible: /novel:bible-create"]
                )
            
            return CommandResult(
                success=True,
                command='bible-view',
                message="Bible内容",
                data={'bible': bible}
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='bible-view',
                message="查看Bible失败",
                errors=[str(e)]
            )
    
    async def _execute_chapter_start(self, args: List[str]) -> CommandResult:
        """执行开始章节命令"""
        if not args:
            return CommandResult(
                success=False,
                command='chapter-start',
                message="缺少章节号",
                errors=["用法: /novel:chapter-start <章节号>"]
            )
        
        try:
            chapter_num = int(args[0])
            current_project = await self.context_manager.get_current_project()
            
            if not current_project:
                return CommandResult(
                    success=False,
                    command='chapter-start',
                    message="没有活动项目",
                    errors=["请先创建或切换到项目"]
                )
            
            # 这里应该调用实际的生成逻辑
            # 目前只是占位实现
            chapter_data = {
                'chapter_number': chapter_num,
                'status': 'generating',
                'message': '章节生成需要集成8-Stream系统'
            }
            
            return CommandResult(
                success=True,
                command='chapter-start',
                message=f"开始生成第{chapter_num}章",
                data={'chapter': chapter_data}
            )
            
        except ValueError:
            return CommandResult(
                success=False,
                command='chapter-start',
                message="章节号必须是数字",
                errors=[f"无效的章节号: {args[0]}"]
            )
        except Exception as e:
            return CommandResult(
                success=False,
                command='chapter-start',
                message="生成章节失败",
                errors=[str(e)]
            )
    
    async def _execute_quality_check(self, args: List[str]) -> CommandResult:
        """执行质量检查命令"""
        try:
            target = args[0] if args else 'all'
            
            # 这里应该调用质量评估系统
            # 目前只是占位实现
            quality_report = {
                'target': target,
                'overall_score': 85,
                'dimensions': {
                    'continuity': 90,
                    'character': 85,
                    'dialogue': 88,
                    'emotion': 82
                }
            }
            
            return CommandResult(
                success=True,
                command='quality-check',
                message=f"质量检查完成",
                data={'report': quality_report}
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='quality-check',
                message="质量检查失败",
                errors=[str(e)]
            )
    
    async def _execute_context_sync(self) -> CommandResult:
        """执行上下文同步命令"""
        try:
            current_project = await self.context_manager.get_current_project()
            
            if not current_project:
                return CommandResult(
                    success=False,
                    command='context-sync',
                    message="没有活动项目",
                    errors=["请先创建或切换到项目"]
                )
            
            # 同步上下文
            sync_result = await self.context_manager.sync_context(current_project)
            
            return CommandResult(
                success=True,
                command='context-sync',
                message="上下文同步成功",
                data={'sync': sync_result}
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                command='context-sync',
                message="上下文同步失败",
                errors=[str(e)]
            )
    
    # ==================== 辅助方法 ====================
    
    async def _brainstorm_project(self, project_name: str) -> Dict:
        """项目头脑风暴（简化实现）"""
        # 这里应该调用AI进行头脑风暴
        # 目前返回模拟数据
        return {
            'project_type': 'standalone',
            'genre': '都市言情',
            'themes': ['成长', '爱情', '梦想'],
            'bible_template': {
                'title': project_name,
                'genre': '都市言情',
                'themes': ['成长', '爱情', '梦想'],
                'chapters_planned': 30
            }
        }
    
    async def _get_chapter_progress(self, project_name: str) -> Dict:
        """获取章节进度"""
        chapters_path = self.data_path / "chapters" / project_name
        
        if not chapters_path.exists():
            return {
                'total': 0,
                'completed': 0,
                'in_progress': 0
            }
        
        completed = len(list(chapters_path.glob("chapter_*.md")))
        
        return {
            'total': 30,  # 应该从Bible中读取
            'completed': completed,
            'in_progress': 0
        }


# ==================== 管理器类 ====================

class ProjectManager:
    """项目管理器"""
    
    def __init__(self, projects_path: Path):
        self.projects_path = projects_path
        self.projects_path.mkdir(parents=True, exist_ok=True)
    
    async def create_project(self, project_name: str) -> Dict:
        """创建新项目"""
        project_path = self.projects_path / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # 创建项目配置
        project_data = {
            'name': project_name,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'type': 'standalone'
        }
        
        config_file = project_path / "project.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(project_data, f, allow_unicode=True)
        
        return project_data
    
    async def project_exists(self, project_name: str) -> bool:
        """检查项目是否存在"""
        project_path = self.projects_path / project_name
        return project_path.exists()
    
    async def list_projects(self) -> List[str]:
        """列出所有项目"""
        projects = []
        for path in self.projects_path.iterdir():
            if path.is_dir():
                projects.append(path.name)
        return projects
    
    async def get_project_status(self, project_name: str) -> Dict:
        """获取项目状态"""
        project_path = self.projects_path / project_name / "project.yaml"
        
        if not project_path.exists():
            return None
        
        with open(project_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)


class BibleManager:
    """Bible管理器"""
    
    def __init__(self, bibles_path: Path):
        self.bibles_path = bibles_path
        self.bibles_path.mkdir(parents=True, exist_ok=True)
    
    async def create_bible(self, project_name: str, template: Any = None) -> Dict:
        """创建Bible"""
        bible_path = self.bibles_path / f"{project_name}.yaml"
        
        # 创建Bible数据
        if isinstance(template, dict):
            bible_data = template
        else:
            bible_data = {
                'title': project_name,
                'created_at': datetime.now().isoformat(),
                'genre': '未定义',
                'themes': [],
                'chapters_planned': 30,
                'characters': {},
                'world_settings': {},
                'plot_outline': []
            }
        
        # 保存Bible
        with open(bible_path, 'w', encoding='utf-8') as f:
            yaml.dump(bible_data, f, allow_unicode=True)
        
        return bible_data
    
    async def load_bible(self, project_name: str) -> Optional[Dict]:
        """加载Bible"""
        bible_path = self.bibles_path / f"{project_name}.yaml"
        
        if not bible_path.exists():
            return None
        
        with open(bible_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    async def get_bible_status(self, project_name: str) -> Dict:
        """获取Bible状态"""
        bible = await self.load_bible(project_name)
        
        if not bible:
            return {'exists': False}
        
        return {
            'exists': True,
            'chapters_planned': bible.get('chapters_planned', 0),
            'characters_count': len(bible.get('characters', {})),
            'themes': bible.get('themes', [])
        }


class ContextManager:
    """上下文管理器"""
    
    def __init__(self, context_path: Path):
        self.context_path = context_path
        self.context_path.mkdir(parents=True, exist_ok=True)
        self.current_project_file = self.context_path / "current_project.json"
    
    async def get_current_project(self) -> Optional[str]:
        """获取当前项目"""
        if not self.current_project_file.exists():
            return None
        
        with open(self.current_project_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('current_project')
    
    async def set_current_project(self, project_name: str):
        """设置当前项目"""
        data = {
            'current_project': project_name,
            'switched_at': datetime.now().isoformat()
        }
        
        with open(self.current_project_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    async def load_project_context(self, project_name: str) -> Dict:
        """加载项目上下文"""
        context_file = self.context_path / f"{project_name}_context.json"
        
        if not context_file.exists():
            return {
                'project': project_name,
                'chapter_current': 0,
                'scene_current': 0,
                'character_states': {},
                'plot_progress': {}
            }
        
        with open(context_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def sync_context(self, project_name: str) -> Dict:
        """同步上下文"""
        # 简化实现：只是重新加载
        context = await self.load_project_context(project_name)
        
        # 更新时间戳
        context['last_sync'] = datetime.now().isoformat()
        
        # 保存
        context_file = self.context_path / f"{project_name}_context.json"
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, ensure_ascii=False, indent=2)
        
        return {'synced': True, 'timestamp': context['last_sync']}


# 测试函数
async def test_command_executor():
    """测试命令执行器"""
    executor = CommandExecutor()
    
    # 测试初始化
    result = await executor.execute('/novel:init')
    print(f"Init: {result.message}")
    
    # 测试创建项目
    result = await executor.execute('/novel:project-new', ['测试小说'])
    print(f"Project New: {result.message}")
    
    # 测试状态
    result = await executor.execute('/novel:status')
    print(f"Status: {result.message}")
    if result.data:
        print(f"  Data: {result.data}")
    
    return executor


if __name__ == "__main__":
    asyncio.run(test_command_executor())