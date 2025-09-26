"""
Incremental Sync Mechanism
增量同步机制
只同步变化的部分，提高效率
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import difflib
import logging

logger = logging.getLogger(__name__)


@dataclass
class SyncRecord:
    """同步记录"""
    sync_id: str
    source_path: str
    target: str  # GitHub Issue ID或其他目标
    timestamp: datetime
    content_hash: str
    changes: Dict[str, Any]
    sync_type: str  # full, incremental, patch
    success: bool
    error_message: Optional[str] = None
    metrics: Dict[str, int] = field(default_factory=dict)


@dataclass 
class ContentVersion:
    """内容版本"""
    version: int
    content_hash: str
    timestamp: datetime
    size: int
    changes_from_previous: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class IncrementalSyncManager:
    """
    增量同步管理器
    实现高效的内容同步
    """
    
    def __init__(self, cache_dir: str = "data/sync_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 同步历史
        self.sync_history: List[SyncRecord] = []
        self.content_cache: Dict[str, str] = {}  # 路径 -> 内容哈希
        self.version_history: Dict[str, List[ContentVersion]] = {}  # 路径 -> 版本历史
        
        # 同步标记
        self.sync_markers: Dict[str, datetime] = {}  # 路径 -> 最后同步时间
        
        # 加载缓存
        self._load_cache()
    
    def _load_cache(self):
        """加载同步缓存"""
        # 加载同步标记
        markers_file = self.cache_dir / "sync_markers.json"
        if markers_file.exists():
            try:
                with open(markers_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sync_markers = {
                        k: datetime.fromisoformat(v)
                        for k, v in data.items()
                    }
            except Exception as e:
                logger.error(f"加载同步标记失败: {e}")
        
        # 加载内容缓存
        cache_file = self.cache_dir / "content_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.content_cache = json.load(f)
            except Exception as e:
                logger.error(f"加载内容缓存失败: {e}")
    
    def _compute_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _get_content(self, file_path: Path) -> Optional[str]:
        """获取文件内容"""
        if not file_path.exists():
            return None
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.dumps(json.load(f), ensure_ascii=False, sort_keys=True)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"读取文件失败 {file_path}: {e}")
            return None
    
    # ============ 变化检测 ============
    
    def detect_changes(self, file_path: Path) -> Tuple[bool, Optional[Dict]]:
        """
        检测文件是否有变化
        返回: (是否有变化, 变化详情)
        """
        str_path = str(file_path)
        current_content = self._get_content(file_path)
        
        if current_content is None:
            return False, None
        
        current_hash = self._compute_hash(current_content)
        
        # 检查缓存
        if str_path in self.content_cache:
            cached_hash = self.content_cache[str_path]
            if cached_hash == current_hash:
                return False, None  # 无变化
            
            # 计算差异
            changes = self._calculate_diff(str_path, current_content)
            
            # 更新缓存
            self.content_cache[str_path] = current_hash
            
            return True, changes
        else:
            # 新文件
            self.content_cache[str_path] = current_hash
            return True, {"type": "new", "size": len(current_content)}
    
    def _calculate_diff(self, file_path: str, new_content: str) -> Dict:
        """
        计算内容差异
        """
        # 获取旧内容（简化版，实际应该从版本历史获取）
        old_content = self._get_cached_content(file_path)
        
        if not old_content:
            return {"type": "new", "size": len(new_content)}
        
        # 计算差异
        differ = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            lineterm=''
        )
        
        diff_lines = list(differ)
        
        # 统计变化
        added_lines = sum(1 for line in diff_lines if line.startswith('+') and not line.startswith('+++'))
        removed_lines = sum(1 for line in diff_lines if line.startswith('-') and not line.startswith('---'))
        
        return {
            "type": "modified",
            "added_lines": added_lines,
            "removed_lines": removed_lines,
            "total_changes": added_lines + removed_lines,
            "diff_size": len(''.join(diff_lines))
        }
    
    def _get_cached_content(self, file_path: str) -> Optional[str]:
        """获取缓存的内容"""
        cache_file = self.cache_dir / f"{hashlib.md5(file_path.encode()).hexdigest()}.cache"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                pass
        return None
    
    # ============ 增量同步 ============
    
    def sync_incremental(self, source_path: Path, target: str,
                        force: bool = False) -> Tuple[bool, SyncRecord]:
        """
        执行增量同步
        """
        str_path = str(source_path)
        
        # 检查是否需要同步
        if not force:
            last_sync = self.sync_markers.get(str_path)
            if last_sync:
                # 如果最近同步过（比如5分钟内），跳过
                if datetime.now() - last_sync < timedelta(minutes=5):
                    logger.info(f"跳过同步 {str_path} (最近已同步)")
                    return False, None
        
        # 检测变化
        has_changes, changes = self.detect_changes(source_path)
        
        if not has_changes and not force:
            logger.info(f"无变化，跳过同步 {str_path}")
            return False, None
        
        # 准备同步内容
        content = self._get_content(source_path)
        if not content:
            return False, None
        
        # 决定同步类型
        sync_type = self._determine_sync_type(changes)
        
        # 执行同步
        start_time = time.time()
        
        if sync_type == "incremental":
            sync_content = self._prepare_incremental_content(str_path, content, changes)
        elif sync_type == "patch":
            sync_content = self._prepare_patch_content(str_path, content, changes)
        else:
            sync_content = content
        
        # 模拟同步到目标（实际应该调用GitHub API等）
        success = self._perform_sync(target, sync_content, sync_type)
        
        sync_time = time.time() - start_time
        
        # 创建同步记录
        sync_record = SyncRecord(
            sync_id=f"sync_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            source_path=str_path,
            target=target,
            timestamp=datetime.now(),
            content_hash=self._compute_hash(content),
            changes=changes or {},
            sync_type=sync_type,
            success=success,
            metrics={
                "sync_time_ms": int(sync_time * 1000),
                "content_size": len(content),
                "sync_size": len(sync_content)
            }
        )
        
        # 更新记录
        if success:
            self.sync_markers[str_path] = datetime.now()
            self._cache_content(str_path, content)
            self._add_version(str_path, content, changes)
        
        self.sync_history.append(sync_record)
        self._save_cache()
        
        logger.info(f"同步完成: {str_path} -> {target} ({sync_type})")
        return success, sync_record
    
    def _determine_sync_type(self, changes: Optional[Dict]) -> str:
        """
        决定同步类型
        """
        if not changes:
            return "full"
        
        if changes.get("type") == "new":
            return "full"
        
        total_changes = changes.get("total_changes", 0)
        
        if total_changes < 10:
            return "patch"  # 小改动用补丁
        elif total_changes < 100:
            return "incremental"  # 中等改动用增量
        else:
            return "full"  # 大改动全量同步
    
    def _prepare_incremental_content(self, file_path: str, 
                                    content: str, changes: Dict) -> str:
        """
        准备增量同步内容
        只包含变化的部分
        """
        # 这里简化处理，实际应该只发送变化的部分
        incremental = {
            "type": "incremental",
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "changes": changes,
            "content_hash": self._compute_hash(content),
            "partial_content": content[:1000] if len(content) > 1000 else content
        }
        
        return json.dumps(incremental, ensure_ascii=False)
    
    def _prepare_patch_content(self, file_path: str,
                             content: str, changes: Dict) -> str:
        """
        准备补丁内容
        使用diff格式
        """
        old_content = self._get_cached_content(file_path) or ""
        
        # 生成补丁
        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            content.splitlines(keepends=True),
            fromfile=f"{file_path}.old",
            tofile=file_path,
            lineterm=''
        )
        
        patch = {
            "type": "patch",
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "patch": ''.join(diff)
        }
        
        return json.dumps(patch, ensure_ascii=False)
    
    def _perform_sync(self, target: str, content: str, sync_type: str) -> bool:
        """
        执行实际的同步操作
        """
        # 这里应该调用实际的同步API（如GitHub API）
        # 现在只是模拟
        logger.info(f"同步到 {target}: {sync_type} ({len(content)} bytes)")
        return True
    
    def _cache_content(self, file_path: str, content: str):
        """缓存内容"""
        cache_file = self.cache_dir / f"{hashlib.md5(file_path.encode()).hexdigest()}.cache"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"缓存内容失败: {e}")
    
    def _add_version(self, file_path: str, content: str, changes: Optional[Dict]):
        """添加版本记录"""
        if file_path not in self.version_history:
            self.version_history[file_path] = []
        
        versions = self.version_history[file_path]
        version_num = len(versions) + 1
        
        version = ContentVersion(
            version=version_num,
            content_hash=self._compute_hash(content),
            timestamp=datetime.now(),
            size=len(content),
            changes_from_previous=json.dumps(changes) if changes else None
        )
        
        versions.append(version)
        
        # 只保留最近10个版本
        if len(versions) > 10:
            versions.pop(0)
    
    # ============ 批量同步 ============
    
    def sync_directory(self, directory: Path, target_prefix: str,
                      pattern: str = "*.md") -> List[SyncRecord]:
        """
        同步整个目录
        """
        results = []
        
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                target = f"{target_prefix}/{file_path.name}"
                success, record = self.sync_incremental(file_path, target)
                if record:
                    results.append(record)
        
        logger.info(f"批量同步完成: {len(results)}个文件")
        return results
    
    def get_pending_syncs(self, directory: Path, 
                         pattern: str = "*.md") -> List[Path]:
        """
        获取待同步的文件
        """
        pending = []
        
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                has_changes, _ = self.detect_changes(file_path)
                if has_changes:
                    pending.append(file_path)
        
        return pending
    
    # ============ 同步优化 ============
    
    def optimize_sync_batch(self, files: List[Path]) -> List[List[Path]]:
        """
        优化同步批次
        将文件分组以提高效率
        """
        # 按文件大小分组
        small_files = []  # < 1KB
        medium_files = []  # 1KB - 100KB
        large_files = []   # > 100KB
        
        for file_path in files:
            if file_path.exists():
                size = file_path.stat().st_size
                if size < 1024:
                    small_files.append(file_path)
                elif size < 102400:
                    medium_files.append(file_path)
                else:
                    large_files.append(file_path)
        
        batches = []
        
        # 小文件可以批量同步
        if small_files:
            # 每批最多20个小文件
            for i in range(0, len(small_files), 20):
                batches.append(small_files[i:i+20])
        
        # 中等文件适度批量
        if medium_files:
            # 每批最多5个中等文件
            for i in range(0, len(medium_files), 5):
                batches.append(medium_files[i:i+5])
        
        # 大文件单独同步
        for large_file in large_files:
            batches.append([large_file])
        
        return batches
    
    # ============ 报告生成 ============
    
    def generate_sync_report(self) -> str:
        """
        生成同步报告
        """
        report = []
        report.append("# 📊 增量同步报告")
        report.append("")
        
        # 统计信息
        total_syncs = len(self.sync_history)
        successful_syncs = sum(1 for s in self.sync_history if s.success)
        
        report.append("## 📈 同步统计")
        report.append(f"- 总同步次数: {total_syncs}")
        report.append(f"- 成功率: {successful_syncs}/{total_syncs}")
        
        if self.sync_history:
            # 同步类型分布
            type_counts = {}
            for record in self.sync_history:
                sync_type = record.sync_type
                type_counts[sync_type] = type_counts.get(sync_type, 0) + 1
            
            report.append("")
            report.append("## 🔄 同步类型分布")
            for sync_type, count in sorted(type_counts.items()):
                percentage = (count / total_syncs) * 100
                report.append(f"- {sync_type}: {count}次 ({percentage:.1f}%)")
            
            # 性能指标
            sync_times = [r.metrics.get("sync_time_ms", 0) for r in self.sync_history]
            if sync_times:
                avg_time = sum(sync_times) / len(sync_times)
                report.append("")
                report.append("## ⚡ 性能指标")
                report.append(f"- 平均同步时间: {avg_time:.0f}ms")
                report.append(f"- 最快: {min(sync_times)}ms")
                report.append(f"- 最慢: {max(sync_times)}ms")
            
            # 数据量统计
            total_synced = sum(r.metrics.get("sync_size", 0) for r in self.sync_history)
            total_original = sum(r.metrics.get("content_size", 0) for r in self.sync_history)
            
            if total_original > 0:
                compression = (1 - total_synced / total_original) * 100
                report.append("")
                report.append("## 💾 数据优化")
                report.append(f"- 原始数据: {total_original/1024:.1f}KB")
                report.append(f"- 同步数据: {total_synced/1024:.1f}KB")
                report.append(f"- 节省: {compression:.1f}%")
        
        # 最近同步
        if self.sync_history:
            report.append("")
            report.append("## 🕐 最近同步")
            for record in self.sync_history[-5:]:
                time_str = record.timestamp.strftime("%H:%M:%S")
                report.append(f"- {time_str}: {Path(record.source_path).name} ({record.sync_type})")
        
        # 待同步文件
        report.append("")
        report.append("## ⏳ 待同步状态")
        report.append(f"- 缓存文件数: {len(self.content_cache)}")
        report.append(f"- 监控路径数: {len(self.sync_markers)}")
        
        return "\n".join(report)
    
    def _save_cache(self):
        """保存缓存"""
        # 保存同步标记
        markers_data = {
            k: v.isoformat()
            for k, v in self.sync_markers.items()
        }
        
        markers_file = self.cache_dir / "sync_markers.json"
        with open(markers_file, 'w', encoding='utf-8') as f:
            json.dump(markers_data, f, ensure_ascii=False, indent=2)
        
        # 保存内容缓存
        cache_file = self.cache_dir / "content_cache.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.content_cache, f, ensure_ascii=False, indent=2)


# 使用示例
if __name__ == "__main__":
    # 创建同步管理器
    sync_manager = IncrementalSyncManager()
    
    # 模拟文件路径
    test_dir = Path("data/chapters")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建测试文件
    test_file = test_dir / "chapter1.md"
    test_file.write_text("# 第一章\n\n这是第一章的内容...")
    
    # 第一次同步（全量）
    success, record = sync_manager.sync_incremental(
        test_file,
        "github://issue/1"
    )
    print(f"第一次同步: {record.sync_type if record else 'skipped'}")
    
    # 修改文件
    test_file.write_text("# 第一章\n\n这是第一章的内容...\n\n新增了一段内容。")
    
    # 第二次同步（增量）
    success, record = sync_manager.sync_incremental(
        test_file,
        "github://issue/1"
    )
    print(f"第二次同步: {record.sync_type if record else 'skipped'}")
    
    # 批量同步
    for i in range(2, 5):
        chapter_file = test_dir / f"chapter{i}.md"
        chapter_file.write_text(f"# 第{i}章\n\n内容...")
    
    records = sync_manager.sync_directory(test_dir, "github://issues")
    print(f"批量同步: {len(records)}个文件")
    
    # 生成报告
    report = sync_manager.generate_sync_report()
    print("\n" + report)