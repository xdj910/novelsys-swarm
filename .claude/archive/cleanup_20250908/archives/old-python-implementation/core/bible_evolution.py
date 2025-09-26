"""
Bible演化系统
管理系列小说的Bible继承、演化和上下文传递
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class CharacterState:
    """角色状态"""
    name: str
    age: int
    status: str  # alive, dead, missing, transformed
    location: str
    relationships: Dict[str, str] = field(default_factory=dict)
    skills: List[str] = field(default_factory=list)
    personality_traits: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    growth_stage: str = "initial"  # initial, developing, mature, transformed


@dataclass
class PlotThread:
    """情节线"""
    id: str
    description: str
    thread_type: str  # main, subplot, mystery, romance, conflict
    status: str  # active, resolved, dormant, abandoned
    books_span: List[int] = field(default_factory=list)
    developments: List[Dict] = field(default_factory=list)
    resolution_book: Optional[int] = None


class BookCompletionSummary:
    """书籍完成总结生成器"""
    
    def __init__(self, series_name: str, book_number: int):
        self.series_name = series_name
        self.book_number = book_number
        self.summary = {
            "book_number": book_number,
            "completion_date": datetime.now().isoformat(),
            "character_evolution": {},
            "plot_impacts": {},
            "worldbuilding_expansion": {},
            "unfinished_business": {},
            "reader_knowledge": {}
        }
    
    def analyze_character_changes(self, book_content: Dict) -> Dict:
        """分析角色变化"""
        character_evolution = {
            "protagonist_changes": [],
            "relationship_shifts": [],
            "new_alliances": [],
            "character_deaths": [],
            "character_transformations": []
        }
        
        # 分析主角变化
        if "protagonist" in book_content:
            protagonist = book_content["protagonist"]
            changes = {
                "name": protagonist.get("name"),
                "growth": protagonist.get("character_arc", ""),
                "new_skills": protagonist.get("acquired_skills", []),
                "trauma": protagonist.get("new_trauma", []),
                "healing": protagonist.get("healing_moments", [])
            }
            character_evolution["protagonist_changes"].append(changes)
        
        # 分析关系变化
        if "relationships" in book_content:
            for rel in book_content["relationships"]:
                if rel.get("changed", False):
                    character_evolution["relationship_shifts"].append({
                        "characters": rel["characters"],
                        "from": rel.get("previous_state"),
                        "to": rel.get("new_state"),
                        "reason": rel.get("change_reason")
                    })
        
        return character_evolution
    
    def analyze_plot_impacts(self, book_content: Dict) -> Dict:
        """分析情节影响"""
        plot_impacts = {
            "resolved_conflicts": [],
            "new_conflicts_introduced": [],
            "world_state_changes": [],
            "power_balance_shifts": [],
            "revealed_secrets": []
        }
        
        # 提取已解决的冲突
        if "conflicts" in book_content:
            for conflict in book_content["conflicts"]:
                if conflict.get("resolved", False):
                    plot_impacts["resolved_conflicts"].append({
                        "conflict": conflict["description"],
                        "resolution": conflict.get("resolution_method"),
                        "consequences": conflict.get("consequences", [])
                    })
                elif conflict.get("introduced", False):
                    plot_impacts["new_conflicts_introduced"].append({
                        "conflict": conflict["description"],
                        "parties": conflict.get("parties", []),
                        "stakes": conflict.get("stakes")
                    })
        
        # 记录揭示的秘密
        if "reveals" in book_content:
            plot_impacts["revealed_secrets"] = book_content["reveals"]
        
        return plot_impacts
    
    def identify_unfinished_business(self, book_content: Dict) -> Dict:
        """识别未完成事项"""
        unfinished = {
            "cliffhangers": book_content.get("cliffhangers", []),
            "foreshadowing": book_content.get("foreshadowing", []),
            "open_questions": book_content.get("open_questions", []),
            "promised_events": book_content.get("promised_events", []),
            "character_goals": []
        }
        
        # 提取未完成的角色目标
        if "characters" in book_content:
            for character in book_content["characters"]:
                unresolved_goals = [
                    goal for goal in character.get("goals", [])
                    if not goal.get("achieved", False)
                ]
                if unresolved_goals:
                    unfinished["character_goals"].append({
                        "character": character["name"],
                        "goals": unresolved_goals
                    })
        
        return unfinished
    
    def generate_summary(self, book_content: Dict) -> Dict:
        """生成完整总结"""
        self.summary["character_evolution"] = self.analyze_character_changes(book_content)
        self.summary["plot_impacts"] = self.analyze_plot_impacts(book_content)
        self.summary["unfinished_business"] = self.identify_unfinished_business(book_content)
        
        # 更新读者知识库
        self.summary["reader_knowledge"] = {
            "known_facts": book_content.get("established_facts", []),
            "revealed_mysteries": book_content.get("solved_mysteries", []),
            "character_backstories": book_content.get("revealed_backstories", []),
            "world_mechanics": book_content.get("explained_mechanics", [])
        }
        
        return self.summary
    
    def save_summary(self, project_path: Path):
        """保存总结到文件"""
        book_dir = project_path / f"book-{self.book_number:02d}"
        summary_path = book_dir / "completion-summary.json"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(self.summary, f, ensure_ascii=False, indent=2)
        
        # 同时导出给下一本书
        export_path = book_dir / "export-to-next.json"
        export_data = {
            "from_book": self.book_number,
            "key_points": self.extract_key_points(),
            "mandatory_continuations": self.identify_mandatory_continuations()
        }
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    def extract_key_points(self) -> List[str]:
        """提取关键要点"""
        key_points = []
        
        # 从各个部分提取关键信息
        if self.summary["character_evolution"]["character_deaths"]:
            for death in self.summary["character_evolution"]["character_deaths"]:
                key_points.append(f"Character death: {death}")
        
        if self.summary["plot_impacts"]["resolved_conflicts"]:
            for conflict in self.summary["plot_impacts"]["resolved_conflicts"]:
                key_points.append(f"Resolved: {conflict['conflict']}")
        
        if self.summary["unfinished_business"]["cliffhangers"]:
            for cliff in self.summary["unfinished_business"]["cliffhangers"]:
                key_points.append(f"Cliffhanger: {cliff}")
        
        return key_points
    
    def identify_mandatory_continuations(self) -> Dict:
        """识别必须延续的元素"""
        return {
            "unresolved_conflicts": [
                c for c in self.summary["plot_impacts"].get("new_conflicts_introduced", [])
                if c.get("stakes") == "high"
            ],
            "promised_events": self.summary["unfinished_business"]["promised_events"],
            "character_arcs": [
                goal for goal in self.summary["unfinished_business"]["character_goals"]
                if goal.get("critical", False)
            ]
        }


class CharacterGrowthTracker:
    """角色成长追踪器"""
    
    def __init__(self, character_name: str):
        self.character_name = character_name
        self.growth_timeline = []
        self.current_state = CharacterState(name=character_name, age=0, status="alive", location="")
    
    def record_book_development(self, book_number: int, developments: Dict):
        """记录在特定书中的发展"""
        book_record = {
            "book": book_number,
            "age": self.current_state.age,
            "physical_changes": developments.get("physical", []),
            "personality_evolution": developments.get("personality", []),
            "skill_development": developments.get("skills", []),
            "relationship_changes": developments.get("relationships", []),
            "trauma_and_healing": developments.get("trauma_healing", []),
            "beliefs_and_values": developments.get("beliefs", []),
            "power_level": developments.get("power", 0),
            "social_position": developments.get("position", ""),
            "goals_and_motivations": developments.get("goals", [])
        }
        
        self.growth_timeline.append(book_record)
        self.update_current_state(developments)
    
    def update_current_state(self, developments: Dict):
        """更新当前状态"""
        if "age_change" in developments:
            self.current_state.age += developments["age_change"]
        
        if "new_skills" in developments:
            self.current_state.skills.extend(developments["new_skills"])
        
        if "personality_traits" in developments:
            self.current_state.personality_traits = developments["personality_traits"]
        
        if "location" in developments:
            self.current_state.location = developments["location"]
        
        if "status" in developments:
            self.current_state.status = developments["status"]
        
        if "growth_stage" in developments:
            self.current_state.growth_stage = developments["growth_stage"]
    
    def generate_growth_arc(self) -> Dict:
        """生成角色成长弧线"""
        if not self.growth_timeline:
            return {"error": "No growth data available"}
        
        return {
            "character": self.character_name,
            "starting_point": self.growth_timeline[0] if self.growth_timeline else {},
            "current_state": {
                "age": self.current_state.age,
                "status": self.current_state.status,
                "location": self.current_state.location,
                "skills": self.current_state.skills,
                "growth_stage": self.current_state.growth_stage
            },
            "major_turning_points": self.identify_turning_points(),
            "total_books": len(self.growth_timeline),
            "character_trajectory": self.analyze_trajectory()
        }
    
    def identify_turning_points(self) -> List[Dict]:
        """识别重要转折点"""
        turning_points = []
        
        for i, record in enumerate(self.growth_timeline):
            # 检查是否有重大变化
            if record.get("trauma_and_healing"):
                turning_points.append({
                    "book": record["book"],
                    "type": "trauma/healing",
                    "description": record["trauma_and_healing"]
                })
            
            if record.get("personality_evolution"):
                turning_points.append({
                    "book": record["book"],
                    "type": "personality_change",
                    "description": record["personality_evolution"]
                })
        
        return turning_points
    
    def analyze_trajectory(self) -> str:
        """分析角色发展轨迹"""
        if self.current_state.growth_stage == "transformed":
            return "complete_transformation"
        elif len(self.growth_timeline) > 3:
            return "steady_growth"
        else:
            return "early_development"


class PlotThreadManager:
    """情节线管理器"""
    
    def __init__(self):
        self.plot_threads = {}
        self.thread_counter = 0
    
    def create_thread(self, description: str, thread_type: str, book_number: int) -> str:
        """创建新的情节线"""
        thread_id = f"thread_{self.thread_counter:03d}"
        self.thread_counter += 1
        
        self.plot_threads[thread_id] = PlotThread(
            id=thread_id,
            description=description,
            thread_type=thread_type,
            status="active",
            books_span=[book_number]
        )
        
        return thread_id
    
    def update_thread(self, thread_id: str, book_number: int, development: Dict):
        """更新情节线发展"""
        if thread_id not in self.plot_threads:
            return
        
        thread = self.plot_threads[thread_id]
        
        # 添加到跨越书籍列表
        if book_number not in thread.books_span:
            thread.books_span.append(book_number)
        
        # 记录发展
        thread.developments.append({
            "book": book_number,
            "development": development.get("description"),
            "reveals": development.get("reveals", []),
            "complications": development.get("complications", []),
            "partial_resolution": development.get("partial_resolution", False)
        })
        
        # 更新状态
        if development.get("resolved", False):
            thread.status = "resolved"
            thread.resolution_book = book_number
        elif development.get("dormant", False):
            thread.status = "dormant"
    
    def get_active_threads(self, book_number: int) -> List[PlotThread]:
        """获取特定书籍的活跃情节线"""
        active = []
        for thread in self.plot_threads.values():
            if thread.status == "active" and book_number in thread.books_span:
                active.append(thread)
        return active
    
    def get_unresolved_threads(self) -> List[PlotThread]:
        """获取所有未解决的情节线"""
        return [
            thread for thread in self.plot_threads.values()
            if thread.status in ["active", "dormant"]
        ]
    
    def calculate_thread_importance(self, thread_id: str) -> int:
        """计算情节线重要性（0-100）"""
        if thread_id not in self.plot_threads:
            return 0
        
        thread = self.plot_threads[thread_id]
        importance = 0
        
        # 主线最重要
        if thread.thread_type == "main":
            importance += 50
        elif thread.thread_type == "subplot":
            importance += 20
        else:
            importance += 10
        
        # 跨越书籍越多越重要
        importance += len(thread.books_span) * 10
        
        # 发展越多越重要
        importance += min(len(thread.developments) * 5, 30)
        
        # 未解决的更重要
        if thread.status == "active":
            importance += 10
        
        return min(importance, 100)


class BibleEvolutionManager:
    """Bible演化管理器"""
    
    def __init__(self, series_path: Path):
        self.series_path = Path(series_path)
        self.character_trackers = {}
        self.plot_manager = PlotThreadManager()
    
    def load_series_bible(self) -> Dict:
        """加载系列总Bible"""
        bible_path = self.series_path / "series-bible.json"
        if bible_path.exists():
            with open(bible_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_previous_summaries(self, up_to_book: int) -> List[Dict]:
        """加载所有前作总结"""
        summaries = []
        
        for book_num in range(1, up_to_book + 1):
            summary_path = self.series_path / f"book-{book_num:02d}" / "completion-summary.json"
            if summary_path.exists():
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summaries.append(json.load(f))
        
        return summaries
    
    def generate_next_book_bible(self, book_number: int) -> Dict:
        """为下一本书生成Bible"""
        # 加载系列Bible
        series_bible = self.load_series_bible()
        
        # 加载前作总结
        previous_summaries = self.load_previous_summaries(book_number - 1)
        
        # 分析累积变化
        cumulative_context = self.analyze_cumulative_changes(previous_summaries)
        
        # 识别必须延续的元素
        mandatory_continuations = self.extract_mandatory_continuations(previous_summaries)
        
        # 生成新书Bible
        new_bible = {
            "book_number": book_number,
            "created_at": datetime.now().isoformat(),
            "inherits": {
                "series_bible": series_bible.get("series_name"),
                "previous_books": list(range(1, book_number))
            },
            "cumulative_context": cumulative_context,
            "mandatory_continuations": mandatory_continuations,
            "book_specific": {
                "starting_situation": self.determine_starting_situation(cumulative_context),
                "available_characters": self.list_available_characters(cumulative_context),
                "active_plot_threads": self.get_active_threads(book_number),
                "world_state": self.determine_world_state(cumulative_context),
                "time_progression": self.calculate_time_progression(previous_summaries)
            },
            "continuity_requirements": {
                "must_address": mandatory_continuations.get("unresolved_conflicts", []),
                "must_continue": mandatory_continuations.get("character_arcs", []),
                "must_fulfill": mandatory_continuations.get("promised_events", []),
                "must_maintain": self.identify_consistency_requirements(series_bible)
            }
        }
        
        return new_bible
    
    def analyze_cumulative_changes(self, summaries: List[Dict]) -> Dict:
        """分析累积变化"""
        cumulative = {
            "total_time_passed": 0,
            "character_deaths": [],
            "major_events": [],
            "world_changes": [],
            "revealed_information": [],
            "relationship_evolution": {}
        }
        
        for summary in summaries:
            # 累积角色死亡
            if "character_evolution" in summary:
                deaths = summary["character_evolution"].get("character_deaths", [])
                cumulative["character_deaths"].extend(deaths)
            
            # 累积重大事件
            if "plot_impacts" in summary:
                resolved = summary["plot_impacts"].get("resolved_conflicts", [])
                cumulative["major_events"].extend(resolved)
            
            # 累积揭示的信息
            if "reader_knowledge" in summary:
                revealed = summary["reader_knowledge"].get("revealed_mysteries", [])
                cumulative["revealed_information"].extend(revealed)
        
        return cumulative
    
    def extract_mandatory_continuations(self, summaries: List[Dict]) -> Dict:
        """提取必须延续的元素"""
        mandatory = {
            "unresolved_conflicts": [],
            "character_arcs": [],
            "promised_events": [],
            "open_questions": []
        }
        
        # 从最近的总结中提取
        if summaries:
            latest = summaries[-1]
            
            if "unfinished_business" in latest:
                unfinished = latest["unfinished_business"]
                mandatory["promised_events"] = unfinished.get("promised_events", [])
                mandatory["open_questions"] = unfinished.get("open_questions", [])
                
                # 提取未完成的角色目标
                for char_goal in unfinished.get("character_goals", []):
                    mandatory["character_arcs"].append(char_goal)
        
        return mandatory
    
    def determine_starting_situation(self, cumulative_context: Dict) -> Dict:
        """确定新书的起始状况"""
        return {
            "time_jump": "TBD",  # 需要作者决定
            "initial_peace": len(cumulative_context.get("major_events", [])) > 0,
            "available_cast": self.calculate_available_cast(cumulative_context),
            "world_status": "evolved" if cumulative_context.get("world_changes") else "stable"
        }
    
    def list_available_characters(self, cumulative_context: Dict) -> List[str]:
        """列出可用角色"""
        # 这需要从系列Bible和累积上下文中提取
        dead_characters = cumulative_context.get("character_deaths", [])
        # 实际实现需要从Bible中获取所有角色并排除死亡角色
        return []
    
    def calculate_available_cast(self, cumulative_context: Dict) -> int:
        """计算可用角色数量"""
        # 简化实现
        total_characters = 10  # 假设初始10个角色
        deaths = len(cumulative_context.get("character_deaths", []))
        return total_characters - deaths
    
    def get_active_threads(self, book_number: int) -> List[str]:
        """获取活跃的情节线"""
        return [thread.description for thread in self.plot_manager.get_active_threads(book_number)]
    
    def determine_world_state(self, cumulative_context: Dict) -> str:
        """确定世界状态"""
        changes = len(cumulative_context.get("world_changes", []))
        if changes > 5:
            return "drastically_changed"
        elif changes > 2:
            return "significantly_evolved"
        else:
            return "relatively_stable"
    
    def calculate_time_progression(self, summaries: List[Dict]) -> str:
        """计算时间进程"""
        # 简化实现，实际需要从每本书的时间跨度累加
        books = len(summaries)
        if books == 0:
            return "series_start"
        elif books < 3:
            return f"after_{books}_books"
        else:
            return f"years_later"
    
    def identify_consistency_requirements(self, series_bible: Dict) -> List[str]:
        """识别一致性要求"""
        return [
            "Character personalities must remain consistent",
            "World rules cannot be violated",
            "Timeline must be coherent",
            "Established facts cannot be contradicted"
        ]


# 使用示例
if __name__ == "__main__":
    # 创建演化管理器
    evolution_manager = BibleEvolutionManager(Path("D:/NOVELSYS-SWARM/projects/mystery-series"))
    
    # 为第二本书生成Bible
    book2_bible = evolution_manager.generate_next_book_bible(2)
    print(json.dumps(book2_bible, indent=2, ensure_ascii=False))
    
    # 创建角色成长追踪
    protagonist_tracker = CharacterGrowthTracker("Detective Li")
    protagonist_tracker.record_book_development(1, {
        "age_change": 1,
        "new_skills": ["advanced deduction"],
        "personality": ["more confident", "less naive"],
        "growth_stage": "developing"
    })
    
    growth_arc = protagonist_tracker.generate_growth_arc()
    print(json.dumps(growth_arc, indent=2, ensure_ascii=False))