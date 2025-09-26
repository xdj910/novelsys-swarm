"""
Agent执行框架
负责Agent的加载、执行和协调
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import asyncio
import yaml
import json
from pathlib import Path
import re
from datetime import datetime

@dataclass
class AgentDefinition:
    """Agent定义"""
    name: str
    description: str
    tools: List[str]
    category: str
    content: str
    stream: Optional[str] = None
    dependencies: List[str] = None
    parallel_safe: bool = True
    
@dataclass
class AgentTask:
    """Agent任务"""
    agent_name: str
    task_type: str
    input_data: Dict
    context: Dict
    priority: int = 5
    dependencies: List[str] = None
    
@dataclass
class AgentResult:
    """Agent执行结果"""
    agent_name: str
    task_type: str
    success: bool
    output: Any
    execution_time: float
    errors: List[str] = None
    warnings: List[str] = None


class AgentLoader:
    """Agent加载器"""
    
    def __init__(self, agents_dir: str = "D:\\NOVELSYS-SWARM\\.claude\\agents"):
        """初始化Agent加载器"""
        self.agents_dir = Path(agents_dir)
        self.agents_cache = {}
        self.category_map = {}
        
    def load_all_agents(self) -> Dict[str, AgentDefinition]:
        """加载所有Agent定义"""
        if self.agents_cache:
            return self.agents_cache
            
        for category_dir in self.agents_dir.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                self.category_map[category] = []
                
                for agent_file in category_dir.glob("*.md"):
                    agent_def = self._load_agent_file(agent_file, category)
                    if agent_def:
                        self.agents_cache[agent_def.name] = agent_def
                        self.category_map[category].append(agent_def.name)
                        
        return self.agents_cache
    
    def _load_agent_file(self, file_path: Path, category: str) -> Optional[AgentDefinition]:
        """加载单个Agent文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 解析YAML前言
            yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            if not yaml_match:
                return None
                
            metadata = yaml.safe_load(yaml_match.group(1))
            agent_content = yaml_match.group(2).strip()
            
            # 解析Stream信息（如果存在）
            stream = None
            if "Stream_" in agent_content:
                stream_match = re.search(r'Stream_([A-D])_', agent_content)
                if stream_match:
                    stream = stream_match.group(1)
            
            return AgentDefinition(
                name=metadata.get('name'),
                description=metadata.get('description', ''),
                tools=metadata.get('tools', []),
                category=category,
                content=agent_content,
                stream=stream,
                dependencies=metadata.get('dependencies', []),
                parallel_safe=metadata.get('parallel_safe', True)
            )
            
        except Exception as e:
            print(f"Error loading agent from {file_path}: {e}")
            return None
    
    def get_agent(self, name: str) -> Optional[AgentDefinition]:
        """获取特定Agent"""
        if not self.agents_cache:
            self.load_all_agents()
        return self.agents_cache.get(name)
    
    def get_agents_by_category(self, category: str) -> List[AgentDefinition]:
        """按类别获取Agent"""
        if not self.agents_cache:
            self.load_all_agents()
        
        agent_names = self.category_map.get(category, [])
        return [self.agents_cache[name] for name in agent_names]
    
    def get_agents_by_stream(self, stream: str) -> List[AgentDefinition]:
        """按Stream获取Agent"""
        if not self.agents_cache:
            self.load_all_agents()
            
        return [
            agent for agent in self.agents_cache.values()
            if agent.stream == stream
        ]


class AgentExecutor:
    """Agent执行器"""
    
    def __init__(self):
        """初始化Agent执行器"""
        self.loader = AgentLoader()
        self.execution_history = []
        self.active_tasks = {}
        self.context_manager = ContextManager()
        
    async def execute_agent(
        self, 
        agent_name: str, 
        task: AgentTask,
        mode: str = 'standalone'
    ) -> AgentResult:
        """
        执行单个Agent
        
        Args:
            agent_name: Agent名称
            task: Agent任务
            mode: 执行模式 (standalone/stream/coordinated)
            
        Returns:
            Agent执行结果
        """
        start_time = asyncio.get_event_loop().time()
        errors = []
        warnings = []
        
        # 加载Agent定义
        agent_def = self.loader.get_agent(agent_name)
        if not agent_def:
            return AgentResult(
                agent_name=agent_name,
                task_type=task.task_type,
                success=False,
                output=None,
                execution_time=0,
                errors=[f"Agent {agent_name} not found"]
            )
        
        try:
            # 准备执行上下文
            execution_context = self._prepare_context(agent_def, task)
            
            # 根据Agent类别执行不同逻辑
            if agent_def.category == 'generation':
                output = await self._execute_generation_agent(agent_def, task, execution_context)
            elif agent_def.category == 'optimization':
                output = await self._execute_optimization_agent(agent_def, task, execution_context)
            elif agent_def.category == 'validation':
                output = await self._execute_validation_agent(agent_def, task, execution_context)
            elif agent_def.category == 'coordination':
                output = await self._execute_coordination_agent(agent_def, task, execution_context)
            elif agent_def.category == 'bible':
                output = await self._execute_bible_agent(agent_def, task, execution_context)
            elif agent_def.category == 'memory':
                output = await self._execute_memory_agent(agent_def, task, execution_context)
            elif agent_def.category == 'detail':
                output = await self._execute_detail_agent(agent_def, task, execution_context)
            elif agent_def.category == 'quality':
                output = await self._execute_quality_agent(agent_def, task, execution_context)
            else:
                output = await self._execute_generic_agent(agent_def, task, execution_context)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # 记录执行历史
            self._record_execution(agent_name, task, output, execution_time)
            
            return AgentResult(
                agent_name=agent_name,
                task_type=task.task_type,
                success=True,
                output=output,
                execution_time=execution_time,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            return AgentResult(
                agent_name=agent_name,
                task_type=task.task_type,
                success=False,
                output=None,
                execution_time=execution_time,
                errors=[str(e)]
            )
    
    async def execute_parallel_agents(
        self,
        tasks: List[Tuple[str, AgentTask]]
    ) -> List[AgentResult]:
        """
        并行执行多个Agent（在Claude环境中实际是顺序执行）
        
        Args:
            tasks: (agent_name, task)元组列表
            
        Returns:
            执行结果列表
        """
        # 检查并行安全性
        parallel_safe_tasks = []
        sequential_tasks = []
        
        for agent_name, task in tasks:
            agent_def = self.loader.get_agent(agent_name)
            if agent_def and agent_def.parallel_safe:
                parallel_safe_tasks.append((agent_name, task))
            else:
                sequential_tasks.append((agent_name, task))
        
        results = []
        
        # 执行并行安全的任务（Claude环境中仍是顺序）
        if parallel_safe_tasks:
            # 在真实环境中这里会是 asyncio.gather
            # 但在Claude中我们顺序执行
            for agent_name, task in parallel_safe_tasks:
                result = await self.execute_agent(agent_name, task)
                results.append(result)
        
        # 执行必须顺序的任务
        for agent_name, task in sequential_tasks:
            result = await self.execute_agent(agent_name, task)
            results.append(result)
        
        return results
    
    async def execute_stream(
        self,
        stream_id: str,
        tasks: List[AgentTask]
    ) -> Dict:
        """
        执行Stream中的所有Agent
        
        Args:
            stream_id: Stream标识 (A/B/C/D)
            tasks: 任务列表
            
        Returns:
            Stream执行结果
        """
        stream_agents = self.loader.get_agents_by_stream(stream_id)
        
        if not stream_agents:
            return {
                'stream': stream_id,
                'success': False,
                'error': f"No agents found for stream {stream_id}"
            }
        
        # 按依赖关系排序任务
        sorted_tasks = self._sort_tasks_by_dependencies(tasks)
        
        results = []
        for task in sorted_tasks:
            # 找到对应的Agent
            agent = self._match_agent_to_task(stream_agents, task)
            if agent:
                result = await self.execute_agent(agent.name, task, mode='stream')
                results.append(result)
        
        return {
            'stream': stream_id,
            'success': all(r.success for r in results),
            'results': results,
            'summary': self._summarize_stream_results(results)
        }
    
    def _prepare_context(self, agent_def: AgentDefinition, task: AgentTask) -> Dict:
        """准备执行上下文"""
        context = {
            'agent_info': {
                'name': agent_def.name,
                'category': agent_def.category,
                'stream': agent_def.stream,
                'tools': agent_def.tools
            },
            'task_info': task.__dict__,
            'global_context': self.context_manager.get_global_context(),
            'execution_time': datetime.now().isoformat()
        }
        
        # 添加依赖Agent的输出
        if task.dependencies:
            context['dependency_outputs'] = {}
            for dep in task.dependencies:
                if dep in self.execution_history:
                    context['dependency_outputs'][dep] = self.execution_history[dep]
        
        return context
    
    async def _execute_generation_agent(
        self, 
        agent_def: AgentDefinition, 
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行生成类Agent"""
        # 简化实现：返回模拟生成结果
        return {
            'type': 'generation',
            'content': f"Generated content by {agent_def.name}",
            'task': task.task_type,
            'quality_score': 0.85
        }
    
    async def _execute_optimization_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行优化类Agent"""
        return {
            'type': 'optimization',
            'optimizations': [
                'Improved pacing',
                'Enhanced dialogue flow',
                'Refined descriptions'
            ],
            'improvement_score': 0.15
        }
    
    async def _execute_validation_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行验证类Agent"""
        return {
            'type': 'validation',
            'validation_passed': True,
            'issues_found': [],
            'quality_metrics': {
                'consistency': 0.92,
                'completeness': 0.88,
                'accuracy': 0.95
            }
        }
    
    async def _execute_coordination_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行协调类Agent"""
        if agent_def.name == 'director':
            return await self._execute_director_agent(agent_def, task, context)
        
        return {
            'type': 'coordination',
            'coordinated_agents': [],
            'conflicts_resolved': [],
            'decisions_made': []
        }
    
    async def _execute_director_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行导演Agent"""
        # Director的特殊逻辑
        return {
            'type': 'direction',
            'streams_coordinated': ['A', 'B', 'C', 'D'],
            'issues_decomposed': 10,
            'gate_enforcement': {
                'current_stage': 3,
                'completion': 0.85,
                'threshold': 0.80,
                'passed': True
            },
            'next_cycle_plan': {
                'priority_streams': ['A', 'C'],
                'focus_areas': ['character_development', 'world_building']
            }
        }
    
    async def _execute_bible_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行Bible管理类Agent"""
        return {
            'type': 'bible_management',
            'bible_updates': [],
            'consistency_checks': [],
            'world_building': {}
        }
    
    async def _execute_memory_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行记忆管理类Agent"""
        return {
            'type': 'memory_management',
            'context_updated': True,
            'memories_stored': 5,
            'memories_retrieved': 3
        }
    
    async def _execute_detail_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行细节增强类Agent"""
        return {
            'type': 'detail_enhancement',
            'details_added': [
                'Cultural elements',
                'Environmental details',
                'Sensory descriptions'
            ]
        }
    
    async def _execute_quality_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行质量保证类Agent"""
        return {
            'type': 'quality_assurance',
            'quality_score': 0.88,
            'issues_detected': [],
            'improvements_suggested': []
        }
    
    async def _execute_generic_agent(
        self,
        agent_def: AgentDefinition,
        task: AgentTask,
        context: Dict
    ) -> Dict:
        """执行通用Agent"""
        return {
            'type': 'generic',
            'agent': agent_def.name,
            'task': task.task_type,
            'output': 'Generic execution completed'
        }
    
    def _sort_tasks_by_dependencies(self, tasks: List[AgentTask]) -> List[AgentTask]:
        """按依赖关系排序任务"""
        # 简化实现：按优先级排序
        return sorted(tasks, key=lambda t: t.priority)
    
    def _match_agent_to_task(
        self, 
        agents: List[AgentDefinition], 
        task: AgentTask
    ) -> Optional[AgentDefinition]:
        """匹配任务到Agent"""
        # 尝试精确匹配
        for agent in agents:
            if agent.name == task.agent_name:
                return agent
        
        # 尝试模糊匹配
        for agent in agents:
            if task.task_type.lower() in agent.name.lower():
                return agent
        
        return agents[0] if agents else None
    
    def _summarize_stream_results(self, results: List[AgentResult]) -> Dict:
        """总结Stream执行结果"""
        return {
            'total_agents': len(results),
            'successful': sum(1 for r in results if r.success),
            'failed': sum(1 for r in results if not r.success),
            'average_execution_time': sum(r.execution_time for r in results) / len(results) if results else 0,
            'errors': [e for r in results if r.errors for e in r.errors]
        }
    
    def _record_execution(
        self,
        agent_name: str,
        task: AgentTask,
        output: Any,
        execution_time: float
    ):
        """记录执行历史"""
        self.execution_history.append({
            'agent': agent_name,
            'task': task.task_type,
            'output': output,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        })


class AgentOrchestrator:
    """Agent编排器 - 负责高级协调"""
    
    def __init__(self):
        """初始化编排器"""
        self.executor = AgentExecutor()
        self.loader = AgentLoader()
        self.issue_tracker = IssueTracker()
        
    async def execute_chapter_generation(
        self,
        chapter_number: int,
        bible: Dict,
        context: Dict
    ) -> Dict:
        """
        执行完整章节生成流程
        
        Args:
            chapter_number: 章节号
            bible: Story Bible
            context: 上下文
            
        Returns:
            章节生成结果
        """
        print(f"\n=== 开始生成第{chapter_number}章 ===")
        
        # 1. Director分解任务为Issues
        issues = await self._decompose_chapter_to_issues(chapter_number, bible, context)
        
        # 2. 按并行组执行Issues
        results = await self._execute_issue_groups(issues)
        
        # 3. Stream整合
        integrated_content = await self._integrate_stream_outputs(results)
        
        # 4. 质量验证
        quality_result = await self._validate_quality(integrated_content)
        
        # 5. 全局优化（如果需要）
        if quality_result['score'] < 0.90:
            integrated_content = await self._apply_global_optimization(integrated_content)
        
        return {
            'chapter_number': chapter_number,
            'content': integrated_content,
            'quality': quality_result,
            'execution_summary': self._summarize_execution(results)
        }
    
    async def _decompose_chapter_to_issues(
        self,
        chapter_number: int,
        bible: Dict,
        context: Dict
    ) -> List[Dict]:
        """分解章节为Issues"""
        # 执行Director Agent进行任务分解
        director_task = AgentTask(
            agent_name='director',
            task_type='decompose_chapter',
            input_data={
                'chapter_number': chapter_number,
                'bible': bible
            },
            context=context,
            priority=1
        )
        
        result = await self.executor.execute_agent('director', director_task)
        
        # 生成Issues列表
        base_issues = [
            {
                'id': f'ch{chapter_number}_001',
                'title': 'Chapter Structure & Outline',
                'agent': 'outline-creator',
                'stream': 'B',
                'group': 1,
                'dependencies': []
            },
            {
                'id': f'ch{chapter_number}_002',
                'title': 'Character Psychology',
                'agent': 'character-psychologist',
                'stream': 'A',
                'group': 2,
                'dependencies': ['ch{chapter_number}_001']
            },
            {
                'id': f'ch{chapter_number}_003',
                'title': 'World Building & Setting',
                'agent': 'world-builder',
                'stream': 'C',
                'group': 1,
                'dependencies': []
            },
            {
                'id': f'ch{chapter_number}_004',
                'title': 'Scene Descriptions',
                'agent': 'scene-painter',
                'stream': 'D',
                'group': 2,
                'dependencies': ['ch{chapter_number}_003']
            },
            {
                'id': f'ch{chapter_number}_005',
                'title': 'Dialogue Creation',
                'agent': 'dialogue-specialist',
                'stream': 'A',
                'group': 3,
                'dependencies': ['ch{chapter_number}_002']
            },
            {
                'id': f'ch{chapter_number}_006',
                'title': 'Emotion Weaving',
                'agent': 'emotion-weaver',
                'stream': 'A',
                'group': 3,
                'dependencies': ['ch{chapter_number}_005']
            },
            {
                'id': f'ch{chapter_number}_007',
                'title': 'Pacing Optimization',
                'agent': 'pacing-optimizer',
                'stream': 'B',
                'group': 4,
                'dependencies': ['ch{chapter_number}_004', 'ch{chapter_number}_005']
            },
            {
                'id': f'ch{chapter_number}_008',
                'title': 'Voice Tuning',
                'agent': 'voice-tuner',
                'stream': 'D',
                'group': 4,
                'dependencies': ['ch{chapter_number}_007']
            },
            {
                'id': f'ch{chapter_number}_009',
                'title': 'Quality Assessment',
                'agent': 'quality-scorer',
                'stream': 'validation',
                'group': 5,
                'dependencies': ['ch{chapter_number}_008']
            }
        ]
        
        return base_issues
    
    async def _execute_issue_groups(self, issues: List[Dict]) -> Dict:
        """按组执行Issues"""
        results = {}
        
        # 获取所有组
        groups = sorted(set(issue['group'] for issue in issues))
        
        for group_num in groups:
            print(f"  执行第{group_num}组Issues...")
            
            # 获取当前组的Issues
            group_issues = [i for i in issues if i['group'] == group_num]
            
            # 准备任务
            tasks = []
            for issue in group_issues:
                task = AgentTask(
                    agent_name=issue['agent'],
                    task_type=issue['title'],
                    input_data={'issue': issue},
                    context={'dependencies': issue['dependencies']},
                    priority=group_num
                )
                tasks.append((issue['agent'], task))
            
            # 执行组内任务
            group_results = await self.executor.execute_parallel_agents(tasks)
            
            # 存储结果
            for issue, result in zip(group_issues, group_results):
                results[issue['id']] = result
        
        return results
    
    async def _integrate_stream_outputs(self, results: Dict) -> Dict:
        """整合Stream输出"""
        # 按Stream分组结果
        stream_outputs = {
            'A': [],  # Character
            'B': [],  # Narrative
            'C': [],  # World
            'D': []   # Prose
        }
        
        for issue_id, result in results.items():
            if result.success and 'stream' in result.output:
                stream = result.output.get('stream', 'D')
                stream_outputs[stream].append(result.output)
        
        # 整合各Stream输出
        integrated = {
            'character_elements': self._merge_outputs(stream_outputs['A']),
            'narrative_structure': self._merge_outputs(stream_outputs['B']),
            'world_building': self._merge_outputs(stream_outputs['C']),
            'prose_craft': self._merge_outputs(stream_outputs['D'])
        }
        
        return integrated
    
    async def _validate_quality(self, content: Dict) -> Dict:
        """验证质量"""
        # 执行质量验证Agent
        validation_task = AgentTask(
            agent_name='quality-scorer',
            task_type='validate_chapter',
            input_data={'content': content},
            context={},
            priority=1
        )
        
        result = await self.executor.execute_agent('quality-scorer', validation_task)
        
        if result.success:
            return result.output
        else:
            return {
                'score': 0.75,
                'passed': False,
                'issues': ['Quality validation failed']
            }
    
    async def _apply_global_optimization(self, content: Dict) -> Dict:
        """应用全局优化"""
        # 这里可以调用之前实现的GlobalOptimizer
        print("  应用全局优化...")
        
        # 简化实现
        optimized = content.copy()
        optimized['optimization_applied'] = True
        optimized['quality_boost'] = 0.05
        
        return optimized
    
    def _merge_outputs(self, outputs: List[Dict]) -> Dict:
        """合并输出"""
        merged = {}
        for output in outputs:
            merged.update(output)
        return merged
    
    def _summarize_execution(self, results: Dict) -> Dict:
        """总结执行情况"""
        total = len(results)
        successful = sum(1 for r in results.values() if r.success)
        
        return {
            'total_issues': total,
            'successful': successful,
            'failed': total - successful,
            'success_rate': successful / total if total > 0 else 0
        }


class IssueTracker:
    """Issue追踪器"""
    
    def __init__(self):
        """初始化Issue追踪器"""
        self.issues = {}
        self.dependencies = {}
        
    def register_issue(self, issue: Dict):
        """注册Issue"""
        self.issues[issue['id']] = issue
        
        # 记录依赖关系
        for dep in issue.get('dependencies', []):
            if dep not in self.dependencies:
                self.dependencies[dep] = []
            self.dependencies[dep].append(issue['id'])
    
    def get_ready_issues(self, completed: List[str]) -> List[Dict]:
        """获取准备就绪的Issues"""
        ready = []
        
        for issue_id, issue in self.issues.items():
            if issue_id in completed:
                continue
                
            # 检查依赖是否都已完成
            deps = issue.get('dependencies', [])
            if all(dep in completed for dep in deps):
                ready.append(issue)
        
        return ready
    
    def mark_completed(self, issue_id: str):
        """标记Issue完成"""
        if issue_id in self.issues:
            self.issues[issue_id]['status'] = 'completed'


class ContextManager:
    """上下文管理器"""
    
    def __init__(self):
        """初始化上下文管理器"""
        self.global_context = {}
        self.stream_contexts = {
            'A': {},  # Character
            'B': {},  # Narrative
            'C': {},  # World
            'D': {}   # Prose
        }
        
    def get_global_context(self) -> Dict:
        """获取全局上下文"""
        return self.global_context.copy()
    
    def update_global_context(self, updates: Dict):
        """更新全局上下文"""
        self.global_context.update(updates)
    
    def get_stream_context(self, stream: str) -> Dict:
        """获取Stream上下文"""
        return self.stream_contexts.get(stream, {}).copy()
    
    def update_stream_context(self, stream: str, updates: Dict):
        """更新Stream上下文"""
        if stream in self.stream_contexts:
            self.stream_contexts[stream].update(updates)


# 导出主要类
__all__ = [
    'AgentLoader',
    'AgentExecutor',
    'AgentOrchestrator',
    'AgentTask',
    'AgentResult',
    'IssueTracker',
    'ContextManager'
]