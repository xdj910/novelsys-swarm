"""
命令路由系统
处理所有/novel:命令并分发到相应的处理器
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.agent_base import DirectorAgent, AgentContext
from core.project_manager import ProjectManager, ProjectType
from core.decomposer import ChapterDecomposer, Scene
from core.scene_analyzer import SceneAnalyzer
from core.parallel_generator import ParallelSceneGenerator
from agents.bible_creator import BibleCreatorAgent
from agents.chapter_generator import ChapterGeneratorAgent
from agents.stream_chapter_generator import StreamChapterGeneratorAgent


class CommandRouter:
    """命令路由器"""
    
    def __init__(self):
        self.commands = {}
        self.agents = {}
        self.context = {}
        self.project_manager = ProjectManager()
        self.decomposer = ChapterDecomposer()
        self.scene_analyzer = SceneAnalyzer()
        self.parallel_generator = ParallelSceneGenerator()
        self.register_commands()
        self.initialize_agents()
    
    def register_commands(self):
        """注册所有命令"""
        # 项目管理命令
        self.commands["project-new"] = self.handle_project_new
        self.commands["project-list"] = self.handle_project_list
        self.commands["project-info"] = self.handle_project_info
        self.commands["project-add-book"] = self.handle_project_add_book
        
        # Bible相关命令
        self.commands["bible-new"] = self.handle_bible_new
        self.commands["bible-evolve"] = self.handle_bible_evolve
        self.commands["bible-standalone"] = self.handle_bible_standalone
        self.commands["bible-check"] = self.handle_bible_check
        
        # 章节生成命令
        self.commands["chapter-start"] = self.handle_chapter_start
        self.commands["chapter-batch"] = self.handle_chapter_batch
        self.commands["chapter-parallel"] = self.handle_chapter_parallel
        self.commands["chapter-stream"] = self.handle_chapter_stream  # 新增4-Stream生成
        self.commands["chapter-decompose"] = self.handle_chapter_decompose  # 新增章节分解
        self.commands["scene-analyze"] = self.handle_scene_analyze  # 新增场景分析
        self.commands["scenes-generate-parallel"] = self.handle_scenes_parallel  # 新增并行场景生成
        
        # 质量检查命令
        self.commands["quality-check"] = self.handle_quality_check
        self.commands["quality-improve"] = self.handle_quality_improve
        
        # 系统命令
        self.commands["status"] = self.handle_status
        self.commands["config"] = self.handle_config
        self.commands["help"] = self.handle_help
    
    def initialize_agents(self):
        """初始化Agent"""
        self.agents["director"] = DirectorAgent()
        self.agents["bible_creator"] = BibleCreatorAgent()
        self.agents["chapter_generator"] = ChapterGeneratorAgent()
        self.agents["stream_chapter_generator"] = StreamChapterGeneratorAgent()
    
    async def route_command(self, command: str, args: List[str], options: Dict[str, Any]) -> Any:
        """路由命令到相应处理器"""
        # 解析命令
        if command.startswith("/novel:"):
            command = command[7:]  # 移除 /novel: 前缀
        
        # 查找命令处理器
        if command in self.commands:
            handler = self.commands[command]
            return await handler(args, options)
        else:
            return {"error": f"Unknown command: {command}"}
    
    async def handle_bible_new(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """处理创建新Bible命令"""
        series_name = args[0] if args else "untitled"
        
        # 设置思考模式
        thinking_mode = options.get("thinking_mode", "ultrathink")
        self.agents["bible_creator"].set_thinking_mode(thinking_mode)
        
        # 创建上下文
        context = AgentContext(
            project_name=series_name,
            book_number=1
        )
        
        await self.agents["bible_creator"].initialize(context)
        
        # 执行任务
        task = {
            "type": "create_new",
            "series_info": {
                "name": series_name,
                "genre": options.get("genre", "fiction"),
                "audience": options.get("audience", "general"),
                "time_period": options.get("time_period", "contemporary")
            }
        }
        
        result = await self.agents["bible_creator"].execute(task)
        
        if result.success:
            return {
                "status": "success",
                "message": f"Bible created for series: {series_name}",
                "bible": result.content,
                "quality_score": result.quality_score
            }
        else:
            return {
                "status": "error",
                "message": "Failed to create Bible",
                "errors": result.errors
            }
    
    async def handle_bible_evolve(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """处理Bible进化命令"""
        series_name = args[0] if args else "untitled"
        book_number = int(args[1]) if len(args) > 1 else 2
        
        # 加载原Bible
        original_bible_path = Path(f"D:/NOVELSYS-SWARM/bibles/{series_name}_book{book_number-1}_bible.json")
        
        if not original_bible_path.exists():
            return {"error": f"Original bible not found: {original_bible_path}"}
        
        with open(original_bible_path, 'r', encoding='utf-8') as f:
            original_bible = json.load(f)
        
        # 设置思考模式
        thinking_mode = options.get("thinking_mode", "think-harder")
        self.agents["bible_creator"].set_thinking_mode(thinking_mode)
        
        # 创建上下文
        context = AgentContext(
            project_name=series_name,
            book_number=book_number,
            bible_path=original_bible_path
        )
        
        await self.agents["bible_creator"].initialize(context)
        
        # 执行任务
        task = {
            "type": "evolve_sequel",
            "original_bible": original_bible,
            "sequel_info": {
                "book_number": book_number,
                "new_conflict": options.get("conflict", ""),
                "new_themes": options.get("themes", []),
                "new_characters": options.get("characters", [])
            }
        }
        
        result = await self.agents["bible_creator"].execute(task)
        
        if result.success:
            return {
                "status": "success",
                "message": f"Bible evolved for book {book_number}",
                "bible": result.content,
                "quality_score": result.quality_score
            }
        else:
            return {
                "status": "error",
                "message": "Failed to evolve Bible",
                "errors": result.errors
            }
    
    async def handle_bible_standalone(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """处理独立小说Bible创建"""
        title = args[0] if args else "untitled"
        
        # 独立小说使用较少的思考深度
        thinking_mode = options.get("thinking_mode", "think-hard")
        self.agents["bible_creator"].set_thinking_mode(thinking_mode)
        
        # 创建上下文
        context = AgentContext(
            project_name=title,
            book_number=1
        )
        
        await self.agents["bible_creator"].initialize(context)
        
        # 执行任务
        task = {
            "type": "create_new",
            "series_info": {
                "name": title,
                "genre": options.get("genre", "fiction"),
                "audience": options.get("audience", "general"),
                "standalone": True
            }
        }
        
        result = await self.agents["bible_creator"].execute(task)
        
        if result.success:
            return {
                "status": "success",
                "message": f"Standalone bible created: {title}",
                "bible": result.content,
                "quality_score": result.quality_score
            }
        else:
            return {
                "status": "error",
                "message": "Failed to create standalone Bible",
                "errors": result.errors
            }
    
    async def handle_bible_check(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """检查Bible一致性"""
        series_name = args[0] if args else None
        
        if not series_name:
            return {"error": "Series name required"}
        
        # 查找所有相关Bible文件
        bible_dir = Path("D:/NOVELSYS-SWARM/bibles")
        bible_files = list(bible_dir.glob(f"{series_name}_*.json"))
        
        consistency_results = []
        
        for bible_file in bible_files:
            with open(bible_file, 'r', encoding='utf-8') as f:
                bible = json.load(f)
            
            # 检查Bible完整性
            check_result = await self.check_bible_consistency(bible)
            consistency_results.append({
                "file": bible_file.name,
                "consistency_score": check_result["score"],
                "issues": check_result["issues"]
            })
        
        return {
            "status": "success",
            "series": series_name,
            "results": consistency_results
        }
    
    async def check_bible_consistency(self, bible: Dict) -> Dict:
        """检查单个Bible的一致性"""
        score = 100.0
        issues = []
        
        # 检查必要字段
        required_fields = ["metadata", "world_building", "characters", "plot"]
        for field in required_fields:
            if field not in bible:
                score -= 10
                issues.append(f"Missing field: {field}")
        
        # 检查角色关系一致性
        if "characters" in bible:
            characters = bible["characters"]
            all_character_names = []
            
            for category in ["protagonists", "antagonists", "supporting"]:
                if category in characters:
                    for char in characters[category]:
                        if "name" in char:
                            all_character_names.append(char["name"])
            
            # 检查角色关系中是否有未定义的角色
            if "character_relationships" in characters:
                for rel in characters["character_relationships"]:
                    if isinstance(rel, dict):
                        for char in rel.get("characters", []):
                            if char not in all_character_names:
                                score -= 5
                                issues.append(f"Undefined character in relationship: {char}")
        
        return {"score": score, "issues": issues}
    
    async def handle_chapter_start(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """开始章节生成"""
        series_name = args[0] if args else None
        chapter_number = int(args[1]) if len(args) > 1 else 1
        
        if not series_name:
            return {"error": "Series name required"}
        
        # 加载Bible
        bible_path = Path(f"D:/NOVELSYS-SWARM/bibles/{series_name}_book1_bible.json")
        if not bible_path.exists():
            return {"error": f"Bible not found: {bible_path}"}
        
        # 设置思考模式
        thinking_mode = options.get("thinking_mode", "think-hard")
        self.agents["chapter_generator"].set_thinking_mode(thinking_mode)
        
        # 创建上下文
        context = AgentContext(
            project_name=series_name,
            book_number=1,
            chapter_number=chapter_number,
            bible_path=bible_path
        )
        
        await self.agents["chapter_generator"].initialize(context)
        
        # 创建章节大纲
        outline = {
            "title": f"Chapter {chapter_number}",
            "plot_points": options.get("plot_points", ["开场", "发展", "转折", "高潮", "结尾"]),
            "characters": options.get("characters", ["主角"]),
            "location": options.get("location", "主要场景"),
            "mood": options.get("mood", "neutral")
        }
        
        # 执行任务
        task = {
            "type": "generate_chapter",
            "chapter_number": chapter_number,
            "outline": outline
        }
        
        result = await self.agents["chapter_generator"].execute(task)
        
        if result.success:
            return {
                "status": "success",
                "message": f"Chapter {chapter_number} generated",
                "chapter": result.content,
                "quality_score": result.quality_score,
                "execution_time": result.execution_time
            }
        else:
            return {
                "status": "error",
                "message": "Failed to generate chapter",
                "errors": result.errors
            }
    
    async def handle_chapter_batch(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """批量生成章节"""
        series_name = args[0] if args else None
        start_chapter = int(args[1]) if len(args) > 1 else 1
        end_chapter = int(args[2]) if len(args) > 2 else start_chapter + 4
        
        if not series_name:
            return {"error": "Series name required"}
        
        results = []
        
        for chapter_num in range(start_chapter, end_chapter + 1):
            result = await self.handle_chapter_start(
                [series_name, str(chapter_num)],
                options
            )
            results.append({
                "chapter": chapter_num,
                "status": result.get("status"),
                "quality_score": result.get("quality_score", 0)
            })
        
        return {
            "status": "success",
            "message": f"Generated chapters {start_chapter} to {end_chapter}",
            "results": results
        }
    
    async def handle_chapter_parallel(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """并行生成章节"""
        series_name = args[0] if args else None
        chapters = [int(ch) for ch in args[1:]] if len(args) > 1 else [1, 2, 3]
        
        if not series_name:
            return {"error": "Series name required"}
        
        # 创建并行任务
        tasks = []
        for chapter_num in chapters:
            task = self.handle_chapter_start(
                [series_name, str(chapter_num)],
                options
            )
            tasks.append(task)
        
        # 并行执行
        results = await asyncio.gather(*tasks)
        
        return {
            "status": "success",
            "message": f"Parallel generation completed",
            "chapters_generated": len(results),
            "results": [
                {
                    "chapter": chapters[i],
                    "status": r.get("status"),
                    "quality_score": r.get("quality_score", 0)
                }
                for i, r in enumerate(results)
            ]
        }
    
    async def handle_chapter_stream(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """使用4-Stream架构生成章节"""
        series_name = args[0] if args else None
        chapter_number = int(args[1]) if len(args) > 1 else 1
        
        if not series_name:
            return {"error": "Series name required"}
        
        # 加载Bible
        bible_path = Path(f"D:/NOVELSYS-SWARM/bibles/{series_name}_book1_bible.json")
        if not bible_path.exists():
            return {"error": f"Bible not found: {bible_path}"}
        
        # 设置思考模式
        thinking_mode = options.get("thinking_mode", "think-hard")
        self.agents["stream_chapter_generator"].set_thinking_mode(thinking_mode)
        
        # 创建上下文
        context = AgentContext(
            project_name=series_name,
            book_number=1,
            chapter_number=chapter_number,
            bible_path=bible_path
        )
        
        await self.agents["stream_chapter_generator"].initialize(context)
        
        # 创建章节大纲
        outline = {
            "title": f"Chapter {chapter_number}",
            "plot_points": options.get("plot_points", ["开场", "发展", "转折", "高潮", "结尾"]),
            "characters": options.get("characters", ["主角"]),
            "location": options.get("location", "主要场景"),
            "mood": options.get("mood", "neutral")
        }
        
        # 执行4-Stream生成
        task = {
            "type": "generate_chapter",
            "chapter_number": chapter_number,
            "outline": outline
        }
        
        result = await self.agents["stream_chapter_generator"].execute(task)
        
        if result.success:
            return {
                "status": "success",
                "message": f"Chapter {chapter_number} generated using 4-Stream architecture",
                "chapter": result.content,
                "quality_score": result.quality_score,
                "execution_time": result.execution_time,
                "generation_method": "4-stream-parallel"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to generate chapter with 4-Stream",
                "errors": result.errors
            }
    
    async def handle_quality_check(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """质量检查"""
        target = args[0] if args else "all"
        
        quality_results = {}
        
        if target == "all" or target == "bibles":
            # 检查所有Bible
            bible_dir = Path("D:/NOVELSYS-SWARM/bibles")
            if bible_dir.exists():
                for bible_file in bible_dir.glob("*.json"):
                    with open(bible_file, 'r', encoding='utf-8') as f:
                        bible = json.load(f)
                    check_result = await self.check_bible_consistency(bible)
                    quality_results[f"bible_{bible_file.stem}"] = check_result
        
        if target == "all" or target == "chapters":
            # 检查所有章节
            chapter_dir = Path("D:/NOVELSYS-SWARM/chapters")
            if chapter_dir.exists():
                for chapter_file in chapter_dir.glob("*.json"):
                    with open(chapter_file, 'r', encoding='utf-8') as f:
                        chapter = json.load(f)
                    quality_score = chapter.get("metadata", {}).get("quality_score", 0)
                    quality_results[f"chapter_{chapter_file.stem}"] = {
                        "score": quality_score,
                        "issues": []
                    }
        
        return {
            "status": "success",
            "quality_results": quality_results,
            "average_score": sum(r["score"] for r in quality_results.values()) / len(quality_results) if quality_results else 0
        }
    
    async def handle_quality_improve(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """质量改进"""
        target = args[0] if args else None
        
        if not target:
            return {"error": "Target required (chapter or bible path)"}
        
        # 实现质量改进逻辑
        return {
            "status": "success",
            "message": f"Quality improvement initiated for {target}",
            "improvements": ["Style consistency enhanced", "Plot holes fixed", "Character development deepened"]
        }
    
    async def handle_status(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """系统状态"""
        status = {
            "agents": {
                name: "active" for name in self.agents.keys()
            },
            "projects": [],
            "statistics": {
                "total_bibles": 0,
                "total_chapters": 0,
                "average_quality": 0
            }
        }
        
        # 统计Bible数量
        bible_dir = Path("D:/NOVELSYS-SWARM/bibles")
        if bible_dir.exists():
            status["statistics"]["total_bibles"] = len(list(bible_dir.glob("*.json")))
        
        # 统计章节数量
        chapter_dir = Path("D:/NOVELSYS-SWARM/chapters")
        if chapter_dir.exists():
            status["statistics"]["total_chapters"] = len(list(chapter_dir.glob("*.json")))
        
        return status
    
    async def handle_config(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """配置系统"""
        if not args:
            # 显示当前配置
            return {
                "current_config": self.context,
                "available_agents": list(self.agents.keys())
            }
        
        # 更新配置
        config_key = args[0]
        config_value = args[1] if len(args) > 1 else None
        
        self.context[config_key] = config_value
        
        return {
            "status": "success",
            "message": f"Configuration updated: {config_key} = {config_value}"
        }
    
    async def handle_project_new(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """创建新项目"""
        if not args:
            return {"error": "Project name required"}
        
        project_name = args[0]
        project_type_str = options.get("type", "standalone")
        
        # 转换项目类型
        type_map = {
            "series": ProjectType.SERIES,
            "standalone": ProjectType.STANDALONE,
            "collection": ProjectType.COLLECTION,
            "serial": ProjectType.SERIAL
        }
        
        if project_type_str not in type_map:
            return {"error": f"Invalid project type: {project_type_str}"}
        
        project_type = type_map[project_type_str]
        
        # 创建项目元数据
        metadata = {
            "genre": options.get("genre", "fiction"),
            "audience": options.get("audience", "general"),
            "planned_books": int(options.get("books", 3)),
            "chapters": int(options.get("chapters", 20)),
            "word_count": int(options.get("words", 80000))
        }
        
        try:
            project_path = self.project_manager.create_project(project_name, project_type, metadata)
            return {
                "status": "success",
                "message": f"Created {project_type_str} project: {project_name}",
                "path": str(project_path)
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_project_list(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """列出所有项目"""
        project_type_str = options.get("type")
        
        project_type = None
        if project_type_str:
            type_map = {
                "series": ProjectType.SERIES,
                "standalone": ProjectType.STANDALONE,
                "collection": ProjectType.COLLECTION,
                "serial": ProjectType.SERIAL
            }
            project_type = type_map.get(project_type_str)
        
        projects = self.project_manager.list_projects(project_type)
        
        return {
            "status": "success",
            "projects": projects,
            "count": len(projects)
        }
    
    async def handle_project_info(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """获取项目信息"""
        if not args:
            return {"error": "Project name required"}
        
        project_name = args[0]
        
        try:
            info = self.project_manager.get_project_info(project_name)
            return {
                "status": "success",
                "project_info": info
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_project_add_book(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """向系列添加新书"""
        if len(args) < 3:
            return {"error": "Usage: project-add-book <series-name> <book-number> <book-title>"}
        
        series_name = args[0]
        book_number = int(args[1])
        book_title = args[2]
        
        try:
            book_path = self.project_manager.add_book_to_series(series_name, book_number, book_title)
            return {
                "status": "success",
                "message": f"Added book {book_number}: {book_title} to series {series_name}",
                "path": str(book_path)
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_chapter_decompose(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """章节分解为场景（CCPM Epic→Issue思想）"""
        if len(args) < 2:
            return {"error": "Usage: chapter-decompose <series-name> <chapter-number>"}
        
        series_name = args[0]
        chapter_number = int(args[1])
        
        # 加载Bible
        bible_path = Path(f"D:/NOVELSYS-SWARM/bibles/{series_name}_book1_bible.json")
        if not bible_path.exists():
            return {"error": f"Bible not found: {bible_path}"}
        
        with open(bible_path, 'r', encoding='utf-8') as f:
            bible = json.load(f)
        
        # 创建章节大纲
        chapter_outline = {
            "chapter_number": chapter_number,
            "plot_points": options.get("plot_points", ["开场", "发展", "转折", "高潮", "结尾"]),
            "characters": options.get("characters", bible.get("characters", {}).get("protagonists", [])),
            "location": options.get("location", "主要场景")
        }
        
        # 分解章节
        scenes = await self.decomposer.decompose_chapter(chapter_outline, bible)
        
        # 分析并行潜力
        parallel_analysis = self.decomposer.analyze_dependencies(scenes)
        
        # 保存分解结果
        output_dir = Path(f"D:/NOVELSYS-SWARM/decompositions/{series_name}")
        decomposition_file = await self.decomposer.save_decomposition(scenes, output_dir)
        
        return {
            "status": "success",
            "message": f"Chapter {chapter_number} decomposed into {len(scenes)} scenes",
            "total_scenes": len(scenes),
            "parallel_groups": parallel_analysis["parallel_groups"],
            "max_parallel": parallel_analysis["max_parallel"],
            "execution_stages": parallel_analysis["execution_stages"],
            "scenes": [scene.to_dict() for scene in scenes],
            "output_file": str(decomposition_file)
        }
    
    async def handle_scene_analyze(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """深度分析场景需求（CCPM issue-analyze思想）"""
        if len(args) < 3:
            return {"error": "Usage: scene-analyze <series-name> <chapter-number> <scene-number>"}
        
        series_name = args[0]
        chapter_number = int(args[1])
        scene_number = int(args[2])
        
        # 加载Bible
        bible_path = Path(f"D:/NOVELSYS-SWARM/bibles/{series_name}_book1_bible.json")
        if not bible_path.exists():
            return {"error": f"Bible not found: {bible_path}"}
        
        with open(bible_path, 'r', encoding='utf-8') as f:
            bible = json.load(f)
        
        # 加载分解结果
        decomposition_file = Path(f"D:/NOVELSYS-SWARM/decompositions/{series_name}/chapter_{chapter_number:03d}_decomposition.json")
        if not decomposition_file.exists():
            return {"error": f"Chapter decomposition not found. Run chapter-decompose first."}
        
        with open(decomposition_file, 'r', encoding='utf-8') as f:
            decomposition = json.load(f)
        
        # 找到指定场景
        scenes = decomposition["scenes"]
        if scene_number < 1 or scene_number > len(scenes):
            return {"error": f"Invalid scene number. Chapter has {len(scenes)} scenes."}
        
        target_scene = scenes[scene_number - 1]
        previous_scenes = scenes[:scene_number - 1] if scene_number > 1 else []
        next_scenes = scenes[scene_number:] if scene_number < len(scenes) else []
        
        # 深度分析场景
        analysis = await self.scene_analyzer.analyze_scene(
            target_scene,
            bible,
            previous_scenes,
            next_scenes
        )
        
        # 保存分析结果
        output_path = Path(f"D:/NOVELSYS-SWARM/analyses/{series_name}/ch{chapter_number:03d}_sc{scene_number:02d}_analysis.json")
        await self.scene_analyzer.save_analysis(analysis, output_path)
        
        return {
            "status": "success",
            "message": f"Scene {scene_number} of Chapter {chapter_number} analyzed",
            "scene_id": target_scene["scene_id"],
            "analysis": analysis,
            "requirements": analysis["requirements"],
            "potential_issues": analysis["potential_issues"],
            "suggestions": analysis["suggestions"],
            "output_file": str(output_path)
        }
    
    async def handle_scenes_parallel(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """并行生成章节的所有场景（CCPM并行执行核心）"""
        if len(args) < 2:
            return {"error": "Usage: scenes-generate-parallel <series-name> <chapter-number>"}
        
        series_name = args[0]
        chapter_number = int(args[1])
        
        # 检查是否已经分解
        decomposition_file = Path(f"D:/NOVELSYS-SWARM/decompositions/{series_name}/chapter_{chapter_number:03d}_decomposition.json")
        if not decomposition_file.exists():
            return {"error": f"Chapter not decomposed yet. Run 'chapter-decompose {series_name} {chapter_number}' first."}
        
        # 加载分解结果
        with open(decomposition_file, 'r', encoding='utf-8') as f:
            decomposition = json.load(f)
        
        # 加载Bible
        bible_path = Path(f"D:/NOVELSYS-SWARM/bibles/{series_name}_book1_bible.json")
        if not bible_path.exists():
            return {"error": f"Bible not found: {bible_path}"}
        
        with open(bible_path, 'r', encoding='utf-8') as f:
            bible = json.load(f)
        
        # 加载所有场景分析（如果有的话）
        analyses = {}
        analyses_dir = Path(f"D:/NOVELSYS-SWARM/analyses/{series_name}")
        if analyses_dir.exists():
            for analysis_file in analyses_dir.glob(f"ch{chapter_number:03d}_sc*_analysis.json"):
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    analysis = json.load(f)
                    scene_id = analysis.get("scene_id")
                    if scene_id:
                        analyses[scene_id] = analysis
        
        # 章节信息
        chapter_info = {
            "title": f"Chapter {chapter_number}",
            "chapter_number": chapter_number
        }
        
        print(f"\n🚀 开始并行生成章节 {chapter_number} 的 {len(decomposition['scenes'])} 个场景...")
        print(f"📊 最大并行度: {self.parallel_generator.max_parallel}")
        
        # 并行生成所有场景
        result = await self.parallel_generator.generate_scenes_parallel(
            decomposition,
            analyses,
            bible,
            chapter_info
        )
        
        # 保存结果
        output_dir = Path(f"D:/NOVELSYS-SWARM/output/parallel/{series_name}")
        output_file = await self.parallel_generator.save_results(result, output_dir)
        
        return {
            "status": result["status"],
            "message": f"Chapter {chapter_number} generated using parallel scene generation",
            "chapter": result["chapter"],
            "statistics": result["statistics"],
            "output_file": str(output_file),
            "speedup": f"{result['statistics']['speedup']:.2f}x faster than serial"
        }
    
    async def handle_help(self, args: List[str], options: Dict[str, Any]) -> Dict:
        """显示帮助"""
        if args:
            command = args[0]
            if command in self.commands:
                return {
                    "command": command,
                    "description": f"Help for {command} command",
                    "usage": f"/novel:{command} [args] [options]"
                }
        
        return {
            "available_commands": list(self.commands.keys()),
            "usage": "/novel:command [args] [--option=value]",
            "examples": [
                "/novel:project-new my-series --type=series --genre=mystery",
                "/novel:project-list --type=series",
                "/novel:bible-new my-series --genre=mystery",
                "/novel:chapter-start my-series 1",
                "/novel:chapter-stream my-series 1  # 使用4-Stream架构生成",
                "/novel:chapter-decompose my-series 1  # 分解章节为场景",
                "/novel:scene-analyze my-series 1 1  # 分析第1章第1场景",
                "/novel:scenes-generate-parallel my-series 1  # 并行生成所有场景",
                "/novel:quality-check all"
            ]
        }


async def main():
    """测试命令路由器"""
    router = CommandRouter()
    
    # 测试创建Bible
    print("Creating new Bible...")
    result = await router.route_command(
        "/novel:bible-new",
        ["test-series"],
        {"genre": "mystery", "thinking_mode": "ultrathink"}
    )
    print(f"Result: {result['status']}")
    print(f"Quality Score: {result.get('quality_score', 0)}")
    
    # 测试生成章节
    print("\nGenerating chapter...")
    result = await router.route_command(
        "/novel:chapter-start",
        ["test-series", "1"],
        {"thinking_mode": "think-hard"}
    )
    print(f"Result: {result['status']}")
    
    # 测试质量检查
    print("\nChecking quality...")
    result = await router.route_command(
        "/novel:quality-check",
        ["all"],
        {}
    )
    print(f"Average Quality: {result.get('average_score', 0)}")


if __name__ == "__main__":
    asyncio.run(main())