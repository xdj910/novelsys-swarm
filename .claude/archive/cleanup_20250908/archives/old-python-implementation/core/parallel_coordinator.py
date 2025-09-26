"""
Parallel Coordinator Implementation
实现真正的并行执行逻辑
基于CCPM的parallel-worker模式
"""

import asyncio
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import logging

from .context_firewall import AgentResponse, ContextFirewall, StreamFirewall
from .agent_type_mapper import DynamicAgentPool, ChapterType
from .execution_status import ExecutionStatusTracker
from .github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class StreamTask:
    """Stream任务定义"""
    stream_name: str
    agent_name: str
    chapter_num: int
    chapter_context: Dict
    bible_context: Dict
    priority: int = 5
    

class NovelParallelCoordinator:
    """
    小说并行执行协调器
    管理8个Stream的并行处理
    """
    
    # 8个核心Stream定义
    EIGHT_STREAMS = [
        ("Character Psychology", "character-psychology-specialist"),
        ("Narrative Structure", "narrative-structure-specialist"),
        ("World Building", "world-building-specialist"),
        ("Prose Craft", "prose-craft-specialist"),
        ("Continuity Guard", "continuity-guard-specialist"),
        ("Foreshadowing", "foreshadowing-specialist"),
        ("Dialogue Master", "dialogue-master-specialist"),
        ("Emotion Weaver", "emotion-weaver-specialist")
    ]
    
    def __init__(self, github_integration: GitHubIntegration = None):
        self.github = github_integration
        self.status_tracker = ExecutionStatusTracker()
        self.agent_pool = DynamicAgentPool()
        self.stream_firewall = StreamFirewall()
        self.current_tasks = []
        self.results = {}
    
    async def execute_chapter(self, chapter_num: int, 
                             chapter_outline: str,
                             bible_context: Dict) -> Dict:
        """
        并行执行章节生成
        """
        logger.info(f"开始并行生成第{chapter_num}章")
        
        # 1. 分析章节并分配Agent
        agents, plan = self.agent_pool.allocate_for_chapter(
            chapter_outline, bible_context
        )
        logger.info(f"分配了{len(agents)}个Agent:\n{plan}")
        
        # 2. 开始追踪
        self.status_tracker.start_chapter(
            chapter_num, 
            bible_context.get('chapter_title', f'第{chapter_num}章'),
            len(agents)
        )
        
        # 3. 创建Stream任务
        tasks = []
        for stream_name, agent_name in self.EIGHT_STREAMS:
            task = StreamTask(
                stream_name=stream_name,
                agent_name=agent_name,
                chapter_num=chapter_num,
                chapter_context={'outline': chapter_outline},
                bible_context=bible_context
            )
            tasks.append(self._execute_stream(task))
        
        # 4. 添加特化Agent任务（如果有）
        specialized_agents = [a for a in agents if a.type == "specialist"]
        for agent in specialized_agents[:4]:  # 最多4个额外Agent
            task = StreamTask(
                stream_name=f"Specialist-{agent.name}",
                agent_name=agent.name,
                chapter_num=chapter_num,
                chapter_context={'outline': chapter_outline},
                bible_context=bible_context,
                priority=agent.priority
            )
            tasks.append(self._execute_stream(task))
        
        # 5. 并行执行所有任务
        try:
            # 在Claude环境中，这可能是顺序执行的优化版本
            # 但架构上支持真正的并行
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 6. 处理结果
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Stream执行失败: {result}")
                    self.status_tracker.fail_agent(
                        self.EIGHT_STREAMS[i][1] if i < 8 else f"specialist-{i-8}",
                        str(result)
                    )
                else:
                    self.results[result.get('stream_name', f'stream-{i}')] = result
            
            # 7. 合并结果
            merged_chapter = await self._merge_results()
            
            # 8. 质量评估
            quality_score = self._assess_quality(merged_chapter)
            
            # 9. 完成章节
            self.status_tracker.complete_chapter(quality_score)
            
            # 10. 同步到GitHub
            if self.github:
                await self._sync_to_github(chapter_num, merged_chapter, quality_score)
            
            return {
                'success': True,
                'chapter_content': merged_chapter,
                'quality_score': quality_score,
                'execution_time': self._get_execution_time(),
                'agent_count': len(agents)
            }
            
        except Exception as e:
            logger.error(f"并行执行失败: {e}")
            self.status_tracker.complete_chapter(0)
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _execute_stream(self, task: StreamTask) -> Dict:
        """
        执行单个Stream任务
        注意：在Claude环境中，这实际上是通过Task工具调用SubAgent
        """
        logger.info(f"执行Stream: {task.stream_name}")
        
        # 开始追踪
        self.status_tracker.start_agent(task.agent_name, "stream")
        
        try:
            # 构建Agent提示词
            prompt = self._build_agent_prompt(task)
            
            # 在实际Claude环境中，这里应该使用Task工具
            # 这里模拟返回
            result = await self._simulate_agent_execution(task, prompt)
            
            # 创建AgentResponse
            response = AgentResponse(
                summary=f"完成{task.stream_name}分析",
                status="success",
                decisions=result.get('decisions', []),
                next_steps=result.get('next_steps', []),
                metrics=result.get('metrics', {}),
                _details=result.get('full_content', '')  # 详细内容不返回主线程
            )
            
            # 应用Context Firewall
            self.stream_firewall.add_stream_response(task.stream_name, response)
            
            # 更新状态
            self.status_tracker.complete_agent(
                task.agent_name,
                quality_score=result.get('quality_score', 90),
                summary=response.summary,
                metrics=response.metrics
            )
            
            # 保存详细内容到文件
            self._save_stream_details(task.stream_name, task.chapter_num, response._details)
            
            return {
                'stream_name': task.stream_name,
                'success': True,
                'summary': response.summary,
                'quality_score': result.get('quality_score', 90),
                'content_snippet': result.get('content', '')[:500]  # 只保留片段
            }
            
        except Exception as e:
            logger.error(f"Stream {task.stream_name} 执行失败: {e}")
            self.status_tracker.fail_agent(task.agent_name, str(e))
            
            return {
                'stream_name': task.stream_name,
                'success': False,
                'error': str(e)
            }
    
    def _build_agent_prompt(self, task: StreamTask) -> str:
        """
        构建Agent提示词
        """
        return f"""
你是{task.agent_name}，负责处理第{task.chapter_num}章的{task.stream_name}维度。

章节大纲：
{task.chapter_context.get('outline', '')}

Bible设定：
{json.dumps(task.bible_context, ensure_ascii=False, indent=2)}

要求：
1. 专注于你的Stream维度
2. 生成高质量内容（目标98分）
3. 使用Context Firewall格式返回
4. 详细内容(2000-3000字)保存到文件
5. 只返回50字摘要给主线程

返回格式：
- summary: 50字以内摘要
- decisions: 3-5个关键决策
- next_steps: 1-3个建议
- metrics: 质量指标
- full_content: 完整内容（不返回主线程）
"""
    
    async def _simulate_agent_execution(self, task: StreamTask, prompt: str) -> Dict:
        """
        模拟Agent执行（实际应该调用Task工具）
        """
        # 模拟延迟
        await asyncio.sleep(0.1)
        
        # 模拟进度更新
        for progress in [20, 50, 80, 100]:
            await asyncio.sleep(0.05)
            self.status_tracker.update_agent_progress(
                task.agent_name, progress,
                f"处理{task.stream_name}中... {progress}%"
            )
        
        # 模拟返回结果
        return {
            'decisions': [
                f"{task.stream_name}决策1",
                f"{task.stream_name}决策2"
            ],
            'next_steps': [
                f"优化{task.stream_name}的某个方面"
            ],
            'metrics': {
                '质量分': 90 + hash(task.stream_name) % 10,
                '字数': 2000 + hash(task.stream_name) % 1000
            },
            'quality_score': 90 + hash(task.stream_name) % 10,
            'content': f"这是{task.stream_name}生成的内容片段...",
            'full_content': f"这是{task.stream_name}的完整2000字内容..."
        }
    
    async def _merge_results(self) -> str:
        """
        合并所有Stream的结果
        """
        logger.info("开始合并Stream结果")
        
        # 检测冲突
        conflicts = self._detect_conflicts()
        if conflicts:
            logger.info(f"检测到{len(conflicts)}个冲突，开始解决")
            self._resolve_conflicts(conflicts)
        
        # 合并内容
        merged_content = []
        merged_content.append("# 合并后的章节内容\n")
        
        # 按优先级合并
        priority_order = [
            "Narrative Structure",  # 叙事结构优先
            "Character Psychology", # 然后是角色
            "World Building",      # 世界构建
            "Dialogue Master",     # 对话
            "Prose Craft",        # 文笔
            "Emotion Weaver",     # 情感
            "Continuity Guard",   # 连贯性
            "Foreshadowing"       # 伏笔
        ]
        
        for stream in priority_order:
            if stream in self.results:
                result = self.results[stream]
                if result.get('success'):
                    merged_content.append(f"\n## {stream}贡献\n")
                    merged_content.append(result.get('content_snippet', ''))
        
        return "\n".join(merged_content)
    
    def _detect_conflicts(self) -> List[Dict]:
        """
        检测Stream间的冲突
        """
        conflicts = []
        
        # 简化的冲突检测逻辑
        # 实际应该比较具体内容
        
        return conflicts
    
    def _resolve_conflicts(self, conflicts: List[Dict]):
        """
        解决冲突
        优先级: 连贯性 > 角色一致性 > 情节逻辑 > 文笔风格
        """
        for conflict in conflicts:
            logger.info(f"解决冲突: {conflict}")
            # 实际的冲突解决逻辑
    
    def _assess_quality(self, content: str) -> int:
        """
        评估章节质量
        """
        scores = []
        
        # 从各个Stream收集质量分
        for result in self.results.values():
            if result.get('success') and result.get('quality_score'):
                scores.append(result['quality_score'])
        
        if scores:
            # 加权平均
            return int(sum(scores) / len(scores))
        
        return 85  # 默认分数
    
    async def _sync_to_github(self, chapter_num: int, content: str, quality_score: int):
        """
        同步到GitHub Issue
        """
        if not self.github:
            return
        
        chapter_data = {
            'number': chapter_num,
            'title': f'第{chapter_num}章',
            'word_count': len(content),
            'quality_score': quality_score,
            'streams': {
                stream: {
                    'completed': result.get('success', False),
                    'score': result.get('quality_score', 0)
                }
                for stream, result in self.results.items()
            },
            'decisions': self._collect_all_decisions(),
            'next_steps': self._collect_all_next_steps()
        }
        
        self.github.sync_chapter_to_issue(chapter_num, chapter_data)
    
    def _collect_all_decisions(self) -> List[str]:
        """收集所有决策"""
        decisions = []
        for response in self.stream_firewall.stream_responses.values():
            decisions.extend(response.decisions[:2])  # 每个Stream最多2个
        return decisions[:10]  # 总共最多10个
    
    def _collect_all_next_steps(self) -> List[str]:
        """收集所有下一步建议"""
        steps = []
        for response in self.stream_firewall.stream_responses.values():
            steps.extend(response.next_steps[:1])  # 每个Stream最多1个
        return steps[:5]  # 总共最多5个
    
    def _save_stream_details(self, stream_name: str, chapter_num: int, content: str):
        """
        保存Stream详细内容到文件
        """
        file_path = Path(f"data/streams/ch{chapter_num}/{stream_name.lower().replace(' ', '_')}.md")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"保存{stream_name}详细内容到{file_path}")
    
    def _get_execution_time(self) -> float:
        """获取执行时间"""
        if self.status_tracker.current_chapter:
            ch = self.status_tracker.current_chapter
            if ch.start_time and ch.end_time:
                return (ch.end_time - ch.start_time).total_seconds()
        return 0
    
    def get_status_report(self) -> str:
        """
        获取状态报告
        """
        # 从Stream Firewall获取摘要
        stream_summary = self.stream_firewall.get_all_streams_summary()
        
        # 从状态追踪器获取详细状态
        execution_status = self.status_tracker.get_status_report()
        
        # 合并报告
        report = []
        report.append("# 📊 并行执行状态报告")
        report.append("")
        report.append(stream_summary)
        report.append("")
        report.append("---")
        report.append("")
        report.append(execution_status)
        
        return "\n".join(report)


# 使用示例
async def main():
    # 初始化
    github = GitHubIntegration()
    coordinator = NovelParallelCoordinator(github)
    
    # 章节大纲
    outline = """
    第1章：觉醒
    主角在平凡的一天突然觉醒异能。
    与神秘组织初次接触。
    发现世界的真相。
    """
    
    bible = {
        'genre': '都市异能',
        'protagonist': '李明',
        'setting': '现代都市'
    }
    
    # 执行并行生成
    result = await coordinator.execute_chapter(1, outline, bible)
    
    if result['success']:
        print(f"章节生成成功！")
        print(f"质量分: {result['quality_score']}")
        print(f"执行时间: {result['execution_time']}秒")
        print(f"使用Agent: {result['agent_count']}个")
        
        # 打印状态报告
        print("\n" + coordinator.get_status_report())
    else:
        print(f"生成失败: {result['error']}")


if __name__ == "__main__":
    asyncio.run(main())