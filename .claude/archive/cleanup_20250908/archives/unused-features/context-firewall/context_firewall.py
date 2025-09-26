"""
Context Firewall System for NOVELSYS-SWARM
保护主线程上下文，防止细节污染
借鉴CCPM的Context Firewall架构
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from functools import wraps

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """
    标准化的Agent响应格式
    确保主线程只接收精炼的摘要信息
    """
    # 返回给主线程的内容
    summary: str                          # 50字以内的执行摘要
    status: str                           # success|partial|failed
    decisions: List[str] = field(default_factory=list)  # 关键决策点
    next_steps: List[str] = field(default_factory=list) # 建议的下一步
    metrics: Dict[str, Any] = field(default_factory=dict) # 关键指标
    
    # 不返回主线程的详细内容
    _details: str = ""                    # 完整的执行细节
    _raw_output: str = ""                 # 原始输出
    _debug_info: Dict = field(default_factory=dict)  # 调试信息
    _timestamp: datetime = field(default_factory=datetime.now)
    
    def to_main_thread(self) -> str:
        """
        生成返回给主线程的精炼内容
        """
        result = []
        
        # 摘要
        result.append(f"## 执行摘要")
        result.append(f"{self.summary}")
        result.append("")
        
        # 关键决策
        if self.decisions:
            result.append("## 关键决策")
            for decision in self.decisions:
                result.append(f"- {decision}")
            result.append("")
        
        # 下一步建议
        if self.next_steps:
            result.append("## 建议下一步")
            for step in self.next_steps:
                result.append(f"- {step}")
            result.append("")
        
        # 关键指标
        if self.metrics:
            result.append("## 关键指标")
            for key, value in self.metrics.items():
                result.append(f"- {key}: {value}")
            result.append("")
        
        # 状态
        status_emoji = {
            "success": "✅",
            "partial": "⚠️",
            "failed": "❌"
        }.get(self.status, "ℹ️")
        result.append(f"**状态**: {status_emoji} {self.status}")
        
        return "\n".join(result)
    
    def save_details(self, filepath: str):
        """
        保存详细内容到文件（不污染上下文）
        """
        data = {
            "summary": self.summary,
            "status": self.status,
            "decisions": self.decisions,
            "next_steps": self.next_steps,
            "metrics": self.metrics,
            "details": self._details,
            "raw_output": self._raw_output,
            "debug_info": self._debug_info,
            "timestamp": self._timestamp.isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class ContextFirewall:
    """
    上下文防火墙
    过滤和管理Agent返回的信息
    """
    
    def __init__(self, max_summary_length: int = 100, 
                 max_decisions: int = 5,
                 max_next_steps: int = 3):
        self.max_summary_length = max_summary_length
        self.max_decisions = max_decisions
        self.max_next_steps = max_next_steps
        self.responses = []
    
    def filter_response(self, response: AgentResponse) -> str:
        """
        过滤Agent响应，只返回精炼内容
        """
        # 截断过长的摘要
        if len(response.summary) > self.max_summary_length:
            response.summary = response.summary[:self.max_summary_length-3] + "..."
        
        # 限制决策点数量
        if len(response.decisions) > self.max_decisions:
            response.decisions = response.decisions[:self.max_decisions]
        
        # 限制下一步数量
        if len(response.next_steps) > self.max_next_steps:
            response.next_steps = response.next_steps[:self.max_next_steps]
        
        # 保存响应历史
        self.responses.append(response)
        
        # 返回精炼内容
        return response.to_main_thread()
    
    def batch_filter(self, responses: List[AgentResponse]) -> str:
        """
        批量过滤多个Agent响应并合并
        """
        filtered = []
        
        for i, response in enumerate(responses, 1):
            filtered.append(f"### Agent {i}")
            filtered.append(self.filter_response(response))
            filtered.append("")
        
        return "\n".join(filtered)
    
    def get_consolidated_summary(self) -> str:
        """
        获取所有响应的统一摘要
        """
        if not self.responses:
            return "无执行记录"
        
        # 统计状态
        status_count = {}
        for r in self.responses:
            status_count[r.status] = status_count.get(r.status, 0) + 1
        
        # 合并所有决策
        all_decisions = []
        for r in self.responses:
            all_decisions.extend(r.decisions)
        
        # 合并所有下一步
        all_next_steps = []
        for r in self.responses:
            all_next_steps.extend(r.next_steps)
        
        # 生成统一摘要
        result = []
        result.append("## 📊 执行汇总")
        result.append("")
        
        # 状态分布
        result.append("### 状态分布")
        for status, count in status_count.items():
            emoji = {"success": "✅", "partial": "⚠️", "failed": "❌"}.get(status, "ℹ️")
            result.append(f"- {emoji} {status}: {count}个Agent")
        result.append("")
        
        # 关键决策汇总
        if all_decisions:
            result.append("### 关键决策汇总")
            for decision in all_decisions[:10]:  # 最多10个
                result.append(f"- {decision}")
            result.append("")
        
        # 建议下一步汇总
        if all_next_steps:
            result.append("### 建议下一步汇总")
            # 去重
            unique_steps = list(dict.fromkeys(all_next_steps))
            for step in unique_steps[:5]:  # 最多5个
                result.append(f"- {step}")
        
        return "\n".join(result)


def context_firewall(max_summary_length: int = 100):
    """
    装饰器：自动应用Context Firewall
    
    使用方法:
    @context_firewall()
    async def my_agent_function():
        # ... 执行逻辑
        return AgentResponse(
            summary="完成了XXX",
            details="很长的细节..."  # 这部分不会返回主线程
        )
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 如果返回的是AgentResponse，自动过滤
            if isinstance(result, AgentResponse):
                firewall = ContextFirewall(max_summary_length=max_summary_length)
                return firewall.filter_response(result)
            
            return result
        
        return wrapper
    return decorator


class StreamFirewall:
    """
    专门为8-Stream系统设计的防火墙
    管理8个Stream的并行输出
    """
    
    def __init__(self):
        self.stream_responses = {}
        self.firewall = ContextFirewall()
    
    def add_stream_response(self, stream_name: str, response: AgentResponse):
        """
        添加Stream响应
        """
        self.stream_responses[stream_name] = response
    
    def get_stream_summary(self, stream_name: str) -> str:
        """
        获取特定Stream的摘要
        """
        if stream_name not in self.stream_responses:
            return f"Stream {stream_name}: 未执行"
        
        return self.firewall.filter_response(self.stream_responses[stream_name])
    
    def get_all_streams_summary(self) -> str:
        """
        获取所有8个Stream的汇总
        """
        result = []
        result.append("## 🎭 8-Stream执行汇总")
        result.append("")
        
        # 定义Stream顺序
        stream_order = [
            "Character Psychology",
            "Narrative Structure", 
            "World Building",
            "Prose Craft",
            "Continuity Guard",
            "Foreshadowing",
            "Dialogue Master",
            "Emotion Weaver"
        ]
        
        for stream in stream_order:
            if stream in self.stream_responses:
                response = self.stream_responses[stream]
                status_emoji = {
                    "success": "✅",
                    "partial": "⚠️",
                    "failed": "❌"
                }.get(response.status, "ℹ️")
                
                result.append(f"### {status_emoji} Stream: {stream}")
                result.append(f"{response.summary}")
                
                # 关键指标
                if response.metrics:
                    metrics_str = ", ".join([f"{k}:{v}" for k, v in response.metrics.items()])
                    result.append(f"指标: {metrics_str}")
                
                result.append("")
        
        # 未执行的Stream
        missing_streams = set(stream_order) - set(self.stream_responses.keys())
        if missing_streams:
            result.append("### ⏳ 待执行Stream")
            for stream in missing_streams:
                result.append(f"- {stream}")
        
        return "\n".join(result)
    
    def should_continue(self) -> bool:
        """
        根据Stream状态决定是否继续
        """
        # 如果有任何失败，停止
        for response in self.stream_responses.values():
            if response.status == "failed":
                return False
        
        # 如果所有都成功，继续
        if len(self.stream_responses) == 8:
            all_success = all(r.status == "success" for r in self.stream_responses.values())
            return not all_success  # 全成功则不需要继续
        
        return True  # 还有Stream未执行


# 使用示例
if __name__ == "__main__":
    # 创建Agent响应
    response = AgentResponse(
        summary="成功生成第1章角色心理分析",
        status="success",
        decisions=[
            "主角内心冲突设定为理想vs现实",
            "使用第一人称限制视角"
        ],
        next_steps=[
            "深化配角动机",
            "增加心理描写密度"
        ],
        metrics={
            "心理深度": "95分",
            "字数": "2000"
        },
        _details="这里是2000字的详细分析内容，不会返回主线程..."
    )
    
    # 应用防火墙
    firewall = ContextFirewall()
    filtered = firewall.filter_response(response)
    print(filtered)
    
    # 8-Stream示例
    stream_firewall = StreamFirewall()
    for i, stream in enumerate(["Character Psychology", "Narrative Structure"], 1):
        stream_response = AgentResponse(
            summary=f"完成{stream}分析",
            status="success",
            metrics={"质量": f"{90+i}分"}
        )
        stream_firewall.add_stream_response(stream, stream_response)
    
    print(stream_firewall.get_all_streams_summary())