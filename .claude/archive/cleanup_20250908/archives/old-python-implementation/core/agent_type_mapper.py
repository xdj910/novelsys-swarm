"""
Dynamic Agent Type Mapping System
根据章节类型动态分配专业Agent
借鉴CCPM的灵活Agent分配机制
"""

from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ChapterType(Enum):
    """章节类型枚举"""
    ACTION = "action"           # 动作场面
    ROMANCE = "romance"         # 感情戏
    MYSTERY = "mystery"         # 悬疑推理
    DIALOGUE = "dialogue"       # 对话密集
    EXPOSITION = "exposition"   # 说明铺垫
    CLIMAX = "climax"          # 高潮场面
    TRANSITION = "transition"   # 过渡章节
    FLASHBACK = "flashback"    # 回忆倒叙
    WORLDBUILD = "worldbuild"  # 世界观构建
    CHARACTER = "character"     # 角色发展


@dataclass
class AgentSpec:
    """Agent规格定义"""
    name: str                   # Agent名称
    type: str                   # Agent类型
    priority: int              # 优先级(1-10)
    required: bool             # 是否必需
    skills: List[str]          # 专长技能
    

class AgentTypeMapper:
    """
    动态Agent类型映射器
    根据章节特征智能分配Agent
    """
    
    # 8个基础Stream Agent（始终启用）
    BASE_STREAMS = [
        AgentSpec("character-psychology-specialist", "stream", 10, True, 
                 ["心理分析", "动机解析", "情感追踪"]),
        AgentSpec("narrative-structure-specialist", "stream", 10, True,
                 ["节奏控制", "结构设计", "冲突构建"]),
        AgentSpec("world-building-specialist", "stream", 10, True,
                 ["环境描写", "感官体验", "氛围营造"]),
        AgentSpec("prose-craft-specialist", "stream", 10, True,
                 ["文笔优化", "修辞技巧", "语言节奏"]),
        AgentSpec("continuity-guard-specialist", "stream", 10, True,
                 ["逻辑检查", "时间线维护", "设定一致"]),
        AgentSpec("foreshadowing-specialist", "stream", 10, True,
                 ["伏笔铺设", "线索管理", "回收追踪"]),
        AgentSpec("dialogue-master-specialist", "stream", 10, True,
                 ["对话创作", "潜台词", "角色语言"]),
        AgentSpec("emotion-weaver-specialist", "stream", 10, True,
                 ["情感渲染", "共鸣构建", "情绪曲线"])
    ]
    
    # 特化Agent映射（根据章节类型额外添加）
    SPECIALIZED_AGENTS = {
        ChapterType.ACTION: [
            AgentSpec("action-choreographer", "specialist", 9, False,
                     ["动作设计", "场面调度", "紧张感营造"]),
            AgentSpec("pacing-specialist", "specialist", 8, False,
                     ["节奏把控", "张力管理", "高潮构建"])
        ],
        ChapterType.ROMANCE: [
            AgentSpec("romance-specialist", "specialist", 9, False,
                     ["情感细腻", "关系发展", "化学反应"]),
            AgentSpec("intimacy-coordinator", "specialist", 8, False,
                     ["亲密场景", "情感深度", "关系进展"])
        ],
        ChapterType.MYSTERY: [
            AgentSpec("suspense-engineer", "specialist", 9, False,
                     ["悬念设置", "线索布局", "真相隐藏"]),
            AgentSpec("clue-tracker", "specialist", 8, False,
                     ["线索管理", "推理逻辑", "误导设计"])
        ],
        ChapterType.DIALOGUE: [
            AgentSpec("conversation-architect", "specialist", 9, False,
                     ["对话节奏", "信息传递", "性格展现"]),
            AgentSpec("subtext-master", "specialist", 8, False,
                     ["潜台词设计", "言外之意", "暗示技巧"])
        ],
        ChapterType.EXPOSITION: [
            AgentSpec("info-architect", "specialist", 8, False,
                     ["信息组织", "自然融入", "避免说教"]),
            AgentSpec("context-builder", "specialist", 7, False,
                     ["背景构建", "历史编织", "设定展示"])
        ],
        ChapterType.CLIMAX: [
            AgentSpec("climax-orchestrator", "specialist", 10, False,
                     ["高潮设计", "冲突爆发", "情感顶点"]),
            AgentSpec("tension-maximizer", "specialist", 9, False,
                     ["张力最大化", "节奏加速", "冲击力"])
        ],
        ChapterType.WORLDBUILD: [
            AgentSpec("lore-master", "specialist", 8, False,
                     ["设定深化", "历史构建", "文化设计"]),
            AgentSpec("sensory-specialist", "specialist", 7, False,
                     ["感官描写", "环境细节", "沉浸体验"])
        ],
        ChapterType.CHARACTER: [
            AgentSpec("character-developer", "specialist", 9, False,
                     ["角色成长", "性格转变", "动机演化"]),
            AgentSpec("relationship-architect", "specialist", 8, False,
                     ["关系构建", "互动设计", "化学反应"])
        ]
    }
    
    def __init__(self):
        self.current_allocation = []
        self.chapter_analysis = {}
    
    def analyze_chapter(self, chapter_outline: str, bible_context: Dict) -> Dict:
        """
        分析章节特征，确定类型
        """
        analysis = {
            "primary_type": None,
            "secondary_types": [],
            "features": [],
            "complexity": 0
        }
        
        # 关键词检测（简化版，实际应该用NLP）
        outline_lower = chapter_outline.lower()
        
        # 检测主要类型
        type_scores = {}
        
        if any(word in outline_lower for word in ["战斗", "追逐", "动作", "fight", "battle"]):
            type_scores[ChapterType.ACTION] = type_scores.get(ChapterType.ACTION, 0) + 3
            
        if any(word in outline_lower for word in ["爱情", "感情", "亲密", "love", "romance"]):
            type_scores[ChapterType.ROMANCE] = type_scores.get(ChapterType.ROMANCE, 0) + 3
            
        if any(word in outline_lower for word in ["谜团", "线索", "推理", "mystery", "clue"]):
            type_scores[ChapterType.MYSTERY] = type_scores.get(ChapterType.MYSTERY, 0) + 3
            
        if any(word in outline_lower for word in ["对话", "谈话", "讨论", "dialogue", "conversation"]):
            type_scores[ChapterType.DIALOGUE] = type_scores.get(ChapterType.DIALOGUE, 0) + 2
            
        if any(word in outline_lower for word in ["高潮", "决战", "对决", "climax", "showdown"]):
            type_scores[ChapterType.CLIMAX] = type_scores.get(ChapterType.CLIMAX, 0) + 4
            
        if any(word in outline_lower for word in ["回忆", "过去", "曾经", "flashback", "memory"]):
            type_scores[ChapterType.FLASHBACK] = type_scores.get(ChapterType.FLASHBACK, 0) + 2
            
        if any(word in outline_lower for word in ["世界", "设定", "环境", "world", "setting"]):
            type_scores[ChapterType.WORLDBUILD] = type_scores.get(ChapterType.WORLDBUILD, 0) + 2
            
        if any(word in outline_lower for word in ["成长", "转变", "觉醒", "growth", "change"]):
            type_scores[ChapterType.CHARACTER] = type_scores.get(ChapterType.CHARACTER, 0) + 2
        
        # 确定主要类型
        if type_scores:
            sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
            analysis["primary_type"] = sorted_types[0][0]
            
            # 次要类型
            if len(sorted_types) > 1:
                analysis["secondary_types"] = [t[0] for t in sorted_types[1:3] if t[1] > 1]
        else:
            # 默认类型
            analysis["primary_type"] = ChapterType.EXPOSITION
        
        # 复杂度评估
        analysis["complexity"] = len(analysis["secondary_types"]) + 1
        
        self.chapter_analysis = analysis
        return analysis
    
    def allocate_agents(self, chapter_type: ChapterType, 
                       secondary_types: List[ChapterType] = None) -> List[AgentSpec]:
        """
        根据章节类型分配Agent
        """
        allocated = []
        
        # 1. 始终包含8个基础Stream
        allocated.extend(self.BASE_STREAMS)
        logger.info(f"分配了{len(self.BASE_STREAMS)}个基础Stream Agent")
        
        # 2. 添加主类型的特化Agent
        if chapter_type in self.SPECIALIZED_AGENTS:
            specialists = self.SPECIALIZED_AGENTS[chapter_type]
            allocated.extend(specialists)
            logger.info(f"为{chapter_type.value}类型添加{len(specialists)}个专门Agent")
        
        # 3. 添加次要类型的Agent（优先级降低）
        if secondary_types:
            for sec_type in secondary_types[:2]:  # 最多2个次要类型
                if sec_type in self.SPECIALIZED_AGENTS:
                    # 只添加高优先级的
                    for agent in self.SPECIALIZED_AGENTS[sec_type]:
                        if agent.priority >= 8 and agent not in allocated:
                            # 降低优先级
                            modified_agent = AgentSpec(
                                name=agent.name,
                                type=agent.type,
                                priority=agent.priority - 1,
                                required=False,
                                skills=agent.skills
                            )
                            allocated.append(modified_agent)
        
        # 4. 按优先级排序
        allocated.sort(key=lambda x: x.priority, reverse=True)
        
        self.current_allocation = allocated
        return allocated
    
    def get_agent_prompt(self, agent_spec: AgentSpec, chapter_context: Dict) -> str:
        """
        生成Agent的具体提示词
        """
        skills_str = "、".join(agent_spec.skills)
        
        prompt = f"""
你是{agent_spec.name}，专长于{skills_str}。

章节信息:
- 章节号: {chapter_context.get('number', 1)}
- 类型: {chapter_context.get('type', '通用')}
- 重点: {chapter_context.get('focus', '均衡')}

你的任务:
1. 专注于你的专业领域
2. 输出高质量内容
3. 与其他Agent协作但保持独立
4. 使用Context Firewall格式返回

质量要求:
- 你的领域必须达到95分以上
- 详细内容保存到文件
- 只返回50字摘要
"""
        
        return prompt
    
    def optimize_allocation(self, performance_history: Dict) -> List[AgentSpec]:
        """
        根据历史表现优化Agent分配
        """
        optimized = self.current_allocation.copy()
        
        # 分析历史表现
        for agent_name, metrics in performance_history.items():
            avg_score = metrics.get('avg_score', 0)
            failure_rate = metrics.get('failure_rate', 0)
            
            # 如果某个Agent经常失败或得分低
            if failure_rate > 0.3 or avg_score < 80:
                # 寻找替代Agent
                for agent in optimized:
                    if agent.name == agent_name and not agent.required:
                        # 降低优先级或移除
                        agent.priority = max(1, agent.priority - 2)
                        logger.warning(f"降低{agent_name}的优先级due to poor performance")
        
        # 重新排序
        optimized.sort(key=lambda x: x.priority, reverse=True)
        
        # 限制总数（避免太多Agent）
        max_agents = 12  # 8基础 + 4额外
        if len(optimized) > max_agents:
            # 保留必需的和高优先级的
            required = [a for a in optimized if a.required]
            optional = [a for a in optimized if not a.required][:max_agents-len(required)]
            optimized = required + optional
        
        return optimized
    
    def get_execution_plan(self) -> str:
        """
        生成执行计划的可视化
        """
        if not self.current_allocation:
            return "未分配Agent"
        
        plan = []
        plan.append("## 🤖 Agent执行计划")
        plan.append("")
        plan.append(f"### 章节类型: {self.chapter_analysis.get('primary_type', '未知')}")
        plan.append(f"### 复杂度: {self.chapter_analysis.get('complexity', 1)}")
        plan.append("")
        
        # 基础Stream
        plan.append("### 📊 基础8-Stream (必需)")
        for agent in self.current_allocation:
            if agent.type == "stream":
                emoji = "🟢" if agent.required else "🟡"
                plan.append(f"{emoji} {agent.name} (优先级:{agent.priority})")
        plan.append("")
        
        # 特化Agent
        specialists = [a for a in self.current_allocation if a.type == "specialist"]
        if specialists:
            plan.append("### 🎯 特化Agent (增强)")
            for agent in specialists:
                skills = ", ".join(agent.skills[:2])
                plan.append(f"🔷 {agent.name} - {skills} (优先级:{agent.priority})")
        
        plan.append("")
        plan.append(f"**总计**: {len(self.current_allocation)}个Agent")
        
        return "\n".join(plan)


class DynamicAgentPool:
    """
    动态Agent池管理
    可以创建新的Agent类型
    """
    
    def __init__(self):
        self.agent_pool = {}
        self.mapper = AgentTypeMapper()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """初始化Agent池"""
        # 注册基础Agent
        for agent in self.mapper.BASE_STREAMS:
            self.register_agent(agent)
        
        # 注册特化Agent
        for agents in self.mapper.SPECIALIZED_AGENTS.values():
            for agent in agents:
                self.register_agent(agent)
    
    def register_agent(self, agent_spec: AgentSpec):
        """注册新Agent类型"""
        self.agent_pool[agent_spec.name] = agent_spec
        logger.info(f"注册Agent: {agent_spec.name}")
    
    def create_custom_agent(self, name: str, skills: List[str], 
                           base_type: str = "specialist") -> AgentSpec:
        """
        动态创建自定义Agent
        """
        custom_agent = AgentSpec(
            name=f"custom-{name}",
            type=base_type,
            priority=7,  # 默认中等优先级
            required=False,
            skills=skills
        )
        
        self.register_agent(custom_agent)
        return custom_agent
    
    def get_agent(self, name: str) -> Optional[AgentSpec]:
        """获取Agent规格"""
        return self.agent_pool.get(name)
    
    def list_available_agents(self) -> List[str]:
        """列出所有可用Agent"""
        return list(self.agent_pool.keys())
    
    def allocate_for_chapter(self, chapter_outline: str, 
                            bible_context: Dict) -> Tuple[List[AgentSpec], str]:
        """
        为章节分配Agent并返回执行计划
        """
        # 分析章节
        analysis = self.mapper.analyze_chapter(chapter_outline, bible_context)
        
        # 分配Agent
        agents = self.mapper.allocate_agents(
            analysis["primary_type"],
            analysis.get("secondary_types", [])
        )
        
        # 生成计划
        plan = self.mapper.get_execution_plan()
        
        return agents, plan


# 使用示例
if __name__ == "__main__":
    # 创建动态Agent池
    pool = DynamicAgentPool()
    
    # 示例章节大纲
    chapter_outline = """
    第5章：决战之夜
    主角与反派在废弃工厂展开最终对决。
    激烈的战斗中，主角回忆起师父的教诲。
    关键时刻，女主角出现，三人情感纠葛爆发。
    最终主角觉醒新力量，击败反派但付出代价。
    """
    
    bible_context = {
        "genre": "都市异能",
        "tone": "热血",
        "protagonist": "李明"
    }
    
    # 分配Agent
    agents, plan = pool.allocate_for_chapter(chapter_outline, bible_context)
    
    print(plan)
    print(f"\n分配了{len(agents)}个Agent")
    
    # 创建自定义Agent
    custom = pool.create_custom_agent(
        "urban-fantasy-expert",
        ["都市设定", "异能系统", "现代融合"]
    )
    print(f"\n创建自定义Agent: {custom.name}")