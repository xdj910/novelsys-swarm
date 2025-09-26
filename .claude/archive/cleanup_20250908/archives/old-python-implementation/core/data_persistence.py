"""
数据持久化层
负责Bible、章节、上下文的存储和管理
适配Claude Code环境，使用文件系统存储
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
from dataclasses import dataclass, asdict
import shutil


@dataclass
class BibleMetadata:
    """Bible元数据"""
    id: str
    title: str
    genre: str
    created_at: str
    updated_at: str
    version: str = "1.0"
    chapters_count: int = 0
    total_words: int = 0
    quality_score: float = 0.0
    
    
@dataclass
class ChapterMetadata:
    """章节元数据"""
    chapter_number: int
    title: str
    word_count: int
    created_at: str
    updated_at: str
    quality_score: float
    status: str  # draft/reviewed/published
    scenes_count: int


class BibleStorage:
    """Bible存储管理器"""
    
    def __init__(self, base_path: str = "D:\\NOVELSYS-SWARM\\data"):
        """
        初始化Bible存储
        
        Args:
            base_path: 数据存储根目录
        """
        self.base_path = Path(base_path)
        self.bibles_path = self.base_path / "bibles"
        self.bibles_path.mkdir(parents=True, exist_ok=True)
        
    def create_bible(self, bible_data: Dict) -> str:
        """
        创建新的Bible
        
        Args:
            bible_data: Bible数据
            
        Returns:
            Bible ID
        """
        # 生成唯一ID
        bible_id = self._generate_bible_id(bible_data.get('title', 'untitled'))
        
        # 创建Bible目录
        bible_dir = self.bibles_path / bible_id
        bible_dir.mkdir(exist_ok=True)
        
        # 创建元数据
        metadata = BibleMetadata(
            id=bible_id,
            title=bible_data.get('title', 'Untitled'),
            genre=bible_data.get('genre', 'fantasy'),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # 保存元数据
        metadata_path = bible_dir / "metadata.yaml"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            yaml.dump(asdict(metadata), f, allow_unicode=True, default_flow_style=False)
        
        # 保存Bible内容
        bible_path = bible_dir / "bible.yaml"
        with open(bible_path, 'w', encoding='utf-8') as f:
            yaml.dump(bible_data, f, allow_unicode=True, default_flow_style=False)
        
        # 创建章节目录
        chapters_dir = bible_dir / "chapters"
        chapters_dir.mkdir(exist_ok=True)
        
        # 创建上下文目录
        context_dir = bible_dir / "context"
        context_dir.mkdir(exist_ok=True)
        
        print(f"Created Bible: {bible_id} at {bible_dir}")
        return bible_id
    
    def read_bible(self, bible_id: str) -> Optional[Dict]:
        """
        读取Bible
        
        Args:
            bible_id: Bible ID
            
        Returns:
            Bible数据
        """
        bible_path = self.bibles_path / bible_id / "bible.yaml"
        
        if not bible_path.exists():
            print(f"Bible not found: {bible_id}")
            return None
        
        with open(bible_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def update_bible(self, bible_id: str, updates: Dict) -> bool:
        """
        更新Bible
        
        Args:
            bible_id: Bible ID
            updates: 更新内容
            
        Returns:
            是否成功
        """
        bible_path = self.bibles_path / bible_id / "bible.yaml"
        
        if not bible_path.exists():
            print(f"Bible not found: {bible_id}")
            return False
        
        # 读取现有数据
        with open(bible_path, 'r', encoding='utf-8') as f:
            bible_data = yaml.safe_load(f)
        
        # 合并更新
        bible_data.update(updates)
        
        # 创建备份
        backup_path = bible_path.with_suffix('.yaml.bak')
        shutil.copy2(bible_path, backup_path)
        
        # 保存更新
        with open(bible_path, 'w', encoding='utf-8') as f:
            yaml.dump(bible_data, f, allow_unicode=True, default_flow_style=False)
        
        # 更新元数据
        self._update_metadata(bible_id, {'updated_at': datetime.now().isoformat()})
        
        return True
    
    def delete_bible(self, bible_id: str) -> bool:
        """
        删除Bible（移到回收站）
        
        Args:
            bible_id: Bible ID
            
        Returns:
            是否成功
        """
        bible_dir = self.bibles_path / bible_id
        
        if not bible_dir.exists():
            print(f"Bible not found: {bible_id}")
            return False
        
        # 移到回收站目录
        trash_dir = self.base_path / "trash" / "bibles"
        trash_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trash_path = trash_dir / f"{bible_id}_{timestamp}"
        
        shutil.move(str(bible_dir), str(trash_path))
        print(f"Moved Bible {bible_id} to trash")
        
        return True
    
    def list_bibles(self) -> List[Dict]:
        """
        列出所有Bible
        
        Returns:
            Bible列表
        """
        bibles = []
        
        for bible_dir in self.bibles_path.iterdir():
            if bible_dir.is_dir():
                metadata_path = bible_dir / "metadata.yaml"
                if metadata_path.exists():
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = yaml.safe_load(f)
                        bibles.append(metadata)
        
        return sorted(bibles, key=lambda x: x.get('updated_at', ''), reverse=True)
    
    def _generate_bible_id(self, title: str) -> str:
        """生成Bible ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        return f"bible_{timestamp}_{title_hash}"
    
    def _update_metadata(self, bible_id: str, updates: Dict):
        """更新元数据"""
        metadata_path = self.bibles_path / bible_id / "metadata.yaml"
        
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
            
            metadata.update(updates)
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                yaml.dump(metadata, f, allow_unicode=True, default_flow_style=False)


class ChapterStorage:
    """章节存储管理器"""
    
    def __init__(self, base_path: str = "D:\\NOVELSYS-SWARM\\data"):
        """
        初始化章节存储
        
        Args:
            base_path: 数据存储根目录
        """
        self.base_path = Path(base_path)
        self.bibles_path = self.base_path / "bibles"
        
    def save_chapter(
        self, 
        bible_id: str, 
        chapter_number: int,
        chapter_data: Dict
    ) -> bool:
        """
        保存章节
        
        Args:
            bible_id: Bible ID
            chapter_number: 章节号
            chapter_data: 章节数据
            
        Returns:
            是否成功
        """
        chapters_dir = self.bibles_path / bible_id / "chapters"
        
        if not chapters_dir.exists():
            print(f"Bible not found: {bible_id}")
            return False
        
        # 创建章节文件
        chapter_file = chapters_dir / f"chapter_{chapter_number:03d}.json"
        
        # 计算字数
        word_count = self._calculate_word_count(chapter_data)
        
        # 创建章节元数据
        metadata = ChapterMetadata(
            chapter_number=chapter_number,
            title=chapter_data.get('title', f'Chapter {chapter_number}'),
            word_count=word_count,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            quality_score=chapter_data.get('quality_score', 0.0),
            status=chapter_data.get('status', 'draft'),
            scenes_count=len(chapter_data.get('scenes', []))
        )
        
        # 合并元数据和内容
        full_data = {
            'metadata': asdict(metadata),
            'content': chapter_data
        }
        
        # 保存章节
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
        
        # 更新Bible元数据
        self._update_bible_stats(bible_id)
        
        print(f"Saved chapter {chapter_number} for Bible {bible_id}")
        return True
    
    def read_chapter(
        self, 
        bible_id: str, 
        chapter_number: int
    ) -> Optional[Dict]:
        """
        读取章节
        
        Args:
            bible_id: Bible ID
            chapter_number: 章节号
            
        Returns:
            章节数据
        """
        chapter_file = (self.bibles_path / bible_id / "chapters" / 
                       f"chapter_{chapter_number:03d}.json")
        
        if not chapter_file.exists():
            print(f"Chapter {chapter_number} not found for Bible {bible_id}")
            return None
        
        with open(chapter_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_chapter(
        self,
        bible_id: str,
        chapter_number: int,
        updates: Dict
    ) -> bool:
        """
        更新章节
        
        Args:
            bible_id: Bible ID
            chapter_number: 章节号
            updates: 更新内容
            
        Returns:
            是否成功
        """
        chapter_file = (self.bibles_path / bible_id / "chapters" / 
                       f"chapter_{chapter_number:03d}.json")
        
        if not chapter_file.exists():
            print(f"Chapter {chapter_number} not found for Bible {bible_id}")
            return False
        
        # 读取现有数据
        with open(chapter_file, 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)
        
        # 更新内容
        if 'content' in chapter_data:
            chapter_data['content'].update(updates)
        
        # 更新元数据
        chapter_data['metadata']['updated_at'] = datetime.now().isoformat()
        
        # 重新计算字数
        if 'scenes' in updates:
            word_count = self._calculate_word_count(chapter_data['content'])
            chapter_data['metadata']['word_count'] = word_count
            chapter_data['metadata']['scenes_count'] = len(updates['scenes'])
        
        # 保存更新
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        
        # 更新Bible统计
        self._update_bible_stats(bible_id)
        
        return True
    
    def list_chapters(self, bible_id: str) -> List[Dict]:
        """
        列出所有章节
        
        Args:
            bible_id: Bible ID
            
        Returns:
            章节列表
        """
        chapters_dir = self.bibles_path / bible_id / "chapters"
        
        if not chapters_dir.exists():
            return []
        
        chapters = []
        
        for chapter_file in sorted(chapters_dir.glob("chapter_*.json")):
            with open(chapter_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                chapters.append(data['metadata'])
        
        return chapters
    
    def delete_chapter(self, bible_id: str, chapter_number: int) -> bool:
        """
        删除章节
        
        Args:
            bible_id: Bible ID
            chapter_number: 章节号
            
        Returns:
            是否成功
        """
        chapter_file = (self.bibles_path / bible_id / "chapters" / 
                       f"chapter_{chapter_number:03d}.json")
        
        if not chapter_file.exists():
            print(f"Chapter {chapter_number} not found")
            return False
        
        # 移到回收站
        trash_dir = self.base_path / "trash" / "chapters" / bible_id
        trash_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trash_file = trash_dir / f"chapter_{chapter_number:03d}_{timestamp}.json"
        
        shutil.move(str(chapter_file), str(trash_file))
        
        # 更新Bible统计
        self._update_bible_stats(bible_id)
        
        return True
    
    def _calculate_word_count(self, chapter_data: Dict) -> int:
        """计算章节字数"""
        total_words = 0
        
        # 计算场景内容字数
        for scene in chapter_data.get('scenes', []):
            if isinstance(scene, dict):
                content = scene.get('content', '')
            else:
                content = str(scene)
            
            # 简单的中文字数统计
            chinese_chars = len([c for c in content if '\u4e00' <= c <= '\u9fff'])
            # 英文单词统计
            english_words = len(content.split()) if content else 0
            
            total_words += max(chinese_chars, english_words)
        
        return total_words
    
    def _update_bible_stats(self, bible_id: str):
        """更新Bible统计信息"""
        chapters = self.list_chapters(bible_id)
        
        total_words = sum(ch.get('word_count', 0) for ch in chapters)
        avg_quality = (sum(ch.get('quality_score', 0) for ch in chapters) / 
                      len(chapters) if chapters else 0)
        
        # 更新Bible元数据
        metadata_path = self.bibles_path / bible_id / "metadata.yaml"
        
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
            
            metadata['chapters_count'] = len(chapters)
            metadata['total_words'] = total_words
            metadata['quality_score'] = avg_quality
            metadata['updated_at'] = datetime.now().isoformat()
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                yaml.dump(metadata, f, allow_unicode=True, default_flow_style=False)


class ContextStorage:
    """上下文存储管理器"""
    
    def __init__(self, base_path: str = "D:\\NOVELSYS-SWARM\\data"):
        """
        初始化上下文存储
        
        Args:
            base_path: 数据存储根目录
        """
        self.base_path = Path(base_path)
        self.bibles_path = self.base_path / "bibles"
        
    def save_context(
        self,
        bible_id: str,
        context_type: str,
        context_data: Dict
    ) -> bool:
        """
        保存上下文
        
        Args:
            bible_id: Bible ID
            context_type: 上下文类型 (global/chapter/character/scene)
            context_data: 上下文数据
            
        Returns:
            是否成功
        """
        context_dir = self.bibles_path / bible_id / "context"
        
        if not context_dir.exists():
            context_dir.mkdir(parents=True, exist_ok=True)
        
        # 根据类型确定文件名
        context_file = context_dir / f"{context_type}_context.json"
        
        # 添加时间戳
        context_data['_updated_at'] = datetime.now().isoformat()
        
        # 保存上下文
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {context_type} context for Bible {bible_id}")
        return True
    
    def read_context(
        self,
        bible_id: str,
        context_type: str
    ) -> Optional[Dict]:
        """
        读取上下文
        
        Args:
            bible_id: Bible ID
            context_type: 上下文类型
            
        Returns:
            上下文数据
        """
        context_file = (self.bibles_path / bible_id / "context" / 
                       f"{context_type}_context.json")
        
        if not context_file.exists():
            return None
        
        with open(context_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def merge_contexts(
        self,
        bible_id: str,
        context_types: List[str] = None
    ) -> Dict:
        """
        合并多个上下文
        
        Args:
            bible_id: Bible ID
            context_types: 要合并的上下文类型列表
            
        Returns:
            合并后的上下文
        """
        if context_types is None:
            context_types = ['global', 'chapter', 'character', 'scene']
        
        merged = {}
        
        for ctx_type in context_types:
            context = self.read_context(bible_id, ctx_type)
            if context:
                # 移除内部时间戳
                context.pop('_updated_at', None)
                merged[ctx_type] = context
        
        return merged
    
    def clear_context(self, bible_id: str, context_type: str = None) -> bool:
        """
        清除上下文
        
        Args:
            bible_id: Bible ID
            context_type: 上下文类型，None表示清除所有
            
        Returns:
            是否成功
        """
        context_dir = self.bibles_path / bible_id / "context"
        
        if not context_dir.exists():
            return False
        
        if context_type:
            # 清除特定类型
            context_file = context_dir / f"{context_type}_context.json"
            if context_file.exists():
                context_file.unlink()
                print(f"Cleared {context_type} context")
        else:
            # 清除所有上下文
            for context_file in context_dir.glob("*_context.json"):
                context_file.unlink()
            print(f"Cleared all contexts for Bible {bible_id}")
        
        return True
    
    def create_snapshot(self, bible_id: str) -> str:
        """
        创建上下文快照
        
        Args:
            bible_id: Bible ID
            
        Returns:
            快照ID
        """
        snapshot_dir = self.bibles_path / bible_id / "context" / "snapshots"
        snapshot_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"snapshot_{timestamp}"
        snapshot_path = snapshot_dir / f"{snapshot_id}.json"
        
        # 收集所有当前上下文
        all_contexts = self.merge_contexts(bible_id)
        
        # 保存快照
        snapshot_data = {
            'id': snapshot_id,
            'created_at': datetime.now().isoformat(),
            'contexts': all_contexts
        }
        
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
        
        print(f"Created context snapshot: {snapshot_id}")
        return snapshot_id
    
    def restore_snapshot(self, bible_id: str, snapshot_id: str) -> bool:
        """
        恢复上下文快照
        
        Args:
            bible_id: Bible ID
            snapshot_id: 快照ID
            
        Returns:
            是否成功
        """
        snapshot_path = (self.bibles_path / bible_id / "context" / 
                        "snapshots" / f"{snapshot_id}.json")
        
        if not snapshot_path.exists():
            print(f"Snapshot {snapshot_id} not found")
            return False
        
        # 读取快照
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            snapshot_data = json.load(f)
        
        # 恢复各个上下文
        for ctx_type, ctx_data in snapshot_data['contexts'].items():
            self.save_context(bible_id, ctx_type, ctx_data)
        
        print(f"Restored snapshot: {snapshot_id}")
        return True


class DataManager:
    """数据管理器 - 统一接口"""
    
    def __init__(self, base_path: str = "D:\\NOVELSYS-SWARM\\data"):
        """
        初始化数据管理器
        
        Args:
            base_path: 数据存储根目录
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 初始化各个存储管理器
        self.bible_storage = BibleStorage(str(base_path))
        self.chapter_storage = ChapterStorage(str(base_path))
        self.context_storage = ContextStorage(str(base_path))
        
        # 当前活动的Bible
        self.current_bible_id = None
        
    def initialize_project(self, project_data: Dict) -> str:
        """
        初始化项目
        
        Args:
            project_data: 项目数据
            
        Returns:
            Bible ID
        """
        # 创建Bible
        bible_id = self.bible_storage.create_bible(project_data)
        
        # 设置为当前Bible
        self.current_bible_id = bible_id
        
        # 初始化全局上下文
        initial_context = {
            'project_name': project_data.get('title'),
            'genre': project_data.get('genre'),
            'created_at': datetime.now().isoformat()
        }
        self.context_storage.save_context(bible_id, 'global', initial_context)
        
        return bible_id
    
    def save_chapter_with_context(
        self,
        chapter_number: int,
        chapter_data: Dict,
        context_updates: Dict = None
    ) -> bool:
        """
        保存章节并更新上下文
        
        Args:
            chapter_number: 章节号
            chapter_data: 章节数据
            context_updates: 上下文更新
            
        Returns:
            是否成功
        """
        if not self.current_bible_id:
            print("No active Bible")
            return False
        
        # 保存章节
        success = self.chapter_storage.save_chapter(
            self.current_bible_id,
            chapter_number,
            chapter_data
        )
        
        if success and context_updates:
            # 更新章节上下文
            chapter_context = {
                'last_chapter': chapter_number,
                'last_updated': datetime.now().isoformat(),
                **context_updates
            }
            self.context_storage.save_context(
                self.current_bible_id,
                'chapter',
                chapter_context
            )
        
        return success
    
    def get_project_status(self) -> Dict:
        """
        获取项目状态
        
        Returns:
            项目状态信息
        """
        if not self.current_bible_id:
            return {'status': 'No active project'}
        
        # 获取Bible信息
        bible = self.bible_storage.read_bible(self.current_bible_id)
        
        # 获取章节列表
        chapters = self.chapter_storage.list_chapters(self.current_bible_id)
        
        # 获取上下文
        contexts = self.context_storage.merge_contexts(self.current_bible_id)
        
        return {
            'bible_id': self.current_bible_id,
            'title': bible.get('title') if bible else 'Unknown',
            'chapters_count': len(chapters),
            'total_words': sum(ch.get('word_count', 0) for ch in chapters),
            'average_quality': (
                sum(ch.get('quality_score', 0) for ch in chapters) / len(chapters)
                if chapters else 0
            ),
            'last_chapter': chapters[-1] if chapters else None,
            'context_types': list(contexts.keys())
        }
    
    def export_project(self, output_path: str = None) -> str:
        """
        导出项目
        
        Args:
            output_path: 输出路径
            
        Returns:
            导出文件路径
        """
        if not self.current_bible_id:
            print("No active Bible")
            return None
        
        if not output_path:
            output_path = f"D:\\NOVELSYS-SWARM\\exports\\{self.current_bible_id}.zip"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建压缩包
        bible_dir = self.bibles_path / self.current_bible_id
        shutil.make_archive(
            str(output_path.with_suffix('')),
            'zip',
            str(bible_dir)
        )
        
        print(f"Exported project to {output_path}")
        return str(output_path)


# 导出主要类
__all__ = [
    'DataManager',
    'BibleStorage',
    'ChapterStorage', 
    'ContextStorage',
    'BibleMetadata',
    'ChapterMetadata'
]