"""
Execution Status Tracking System
实时追踪和可视化执行进度
借鉴CCPM的透明化机制
"""

import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import threading
import logging

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent状态枚举"""
    PENDING = "pending"       # 待执行
    RUNNING = "running"       # 执行中
    SUCCESS = "success"       # 成功
    FAILED = "failed"        # 失败
    TIMEOUT = "timeout"      # 超时
    SKIPPED = "skipped"      # 跳过


@dataclass
class AgentExecution:
    """Agent执行记录"""
    agent_name: str
    agent_type: str
    status: AgentStatus
    progress: int  # 0-100
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    output_summary: str = ""
    quality_score: Optional[int] = None
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        data['status'] = self.status.value
        if self.start_time:
            data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data


@dataclass 
class ChapterExecution:
    """章节执行记录"""
    chapter_num: int
    title: str
    total_agents: int
    completed_agents: int = 0
    failed_agents: int = 0
    overall_progress: int = 0
    overall_quality: Optional[int] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    agents: Dict[str, AgentExecution] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        data['agents'] = {k: v.to_dict() for k, v in self.agents.items()}
        return data


class ExecutionStatusTracker:
    """
    执行状态追踪器
    实时监控Agent执行和章节生成进度
    """
    
    def __init__(self, status_file: str = "data/status/execution_status.json"):
        self.status_file = Path(status_file)
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.current_chapter: Optional[ChapterExecution] = None
        self.agent_executions: Dict[str, AgentExecution] = {}
        self.history: List[ChapterExecution] = []
        
        # 实时更新标志
        self.is_running = False
        self.update_thread = None
        
        # 加载历史记录
        self._load_history()
    
    def _load_history(self):
        """加载历史执行记录"""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 这里简化处理，实际需要反序列化
                    logger.info(f"加载了{len(data.get('history', []))}条历史记录")
            except Exception as e:
                logger.error(f"加载历史记录失败: {e}")
    
    def start_chapter(self, chapter_num: int, title: str, total_agents: int):
        """
        开始新章节执行
        """
        self.current_chapter = ChapterExecution(
            chapter_num=chapter_num,
            title=title,
            total_agents=total_agents
        )
        
        self.agent_executions.clear()
        self.is_running = True
        
        # 启动实时更新线程
        self.update_thread = threading.Thread(target=self._update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        logger.info(f"开始执行第{chapter_num}章: {title}, 共{total_agents}个Agent")
        
        # 保存初始状态
        self._save_status()
    
    def start_agent(self, agent_name: str, agent_type: str = "stream"):
        """
        Agent开始执行
        """
        if not self.current_chapter:
            logger.warning("没有活跃的章节执行")
            return
        
        execution = AgentExecution(
            agent_name=agent_name,
            agent_type=agent_type,
            status=AgentStatus.RUNNING,
            progress=0,
            start_time=datetime.now()
        )
        
        self.agent_executions[agent_name] = execution
        self.current_chapter.agents[agent_name] = execution
        
        logger.info(f"Agent {agent_name} 开始执行")
    
    def update_agent_progress(self, agent_name: str, progress: int, 
                            message: str = None):
        """
        更新Agent进度
        """
        if agent_name not in self.agent_executions:
            logger.warning(f"Agent {agent_name} 未注册")
            return
        
        agent = self.agent_executions[agent_name]
        agent.progress = min(100, max(0, progress))
        
        if message:
            agent.output_summary = message
        
        # 更新章节整体进度
        self._update_chapter_progress()
    
    def complete_agent(self, agent_name: str, quality_score: int = None,
                      summary: str = "", metrics: Dict = None):
        """
        Agent执行完成
        """
        if agent_name not in self.agent_executions:
            logger.warning(f"Agent {agent_name} 未注册")
            return
        
        agent = self.agent_executions[agent_name]
        agent.status = AgentStatus.SUCCESS
        agent.progress = 100
        agent.end_time = datetime.now()
        agent.duration = (agent.end_time - agent.start_time).total_seconds()
        agent.quality_score = quality_score
        agent.output_summary = summary
        
        if metrics:
            agent.metrics.update(metrics)
        
        self.current_chapter.completed_agents += 1
        
        logger.info(f"Agent {agent_name} 完成, 质量分: {quality_score}")
        
        # 更新进度
        self._update_chapter_progress()
    
    def fail_agent(self, agent_name: str, error_message: str):
        """
        Agent执行失败
        """
        if agent_name not in self.agent_executions:
            logger.warning(f"Agent {agent_name} 未注册")
            return
        
        agent = self.agent_executions[agent_name]
        agent.status = AgentStatus.FAILED
        agent.end_time = datetime.now()
        agent.duration = (agent.end_time - agent.start_time).total_seconds()
        agent.error_message = error_message
        
        self.current_chapter.failed_agents += 1
        
        logger.error(f"Agent {agent_name} 失败: {error_message}")
        
        # 更新进度
        self._update_chapter_progress()
    
    def complete_chapter(self, overall_quality: int = None):
        """
        章节执行完成
        """
        if not self.current_chapter:
            logger.warning("没有活跃的章节执行")
            return
        
        self.current_chapter.end_time = datetime.now()
        self.current_chapter.overall_quality = overall_quality
        
        # 停止更新线程
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=1)
        
        # 保存到历史
        self.history.append(self.current_chapter)
        
        logger.info(f"第{self.current_chapter.chapter_num}章完成, 质量分: {overall_quality}")
        
        # 最终保存
        self._save_status()
        
        # 清理当前状态
        self.current_chapter = None
        self.agent_executions.clear()
    
    def _update_chapter_progress(self):
        """
        更新章节整体进度
        """
        if not self.current_chapter:
            return
        
        total_progress = 0
        for agent in self.agent_executions.values():
            total_progress += agent.progress
        
        if self.current_chapter.total_agents > 0:
            self.current_chapter.overall_progress = int(
                total_progress / self.current_chapter.total_agents
            )
    
    def _update_loop(self):
        """
        实时更新循环
        """
        while self.is_running:
            self._save_status()
            time.sleep(5)  # 每5秒保存一次
    
    def _save_status(self):
        """
        保存当前状态到文件
        """
        try:
            status_data = {
                "timestamp": datetime.now().isoformat(),
                "current_chapter": self.current_chapter.to_dict() if self.current_chapter else None,
                "history": [ch.to_dict() for ch in self.history[-10:]]  # 保留最近10章
            }
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存状态失败: {e}")
    
    def get_status_report(self) -> str:
        """
        生成状态报告
        """
        if not self.current_chapter:
            return "当前没有执行中的任务"
        
        report = []
        report.append(f"## 📊 NOVELSYS执行状态")
        report.append(f"*更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report.append("")
        
        # 章节信息
        ch = self.current_chapter
        report.append(f"### 📖 第{ch.chapter_num}章: {ch.title}")
        report.append(f"- 整体进度: {ch.overall_progress}%")
        report.append(f"- Agent状态: {ch.completed_agents}/{ch.total_agents} 完成")
        if ch.failed_agents > 0:
            report.append(f"- ⚠️ 失败: {ch.failed_agents}个")
        report.append("")
        
        # Agent详情
        report.append("### 🤖 Agent执行状态")
        
        # 8个基础Stream
        streams = [a for a in self.agent_executions.values() if a.agent_type == "stream"]
        if streams:
            report.append("#### 8-Stream状态")
            for agent in streams:
                status_emoji = {
                    AgentStatus.SUCCESS: "✅",
                    AgentStatus.RUNNING: "⏳",
                    AgentStatus.FAILED: "❌",
                    AgentStatus.PENDING: "⏸️"
                }.get(agent.status, "❓")
                
                progress_bar = self._create_progress_bar(agent.progress)
                score_str = f" - {agent.quality_score}分" if agent.quality_score else ""
                
                report.append(f"{status_emoji} {agent.agent_name}: {progress_bar} {agent.progress}%{score_str}")
                
                if agent.output_summary:
                    report.append(f"   └─ {agent.output_summary[:50]}")
        
        # 特化Agent
        specialists = [a for a in self.agent_executions.values() if a.agent_type != "stream"]
        if specialists:
            report.append("")
            report.append("#### 特化Agent状态")
            for agent in specialists:
                status_emoji = {
                    AgentStatus.SUCCESS: "✅",
                    AgentStatus.RUNNING: "⏳",
                    AgentStatus.FAILED: "❌"
                }.get(agent.status, "❓")
                
                report.append(f"{status_emoji} {agent.agent_name}: {agent.progress}%")
        
        # 质量评估
        if ch.overall_quality:
            report.append("")
            report.append(f"### 🎯 质量评估")
            report.append(f"- 综合质量: {ch.overall_quality}/100")
            
            # 各维度得分
            quality_scores = {}
            for agent in self.agent_executions.values():
                if agent.quality_score:
                    quality_scores[agent.agent_name] = agent.quality_score
            
            if quality_scores:
                avg_score = sum(quality_scores.values()) / len(quality_scores)
                report.append(f"- 平均得分: {avg_score:.1f}")
                
                # 找出最高和最低
                best = max(quality_scores.items(), key=lambda x: x[1])
                worst = min(quality_scores.items(), key=lambda x: x[1])
                report.append(f"- 最佳: {best[0]} ({best[1]}分)")
                report.append(f"- 待改进: {worst[0]} ({worst[1]}分)")
        
        # 时间统计
        if ch.start_time:
            elapsed = (datetime.now() - ch.start_time).total_seconds()
            report.append("")
            report.append(f"### ⏱️ 时间统计")
            report.append(f"- 已用时: {int(elapsed//60)}分{int(elapsed%60)}秒")
            
            # 预估剩余时间
            if ch.overall_progress > 0:
                estimated_total = elapsed / (ch.overall_progress / 100)
                remaining = estimated_total - elapsed
                report.append(f"- 预计剩余: {int(remaining//60)}分{int(remaining%60)}秒")
        
        return "\n".join(report)
    
    def _create_progress_bar(self, progress: int, width: int = 20) -> str:
        """
        创建进度条
        """
        filled = int(width * progress / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"
    
    def get_agent_metrics(self, agent_name: str) -> Optional[Dict]:
        """
        获取Agent的详细指标
        """
        if agent_name in self.agent_executions:
            return self.agent_executions[agent_name].metrics
        return None
    
    def export_to_github_comment(self) -> str:
        """
        导出为GitHub评论格式
        """
        report = self.get_status_report()
        
        # 添加GitHub特有的格式
        github_report = []
        github_report.append(report)
        github_report.append("")
        github_report.append("---")
        github_report.append("*由NOVELSYS-SWARM自动生成 | [查看详情](data/status/execution_status.json)*")
        
        return "\n".join(github_report)


class LiveStatusMonitor:
    """
    实时状态监控器
    提供实时更新的控制台输出
    """
    
    def __init__(self, tracker: ExecutionStatusTracker):
        self.tracker = tracker
        self.running = False
    
    def start_monitoring(self):
        """
        开始实时监控
        """
        self.running = True
        
        while self.running:
            # 清屏（简化版，实际可能需要根据OS调整）
            print("\033[2J\033[H")  # ANSI清屏
            
            # 打印状态
            print(self.tracker.get_status_report())
            
            # 等待更新
            time.sleep(2)
    
    def stop_monitoring(self):
        """
        停止监控
        """
        self.running = False


# 使用示例
if __name__ == "__main__":
    # 创建追踪器
    tracker = ExecutionStatusTracker()
    
    # 开始章节
    tracker.start_chapter(1, "觉醒之日", 12)
    
    # 模拟Agent执行
    agents = [
        "character-psychology-specialist",
        "narrative-structure-specialist",
        "world-building-specialist",
        "prose-craft-specialist"
    ]
    
    for agent in agents:
        tracker.start_agent(agent, "stream")
        
        # 模拟进度更新
        for progress in [20, 50, 80, 100]:
            time.sleep(0.5)
            tracker.update_agent_progress(
                agent, progress, 
                f"处理中... {progress}%"
            )
        
        # 完成
        tracker.complete_agent(
            agent,
            quality_score=90 + (hash(agent) % 10),
            summary=f"{agent}完成分析",
            metrics={"tokens": 1000, "time": 30}
        )
    
    # 打印最终报告
    print(tracker.get_status_report())
    
    # 完成章节
    tracker.complete_chapter(overall_quality=93)
    
    # 导出GitHub评论
    github_comment = tracker.export_to_github_comment()
    print("\n=== GitHub Comment ===")
    print(github_comment)