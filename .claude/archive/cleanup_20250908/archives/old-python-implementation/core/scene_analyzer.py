"""
场景分析器 - 深度分析场景需求
基于CCPM的issue-analyze思想
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime


class SceneAnalyzer:
    """场景深度分析器"""
    
    def __init__(self):
        self.analysis_dimensions = [
            "character_requirements",
            "emotional_trajectory", 
            "plot_connections",
            "foreshadowing_needs",
            "world_building_elements",
            "dialogue_style",
            "pacing_requirements"
        ]
    
    async def analyze_scene(self, 
                           scene: Dict[str, Any],
                           bible: Dict[str, Any],
                           previous_scenes: List[Dict] = None,
                           next_scenes: List[Dict] = None) -> Dict[str, Any]:
        """
        深度分析场景需求
        
        Args:
            scene: 场景信息
            bible: 小说Bible
            previous_scenes: 前置场景
            next_scenes: 后续场景
            
        Returns:
            场景分析结果
        """
        analysis = {
            "scene_id": scene.get("scene_id"),
            "timestamp": datetime.now().isoformat(),
            "dimensions": {}
        }
        
        # 分析各个维度
        analysis["dimensions"]["characters"] = await self._analyze_characters(scene, bible)
        analysis["dimensions"]["emotions"] = await self._analyze_emotions(scene, previous_scenes)
        analysis["dimensions"]["plot"] = await self._analyze_plot_connections(scene, previous_scenes, next_scenes)
        analysis["dimensions"]["foreshadowing"] = await self._analyze_foreshadowing(scene, bible, next_scenes)
        analysis["dimensions"]["world"] = await self._analyze_world_building(scene, bible)
        analysis["dimensions"]["dialogue"] = await self._analyze_dialogue_needs(scene, bible)
        analysis["dimensions"]["pacing"] = await self._analyze_pacing(scene, previous_scenes, next_scenes)
        
        # 生成具体要求
        analysis["requirements"] = self._generate_requirements(analysis["dimensions"])
        
        # 识别潜在问题
        analysis["potential_issues"] = self._identify_issues(analysis["dimensions"])
        
        # 生成创作建议
        analysis["suggestions"] = self._generate_suggestions(analysis)
        
        return analysis
    
    async def _analyze_characters(self, scene: Dict, bible: Dict) -> Dict:
        """分析角色需求"""
        characters_in_scene = scene.get("characters", [])
        character_analysis = {
            "required_characters": characters_in_scene,
            "character_states": {},
            "interaction_patterns": []
        }
        
        # 从Bible获取角色信息
        all_characters = bible.get("characters", {})
        
        for char_name in characters_in_scene:
            # 查找角色详细信息
            char_info = self._find_character_info(char_name, all_characters)
            
            if char_info:
                character_analysis["character_states"][char_name] = {
                    "personality": char_info.get("personality", ""),
                    "motivation": char_info.get("motivation", ""),
                    "speech_pattern": char_info.get("speech_pattern", ""),
                    "current_goal": char_info.get("current_goal", "")
                }
        
        # 分析角色互动模式
        if len(characters_in_scene) >= 2:
            character_analysis["interaction_patterns"] = self._analyze_interactions(
                characters_in_scene, all_characters
            )
        
        return character_analysis
    
    async def _analyze_emotions(self, scene: Dict, previous_scenes: List[Dict]) -> Dict:
        """分析情感轨迹"""
        scene_mood = scene.get("mood", "neutral")
        scene_type = scene.get("type", "mixed")
        
        emotion_analysis = {
            "primary_emotion": scene_mood,
            "emotional_intensity": self._calculate_intensity(scene_type, scene_mood),
            "emotional_arc": "building"  # rising, stable, falling, building
        }
        
        # 基于前置场景分析情感变化
        if previous_scenes:
            prev_mood = previous_scenes[-1].get("mood", "neutral") if previous_scenes else "neutral"
            emotion_analysis["transition_from"] = prev_mood
            emotion_analysis["emotional_arc"] = self._determine_arc(prev_mood, scene_mood)
        
        return emotion_analysis
    
    async def _analyze_plot_connections(self, scene: Dict, 
                                       previous_scenes: List[Dict],
                                       next_scenes: List[Dict]) -> Dict:
        """分析情节连接"""
        plot_analysis = {
            "plot_function": self._determine_plot_function(scene),
            "connections": {
                "backward": [],
                "forward": []
            },
            "critical_elements": []
        }
        
        # 分析与前置场景的连接
        if previous_scenes:
            for prev_scene in previous_scenes[-3:]:  # 检查最近3个场景
                if self._has_connection(prev_scene, scene):
                    plot_analysis["connections"]["backward"].append({
                        "scene_id": prev_scene.get("scene_id"),
                        "connection_type": "continuity"
                    })
        
        # 分析与后续场景的连接
        if next_scenes:
            for next_scene in next_scenes[:3]:  # 检查接下来3个场景
                if self._needs_setup(scene, next_scene):
                    plot_analysis["connections"]["forward"].append({
                        "scene_id": next_scene.get("scene_id"),
                        "connection_type": "setup"
                    })
        
        return plot_analysis
    
    async def _analyze_foreshadowing(self, scene: Dict, 
                                    bible: Dict,
                                    next_scenes: List[Dict]) -> Dict:
        """分析伏笔需求"""
        foreshadowing = {
            "plant": [],  # 需要埋设的伏笔
            "reveal": [],  # 需要揭示的伏笔
            "maintain": []  # 需要维持的伏笔
        }
        
        # 基于场景类型和位置判断
        scene_number = scene.get("scene_number", 1)
        scene_type = scene.get("type", "mixed")
        
        # 早期场景多埋伏笔
        if scene_number <= 3:
            foreshadowing["plant"].append({
                "type": "mystery_hint",
                "subtlety": "high",
                "purpose": "long_term_setup"
            })
        
        # 中期场景可能揭示部分伏笔
        if 3 < scene_number <= 7:
            foreshadowing["reveal"].append({
                "type": "partial_reveal",
                "impact": "medium"
            })
        
        # 高潮场景揭示主要伏笔
        if scene_type in ["climax", "emotional"]:
            foreshadowing["reveal"].append({
                "type": "major_reveal",
                "impact": "high"
            })
        
        return foreshadowing
    
    async def _analyze_world_building(self, scene: Dict, bible: Dict) -> Dict:
        """分析世界构建需求"""
        location = scene.get("location", "")
        world_building = bible.get("world_building", {})
        
        world_analysis = {
            "location_details": {},
            "atmosphere_elements": [],
            "cultural_elements": []
        }
        
        # 获取地点详情
        if location:
            location_info = world_building.get("locations", {}).get(location, {})
            world_analysis["location_details"] = {
                "description": location_info.get("description", ""),
                "atmosphere": location_info.get("atmosphere", scene.get("mood", "neutral")),
                "key_features": location_info.get("features", [])
            }
        
        # 基于场景类型添加氛围元素
        scene_type = scene.get("type", "mixed")
        if scene_type == "description":
            world_analysis["atmosphere_elements"].extend([
                "detailed_environment",
                "sensory_details",
                "mood_setting"
            ])
        
        return world_analysis
    
    async def _analyze_dialogue_needs(self, scene: Dict, bible: Dict) -> Dict:
        """分析对话需求"""
        scene_type = scene.get("type", "mixed")
        characters = scene.get("characters", [])
        
        dialogue_analysis = {
            "dialogue_intensity": "low",
            "style_requirements": [],
            "key_exchanges": []
        }
        
        if scene_type == "dialogue":
            dialogue_analysis["dialogue_intensity"] = "high"
            dialogue_analysis["style_requirements"] = [
                "character_voice_distinction",
                "natural_flow",
                "subtext_layers"
            ]
            
            # 生成关键对话交换建议
            if len(characters) >= 2:
                dialogue_analysis["key_exchanges"].append({
                    "participants": characters[:2],
                    "purpose": "conflict_escalation",
                    "tone": scene.get("mood", "neutral")
                })
        elif scene_type in ["action", "mixed"]:
            dialogue_analysis["dialogue_intensity"] = "medium"
            dialogue_analysis["style_requirements"] = [
                "brief_impactful",
                "action_integrated"
            ]
        
        return dialogue_analysis
    
    async def _analyze_pacing(self, scene: Dict,
                             previous_scenes: List[Dict],
                             next_scenes: List[Dict]) -> Dict:
        """分析节奏需求"""
        scene_type = scene.get("type", "mixed")
        scene_number = scene.get("scene_number", 1)
        
        pacing_analysis = {
            "tempo": "moderate",  # slow, moderate, fast
            "tension_level": 0.5,  # 0-1
            "recommended_length": scene.get("estimated_words", 600)
        }
        
        # 基于场景类型调整节奏
        tempo_map = {
            "action": "fast",
            "dialogue": "moderate",
            "description": "slow",
            "emotional": "variable",
            "mixed": "moderate"
        }
        pacing_analysis["tempo"] = tempo_map.get(scene_type, "moderate")
        
        # 基于场景位置调整张力
        if scene_type in ["climax", "conflict"]:
            pacing_analysis["tension_level"] = 0.8
        elif scene_type == "resolution":
            pacing_analysis["tension_level"] = 0.3
        
        # 基于前后场景调整
        if previous_scenes:
            prev_type = previous_scenes[-1].get("type", "mixed")
            if prev_type == "action" and scene_type != "action":
                pacing_analysis["tempo"] = "slow"  # 动作后需要缓冲
        
        return pacing_analysis
    
    def _find_character_info(self, char_name: str, all_characters: Dict) -> Optional[Dict]:
        """查找角色信息"""
        for category in ["protagonists", "antagonists", "supporting"]:
            if category in all_characters:
                for char in all_characters[category]:
                    if char.get("name") == char_name:
                        return char
        return None
    
    def _analyze_interactions(self, characters: List[str], all_characters: Dict) -> List[Dict]:
        """分析角色互动模式"""
        interactions = []
        
        # 简单实现：基于角色类型判断互动模式
        for i in range(len(characters)):
            for j in range(i+1, len(characters)):
                interactions.append({
                    "characters": [characters[i], characters[j]],
                    "type": "dialogue",  # dialogue, conflict, cooperation
                    "intensity": "medium"
                })
        
        return interactions
    
    def _calculate_intensity(self, scene_type: str, mood: str) -> float:
        """计算情感强度"""
        base_intensity = {
            "action": 0.7,
            "emotional": 0.8,
            "climax": 0.9,
            "dialogue": 0.5,
            "description": 0.3,
            "mixed": 0.5
        }
        
        mood_modifier = {
            "tense": 0.2,
            "intense": 0.3,
            "peaceful": -0.2,
            "calm": -0.2,
            "neutral": 0
        }
        
        intensity = base_intensity.get(scene_type, 0.5)
        intensity += mood_modifier.get(mood, 0)
        
        return min(max(intensity, 0), 1)  # 限制在0-1之间
    
    def _determine_arc(self, prev_mood: str, current_mood: str) -> str:
        """判断情感弧线"""
        intensity_map = {
            "peaceful": 1,
            "calm": 2,
            "neutral": 3,
            "building": 4,
            "tense": 5,
            "intense": 6
        }
        
        prev_intensity = intensity_map.get(prev_mood, 3)
        curr_intensity = intensity_map.get(current_mood, 3)
        
        if curr_intensity > prev_intensity:
            return "rising"
        elif curr_intensity < prev_intensity:
            return "falling"
        else:
            return "stable"
    
    def _determine_plot_function(self, scene: Dict) -> str:
        """判断场景的情节功能"""
        scene_type = scene.get("type", "mixed")
        scene_number = scene.get("scene_number", 1)
        
        if scene_number == 1:
            return "setup"
        elif scene_type == "climax":
            return "climax"
        elif scene_type == "resolution":
            return "resolution"
        elif scene_type == "conflict":
            return "complication"
        else:
            return "development"
    
    def _has_connection(self, scene1: Dict, scene2: Dict) -> bool:
        """判断两个场景是否有连接"""
        # 简单判断：共享角色或地点
        chars1 = set(scene1.get("characters", []))
        chars2 = set(scene2.get("characters", []))
        
        if chars1.intersection(chars2):
            return True
        
        if scene1.get("location") == scene2.get("location"):
            return True
        
        return False
    
    def _needs_setup(self, current_scene: Dict, future_scene: Dict) -> bool:
        """判断是否需要为未来场景做铺垫"""
        # 如果未来场景是高潮或冲突，当前场景需要铺垫
        future_type = future_scene.get("type", "mixed")
        return future_type in ["climax", "conflict", "emotional"]
    
    def _generate_requirements(self, dimensions: Dict) -> List[Dict]:
        """生成具体创作要求"""
        requirements = []
        
        # 基于分析维度生成要求
        if dimensions.get("characters", {}).get("required_characters"):
            requirements.append({
                "type": "character",
                "priority": "high",
                "description": f"Include characters: {', '.join(dimensions['characters']['required_characters'])}"
            })
        
        if dimensions.get("emotions", {}).get("emotional_intensity", 0) > 0.7:
            requirements.append({
                "type": "emotion",
                "priority": "high",
                "description": "Build high emotional intensity"
            })
        
        if dimensions.get("foreshadowing", {}).get("plant"):
            requirements.append({
                "type": "foreshadowing",
                "priority": "medium",
                "description": "Plant subtle hints for future reveals"
            })
        
        return requirements
    
    def _identify_issues(self, dimensions: Dict) -> List[Dict]:
        """识别潜在问题"""
        issues = []
        
        # 检查角色一致性
        if not dimensions.get("characters", {}).get("character_states"):
            issues.append({
                "type": "character_undefined",
                "severity": "medium",
                "description": "Character details not found in Bible"
            })
        
        # 检查情感过渡
        emotions = dimensions.get("emotions", {})
        if emotions.get("emotional_arc") == "rising" and emotions.get("emotional_intensity", 0) > 0.9:
            issues.append({
                "type": "emotional_overload",
                "severity": "low",
                "description": "Very high emotional intensity - ensure reader can process"
            })
        
        return issues
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """生成创作建议"""
        suggestions = []
        
        # 基于分析结果生成建议
        emotions = analysis["dimensions"].get("emotions", {})
        if emotions.get("emotional_arc") == "rising":
            suggestions.append("Build tension gradually through dialogue and action")
        
        pacing = analysis["dimensions"].get("pacing", {})
        if pacing.get("tempo") == "fast":
            suggestions.append("Use short sentences and active verbs for fast pacing")
        elif pacing.get("tempo") == "slow":
            suggestions.append("Include sensory details and introspection for slower pacing")
        
        dialogue = analysis["dimensions"].get("dialogue", {})
        if dialogue.get("dialogue_intensity") == "high":
            suggestions.append("Focus on distinctive character voices and subtext")
        
        return suggestions
    
    async def save_analysis(self, analysis: Dict, output_path: Path):
        """保存分析结果"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        return output_path