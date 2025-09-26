"""
Stream集成优化器
基于Claude的智能合并系统
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class StreamOutput:
    """Stream输出数据"""
    stream_name: str
    content: str
    style: str
    focus: str
    metadata: Dict[str, Any]


class ClaudeStreamIntegrator:
    """基于Claude的Stream智能集成器"""
    
    def __init__(self):
        self.thinking_mode = "think-hard"  # 默认思考模式
        self.merge_strategies = {
            "dialogue": self.merge_dialogue_focused,
            "action": self.merge_action_focused,
            "description": self.merge_description_focused,
            "emotional": self.merge_emotional_focused,
            "mixed": self.merge_balanced
        }
    
    async def smart_merge(self, stream_outputs: Dict[str, StreamOutput]) -> str:
        """
        使用Claude智能合并多个Stream输出
        
        这个方法会在Claude Code环境中运行，
        利用Claude的能力进行智能文本分析和合并
        """
        
        # 1. 冲突检测 - Claude分析各Stream是否有矛盾
        conflicts = await self.detect_conflicts_with_claude(stream_outputs)
        
        # 2. 解决冲突 - Claude智能判断和调和
        if conflicts:
            stream_outputs = await self.resolve_conflicts_with_claude(
                stream_outputs, conflicts
            )
        
        # 3. 场景类型识别 - Claude分析场景特征
        scene_type = await self.analyze_scene_type_with_claude(stream_outputs)
        
        # 4. 选择合并策略
        merge_strategy = self.merge_strategies.get(scene_type, self.merge_balanced)
        
        # 5. 执行智能合并 - Claude进行创造性融合
        merged_content = await merge_strategy(stream_outputs)
        
        # 6. 优化和润色 - Claude最终优化
        final_content = await self.polish_with_claude(merged_content, scene_type)
        
        return final_content
    
    async def detect_conflicts_with_claude(self, outputs: Dict[str, StreamOutput]) -> List[Dict]:
        """
        使用Claude检测Stream间的冲突
        
        在Claude Code环境中，这会调用Claude的分析能力
        """
        # 构建分析提示
        analysis_prompt = self._build_conflict_detection_prompt(outputs)
        
        # Claude会分析并返回冲突列表
        # 这里模拟Claude的分析结果格式
        conflicts = []
        
        # 检查时空一致性
        if self._has_spatial_temporal_conflict(outputs):
            conflicts.append({
                "type": "spatial_temporal",
                "description": "角色位置或时间设定存在矛盾",
                "affected_streams": ["stream_a", "stream_c"]
            })
        
        # 检查角色状态一致性
        if self._has_character_state_conflict(outputs):
            conflicts.append({
                "type": "character_state",
                "description": "角色状态描述不一致",
                "affected_streams": ["stream_a", "stream_b"]
            })
        
        return conflicts
    
    async def resolve_conflicts_with_claude(
        self, 
        outputs: Dict[str, StreamOutput], 
        conflicts: List[Dict]
    ) -> Dict[str, StreamOutput]:
        """
        使用Claude智能解决冲突
        
        Claude会根据上下文和Bible权威性来判断
        """
        for conflict in conflicts:
            if conflict["type"] == "spatial_temporal":
                # Claude选择最合理的时空设定
                outputs = await self._unify_spatial_temporal(outputs)
            
            elif conflict["type"] == "character_state":
                # Claude选择最符合角色发展的状态
                outputs = await self._unify_character_state(outputs)
        
        return outputs
    
    async def analyze_scene_type_with_claude(self, outputs: Dict[str, StreamOutput]) -> str:
        """
        使用Claude分析场景类型
        
        Claude会综合判断这是什么类型的场景
        """
        # 分析各Stream的内容特征
        content_features = self._extract_content_features(outputs)
        
        # Claude判断场景类型
        if self._is_dialogue_heavy(content_features):
            return "dialogue"
        elif self._is_action_heavy(content_features):
            return "action"
        elif self._is_description_heavy(content_features):
            return "description"
        elif self._is_emotional_heavy(content_features):
            return "emotional"
        else:
            return "mixed"
    
    async def merge_dialogue_focused(self, outputs: Dict[str, StreamOutput]) -> str:
        """对话为主的场景合并策略"""
        # 优先使用Character Stream的对话
        # 轻度使用World Stream的环境描写作为背景
        # minimal使用Prose Stream的修饰
        
        merged = []
        
        # 从Character Stream提取对话
        if "character_psychology" in outputs:
            dialogue = outputs["character_psychology"].content
            merged.append(dialogue)
        
        # 添加少量环境描写
        if "world_building" in outputs:
            setting = self._extract_brief_setting(outputs["world_building"].content)
            if setting:
                merged.insert(0, setting)  # 放在开头设置场景
        
        return "\n\n".join(merged)
    
    async def merge_action_focused(self, outputs: Dict[str, StreamOutput]) -> str:
        """动作为主的场景合并策略"""
        # 优先使用Structure Stream的节奏
        # 强调动作描写
        # 减少心理描写
        
        merged = []
        
        # 从Structure Stream获取动作主线
        if "narrative_structure" in outputs:
            action_line = outputs["narrative_structure"].content
            merged.append(action_line)
        
        # 补充具体动作细节
        if "world_building" in outputs:
            action_details = self._extract_action_details(outputs["world_building"].content)
            merged.append(action_details)
        
        return " ".join(merged)  # 动作场景用紧凑的连接
    
    async def merge_description_focused(self, outputs: Dict[str, StreamOutput]) -> str:
        """描写为主的场景合并策略"""
        # 优先使用World Stream的环境描写
        # 添加Prose Stream的文学修饰
        # 少量心理活动点缀
        
        merged = []
        
        if "world_building" in outputs:
            description = outputs["world_building"].content
            merged.append(description)
        
        if "prose_craft" in outputs:
            prose = outputs["prose_craft"].content
            merged.append(prose)
        
        return "\n\n".join(merged)
    
    async def merge_emotional_focused(self, outputs: Dict[str, StreamOutput]) -> str:
        """情感为主的场景合并策略"""
        # 优先使用Character Stream的心理描写
        # 配合Prose Stream的抒情
        # 少量环境烘托
        
        merged = []
        
        if "character_psychology" in outputs:
            psychology = outputs["character_psychology"].content
            merged.append(psychology)
        
        if "prose_craft" in outputs:
            emotional_prose = outputs["prose_craft"].content
            merged.append(emotional_prose)
        
        return "\n\n".join(merged)
    
    async def merge_balanced(self, outputs: Dict[str, StreamOutput]) -> str:
        """平衡的合并策略"""
        # 均衡使用各Stream
        # Claude智能编织
        
        # 收集所有内容
        all_content = []
        for stream_name, output in outputs.items():
            all_content.append(f"[{output.focus}]\n{output.content}")
        
        # Claude会智能编织这些内容
        # 实际实现时，这里会调用Claude的创造性写作能力
        merged = "\n\n".join(all_content)
        
        return merged
    
    async def polish_with_claude(self, content: str, scene_type: str) -> str:
        """
        使用Claude进行最终润色
        
        Claude会：
        1. 添加自然过渡
        2. 统一文风
        3. 调整节奏
        4. 确保连贯性
        """
        # 在Claude Code环境中，这会是一个Claude任务
        # Claude会根据场景类型进行针对性优化
        
        polished = content  # 实际会由Claude优化
        
        # 添加过渡
        polished = self._add_transitions(polished)
        
        # 调整节奏
        if scene_type == "action":
            polished = self._quicken_pace(polished)
        elif scene_type == "emotional":
            polished = self._slow_pace(polished)
        
        return polished
    
    # === 辅助方法 ===
    
    def _build_conflict_detection_prompt(self, outputs: Dict[str, StreamOutput]) -> str:
        """构建冲突检测提示"""
        prompt = "分析以下Stream输出是否存在冲突：\n\n"
        for name, output in outputs.items():
            prompt += f"{name}: {output.content[:200]}...\n\n"
        return prompt
    
    def _has_spatial_temporal_conflict(self, outputs: Dict[str, StreamOutput]) -> bool:
        """检查时空冲突"""
        # 简化实现，实际由Claude判断
        return False
    
    def _has_character_state_conflict(self, outputs: Dict[str, StreamOutput]) -> bool:
        """检查角色状态冲突"""
        # 简化实现，实际由Claude判断
        return False
    
    async def _unify_spatial_temporal(self, outputs: Dict[str, StreamOutput]) -> Dict:
        """统一时空设定"""
        # Claude会选择最合理的设定
        return outputs
    
    async def _unify_character_state(self, outputs: Dict[str, StreamOutput]) -> Dict:
        """统一角色状态"""
        # Claude会选择最符合角色弧的状态
        return outputs
    
    def _extract_content_features(self, outputs: Dict[str, StreamOutput]) -> Dict:
        """提取内容特征"""
        features = {
            "dialogue_ratio": 0,
            "action_ratio": 0,
            "description_ratio": 0,
            "emotion_ratio": 0
        }
        # 实际由Claude分析
        return features
    
    def _is_dialogue_heavy(self, features: Dict) -> bool:
        """判断是否对话为主"""
        return features.get("dialogue_ratio", 0) > 0.5
    
    def _is_action_heavy(self, features: Dict) -> bool:
        """判断是否动作为主"""
        return features.get("action_ratio", 0) > 0.5
    
    def _is_description_heavy(self, features: Dict) -> bool:
        """判断是否描写为主"""
        return features.get("description_ratio", 0) > 0.5
    
    def _is_emotional_heavy(self, features: Dict) -> bool:
        """判断是否情感为主"""
        return features.get("emotion_ratio", 0) > 0.5
    
    def _extract_brief_setting(self, content: str) -> str:
        """提取简短的环境设定"""
        # 取前50字作为场景设定
        return content[:50] + "..."
    
    def _extract_action_details(self, content: str) -> str:
        """提取动作细节"""
        return content
    
    def _add_transitions(self, content: str) -> str:
        """添加过渡"""
        # Claude会智能添加
        return content
    
    def _quicken_pace(self, content: str) -> str:
        """加快节奏"""
        # 短句、动词
        return content
    
    def _slow_pace(self, content: str) -> str:
        """放慢节奏"""
        # 长句、描写
        return content
    
    def set_thinking_mode(self, mode: str):
        """设置Claude的思考模式"""
        valid_modes = ["think", "think-hard", "think-harder", "ultrathink"]
        if mode in valid_modes:
            self.thinking_mode = mode


# 集成到命令系统的示例
class IntegratedChapterGenerator:
    """集成了智能合并的章节生成器"""
    
    def __init__(self):
        self.integrator = ClaudeStreamIntegrator()
        self.integrator.set_thinking_mode("think-hard")
    
    async def generate_chapter_with_integration(self, chapter_spec: Dict) -> str:
        """生成章节并智能合并"""
        
        # 1. 四个Stream并行工作（现有逻辑）
        stream_outputs = await self.run_parallel_streams(chapter_spec)
        
        # 2. 智能合并（新增）
        merged_content = await self.integrator.smart_merge(stream_outputs)
        
        return merged_content
    
    async def run_parallel_streams(self, spec: Dict) -> Dict[str, StreamOutput]:
        """运行并行Stream（模拟）"""
        return {
            "character_psychology": StreamOutput(
                stream_name="character_psychology",
                content="角色心理描写内容...",
                style="introspective",
                focus="角色内心",
                metadata={}
            ),
            "narrative_structure": StreamOutput(
                stream_name="narrative_structure",
                content="叙事结构内容...",
                style="structured",
                focus="情节推进",
                metadata={}
            ),
            "world_building": StreamOutput(
                stream_name="world_building",
                content="世界构建内容...",
                style="descriptive",
                focus="环境氛围",
                metadata={}
            ),
            "prose_craft": StreamOutput(
                stream_name="prose_craft",
                content="文笔润色内容...",
                style="literary",
                focus="语言艺术",
                metadata={}
            )
        }