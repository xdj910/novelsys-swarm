"""
Agent任务调度器
负责任务分发、优先级管理和执行调度
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import heapq
from enum import Enum
import json

from .agent_executor import (
    AgentExecutor, 
    AgentTask, 
    AgentResult,
    AgentOrchestrator
)


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 1
    HIGH = 3
    NORMAL = 5
    LOW = 7
    BACKGROUND = 9


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduledTask:
    """调度任务"""
    id: str
    agent_name: str
    task: AgentTask
    priority: int
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[AgentResult] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __lt__(self, other):
        """用于优先队列排序"""
        return self.priority < other.priority


class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        """初始化任务队列"""
        self.queue = []
        self.task_map = {}
        self.counter = 0
        
    def add_task(self, task: ScheduledTask):
        """添加任务到队列"""
        self.counter += 1
        # 使用(优先级, 计数器, 任务)确保稳定排序
        heapq.heappush(self.queue, (task.priority, self.counter, task))
        self.task_map[task.id] = task
        
    def get_next_task(self) -> Optional[ScheduledTask]:
        """获取下一个任务"""
        while self.queue:
            _, _, task = heapq.heappop(self.queue)
            if task.status == TaskStatus.PENDING:
                return task
        return None
    
    def has_tasks(self) -> bool:
        """检查是否有待执行任务"""
        return any(
            task.status == TaskStatus.PENDING 
            for _, _, task in self.queue
        )
    
    def get_task_by_id(self, task_id: str) -> Optional[ScheduledTask]:
        """根据ID获取任务"""
        return self.task_map.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self.task_map.get(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True
        return False
    
    def get_queue_status(self) -> Dict:
        """获取队列状态"""
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = 0
        
        for _, _, task in self.queue:
            status_counts[task.status.value] += 1
        
        return {
            'total': len(self.queue),
            'by_status': status_counts,
            'pending': status_counts[TaskStatus.PENDING.value]
        }


class AgentDispatcher:
    """Agent任务调度器"""
    
    def __init__(self, max_concurrent: int = 1):
        """
        初始化调度器
        
        Args:
            max_concurrent: 最大并发任务数（Claude环境默认为1）
        """
        self.executor = AgentExecutor()
        self.orchestrator = AgentOrchestrator()
        self.task_queue = TaskQueue()
        self.max_concurrent = max_concurrent
        self.running_tasks = {}
        self.completed_tasks = []
        self.failed_tasks = []
        self.task_counter = 0
        self.callbacks = {}
        
    def schedule_task(
        self,
        agent_name: str,
        task: AgentTask,
        priority: TaskPriority = TaskPriority.NORMAL,
        callback: Optional[Callable] = None
    ) -> str:
        """
        调度任务
        
        Args:
            agent_name: Agent名称
            task: 任务
            priority: 优先级
            callback: 完成回调
            
        Returns:
            任务ID
        """
        self.task_counter += 1
        task_id = f"task_{self.task_counter:06d}"
        
        scheduled_task = ScheduledTask(
            id=task_id,
            agent_name=agent_name,
            task=task,
            priority=priority.value
        )
        
        self.task_queue.add_task(scheduled_task)
        
        if callback:
            self.callbacks[task_id] = callback
        
        print(f"Scheduled task {task_id} for agent {agent_name} with priority {priority.name}")
        
        return task_id
    
    def schedule_batch(
        self,
        tasks: List[tuple],
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> List[str]:
        """
        批量调度任务
        
        Args:
            tasks: (agent_name, task)元组列表
            priority: 优先级
            
        Returns:
            任务ID列表
        """
        task_ids = []
        
        for agent_name, task in tasks:
            task_id = self.schedule_task(agent_name, task, priority)
            task_ids.append(task_id)
        
        return task_ids
    
    async def run(self):
        """运行调度器主循环"""
        print("\n=== Agent Dispatcher Started ===")
        
        while self.task_queue.has_tasks() or self.running_tasks:
            # 检查是否可以启动新任务
            while (len(self.running_tasks) < self.max_concurrent and 
                   self.task_queue.has_tasks()):
                
                task = self.task_queue.get_next_task()
                if task:
                    asyncio.create_task(self._execute_task(task))
            
            # 等待一小段时间再检查
            await asyncio.sleep(0.1)
        
        print("\n=== Agent Dispatcher Completed ===")
        self._print_summary()
    
    async def run_until_complete(self, timeout: Optional[float] = None):
        """
        运行直到所有任务完成
        
        Args:
            timeout: 超时时间（秒）
        """
        try:
            if timeout:
                await asyncio.wait_for(self.run(), timeout=timeout)
            else:
                await self.run()
        except asyncio.TimeoutError:
            print(f"Dispatcher timed out after {timeout} seconds")
            await self.shutdown()
    
    async def _execute_task(self, task: ScheduledTask):
        """执行单个任务"""
        task_id = task.id
        
        try:
            # 更新任务状态
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            self.running_tasks[task_id] = task
            
            print(f"  Executing task {task_id}: {task.agent_name}")
            
            # 执行Agent
            result = await self.executor.execute_agent(
                task.agent_name,
                task.task
            )
            
            # 更新任务结果
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            
            # 移到完成列表
            del self.running_tasks[task_id]
            self.completed_tasks.append(task)
            
            print(f"  ✓ Task {task_id} completed successfully")
            
            # 执行回调
            if task_id in self.callbacks:
                callback = self.callbacks[task_id]
                await self._execute_callback(callback, task, result)
            
        except Exception as e:
            # 处理失败
            print(f"  ✗ Task {task_id} failed: {e}")
            
            task.retry_count += 1
            
            if task.retry_count < task.max_retries:
                # 重试
                print(f"  Retrying task {task_id} ({task.retry_count}/{task.max_retries})")
                task.status = TaskStatus.PENDING
                task.priority += 1  # 稍微降低优先级
                self.task_queue.add_task(task)
            else:
                # 最终失败
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()
                del self.running_tasks[task_id]
                self.failed_tasks.append(task)
    
    async def _execute_callback(
        self,
        callback: Callable,
        task: ScheduledTask,
        result: AgentResult
    ):
        """执行回调函数"""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(task, result)
            else:
                callback(task, result)
        except Exception as e:
            print(f"  Warning: Callback failed for task {task.id}: {e}")
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """获取任务状态"""
        task = self.task_queue.get_task_by_id(task_id)
        return task.status if task else None
    
    def get_task_result(self, task_id: str) -> Optional[AgentResult]:
        """获取任务结果"""
        # 检查完成的任务
        for task in self.completed_tasks:
            if task.id == task_id:
                return task.result
        
        # 检查失败的任务
        for task in self.failed_tasks:
            if task.id == task_id:
                return task.result
        
        return None
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        return self.task_queue.cancel_task(task_id)
    
    async def shutdown(self):
        """关闭调度器"""
        print("\n=== Shutting down dispatcher ===")
        
        # 取消所有待执行任务
        for _, _, task in self.task_queue.queue:
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CANCELLED
        
        # 等待运行中的任务完成（给一个超时）
        if self.running_tasks:
            print(f"Waiting for {len(self.running_tasks)} running tasks to complete...")
            
            for _ in range(30):  # 最多等待3秒
                if not self.running_tasks:
                    break
                await asyncio.sleep(0.1)
        
        self._print_summary()
    
    def _print_summary(self):
        """打印执行摘要"""
        print("\n=== Execution Summary ===")
        print(f"Total tasks: {self.task_counter}")
        print(f"Completed: {len(self.completed_tasks)}")
        print(f"Failed: {len(self.failed_tasks)}")
        print(f"Running: {len(self.running_tasks)}")
        
        queue_status = self.task_queue.get_queue_status()
        print(f"Pending: {queue_status['pending']}")
        print(f"Cancelled: {queue_status['by_status'].get(TaskStatus.CANCELLED.value, 0)}")
        
        # 打印失败任务详情
        if self.failed_tasks:
            print("\nFailed tasks:")
            for task in self.failed_tasks:
                print(f"  - {task.id}: {task.agent_name} (retries: {task.retry_count})")
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        total_execution_time = 0
        successful_execution_times = []
        
        for task in self.completed_tasks:
            if task.started_at and task.completed_at:
                exec_time = (task.completed_at - task.started_at).total_seconds()
                total_execution_time += exec_time
                successful_execution_times.append(exec_time)
        
        avg_execution_time = (
            sum(successful_execution_times) / len(successful_execution_times)
            if successful_execution_times else 0
        )
        
        return {
            'total_tasks': self.task_counter,
            'completed': len(self.completed_tasks),
            'failed': len(self.failed_tasks),
            'running': len(self.running_tasks),
            'pending': self.task_queue.get_queue_status()['pending'],
            'success_rate': (
                len(self.completed_tasks) / self.task_counter 
                if self.task_counter > 0 else 0
            ),
            'average_execution_time': avg_execution_time,
            'total_execution_time': total_execution_time
        }


class WorkflowDispatcher:
    """工作流调度器 - 处理复杂的多Agent工作流"""
    
    def __init__(self):
        """初始化工作流调度器"""
        self.dispatcher = AgentDispatcher()
        self.workflows = {}
        
    async def execute_chapter_workflow(
        self,
        chapter_number: int,
        bible: Dict,
        context: Dict
    ) -> Dict:
        """
        执行章节生成工作流
        
        Args:
            chapter_number: 章节号
            bible: Story Bible
            context: 上下文
            
        Returns:
            工作流执行结果
        """
        workflow_id = f"chapter_{chapter_number}"
        print(f"\n=== Starting Chapter {chapter_number} Workflow ===")
        
        # 定义工作流阶段
        stages = [
            {
                'name': 'Planning',
                'agents': [
                    ('director', AgentTask(
                        agent_name='director',
                        task_type='chapter_planning',
                        input_data={'chapter': chapter_number, 'bible': bible},
                        context=context,
                        priority=1
                    )),
                    ('outline-creator', AgentTask(
                        agent_name='outline-creator',
                        task_type='create_outline',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=2
                    ))
                ]
            },
            {
                'name': 'Generation',
                'agents': [
                    ('scene-painter', AgentTask(
                        agent_name='scene-painter',
                        task_type='paint_scenes',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=3
                    )),
                    ('dialogue-specialist', AgentTask(
                        agent_name='dialogue-specialist',
                        task_type='create_dialogue',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=3
                    )),
                    ('emotion-weaver', AgentTask(
                        agent_name='emotion-weaver',
                        task_type='weave_emotions',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=4
                    ))
                ]
            },
            {
                'name': 'Optimization',
                'agents': [
                    ('pacing-optimizer', AgentTask(
                        agent_name='pacing-optimizer',
                        task_type='optimize_pacing',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=5
                    )),
                    ('voice-tuner', AgentTask(
                        agent_name='voice-tuner',
                        task_type='tune_voice',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=5
                    ))
                ]
            },
            {
                'name': 'Validation',
                'agents': [
                    ('consistency-guardian', AgentTask(
                        agent_name='consistency-guardian',
                        task_type='check_consistency',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=6
                    )),
                    ('quality-scorer', AgentTask(
                        agent_name='quality-scorer',
                        task_type='score_quality',
                        input_data={'chapter': chapter_number},
                        context=context,
                        priority=7
                    ))
                ]
            }
        ]
        
        workflow_results = {
            'workflow_id': workflow_id,
            'stages': []
        }
        
        # 执行各阶段
        for stage in stages:
            print(f"\n  Stage: {stage['name']}")
            
            # 调度阶段内的所有Agent
            task_ids = []
            for agent_name, task in stage['agents']:
                task_id = self.dispatcher.schedule_task(
                    agent_name,
                    task,
                    TaskPriority.HIGH
                )
                task_ids.append(task_id)
            
            # 等待阶段完成
            await self._wait_for_tasks(task_ids)
            
            # 收集阶段结果
            stage_results = {
                'name': stage['name'],
                'tasks': []
            }
            
            for task_id in task_ids:
                result = self.dispatcher.get_task_result(task_id)
                if result:
                    stage_results['tasks'].append({
                        'task_id': task_id,
                        'agent': result.agent_name,
                        'success': result.success,
                        'execution_time': result.execution_time
                    })
            
            workflow_results['stages'].append(stage_results)
            
            # 检查是否需要中断工作流
            if not self._should_continue(stage_results):
                print(f"  ⚠ Stage {stage['name']} failed, stopping workflow")
                break
        
        # 运行调度器
        await self.dispatcher.run_until_complete()
        
        # 生成最终报告
        workflow_results['summary'] = self._generate_workflow_summary(workflow_results)
        
        return workflow_results
    
    async def _wait_for_tasks(self, task_ids: List[str]):
        """等待任务完成"""
        while True:
            all_done = True
            for task_id in task_ids:
                status = self.dispatcher.get_task_status(task_id)
                if status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                    all_done = False
                    break
            
            if all_done:
                break
            
            await asyncio.sleep(0.1)
    
    def _should_continue(self, stage_results: Dict) -> bool:
        """判断是否继续工作流"""
        # 如果有超过50%的任务失败，停止工作流
        total_tasks = len(stage_results['tasks'])
        failed_tasks = sum(
            1 for task in stage_results['tasks'] 
            if not task['success']
        )
        
        return failed_tasks < total_tasks / 2
    
    def _generate_workflow_summary(self, workflow_results: Dict) -> Dict:
        """生成工作流摘要"""
        total_tasks = 0
        successful_tasks = 0
        total_time = 0
        
        for stage in workflow_results['stages']:
            for task in stage['tasks']:
                total_tasks += 1
                if task['success']:
                    successful_tasks += 1
                total_time += task['execution_time']
        
        return {
            'total_stages': len(workflow_results['stages']),
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
            'total_execution_time': total_time
        }


# 导出主要类
__all__ = [
    'AgentDispatcher',
    'WorkflowDispatcher',
    'TaskQueue',
    'ScheduledTask',
    'TaskPriority',
    'TaskStatus'
]