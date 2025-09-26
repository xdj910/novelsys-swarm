"""
项目管理器
负责创建和管理不同类型的小说项目结构
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class ProjectType(Enum):
    """项目类型枚举"""
    SERIES = "series"           # 系列小说
    STANDALONE = "standalone"   # 单本小说
    COLLECTION = "collection"   # 短篇集
    SERIAL = "serial"          # 连载小说


class ProjectManager:
    """项目管理器"""
    
    def __init__(self, base_path: str = "D:/NOVELSYS-SWARM/projects"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def create_project(self, name: str, project_type: ProjectType, metadata: Dict[str, Any] = None) -> Path:
        """创建新项目"""
        project_path = self.base_path / name
        
        if project_path.exists():
            raise ValueError(f"Project {name} already exists")
        
        # 根据类型创建项目结构
        if project_type == ProjectType.SERIES:
            return self._create_series_project(project_path, metadata)
        elif project_type == ProjectType.STANDALONE:
            return self._create_standalone_project(project_path, metadata)
        elif project_type == ProjectType.COLLECTION:
            return self._create_collection_project(project_path, metadata)
        elif project_type == ProjectType.SERIAL:
            return self._create_serial_project(project_path, metadata)
        else:
            raise ValueError(f"Unknown project type: {project_type}")
    
    def _create_series_project(self, project_path: Path, metadata: Dict[str, Any] = None) -> Path:
        """创建系列小说项目结构"""
        # 创建目录结构
        project_path.mkdir(parents=True)
        
        # 创建项目类型标识
        (project_path / ".project-type").write_text("series")
        
        # 创建系列元数据
        series_meta = {
            "type": "series",
            "name": project_path.name,
            "created_at": datetime.now().isoformat(),
            "genre": metadata.get("genre", "fiction") if metadata else "fiction",
            "target_audience": metadata.get("audience", "general") if metadata else "general",
            "planned_books": metadata.get("planned_books", 3) if metadata else 3,
            "status": "active"
        }
        
        with open(project_path / "series.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(series_meta, f, allow_unicode=True)
        
        # 创建系列Bible
        series_bible = self._create_series_bible_template(project_path.name, metadata)
        with open(project_path / "series-bible.json", 'w', encoding='utf-8') as f:
            json.dump(series_bible, f, ensure_ascii=False, indent=2)
        
        # 创建子目录
        (project_path / "characters").mkdir()
        (project_path / "worldbuilding").mkdir()
        (project_path / ".claude").mkdir()
        (project_path / ".claude" / "context").mkdir()
        (project_path / ".claude" / "memory").mkdir()
        
        # 创建角色文件
        self._create_character_files(project_path / "characters")
        
        # 创建世界观文件
        self._create_worldbuilding_files(project_path / "worldbuilding")
        
        print(f"Created series project: {project_path}")
        return project_path
    
    def _create_standalone_project(self, project_path: Path, metadata: Dict[str, Any] = None) -> Path:
        """创建单本小说项目结构"""
        project_path.mkdir(parents=True)
        
        # 创建项目类型标识
        (project_path / ".project-type").write_text("standalone")
        
        # 创建书籍元数据
        book_meta = {
            "type": "standalone",
            "title": project_path.name,
            "created_at": datetime.now().isoformat(),
            "genre": metadata.get("genre", "fiction") if metadata else "fiction",
            "target_audience": metadata.get("audience", "general") if metadata else "general",
            "target_word_count": metadata.get("word_count", 80000) if metadata else 80000,
            "status": "draft"
        }
        
        with open(project_path / "book.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(book_meta, f, allow_unicode=True)
        
        # 创建独立Bible
        bible = self._create_standalone_bible_template(project_path.name, metadata)
        with open(project_path / "bible.json", 'w', encoding='utf-8') as f:
            json.dump(bible, f, ensure_ascii=False, indent=2)
        
        # 创建子目录
        (project_path / "chapters").mkdir()
        (project_path / "characters").mkdir()
        (project_path / "worldbuilding").mkdir()
        (project_path / "exports").mkdir()
        (project_path / ".claude").mkdir()
        (project_path / ".claude" / "context").mkdir()
        
        # 创建大纲文件
        outline = {
            "title": project_path.name,
            "chapters": [],
            "total_chapters": metadata.get("chapters", 20) if metadata else 20
        }
        with open(project_path / "outline.json", 'w', encoding='utf-8') as f:
            json.dump(outline, f, ensure_ascii=False, indent=2)
        
        print(f"Created standalone project: {project_path}")
        return project_path
    
    def _create_collection_project(self, project_path: Path, metadata: Dict[str, Any] = None) -> Path:
        """创建短篇集项目结构"""
        project_path.mkdir(parents=True)
        
        # 创建项目类型标识
        (project_path / ".project-type").write_text("collection")
        
        # 创建合集元数据
        collection_meta = {
            "type": "collection",
            "title": project_path.name,
            "created_at": datetime.now().isoformat(),
            "theme": metadata.get("theme", "various") if metadata else "various",
            "planned_stories": metadata.get("stories", 10) if metadata else 10,
            "status": "collecting"
        }
        
        with open(project_path / "collection.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(collection_meta, f, allow_unicode=True)
        
        # 创建主题配置
        theme_config = {
            "unifying_theme": metadata.get("theme", "various") if metadata else "various",
            "tone": metadata.get("tone", "mixed") if metadata else "mixed",
            "recurring_elements": []
        }
        with open(project_path / "collection-theme.json", 'w', encoding='utf-8') as f:
            json.dump(theme_config, f, ensure_ascii=False, indent=2)
        
        # 创建子目录
        (project_path / "stories").mkdir()
        (project_path / "exports").mkdir()
        (project_path / ".claude").mkdir()
        (project_path / ".claude" / "context").mkdir()
        
        print(f"Created collection project: {project_path}")
        return project_path
    
    def _create_serial_project(self, project_path: Path, metadata: Dict[str, Any] = None) -> Path:
        """创建连载小说项目结构"""
        project_path.mkdir(parents=True)
        
        # 创建项目类型标识
        (project_path / ".project-type").write_text("serial")
        
        # 创建连载元数据
        serial_meta = {
            "type": "serial",
            "title": project_path.name,
            "created_at": datetime.now().isoformat(),
            "update_schedule": metadata.get("schedule", "daily") if metadata else "daily",
            "planned_chapters": metadata.get("chapters", 500) if metadata else 500,
            "status": "ongoing"
        }
        
        with open(project_path / "serial.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(serial_meta, f, allow_unicode=True)
        
        # 创建Bible
        bible = self._create_serial_bible_template(project_path.name, metadata)
        with open(project_path / "bible.json", 'w', encoding='utf-8') as f:
            json.dump(bible, f, ensure_ascii=False, indent=2)
        
        # 创建子目录
        (project_path / "arcs").mkdir()
        (project_path / "daily-updates").mkdir()
        (project_path / ".claude").mkdir()
        (project_path / ".claude" / "context").mkdir()
        
        print(f"Created serial project: {project_path}")
        return project_path
    
    def add_book_to_series(self, series_name: str, book_number: int, book_title: str) -> Path:
        """向系列添加新书"""
        series_path = self.base_path / series_name
        
        if not series_path.exists():
            raise ValueError(f"Series {series_name} does not exist")
        
        if (series_path / ".project-type").read_text() != "series":
            raise ValueError(f"{series_name} is not a series project")
        
        # 创建书籍目录
        book_dir = series_path / f"book-{book_number:02d}-{book_title}"
        book_dir.mkdir(parents=True)
        
        # 创建书籍元数据
        book_meta = {
            "book_number": book_number,
            "title": book_title,
            "series": series_name,
            "created_at": datetime.now().isoformat(),
            "status": "planning"
        }
        
        with open(book_dir / "book.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(book_meta, f, allow_unicode=True)
        
        # 创建书籍Bible（继承系列Bible）
        series_bible_path = series_path / "series-bible.json"
        with open(series_bible_path, 'r', encoding='utf-8') as f:
            series_bible = json.load(f)
        
        book_bible = {
            "inherits_from": "series-bible.json",
            "book_specific": {
                "book_number": book_number,
                "title": book_title,
                "plot": {},
                "new_characters": [],
                "timeline": []
            }
        }
        
        with open(book_dir / "book-bible.json", 'w', encoding='utf-8') as f:
            json.dump(book_bible, f, ensure_ascii=False, indent=2)
        
        # 创建子目录
        (book_dir / "chapters").mkdir()
        (book_dir / "exports").mkdir()
        (book_dir / "quality").mkdir()
        
        # 创建大纲
        outline = {
            "book_title": book_title,
            "book_number": book_number,
            "chapters": []
        }
        
        with open(book_dir / "outline.json", 'w', encoding='utf-8') as f:
            json.dump(outline, f, ensure_ascii=False, indent=2)
        
        print(f"Added book {book_number}: {book_title} to series {series_name}")
        return book_dir
    
    def create_chapter(self, project_path: Path, chapter_number: int) -> Path:
        """创建章节目录结构"""
        # 判断项目类型
        project_type = (project_path / ".project-type").read_text()
        
        if project_type == "series":
            # 系列小说需要指定具体的书
            raise ValueError("For series, please specify the book directory")
        
        # 确定章节目录位置
        if project_type in ["standalone", "series"]:
            chapters_dir = project_path / "chapters"
        else:
            raise ValueError(f"Chapter creation not supported for {project_type}")
        
        # 创建章节目录
        chapter_dir = chapters_dir / f"ch{chapter_number:03d}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建章节文件
        chapter_data = {
            "chapter_number": chapter_number,
            "title": f"Chapter {chapter_number}",
            "content": "",
            "scenes": [],
            "word_count": 0,
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "quality_score": 0
        }
        
        with open(chapter_dir / "chapter.json", 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        
        # 创建场景文件
        scenes_data = {
            "chapter": chapter_number,
            "scenes": []
        }
        
        with open(chapter_dir / "scenes.json", 'w', encoding='utf-8') as f:
            json.dump(scenes_data, f, ensure_ascii=False, indent=2)
        
        # 创建笔记文件
        (chapter_dir / "notes.md").write_text(f"# Chapter {chapter_number} Notes\n\n")
        
        # 创建版本目录
        (chapter_dir / "versions").mkdir(exist_ok=True)
        
        return chapter_dir
    
    def _create_series_bible_template(self, series_name: str, metadata: Dict[str, Any] = None) -> Dict:
        """创建系列Bible模板"""
        return {
            "series_name": series_name,
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "world_building": {
                "setting": {},
                "rules": {},
                "history": []
            },
            "recurring_characters": {
                "protagonists": [],
                "supporting": []
            },
            "series_themes": [],
            "series_arc": {
                "overall_conflict": "",
                "planned_resolution": ""
            },
            "style_guide": {
                "narrative_voice": "",
                "tone": "",
                "recurring_motifs": []
            }
        }
    
    def _create_standalone_bible_template(self, book_title: str, metadata: Dict[str, Any] = None) -> Dict:
        """创建单本Bible模板"""
        return {
            "book_title": book_title,
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "world_building": {
                "setting": {},
                "atmosphere": ""
            },
            "characters": {
                "protagonists": [],
                "antagonists": [],
                "supporting": []
            },
            "plot": {
                "central_conflict": "",
                "themes": [],
                "structure": {}
            },
            "style_guide": {
                "narrative_voice": "",
                "tone": "",
                "language_style": ""
            }
        }
    
    def _create_serial_bible_template(self, serial_title: str, metadata: Dict[str, Any] = None) -> Dict:
        """创建连载Bible模板"""
        return {
            "serial_title": serial_title,
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "world_building": {
                "power_system": {},
                "factions": [],
                "locations": []
            },
            "characters": {
                "main_cast": [],
                "recurring": [],
                "arc_specific": {}
            },
            "arcs": [],
            "update_schedule": metadata.get("schedule", "daily") if metadata else "daily"
        }
    
    def _create_character_files(self, characters_dir: Path):
        """创建角色文件"""
        # 主角文件
        protagonists = {
            "characters": [],
            "relationships": []
        }
        with open(characters_dir / "protagonists.json", 'w', encoding='utf-8') as f:
            json.dump(protagonists, f, ensure_ascii=False, indent=2)
        
        # 重复角色文件
        recurring = {
            "characters": [],
            "appearances": {}
        }
        with open(characters_dir / "recurring.json", 'w', encoding='utf-8') as f:
            json.dump(recurring, f, ensure_ascii=False, indent=2)
        
        # 关系网络文件
        relationships = {
            "relationships": [],
            "relationship_types": ["family", "friend", "rival", "romantic", "professional"]
        }
        with open(characters_dir / "relationships.json", 'w', encoding='utf-8') as f:
            json.dump(relationships, f, ensure_ascii=False, indent=2)
    
    def _create_worldbuilding_files(self, worldbuilding_dir: Path):
        """创建世界观文件"""
        # 地点文件
        locations = {
            "primary_locations": [],
            "secondary_locations": [],
            "location_connections": []
        }
        with open(worldbuilding_dir / "locations.json", 'w', encoding='utf-8') as f:
            json.dump(locations, f, ensure_ascii=False, indent=2)
        
        # 时间线文件
        timeline = {
            "historical_events": [],
            "story_timeline": []
        }
        with open(worldbuilding_dir / "timeline.json", 'w', encoding='utf-8') as f:
            json.dump(timeline, f, ensure_ascii=False, indent=2)
        
        # 规则文件
        rules = {
            "physical_laws": [],
            "social_rules": [],
            "magic_system": {}
        }
        with open(worldbuilding_dir / "rules.json", 'w', encoding='utf-8') as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
    
    def list_projects(self, project_type: Optional[ProjectType] = None) -> list:
        """列出所有项目"""
        projects = []
        
        for project_dir in self.base_path.iterdir():
            if project_dir.is_dir() and (project_dir / ".project-type").exists():
                p_type = (project_dir / ".project-type").read_text()
                
                if project_type is None or p_type == project_type.value:
                    projects.append({
                        "name": project_dir.name,
                        "type": p_type,
                        "path": str(project_dir)
                    })
        
        return projects
    
    def get_project_info(self, project_name: str) -> Dict[str, Any]:
        """获取项目信息"""
        project_path = self.base_path / project_name
        
        if not project_path.exists():
            raise ValueError(f"Project {project_name} does not exist")
        
        project_type = (project_path / ".project-type").read_text()
        
        info = {
            "name": project_name,
            "type": project_type,
            "path": str(project_path)
        }
        
        # 根据类型读取元数据
        if project_type == "series":
            with open(project_path / "series.yaml", 'r', encoding='utf-8') as f:
                info["metadata"] = yaml.safe_load(f)
            # 统计书籍数量
            books = [d for d in project_path.iterdir() if d.is_dir() and d.name.startswith("book-")]
            info["books_count"] = len(books)
            info["books"] = [d.name for d in books]
            
        elif project_type == "standalone":
            with open(project_path / "book.yaml", 'r', encoding='utf-8') as f:
                info["metadata"] = yaml.safe_load(f)
            # 统计章节数量
            chapters_dir = project_path / "chapters"
            if chapters_dir.exists():
                chapters = [d for d in chapters_dir.iterdir() if d.is_dir() and d.name.startswith("ch")]
                info["chapters_count"] = len(chapters)
                
        elif project_type == "collection":
            with open(project_path / "collection.yaml", 'r', encoding='utf-8') as f:
                info["metadata"] = yaml.safe_load(f)
            # 统计故事数量
            stories_dir = project_path / "stories"
            if stories_dir.exists():
                stories = [d for d in stories_dir.iterdir() if d.is_dir()]
                info["stories_count"] = len(stories)
                info["stories"] = [d.name for d in stories]
                
        elif project_type == "serial":
            with open(project_path / "serial.yaml", 'r', encoding='utf-8') as f:
                info["metadata"] = yaml.safe_load(f)
            # 统计故事弧数量
            arcs_dir = project_path / "arcs"
            if arcs_dir.exists():
                arcs = [d for d in arcs_dir.iterdir() if d.is_dir()]
                info["arcs_count"] = len(arcs)
                info["arcs"] = [d.name for d in arcs]
        
        return info


# 测试代码
if __name__ == "__main__":
    pm = ProjectManager()
    
    # 创建系列小说项目
    series_path = pm.create_project(
        "mystery-series",
        ProjectType.SERIES,
        {"genre": "mystery", "audience": "adult", "planned_books": 5}
    )
    
    # 向系列添加第一本书
    book1_path = pm.add_book_to_series("mystery-series", 1, "温泉谜案")
    
    # 创建单本小说项目
    standalone_path = pm.create_project(
        "the-last-sunset",
        ProjectType.STANDALONE,
        {"genre": "drama", "word_count": 100000, "chapters": 25}
    )
    
    # 列出所有项目
    projects = pm.list_projects()
    print("\nAll projects:")
    for p in projects:
        print(f"  - {p['name']} ({p['type']})")
    
    # 获取项目信息
    info = pm.get_project_info("mystery-series")
    print(f"\nProject info for {info['name']}:")
    print(f"  Type: {info['type']}")
    print(f"  Books: {info.get('books_count', 0)}")