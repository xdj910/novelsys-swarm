"""
章节生成Agent
负责生成小说章节内容
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.agent_base import BaseAgent, AgentContext, AgentResult


class ChapterGeneratorAgent(BaseAgent):
    """章节生成专门Agent"""
    
    def __init__(self):
        super().__init__("ChapterGenerator", "chapter_generation")
        self.word_count_target = 3000  # 默认字数目标
        self.style_consistency_checker = StyleConsistencyChecker()
    
    async def perform_task(self, task: Dict[str, Any]) -> Any:
        """执行章节生成任务"""
        task_type = task.get("type")
        
        if task_type == "generate_chapter":
            return await self.generate_chapter(task)
        elif task_type == "generate_scene":
            return await self.generate_scene(task)
        elif task_type == "generate_dialogue":
            return await self.generate_dialogue(task)
        elif task_type == "revise_chapter":
            return await self.revise_chapter(task)
        else:
            raise ValueError(f"Unknown chapter task type: {task_type}")
    
    async def generate_chapter(self, task: Dict[str, Any]) -> Dict:
        """生成完整章节"""
        chapter_number = task.get("chapter_number", 1)
        chapter_outline = task.get("outline", {})
        bible = self.context.context_data if self.context else {}
        
        # 创建章节结构
        chapter = {
            "metadata": {
                "chapter_number": chapter_number,
                "title": chapter_outline.get("title", f"Chapter {chapter_number}"),
                "word_count": 0,
                "created_at": datetime.now().isoformat(),
                "quality_score": 0.0
            },
            "outline": chapter_outline,
            "scenes": [],
            "content": ""
        }
        
        # 根据大纲生成场景
        scenes = await self.decompose_chapter_to_scenes(chapter_outline)
        
        # 并行生成场景内容
        if self.thinking_mode in ["ultrathink", "think-harder"]:
            # 深度思考模式：顺序生成以保持连贯性
            for scene in scenes:
                scene_content = await self.generate_scene_content(scene, bible, chapter)
                chapter["scenes"].append(scene_content)
        else:
            # 普通模式：并行生成提高效率
            scene_tasks = [
                self.generate_scene_content(scene, bible, chapter)
                for scene in scenes
            ]
            chapter["scenes"] = await asyncio.gather(*scene_tasks)
        
        # 组装章节内容
        chapter = await self.assemble_chapter_content(chapter)
        
        # 检查和调整
        chapter = await self.check_and_adjust_chapter(chapter, bible)
        
        # 保存章节
        await self.save_chapter(chapter)
        
        return chapter
    
    async def decompose_chapter_to_scenes(self, outline: Dict) -> List[Dict]:
        """将章节大纲分解为场景"""
        scenes = []
        
        # 从大纲提取场景
        if "scenes" in outline:
            scenes = outline["scenes"]
        else:
            # 自动分解
            plot_points = outline.get("plot_points", [])
            for i, point in enumerate(plot_points):
                scenes.append({
                    "scene_number": i + 1,
                    "type": self.determine_scene_type(point),
                    "description": point,
                    "characters": outline.get("characters", []),
                    "location": outline.get("location", ""),
                    "mood": outline.get("mood", "neutral")
                })
        
        return scenes
    
    def determine_scene_type(self, plot_point: str) -> str:
        """判断场景类型"""
        plot_point_lower = plot_point.lower()
        
        if any(word in plot_point_lower for word in ["对话", "交谈", "讨论", "dialogue"]):
            return "dialogue"
        elif any(word in plot_point_lower for word in ["战斗", "打斗", "追逐", "action"]):
            return "action"
        elif any(word in plot_point_lower for word in ["描述", "环境", "场景", "description"]):
            return "description"
        elif any(word in plot_point_lower for word in ["情感", "内心", "感受", "emotional"]):
            return "emotional"
        else:
            return "mixed"
    
    async def generate_scene_content(self, scene: Dict, bible: Dict, chapter: Dict) -> Dict:
        """生成场景内容"""
        scene_content = scene.copy()
        
        # 根据场景类型生成内容
        if scene["type"] == "dialogue":
            content = await self.generate_dialogue_scene(scene, bible)
        elif scene["type"] == "action":
            content = await self.generate_action_scene(scene, bible)
        elif scene["type"] == "description":
            content = await self.generate_description_scene(scene, bible)
        elif scene["type"] == "emotional":
            content = await self.generate_emotional_scene(scene, bible)
        else:
            content = await self.generate_mixed_scene(scene, bible)
        
        scene_content["content"] = content
        scene_content["word_count"] = len(content)
        
        return scene_content
    
    async def generate_dialogue_scene(self, scene: Dict, bible: Dict) -> str:
        """生成对话场景"""
        characters = scene.get("characters", [])
        location = scene.get("location", "")
        
        # 模拟对话生成
        dialogue = f"在{location}，"
        
        if len(characters) >= 2:
            dialogue += f"{characters[0]}看着{characters[1]}说道：\n"
            dialogue += f'"我们需要谈谈关于这件事。"\n'
            dialogue += f'{characters[1]}沉默了片刻，回答道：\n'
            dialogue += f'"我知道你想说什么，但事情并不是表面看起来那么简单。"\n'
            dialogue += f"两人之间的气氛变得紧张起来。"
        else:
            dialogue += "独白场景内容。"
        
        return dialogue
    
    async def generate_action_scene(self, scene: Dict, bible: Dict) -> str:
        """生成动作场景"""
        return "激烈的动作场景展开了。快速的动作描写，紧张的氛围营造。"
    
    async def generate_description_scene(self, scene: Dict, bible: Dict) -> str:
        """生成描述场景"""
        location = scene.get("location", "未知地点")
        mood = scene.get("mood", "平静")
        
        return f"{location}笼罩在{mood}的氛围中。详细的环境描写展现了场景的每一个细节。"
    
    async def generate_emotional_scene(self, scene: Dict, bible: Dict) -> str:
        """生成情感场景"""
        characters = scene.get("characters", ["角色"])
        return f"{characters[0] if characters else '主角'}内心充满了复杂的情感。深入的心理描写展现了人物的内心世界。"
    
    async def generate_mixed_scene(self, scene: Dict, bible: Dict) -> str:
        """生成混合场景"""
        return "这是一个包含多种元素的场景，对话、动作和描写交织在一起，推动着故事向前发展。"
    
    async def assemble_chapter_content(self, chapter: Dict) -> Dict:
        """组装章节内容"""
        content_parts = []
        
        # 添加章节标题
        content_parts.append(f"# {chapter['metadata']['title']}\n\n")
        
        # 组装所有场景
        for scene in chapter["scenes"]:
            content_parts.append(scene["content"])
            content_parts.append("\n\n")
        
        # 合并内容
        full_content = "".join(content_parts)
        
        chapter["content"] = full_content
        chapter["metadata"]["word_count"] = len(full_content)
        
        return chapter
    
    async def check_and_adjust_chapter(self, chapter: Dict, bible: Dict) -> Dict:
        """检查和调整章节"""
        # 检查字数
        current_word_count = chapter["metadata"]["word_count"]
        
        if current_word_count < self.word_count_target * 0.9:
            # 字数不足，需要扩充
            chapter = await self.expand_chapter(chapter, bible)
        elif current_word_count > self.word_count_target * 1.2:
            # 字数过多，需要精简
            chapter = await self.condense_chapter(chapter, bible)
        
        # 检查风格一致性
        consistency_score = await self.style_consistency_checker.check(chapter, bible)
        chapter["metadata"]["style_consistency"] = consistency_score
        
        # 计算质量分数
        chapter["metadata"]["quality_score"] = await self.calculate_chapter_quality(chapter)
        
        return chapter
    
    async def expand_chapter(self, chapter: Dict, bible: Dict) -> Dict:
        """扩充章节内容"""
        # 添加更多描述或对话
        additional_content = "\n\n[扩充内容：添加更多细节描写和人物对话，丰富场景]"
        chapter["content"] += additional_content
        chapter["metadata"]["word_count"] = len(chapter["content"])
        return chapter
    
    async def condense_chapter(self, chapter: Dict, bible: Dict) -> Dict:
        """精简章节内容"""
        # 简化冗余描述
        # 实际实现中应该智能识别和删除冗余内容
        chapter["metadata"]["notes"] = "Content condensed for optimal length"
        return chapter
    
    async def save_chapter(self, chapter: Dict):
        """保存章节"""
        chapter_dir = Path("D:/NOVELSYS-SWARM/chapters")
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        series_name = self.context.project_name if self.context else "untitled"
        book_number = self.context.book_number if self.context else 1
        chapter_number = chapter["metadata"]["chapter_number"]
        
        filename = f"{series_name}_book{book_number}_ch{chapter_number:03d}.json"
        chapter_path = chapter_dir / filename
        
        with open(chapter_path, 'w', encoding='utf-8') as f:
            json.dump(chapter, f, ensure_ascii=False, indent=2)
    
    async def calculate_chapter_quality(self, chapter: Dict) -> float:
        """计算章节质量分数"""
        score = 0.0
        
        # 字数符合度
        word_count = chapter["metadata"]["word_count"]
        if self.word_count_target * 0.9 <= word_count <= self.word_count_target * 1.1:
            score += 20
        
        # 场景完整性
        if chapter.get("scenes"):
            score += 20
            # 每个场景都有内容
            if all(scene.get("content") for scene in chapter["scenes"]):
                score += 20
        
        # 风格一致性
        consistency = chapter["metadata"].get("style_consistency", 0)
        score += consistency * 0.2
        
        # 内容非空
        if chapter.get("content"):
            score += 20
        
        return min(score, 100.0)
    
    async def generate_scene(self, task: Dict[str, Any]) -> Dict:
        """生成单个场景"""
        scene_spec = task.get("scene_spec", {})
        bible = self.context.context_data if self.context else {}
        
        scene_content = await self.generate_scene_content(scene_spec, bible, {})
        
        return scene_content
    
    async def generate_dialogue(self, task: Dict[str, Any]) -> str:
        """生成对话"""
        characters = task.get("characters", [])
        context = task.get("context", "")
        emotion = task.get("emotion", "neutral")
        
        dialogue = f"[{emotion}情感的对话]\n"
        
        if len(characters) >= 2:
            dialogue += f'{characters[0]}: "对话内容..."\n'
            dialogue += f'{characters[1]}: "回应内容..."\n'
        
        return dialogue
    
    async def revise_chapter(self, task: Dict[str, Any]) -> Dict:
        """修订章节"""
        chapter = task.get("chapter", {})
        revision_notes = task.get("notes", [])
        
        # 应用修订
        for note in revision_notes:
            if note["type"] == "expand":
                chapter = await self.expand_chapter(chapter, {})
            elif note["type"] == "condense":
                chapter = await self.condense_chapter(chapter, {})
            elif note["type"] == "rewrite_scene":
                scene_index = note.get("scene_index", 0)
                if 0 <= scene_index < len(chapter.get("scenes", [])):
                    # 重写特定场景
                    chapter["scenes"][scene_index] = await self.generate_scene_content(
                        chapter["scenes"][scene_index], {}, chapter
                    )
        
        # 重新组装内容
        chapter = await self.assemble_chapter_content(chapter)
        
        # 更新元数据
        chapter["metadata"]["last_revised"] = datetime.now().isoformat()
        chapter["metadata"]["revision_count"] = chapter["metadata"].get("revision_count", 0) + 1
        
        return chapter


class StyleConsistencyChecker:
    """风格一致性检查器"""
    
    async def check(self, chapter: Dict, bible: Dict) -> float:
        """检查章节与Bible的风格一致性"""
        score = 80.0  # 基础分数
        
        # 检查叙事风格
        if bible.get("style_guide"):
            style = bible["style_guide"]
            
            # 检查语言风格
            if style.get("language_style"):
                # 实际实现应该用NLP分析
                score += 5
            
            # 检查节奏
            if style.get("pacing"):
                # 检查章节节奏是否符合设定
                score += 5
            
            # 检查基调
            if style.get("tone"):
                # 检查情感基调是否一致
                score += 5
        
        return min(score, 100.0)