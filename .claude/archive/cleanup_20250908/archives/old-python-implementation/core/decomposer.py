"""
章节分解器 - 将章节分解为可并行执行的场景
基于CCPM的Epic→Issue→Module思想
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Scene:
    """场景定义"""
    scene_id: str
    chapter_number: int
    scene_number: int
    type: str  # dialogue, action, description, emotional, mixed
    title: str
    description: str
    characters: List[str]
    location: str
    mood: str
    estimated_words: int
    dependencies: List[str] = None  # 依赖的其他场景
    status: str = "pending"  # pending, in_progress, completed, blocked
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_issue_format(self) -> Dict:
        """转换为Issue格式（CCPM风格）"""
        return {
            "id": self.scene_id,
            "type": "scene",
            "title": f"Scene {self.scene_number}: {self.title}",
            "description": self.description,
            "metadata": {
                "chapter": self.chapter_number,
                "scene": self.scene_number,
                "scene_type": self.type,
                "characters": self.characters,
                "location": self.location,
                "mood": self.mood,
                "estimated_words": self.estimated_words
            },
            "dependencies": self.dependencies or [],
            "status": self.status,
            "created_at": datetime.now().isoformat()
        }


class ChapterDecomposer:
    """章节分解器"""
    
    def __init__(self):
        self.default_scenes_per_chapter = 5
        self.scene_templates = {
            "opening": {
                "type": "mixed",
                "mood": "establishing",
                "words": 600
            },
            "development": {
                "type": "dialogue",
                "mood": "building",
                "words": 500
            },
            "conflict": {
                "type": "action",
                "mood": "tense",
                "words": 700
            },
            "climax": {
                "type": "emotional",
                "mood": "intense",
                "words": 600
            },
            "resolution": {
                "type": "description",
                "mood": "settling",
                "words": 600
            }
        }
    
    async def decompose_chapter(self, 
                               chapter_outline: Dict[str, Any],
                               bible: Dict[str, Any]) -> List[Scene]:
        """
        将章节大纲分解为场景
        
        Args:
            chapter_outline: 章节大纲
            bible: 小说Bible
            
        Returns:
            场景列表
        """
        chapter_number = chapter_outline.get("chapter_number", 1)
        plot_points = chapter_outline.get("plot_points", [])
        characters = chapter_outline.get("characters", [])
        location = chapter_outline.get("location", "")
        
        scenes = []
        
        # 如果有明确的情节点，基于情节点分解
        if plot_points and len(plot_points) >= 3:
            scenes = await self._decompose_by_plot_points(
                chapter_number, plot_points, characters, location
            )
        else:
            # 使用标准模板分解
            scenes = await self._decompose_by_template(
                chapter_number, chapter_outline, bible
            )
        
        # 建立场景依赖关系
        scenes = self._establish_dependencies(scenes)
        
        return scenes
    
    async def _decompose_by_plot_points(self,
                                       chapter_number: int,
                                       plot_points: List[str],
                                       characters: List[str],
                                       location: str) -> List[Scene]:
        """基于情节点分解"""
        scenes = []
        
        for i, plot_point in enumerate(plot_points):
            scene_number = i + 1
            scene_type = self._determine_scene_type(plot_point)
            
            scene = Scene(
                scene_id=f"ch{chapter_number:03d}_sc{scene_number:02d}",
                chapter_number=chapter_number,
                scene_number=scene_number,
                type=scene_type,
                title=self._extract_scene_title(plot_point),
                description=plot_point,
                characters=self._extract_scene_characters(plot_point, characters),
                location=self._extract_scene_location(plot_point, location),
                mood=self._determine_mood(plot_point, scene_type),
                estimated_words=self._estimate_word_count(scene_type)
            )
            
            scenes.append(scene)
        
        return scenes
    
    async def _decompose_by_template(self,
                                    chapter_number: int,
                                    chapter_outline: Dict,
                                    bible: Dict) -> List[Scene]:
        """使用标准模板分解"""
        scenes = []
        templates = ["opening", "development", "conflict", "climax", "resolution"]
        
        characters = chapter_outline.get("characters", 
                                        bible.get("characters", {}).get("protagonists", []))
        location = chapter_outline.get("location", "主要场景")
        
        for i, template_name in enumerate(templates):
            scene_number = i + 1
            template = self.scene_templates[template_name]
            
            scene = Scene(
                scene_id=f"ch{chapter_number:03d}_sc{scene_number:02d}",
                chapter_number=chapter_number,
                scene_number=scene_number,
                type=template["type"],
                title=f"{template_name.capitalize()} Scene",
                description=f"Chapter {chapter_number} {template_name}",
                characters=characters[:2] if scene_number % 2 == 0 else characters,
                location=location,
                mood=template["mood"],
                estimated_words=template["words"]
            )
            
            scenes.append(scene)
        
        return scenes
    
    def _determine_scene_type(self, plot_point: str) -> str:
        """判断场景类型"""
        plot_lower = plot_point.lower()
        
        if any(word in plot_lower for word in ["对话", "交谈", "讨论", "dialogue", "talk"]):
            return "dialogue"
        elif any(word in plot_lower for word in ["战斗", "打斗", "追逐", "action", "fight"]):
            return "action"
        elif any(word in plot_lower for word in ["描述", "环境", "场景", "description"]):
            return "description"
        elif any(word in plot_lower for word in ["情感", "内心", "感受", "emotional", "feeling"]):
            return "emotional"
        else:
            return "mixed"
    
    def _extract_scene_title(self, plot_point: str) -> str:
        """提取场景标题"""
        # 取前20个字符作为标题
        title = plot_point[:20]
        if len(plot_point) > 20:
            title += "..."
        return title
    
    def _extract_scene_characters(self, plot_point: str, all_characters: List[str]) -> List[str]:
        """提取场景中的角色"""
        scene_characters = []
        
        for character in all_characters:
            if character in plot_point:
                scene_characters.append(character)
        
        # 如果没有找到，返回前两个主要角色
        if not scene_characters and all_characters:
            scene_characters = all_characters[:2]
        
        return scene_characters
    
    def _extract_scene_location(self, plot_point: str, default_location: str) -> str:
        """提取场景地点"""
        # 简单实现，后续可以用NLP改进
        location_keywords = ["在", "于", "at", "in", "on"]
        
        for keyword in location_keywords:
            if keyword in plot_point:
                # 尝试提取地点
                parts = plot_point.split(keyword)
                if len(parts) > 1:
                    location = parts[1].split()[0] if parts[1].split() else default_location
                    return location
        
        return default_location
    
    def _determine_mood(self, plot_point: str, scene_type: str) -> str:
        """判断场景情绪"""
        mood_map = {
            "action": "tense",
            "emotional": "intense",
            "dialogue": "neutral",
            "description": "calm",
            "mixed": "building"
        }
        
        # 基于关键词调整
        if any(word in plot_point.lower() for word in ["紧张", "危险", "tense", "danger"]):
            return "tense"
        elif any(word in plot_point.lower() for word in ["平静", "宁静", "peaceful", "calm"]):
            return "peaceful"
        elif any(word in plot_point.lower() for word in ["神秘", "诡异", "mysterious", "strange"]):
            return "mysterious"
        
        return mood_map.get(scene_type, "neutral")
    
    def _estimate_word_count(self, scene_type: str) -> int:
        """估算场景字数"""
        word_count_map = {
            "action": 700,
            "dialogue": 500,
            "description": 600,
            "emotional": 600,
            "mixed": 600
        }
        return word_count_map.get(scene_type, 600)
    
    def _establish_dependencies(self, scenes: List[Scene]) -> List[Scene]:
        """建立场景间的依赖关系"""
        for i, scene in enumerate(scenes):
            if i > 0:
                # 默认依赖前一个场景（线性依赖）
                scene.dependencies = [scenes[i-1].scene_id]
            
            # 特殊依赖规则
            if scene.type == "climax" and i > 2:
                # 高潮场景依赖所有前置场景
                scene.dependencies = [s.scene_id for s in scenes[:i]]
            elif scene.type == "resolution":
                # 结局场景依赖高潮场景
                climax_scenes = [s for s in scenes[:i] if s.type in ["climax", "emotional"]]
                if climax_scenes:
                    scene.dependencies = [s.scene_id for s in climax_scenes]
        
        return scenes
    
    async def save_decomposition(self, scenes: List[Scene], output_dir: Path):
        """保存分解结果"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存整体分解结果
        decomposition = {
            "total_scenes": len(scenes),
            "chapter_number": scenes[0].chapter_number if scenes else 0,
            "created_at": datetime.now().isoformat(),
            "scenes": [scene.to_dict() for scene in scenes]
        }
        
        decomposition_file = output_dir / f"chapter_{scenes[0].chapter_number:03d}_decomposition.json"
        with open(decomposition_file, 'w', encoding='utf-8') as f:
            json.dump(decomposition, f, ensure_ascii=False, indent=2)
        
        # 为每个场景创建Issue文件（CCPM风格）
        issues_dir = output_dir / "issues"
        issues_dir.mkdir(exist_ok=True)
        
        for scene in scenes:
            issue_file = issues_dir / f"{scene.scene_id}.json"
            with open(issue_file, 'w', encoding='utf-8') as f:
                json.dump(scene.to_issue_format(), f, ensure_ascii=False, indent=2)
        
        return decomposition_file
    
    def analyze_dependencies(self, scenes: List[Scene]) -> Dict[str, Any]:
        """分析场景依赖关系，找出可并行的场景组"""
        parallel_groups = []
        current_group = []
        
        for scene in scenes:
            if not scene.dependencies:
                # 没有依赖的场景可以并行
                current_group.append(scene.scene_id)
            else:
                # 检查依赖是否在当前组中
                deps_in_current = any(dep in current_group for dep in scene.dependencies)
                
                if deps_in_current:
                    # 依赖在当前组，需要新建组
                    if current_group:
                        parallel_groups.append(current_group)
                    current_group = [scene.scene_id]
                else:
                    # 可以加入当前组
                    current_group.append(scene.scene_id)
        
        if current_group:
            parallel_groups.append(current_group)
        
        return {
            "total_scenes": len(scenes),
            "parallel_groups": parallel_groups,
            "max_parallel": max(len(group) for group in parallel_groups) if parallel_groups else 0,
            "execution_stages": len(parallel_groups)
        }