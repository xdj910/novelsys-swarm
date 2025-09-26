"""
Bible创建Agent
负责创建和管理小说Bible
"""

import json
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.agent_base import BaseAgent, AgentContext, AgentResult


class BibleCreatorAgent(BaseAgent):
    """Bible创建专门Agent"""
    
    def __init__(self):
        super().__init__("BibleCreator", "bible_creation")
        self.bible_template = self.get_bible_template()
    
    def get_bible_template(self) -> Dict[str, Any]:
        """获取Bible模板"""
        return {
            "metadata": {
                "series_name": "",
                "book_number": 1,
                "genre": "",
                "target_audience": "",
                "created_at": "",
                "last_updated": "",
                "version": "1.0.0"
            },
            "world_building": {
                "setting": {
                    "time_period": "",
                    "locations": [],
                    "atmosphere": "",
                    "cultural_context": ""
                },
                "rules": {
                    "physical_laws": [],
                    "social_structures": [],
                    "economic_system": "",
                    "political_system": ""
                }
            },
            "characters": {
                "protagonists": [],
                "antagonists": [],
                "supporting": [],
                "character_relationships": []
            },
            "plot": {
                "central_conflict": "",
                "themes": [],
                "plot_structure": {
                    "exposition": "",
                    "rising_action": [],
                    "climax": "",
                    "falling_action": [],
                    "resolution": ""
                },
                "subplots": []
            },
            "style_guide": {
                "narrative_voice": "",
                "tone": "",
                "pacing": "",
                "language_style": "",
                "recurring_motifs": []
            }
        }
    
    async def perform_task(self, task: Dict[str, Any]) -> Any:
        """执行Bible创建任务"""
        task_type = task.get("type")
        
        if task_type == "create_new":
            return await self.create_new_bible(task)
        elif task_type == "evolve_sequel":
            return await self.evolve_bible_for_sequel(task)
        elif task_type == "update_bible":
            return await self.update_existing_bible(task)
        else:
            raise ValueError(f"Unknown bible task type: {task_type}")
    
    async def create_new_bible(self, task: Dict[str, Any]) -> Dict:
        """创建全新的Bible"""
        series_info = task.get("series_info", {})
        
        bible = self.bible_template.copy()
        
        # 填充基础信息
        bible["metadata"]["series_name"] = series_info.get("name", "Untitled")
        bible["metadata"]["genre"] = series_info.get("genre", "fiction")
        bible["metadata"]["target_audience"] = series_info.get("audience", "general")
        bible["metadata"]["created_at"] = datetime.now().isoformat()
        bible["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # 根据思考模式深度创建内容
        if self.thinking_mode in ["ultrathink", "think-harder"]:
            bible = await self.deep_world_building(bible, series_info)
            bible = await self.detailed_character_development(bible, series_info)
            bible = await self.complex_plot_design(bible, series_info)
        else:
            bible = await self.basic_world_building(bible, series_info)
            bible = await self.basic_character_setup(bible, series_info)
            bible = await self.basic_plot_outline(bible, series_info)
        
        # 保存Bible
        await self.save_bible(bible)
        
        return bible
    
    async def deep_world_building(self, bible: Dict, series_info: Dict) -> Dict:
        """深度世界观构建"""
        bible["world_building"]["setting"]["time_period"] = series_info.get("time_period", "contemporary")
        bible["world_building"]["setting"]["locations"] = [
            {
                "name": "主要城市",
                "description": "故事主要发生地",
                "significance": "核心剧情场景",
                "atmosphere": "现代都市氛围"
            }
        ]
        bible["world_building"]["setting"]["atmosphere"] = "悬疑紧张"
        bible["world_building"]["rules"]["physical_laws"] = ["符合现实物理规律"]
        bible["world_building"]["rules"]["social_structures"] = ["现代社会体系"]
        
        return bible
    
    async def basic_world_building(self, bible: Dict, series_info: Dict) -> Dict:
        """基础世界观设置"""
        bible["world_building"]["setting"]["time_period"] = "contemporary"
        bible["world_building"]["setting"]["locations"] = ["城市"]
        return bible
    
    async def detailed_character_development(self, bible: Dict, series_info: Dict) -> Dict:
        """详细角色开发"""
        bible["characters"]["protagonists"] = [
            {
                "name": "主角",
                "age": 30,
                "occupation": "侦探",
                "personality": {
                    "traits": ["聪明", "固执", "正义"],
                    "flaws": ["过度自信", "不善社交"],
                    "growth_arc": "从独狼到团队合作"
                },
                "backstory": "曾经的警察，因为某个案件离职成为私家侦探",
                "motivation": "追求真相和正义",
                "relationships": []
            }
        ]
        
        bible["characters"]["antagonists"] = [
            {
                "name": "反派",
                "role": "主要对手",
                "motivation": "复仇",
                "methods": "精心策划的犯罪"
            }
        ]
        
        return bible
    
    async def basic_character_setup(self, bible: Dict, series_info: Dict) -> Dict:
        """基础角色设置"""
        bible["characters"]["protagonists"] = [{"name": "主角", "role": "hero"}]
        bible["characters"]["antagonists"] = [{"name": "反派", "role": "villain"}]
        return bible
    
    async def complex_plot_design(self, bible: Dict, series_info: Dict) -> Dict:
        """复杂剧情设计"""
        bible["plot"]["central_conflict"] = "正义与邪恶的对抗"
        bible["plot"]["themes"] = ["真相", "正义", "牺牲", "成长"]
        bible["plot"]["plot_structure"]["exposition"] = "案件发生，主角介入"
        bible["plot"]["plot_structure"]["rising_action"] = [
            "线索收集",
            "第一次对抗",
            "深入调查",
            "意外发现"
        ]
        bible["plot"]["plot_structure"]["climax"] = "最终对决"
        bible["plot"]["plot_structure"]["resolution"] = "真相大白，正义得伸"
        
        return bible
    
    async def basic_plot_outline(self, bible: Dict, series_info: Dict) -> Dict:
        """基础剧情大纲"""
        bible["plot"]["central_conflict"] = "主要冲突"
        bible["plot"]["themes"] = ["主题"]
        return bible
    
    async def evolve_bible_for_sequel(self, task: Dict[str, Any]) -> Dict:
        """为续集进化Bible"""
        original_bible = task.get("original_bible", {})
        sequel_info = task.get("sequel_info", {})
        
        # 复制原Bible
        evolved_bible = original_bible.copy()
        
        # 更新元数据
        evolved_bible["metadata"]["book_number"] = sequel_info.get("book_number", 2)
        evolved_bible["metadata"]["last_updated"] = datetime.now().isoformat()
        evolved_bible["metadata"]["version"] = self.increment_version(
            evolved_bible["metadata"].get("version", "1.0.0")
        )
        
        # 进化角色（成长、新角色等）
        evolved_bible = await self.evolve_characters(evolved_bible, sequel_info)
        
        # 进化剧情
        evolved_bible = await self.evolve_plot(evolved_bible, sequel_info)
        
        # 保存进化后的Bible
        await self.save_bible(evolved_bible)
        
        return evolved_bible
    
    async def evolve_characters(self, bible: Dict, sequel_info: Dict) -> Dict:
        """进化角色设定"""
        # 角色成长
        for protagonist in bible["characters"]["protagonists"]:
            if "growth_arc" in protagonist.get("personality", {}):
                protagonist["personality"]["growth_stage"] = "advanced"
        
        # 添加新角色
        new_characters = sequel_info.get("new_characters", [])
        if new_characters:
            bible["characters"]["supporting"].extend(new_characters)
        
        return bible
    
    async def evolve_plot(self, bible: Dict, sequel_info: Dict) -> Dict:
        """进化剧情设定"""
        # 基于前作的新冲突
        bible["plot"]["central_conflict"] = sequel_info.get(
            "new_conflict", 
            "Evolution of previous conflict"
        )
        
        # 添加新主题
        new_themes = sequel_info.get("new_themes", [])
        if new_themes:
            bible["plot"]["themes"].extend(new_themes)
        
        return bible
    
    async def update_existing_bible(self, task: Dict[str, Any]) -> Dict:
        """更新现有Bible"""
        bible = task.get("bible", {})
        updates = task.get("updates", {})
        
        # 递归更新字典
        def update_nested_dict(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = update_nested_dict(d.get(k, {}), v)
                else:
                    d[k] = v
            return d
        
        updated_bible = update_nested_dict(bible, updates)
        updated_bible["metadata"]["last_updated"] = datetime.now().isoformat()
        
        await self.save_bible(updated_bible)
        
        return updated_bible
    
    async def save_bible(self, bible: Dict):
        """保存Bible到文件"""
        # 确定保存路径
        series_name = bible["metadata"]["series_name"]
        book_number = bible["metadata"]["book_number"]
        
        bible_dir = Path("D:/NOVELSYS-SWARM/bibles")
        bible_dir.mkdir(parents=True, exist_ok=True)
        
        bible_path = bible_dir / f"{series_name}_book{book_number}_bible.json"
        
        with open(bible_path, 'w', encoding='utf-8') as f:
            json.dump(bible, f, ensure_ascii=False, indent=2)
        
        # 更新上下文
        if self.context:
            self.context.bible_path = bible_path
    
    def increment_version(self, version: str) -> str:
        """增加版本号"""
        parts = version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)
    
    async def check_quality(self, result: Any) -> float:
        """检查Bible质量"""
        if not isinstance(result, dict):
            return 0.0
        
        score = 0.0
        max_score = 100.0
        
        # 检查必要字段完整性
        required_sections = ["metadata", "world_building", "characters", "plot", "style_guide"]
        for section in required_sections:
            if section in result and result[section]:
                score += 10
        
        # 检查角色深度
        if "characters" in result:
            protagonists = result["characters"].get("protagonists", [])
            if protagonists:
                for p in protagonists:
                    if "personality" in p and "backstory" in p:
                        score += 10
                        break
        
        # 检查剧情完整性
        if "plot" in result:
            plot = result["plot"]
            if plot.get("central_conflict") and plot.get("themes"):
                score += 15
            if "plot_structure" in plot:
                structure = plot["plot_structure"]
                if all(k in structure for k in ["exposition", "climax", "resolution"]):
                    score += 15
        
        # 检查世界观设定
        if "world_building" in result:
            wb = result["world_building"]
            if "setting" in wb and wb["setting"].get("time_period"):
                score += 10
            if "rules" in wb and wb["rules"]:
                score += 10
        
        return min(score, max_score)