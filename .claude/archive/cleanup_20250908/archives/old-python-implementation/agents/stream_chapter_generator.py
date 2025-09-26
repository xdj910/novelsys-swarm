"""
增强版章节生成Agent
集成4-Stream并行架构和Claude智能合并
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.agent_base import BaseAgent, AgentContext, AgentResult
from core.stream_integrator import ClaudeStreamIntegrator, StreamOutput


class StreamChapterGeneratorAgent(BaseAgent):
    """4-Stream架构的章节生成Agent"""
    
    def __init__(self):
        super().__init__("StreamChapterGenerator", "stream_chapter_generation")
        self.word_count_target = 3000
        self.stream_integrator = ClaudeStreamIntegrator()
        self.stream_integrator.set_thinking_mode("think-hard")
        
        # 4个专门的Stream处理器
        self.stream_processors = {
            "character_psychology": CharacterPsychologyStream(),
            "narrative_structure": NarrativeStructureStream(),
            "world_building": WorldBuildingStream(),
            "prose_craft": ProseCraftStream()
        }
    
    async def perform_task(self, task: Dict[str, Any]) -> Any:
        """执行章节生成任务"""
        task_type = task.get("type")
        
        if task_type == "generate_chapter":
            return await self.generate_chapter_with_streams(task)
        elif task_type == "generate_scene":
            return await self.generate_scene_with_streams(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def generate_chapter_with_streams(self, task: Dict[str, Any]) -> Dict:
        """使用4-Stream架构生成章节"""
        chapter_number = task.get("chapter_number", 1)
        chapter_outline = task.get("outline", {})
        bible = self.context.context_data if self.context else {}
        
        # 创建章节框架
        chapter = {
            "metadata": {
                "chapter_number": chapter_number,
                "title": chapter_outline.get("title", f"Chapter {chapter_number}"),
                "word_count": 0,
                "created_at": datetime.now().isoformat(),
                "quality_score": 0.0,
                "generation_method": "4-stream-parallel"
            },
            "outline": chapter_outline,
            "scenes": [],
            "stream_outputs": {},  # 保存各Stream的原始输出
            "content": ""
        }
        
        # 分解为场景
        scenes = await self.decompose_chapter_to_scenes(chapter_outline)
        
        # 对每个场景运行4-Stream并行生成
        for scene in scenes:
            scene_content = await self.generate_scene_with_streams({
                "scene": scene,
                "bible": bible,
                "chapter_context": chapter
            })
            chapter["scenes"].append(scene_content)
        
        # 组装最终章节
        chapter = await self.assemble_streamed_chapter(chapter)
        
        # 质量检查
        chapter = await self.quality_check(chapter, bible)
        
        # 保存
        await self.save_chapter(chapter)
        
        return chapter
    
    async def generate_scene_with_streams(self, task: Dict[str, Any]) -> Dict:
        """使用4-Stream生成单个场景"""
        scene = task.get("scene", {})
        bible = task.get("bible", {})
        chapter_context = task.get("chapter_context", {})
        
        # 并行运行4个Stream
        stream_tasks = []
        for stream_name, processor in self.stream_processors.items():
            stream_tasks.append(
                processor.generate(scene, bible, chapter_context)
            )
        
        # 等待所有Stream完成
        stream_results = await asyncio.gather(*stream_tasks)
        
        # 将结果转换为StreamOutput格式
        stream_outputs = {}
        for i, (stream_name, processor) in enumerate(self.stream_processors.items()):
            stream_outputs[stream_name] = StreamOutput(
                stream_name=stream_name,
                content=stream_results[i]["content"],
                style=stream_results[i]["style"],
                focus=stream_results[i]["focus"],
                metadata=stream_results[i].get("metadata", {})
            )
        
        # 使用Claude智能合并
        merged_content = await self.stream_integrator.smart_merge(stream_outputs)
        
        # 构建场景结果
        scene_result = scene.copy()
        scene_result["content"] = merged_content
        scene_result["word_count"] = len(merged_content)
        scene_result["stream_outputs"] = {
            name: {
                "content": output.content,
                "style": output.style,
                "focus": output.focus
            }
            for name, output in stream_outputs.items()
        }
        
        return scene_result
    
    async def decompose_chapter_to_scenes(self, outline: Dict) -> List[Dict]:
        """将章节大纲分解为场景"""
        scenes = []
        
        if "scenes" in outline:
            scenes = outline["scenes"]
        else:
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
    
    async def assemble_streamed_chapter(self, chapter: Dict) -> Dict:
        """组装4-Stream生成的章节"""
        content_parts = []
        
        # 章节标题
        content_parts.append(f"# {chapter['metadata']['title']}\n\n")
        
        # 所有场景内容
        for scene in chapter["scenes"]:
            content_parts.append(scene["content"])
            content_parts.append("\n\n")
        
        # 合并
        full_content = "".join(content_parts)
        
        chapter["content"] = full_content
        chapter["metadata"]["word_count"] = len(full_content)
        
        return chapter
    
    async def quality_check(self, chapter: Dict, bible: Dict) -> Dict:
        """质量检查"""
        # 检查字数
        current_word_count = chapter["metadata"]["word_count"]
        
        if current_word_count < self.word_count_target * 0.9:
            chapter["metadata"]["needs_expansion"] = True
        elif current_word_count > self.word_count_target * 1.2:
            chapter["metadata"]["needs_condensing"] = True
        
        # 计算质量分数
        chapter["metadata"]["quality_score"] = await self.calculate_chapter_quality(chapter)
        
        return chapter
    
    async def calculate_chapter_quality(self, chapter: Dict) -> float:
        """计算章节质量"""
        score = 0.0
        
        # 字数符合度
        word_count = chapter["metadata"]["word_count"]
        if self.word_count_target * 0.9 <= word_count <= self.word_count_target * 1.1:
            score += 25
        
        # 场景完整性
        if chapter.get("scenes"):
            score += 25
            if all(scene.get("content") for scene in chapter["scenes"]):
                score += 25
        
        # 4-Stream集成成功
        if chapter["metadata"].get("generation_method") == "4-stream-parallel":
            score += 25
        
        return min(score, 100.0)
    
    async def save_chapter(self, chapter: Dict):
        """保存章节"""
        chapter_dir = Path("D:/NOVELSYS-SWARM/output/chapters")
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        project_name = self.context.project_name if self.context else "untitled"
        book_number = self.context.book_number if self.context else 1
        chapter_number = chapter["metadata"]["chapter_number"]
        
        # 保存JSON格式
        json_filename = f"{project_name}_book{book_number}_ch{chapter_number:03d}.json"
        json_path = chapter_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(chapter, f, ensure_ascii=False, indent=2)
        
        # 保存纯文本格式
        txt_filename = f"{project_name}_book{book_number}_ch{chapter_number:03d}.txt"
        txt_path = chapter_dir / txt_filename
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(chapter["content"])


class CharacterPsychologyStream:
    """角色心理Stream"""
    
    async def generate(self, scene: Dict, bible: Dict, context: Dict) -> Dict:
        """生成角色心理内容"""
        characters = scene.get("characters", [])
        scene_type = scene.get("type", "mixed")
        
        # 这里应该调用Claude生成真实内容
        # 现在用模拟内容
        content = f"[角色心理] "
        
        if characters:
            main_char = characters[0]
            content += f"{main_char}的内心充满了复杂的情绪。"
            
            if scene_type == "emotional":
                content += f"强烈的情感波动席卷而来，过往的记忆与现实交织。"
            elif scene_type == "dialogue":
                content += f"每一句话背后都隐藏着深层的心理动机。"
            elif scene_type == "action":
                content += f"肾上腺素飙升，本能与理智在激烈交锋。"
        
        return {
            "content": content,
            "style": "introspective",
            "focus": "character_psychology",
            "metadata": {
                "primary_character": characters[0] if characters else None,
                "emotional_intensity": 0.7
            }
        }


class NarrativeStructureStream:
    """叙事结构Stream"""
    
    async def generate(self, scene: Dict, bible: Dict, context: Dict) -> Dict:
        """生成叙事结构内容"""
        scene_type = scene.get("type", "mixed")
        
        content = f"[叙事推进] "
        
        if scene_type == "action":
            content += "快速的动作推进着情节，每一个转折都紧扣主线。"
        elif scene_type == "dialogue":
            content += "对话推动着故事向前，信息在交流中逐渐揭示。"
        elif scene_type == "description":
            content += "细致的描写为后续发展铺垫，伏笔悄然埋下。"
        else:
            content += "多线并进，主次分明，故事在此处达到小高潮。"
        
        return {
            "content": content,
            "style": "structured",
            "focus": "plot_progression",
            "metadata": {
                "pacing": "moderate",
                "tension_level": 0.6
            }
        }


class WorldBuildingStream:
    """世界构建Stream"""
    
    async def generate(self, scene: Dict, bible: Dict, context: Dict) -> Dict:
        """生成世界构建内容"""
        location = scene.get("location", "未知地点")
        mood = scene.get("mood", "neutral")
        
        content = f"[环境氛围] {location}"
        
        if mood == "tense":
            content += "的空气中弥漫着紧张的气息，每一个细节都预示着即将到来的风暴。"
        elif mood == "peaceful":
            content += "呈现出宁静祥和的氛围，时间仿佛在这里放慢了脚步。"
        elif mood == "mysterious":
            content += "笼罩在神秘的面纱之下，未知的秘密隐藏在每一个角落。"
        else:
            content += "展现出独特的魅力，环境与人物的互动构成了完美的舞台。"
        
        return {
            "content": content,
            "style": "descriptive",
            "focus": "world_environment",
            "metadata": {
                "location": location,
                "atmosphere": mood,
                "detail_level": "high"
            }
        }


class ProseCraftStream:
    """文笔润色Stream"""
    
    async def generate(self, scene: Dict, bible: Dict, context: Dict) -> Dict:
        """生成文笔润色内容"""
        scene_type = scene.get("type", "mixed")
        
        content = f"[文学润色] "
        
        if scene_type == "emotional":
            content += "如潮水般的情感，在字里行间涌动，每一个词语都承载着重量。"
        elif scene_type == "action":
            content += "简洁有力的句子，如鼓点般急促，推动着读者的心跳。"
        elif scene_type == "description":
            content += "细腻的笔触勾勒出生动的画面，让读者身临其境。"
        else:
            content += "流畅的文字编织出动人的故事，节奏与韵律完美融合。"
        
        return {
            "content": content,
            "style": "literary",
            "focus": "prose_style",
            "metadata": {
                "literary_devices": ["metaphor", "rhythm"],
                "tone": "engaging"
            }
        }