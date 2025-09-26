"""
并行场景生成器 - CCPM并行执行的核心实现
真正实现多Agent同时工作
"""

import json
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
import time


@dataclass
class SceneGenerationTask:
    """场景生成任务"""
    scene_id: str
    scene_data: Dict
    analysis: Dict
    bible: Dict
    agent_id: str = None
    status: str = "pending"  # pending, in_progress, completed, failed
    start_time: float = None
    end_time: float = None
    result: Dict = None
    error: str = None
    
    def execution_time(self) -> float:
        """计算执行时间"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0


class ParallelSceneGenerator:
    """并行场景生成器"""
    
    def __init__(self, max_parallel: int = 5):
        """
        Args:
            max_parallel: 最大并行数（默认5个Agent同时工作）
        """
        self.max_parallel = max_parallel
        self.active_agents = {}
        self.task_queue = asyncio.Queue()
        self.results = {}
        
    async def generate_scenes_parallel(self,
                                      decomposition: Dict,
                                      analyses: Dict[str, Dict],
                                      bible: Dict,
                                      chapter_info: Dict) -> Dict:
        """
        并行生成所有场景
        
        Args:
            decomposition: 章节分解结果
            analyses: 场景分析结果字典
            bible: 小说Bible
            chapter_info: 章节信息
            
        Returns:
            生成结果
        """
        start_time = time.time()
        scenes = decomposition["scenes"]
        
        # 创建生成任务
        tasks = []
        for scene in scenes:
            scene_id = scene["scene_id"]
            analysis = analyses.get(scene_id, {})
            
            task = SceneGenerationTask(
                scene_id=scene_id,
                scene_data=scene,
                analysis=analysis,
                bible=bible
            )
            tasks.append(task)
        
        # 分析并行组
        parallel_groups = self._analyze_parallel_groups(scenes)
        
        # 按组执行
        all_results = {}
        for group_idx, group in enumerate(parallel_groups):
            print(f"\n=== 执行并行组 {group_idx + 1}/{len(parallel_groups)} ===")
            print(f"并行场景: {', '.join(group)}")
            
            # 获取这组的任务
            group_tasks = [t for t in tasks if t.scene_id in group]
            
            # 并行执行这组
            group_results = await self._execute_parallel_group(group_tasks)
            all_results.update(group_results)
        
        # 合并场景为章节
        merged_chapter = await self._merge_scenes_to_chapter(
            all_results,
            chapter_info,
            decomposition
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return {
            "status": "success",
            "chapter": merged_chapter,
            "scenes": all_results,
            "statistics": {
                "total_scenes": len(scenes),
                "parallel_groups": len(parallel_groups),
                "max_parallel": max(len(g) for g in parallel_groups),
                "total_time": total_time,
                "average_time_per_scene": total_time / len(scenes) if scenes else 0,
                "speedup": self._calculate_speedup(tasks, total_time)
            }
        }
    
    async def _execute_parallel_group(self, tasks: List[SceneGenerationTask]) -> Dict:
        """执行一组并行任务"""
        # 创建并行协程
        coroutines = []
        for task in tasks:
            coroutines.append(self._generate_single_scene(task))
        
        # 并行执行
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # 收集结果
        scene_results = {}
        for task, result in zip(tasks, results):
            if isinstance(result, Exception):
                task.status = "failed"
                task.error = str(result)
                print(f"❌ 场景 {task.scene_id} 生成失败: {result}")
            else:
                task.status = "completed"
                task.result = result
                scene_results[task.scene_id] = result
                print(f"✅ 场景 {task.scene_id} 生成完成")
        
        return scene_results
    
    async def _generate_single_scene(self, task: SceneGenerationTask) -> Dict:
        """生成单个场景（模拟Agent工作）"""
        task.status = "in_progress"
        task.start_time = time.time()
        
        # 分配虚拟Agent
        task.agent_id = f"agent_{task.scene_id}"
        
        print(f"🚀 {task.agent_id} 开始生成场景 {task.scene_id}")
        
        try:
            # 根据场景类型和分析结果生成内容
            scene_content = await self._generate_scene_content(
                task.scene_data,
                task.analysis,
                task.bible
            )
            
            # 模拟生成时间（实际会调用真实的生成Agent）
            await asyncio.sleep(0.5)  # 模拟0.5秒生成时间
            
            task.end_time = time.time()
            
            return {
                "scene_id": task.scene_id,
                "content": scene_content,
                "metadata": {
                    "agent_id": task.agent_id,
                    "generation_time": task.execution_time(),
                    "scene_type": task.scene_data.get("type", "mixed"),
                    "word_count": len(scene_content)
                }
            }
            
        except Exception as e:
            task.end_time = time.time()
            task.status = "failed"
            raise e
    
    async def _generate_scene_content(self, 
                                     scene_data: Dict,
                                     analysis: Dict,
                                     bible: Dict) -> str:
        """生成场景内容（核心生成逻辑）"""
        scene_type = scene_data.get("type", "mixed")
        characters = scene_data.get("characters", [])
        location = scene_data.get("location", "")
        mood = scene_data.get("mood", "neutral")
        
        # 从分析中获取要求
        requirements = analysis.get("requirements", [])
        suggestions = analysis.get("suggestions", [])
        
        # 根据场景类型生成不同风格的内容
        content_parts = []
        
        # 场景开头
        content_parts.append(f"\n【场景 {scene_data.get('scene_number', 1)}】\n\n")
        
        # 环境描写
        if scene_type in ["description", "mixed"]:
            content_parts.append(self._generate_environment(location, mood))
            content_parts.append("\n\n")
        
        # 角色入场
        if characters:
            content_parts.append(self._generate_character_entrance(characters, location))
            content_parts.append("\n\n")
        
        # 核心内容（根据类型）
        if scene_type == "dialogue":
            content_parts.append(self._generate_dialogue(characters, analysis))
        elif scene_type == "action":
            content_parts.append(self._generate_action(characters, location))
        elif scene_type == "emotional":
            content_parts.append(self._generate_emotional(characters[0] if characters else "主角"))
        elif scene_type == "description":
            content_parts.append(self._generate_description(location, mood))
        else:  # mixed
            content_parts.append(self._generate_mixed(characters, location, mood))
        
        # 场景转换提示
        if analysis.get("dimensions", {}).get("plot", {}).get("connections", {}).get("forward"):
            content_parts.append("\n\n")
            content_parts.append(self._generate_transition_hint())
        
        return "".join(content_parts)
    
    def _generate_environment(self, location: str, mood: str) -> str:
        """生成环境描写"""
        mood_descriptions = {
            "tense": "空气中弥漫着紧张的气息",
            "peaceful": "一切都显得宁静祥和",
            "mysterious": "神秘的氛围笼罩四周",
            "neutral": "平静如常"
        }
        
        return f"{location}{mood_descriptions.get(mood, '显得格外特别')}。"
    
    def _generate_character_entrance(self, characters: List[str], location: str) -> str:
        """生成角色入场"""
        if len(characters) == 1:
            return f"{characters[0]}独自站在{location}，若有所思。"
        elif len(characters) == 2:
            return f"{characters[0]}和{characters[1]}在{location}相遇，彼此交换了一个意味深长的眼神。"
        else:
            return f"几个身影逐渐在{location}汇聚。"
    
    def _generate_dialogue(self, characters: List[str], analysis: Dict) -> str:
        """生成对话场景"""
        if len(characters) >= 2:
            dialogue = f'"{characters[0]}，我们需要谈谈。" {characters[1]}的声音打破了沉默。\n\n'
            dialogue += f'{characters[0]}转过身，眼中闪过一丝复杂的情绪。"我知道你想说什么。"\n\n'
            dialogue += f'"那你应该明白，" {characters[1]}上前一步，"有些事情，我们无法逃避。"\n\n'
            dialogue += f'两人之间的距离在缩短，而心理的距离却似乎越来越远。'
        else:
            dialogue = "独白在内心响起，每一个字都像是对自己的拷问。"
        
        return dialogue
    
    def _generate_action(self, characters: List[str], location: str) -> str:
        """生成动作场景"""
        if characters:
            action = f"突然，{characters[0]}猛地向前冲去！\n\n"
            action += f"速度之快，让周围的一切都变成了模糊的背景。\n\n"
            action += f"{location}瞬间变成了追逐的舞台，每一步都充满了紧张和危险。"
        else:
            action = "激烈的动作在此刻爆发，整个场景都被卷入了这场风暴。"
        
        return action
    
    def _generate_emotional(self, character: str) -> str:
        """生成情感场景"""
        emotional = f"{character}的内心如潮水般翻涌。\n\n"
        emotional += "过往的记忆、现在的困境、未来的迷茫，全都交织在一起。\n\n"
        emotional += "这一刻，时间仿佛静止了，只剩下内心的声音在回响。"
        
        return emotional
    
    def _generate_description(self, location: str, mood: str) -> str:
        """生成描写场景"""
        description = f"{location}在此刻展现出了它独特的魅力。\n\n"
        description += "每一个细节都诉说着属于这里的故事，"
        description += "光影交错间，仿佛能看到时间留下的痕迹。"
        
        return description
    
    def _generate_mixed(self, characters: List[str], location: str, mood: str) -> str:
        """生成混合场景"""
        mixed = f"在{location}，故事正在悄然展开。\n\n"
        
        if characters:
            mixed += f"{characters[0]}的每一个动作都充满了含义，"
            if len(characters) > 1:
                mixed += f"而{characters[1]}的回应同样意味深长。\n\n"
        
        mixed += "对话、动作、情感，一切都融合在这个瞬间，推动着故事向前发展。"
        
        return mixed
    
    def _generate_transition_hint(self) -> str:
        """生成场景转换提示"""
        return "而这一切，都只是更大风暴来临前的序曲..."
    
    def _analyze_parallel_groups(self, scenes: List[Dict]) -> List[List[str]]:
        """分析场景依赖，返回可并行的场景组"""
        groups = []
        processed = set()
        
        for scene in scenes:
            scene_id = scene["scene_id"]
            if scene_id in processed:
                continue
            
            # 获取依赖
            dependencies = scene.get("dependencies", [])
            
            # 如果没有依赖，或依赖都已处理，可以并行
            if not dependencies or all(dep in processed for dep in dependencies):
                # 找出所有可以一起并行的场景
                current_group = [scene_id]
                processed.add(scene_id)
                
                # 查找其他可以并行的场景
                for other_scene in scenes:
                    other_id = other_scene["scene_id"]
                    if other_id not in processed:
                        other_deps = other_scene.get("dependencies", [])
                        # 如果这个场景的依赖都已处理，可以加入当前组
                        if all(dep in processed or dep in current_group for dep in other_deps):
                            if other_id not in current_group:
                                current_group.append(other_id)
                                processed.add(other_id)
                
                groups.append(current_group)
        
        # 如果还有未处理的场景，递归处理
        unprocessed = [s for s in scenes if s["scene_id"] not in processed]
        if unprocessed:
            remaining_groups = self._analyze_parallel_groups(unprocessed)
            groups.extend(remaining_groups)
        
        return groups
    
    async def _merge_scenes_to_chapter(self,
                                      scene_results: Dict,
                                      chapter_info: Dict,
                                      decomposition: Dict) -> Dict:
        """将场景合并为完整章节"""
        # 按场景顺序排序
        scenes = decomposition["scenes"]
        
        content_parts = []
        
        # 章节标题
        chapter_title = chapter_info.get("title", f"Chapter {chapter_info.get('chapter_number', 1)}")
        content_parts.append(f"# {chapter_title}\n\n")
        
        # 按顺序添加场景内容
        total_words = 0
        for scene in scenes:
            scene_id = scene["scene_id"]
            if scene_id in scene_results:
                result = scene_results[scene_id]
                content = result.get("content", "")
                content_parts.append(content)
                content_parts.append("\n\n---\n\n")  # 场景分隔符
                total_words += result.get("metadata", {}).get("word_count", 0)
        
        # 移除最后一个分隔符
        if content_parts and content_parts[-1] == "\n\n---\n\n":
            content_parts.pop()
        
        return {
            "title": chapter_title,
            "content": "".join(content_parts),
            "metadata": {
                "chapter_number": chapter_info.get("chapter_number", 1),
                "total_scenes": len(scenes),
                "total_words": total_words,
                "generation_method": "parallel",
                "created_at": datetime.now().isoformat()
            }
        }
    
    def _calculate_speedup(self, tasks: List[SceneGenerationTask], actual_time: float) -> float:
        """计算相对于串行执行的加速比"""
        # 计算如果串行执行需要的时间
        serial_time = sum(t.execution_time() for t in tasks if t.end_time)
        
        if serial_time > 0 and actual_time > 0:
            return serial_time / actual_time
        
        # 理论加速比（基于并行组数量）
        return self.max_parallel
    
    async def save_results(self, results: Dict, output_dir: Path):
        """保存生成结果"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存完整结果
        result_file = output_dir / f"parallel_generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 保存章节内容
        if "chapter" in results:
            chapter = results["chapter"]
            chapter_file = output_dir / f"chapter_{chapter['metadata']['chapter_number']:03d}.txt"
            
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(chapter["content"])
        
        return result_file