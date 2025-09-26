"""
NOVELSYS-SWARM Agent基础架构
基于CCPM模式的Agent实现
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """Agent上下文数据"""
    project_name: str
    book_number: int = 1
    chapter_number: Optional[int] = None
    issue_id: Optional[str] = None
    bible_path: Optional[Path] = None
    context_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context_data is None:
            self.context_data = {}


@dataclass
class AgentResult:
    """Agent执行结果"""
    success: bool
    content: Any
    quality_score: float
    execution_time: float
    errors: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class BaseAgent:
    """基础Agent类 - 所有专门Agent的父类"""
    
    def __init__(self, name: str, specialization: str):
        self.name = name
        self.specialization = specialization
        self.context: Optional[AgentContext] = None
        self.start_time = None
        self.thinking_mode = "think"  # 默认思考模式
        
    async def initialize(self, context: AgentContext):
        """初始化Agent上下文"""
        self.context = context
        await self.load_context_data()
        logger.info(f"Agent {self.name} initialized with context: {context.project_name}")
        
    async def load_context_data(self):
        """加载上下文数据"""
        if self.context.bible_path and self.context.bible_path.exists():
            with open(self.context.bible_path, 'r', encoding='utf-8') as f:
                bible_data = json.load(f)
                self.context.context_data.update(bible_data)
                
    async def execute(self, task: Dict[str, Any]) -> AgentResult:
        """执行任务的主方法"""
        self.start_time = datetime.now()
        
        try:
            # 验证任务
            await self.validate_task(task)
            
            # 执行前准备
            await self.pre_execute(task)
            
            # 执行核心任务
            result = await self.perform_task(task)
            
            # 执行后处理
            await self.post_execute(result)
            
            # 质量检查
            quality_score = await self.check_quality(result)
            
            execution_time = (datetime.now() - self.start_time).total_seconds()
            
            return AgentResult(
                success=True,
                content=result,
                quality_score=quality_score,
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Agent {self.name} execution failed: {str(e)}")
            execution_time = (datetime.now() - self.start_time).total_seconds()
            return AgentResult(
                success=False,
                content=None,
                quality_score=0.0,
                execution_time=execution_time,
                errors=[str(e)]
            )
    
    async def validate_task(self, task: Dict[str, Any]):
        """验证任务有效性"""
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in task:
                raise ValueError(f"Missing required field: {field}")
    
    def get_required_fields(self) -> List[str]:
        """获取必需的任务字段 - 子类应重写"""
        return ["type"]
    
    async def pre_execute(self, task: Dict[str, Any]):
        """执行前准备 - 子类可重写"""
        pass
    
    async def perform_task(self, task: Dict[str, Any]) -> Any:
        """执行核心任务 - 子类必须实现"""
        raise NotImplementedError(f"Agent {self.name} must implement perform_task")
    
    async def post_execute(self, result: Any):
        """执行后处理 - 子类可重写"""
        pass
    
    async def check_quality(self, result: Any) -> float:
        """检查结果质量 - 子类应重写"""
        return 90.0  # 默认质量分数
    
    def set_thinking_mode(self, mode: str):
        """设置思考模式"""
        valid_modes = ["think", "think-hard", "think-harder", "ultrathink"]
        if mode in valid_modes:
            self.thinking_mode = mode
            logger.info(f"Agent {self.name} thinking mode set to: {mode}")
        else:
            raise ValueError(f"Invalid thinking mode: {mode}")


class DirectorAgent(BaseAgent):
    """导演Agent - 最高层决策者"""
    
    def __init__(self):
        super().__init__("NovelDirector", "strategic_coordination")
        self.epic_coordinators = []
        self.task_queue = []
        
    async def decompose_project(self, project_spec: Dict[str, Any]) -> List[Dict]:
        """分解项目为Epic级别任务"""
        epics = []
        
        if project_spec.get("type") == "new_series":
            # 新系列需要完整Bible创建
            epics.append({
                "id": "EPIC-001",
                "type": "bible_creation",
                "title": "Create Series Bible",
                "priority": 1,
                "thinking_mode": "ultrathink"
            })
            
        elif project_spec.get("type") == "sequel":
            # 续集需要Bible进化
            epics.append({
                "id": "EPIC-001",
                "type": "bible_evolution",
                "title": "Evolve Bible for Sequel",
                "priority": 1,
                "thinking_mode": "think-harder"
            })
        
        # 添加章节创作Epic
        for i in range(1, project_spec.get("chapter_count", 10) + 1):
            epics.append({
                "id": f"EPIC-CH{i:03d}",
                "type": "chapter_creation",
                "title": f"Create Chapter {i}",
                "priority": 2,
                "chapter_number": i,
                "thinking_mode": "think-hard"
            })
        
        return epics
    
    async def perform_task(self, task: Dict[str, Any]) -> Any:
        """执行导演任务"""
        if task["type"] == "project_initialization":
            return await self.decompose_project(task["project_spec"])
        elif task["type"] == "coordinate_epics":
            return await self.coordinate_epic_execution(task["epics"])
        else:
            raise ValueError(f"Unknown director task type: {task['type']}")
    
    async def coordinate_epic_execution(self, epics: List[Dict]) -> Dict:
        """协调Epic执行"""
        results = {}
        
        # 按优先级分组
        priority_groups = {}
        for epic in epics:
            priority = epic.get("priority", 99)
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(epic)
        
        # 按优先级顺序执行
        for priority in sorted(priority_groups.keys()):
            group_epics = priority_groups[priority]
            
            # 并行执行同优先级的Epic
            tasks = []
            for epic in group_epics:
                # 这里应该调用实际的Epic Coordinator
                # 现在只是模拟
                tasks.append(self.simulate_epic_execution(epic))
            
            group_results = await asyncio.gather(*tasks)
            
            for epic, result in zip(group_epics, group_results):
                results[epic["id"]] = result
        
        return results
    
    async def simulate_epic_execution(self, epic: Dict) -> Dict:
        """模拟Epic执行（实际应调用Epic Coordinator）"""
        await asyncio.sleep(0.1)  # 模拟执行时间
        return {
            "epic_id": epic["id"],
            "status": "completed",
            "quality_score": 95.0
        }