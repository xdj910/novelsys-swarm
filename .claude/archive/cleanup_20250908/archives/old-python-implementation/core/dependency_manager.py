"""
Dependency Management System
章节依赖管理系统
处理伏笔依赖、情节依赖、角色发展依赖等
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import networkx as nx
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DependencyType(Enum):
    """依赖类型"""
    FORESHADOWING = "foreshadowing"      # 伏笔依赖
    PLOT = "plot"                        # 情节依赖
    CHARACTER = "character"              # 角色发展依赖
    WORLD = "world"                      # 世界设定依赖
    TEMPORAL = "temporal"                # 时间顺序依赖
    THEMATIC = "thematic"                # 主题依赖
    EMOTIONAL = "emotional"              # 情感弧线依赖


@dataclass
class Dependency:
    """依赖关系定义"""
    id: str
    type: DependencyType
    source: str                         # 依赖源（章节/场景ID）
    target: str                         # 依赖目标
    description: str
    strength: int = 5                   # 依赖强度 1-10
    is_hard: bool = True                # 硬依赖还是软依赖
    created_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution_note: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class Foreshadowing:
    """伏笔管理"""
    id: str
    name: str
    description: str
    setup_chapter: int                  # 铺设章节
    setup_scene: Optional[str] = None   # 铺设场景
    payoff_chapter: Optional[int] = None # 回收章节
    payoff_scene: Optional[str] = None  # 回收场景
    importance: int = 5                 # 重要性 1-10
    status: str = "setup"               # setup, active, resolved, abandoned
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    notes: List[str] = field(default_factory=list)


class DependencyManager:
    """
    依赖管理器
    管理章节间的各种依赖关系
    """
    
    def __init__(self, project_dir: str = "data/dependencies"):
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # 依赖图
        self.dependency_graph = nx.DiGraph()
        
        # 数据存储
        self.dependencies: Dict[str, Dependency] = {}
        self.foreshadowings: Dict[str, Foreshadowing] = {}
        self.chapter_dependencies: Dict[int, List[str]] = {}
        
        # 加载已有数据
        self._load_dependencies()
    
    def _load_dependencies(self):
        """加载已有的依赖数据"""
        # 加载依赖关系
        deps_file = self.project_dir / "dependencies.json"
        if deps_file.exists():
            try:
                with open(deps_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for dep_data in data.get("dependencies", []):
                        dep = Dependency(
                            id=dep_data["id"],
                            type=DependencyType(dep_data["type"]),
                            source=dep_data["source"],
                            target=dep_data["target"],
                            description=dep_data["description"],
                            strength=dep_data.get("strength", 5),
                            is_hard=dep_data.get("is_hard", True),
                            resolved=dep_data.get("resolved", False)
                        )
                        self.dependencies[dep.id] = dep
                        self.dependency_graph.add_edge(
                            dep.source, dep.target,
                            dependency=dep
                        )
            except Exception as e:
                logger.error(f"加载依赖失败: {e}")
        
        # 加载伏笔
        foreshadowings_file = self.project_dir / "foreshadowings.json"
        if foreshadowings_file.exists():
            try:
                with open(foreshadowings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for fs_data in data.get("foreshadowings", []):
                        fs = Foreshadowing(
                            id=fs_data["id"],
                            name=fs_data["name"],
                            description=fs_data["description"],
                            setup_chapter=fs_data["setup_chapter"],
                            payoff_chapter=fs_data.get("payoff_chapter"),
                            importance=fs_data.get("importance", 5),
                            status=fs_data.get("status", "setup")
                        )
                        self.foreshadowings[fs.id] = fs
            except Exception as e:
                logger.error(f"加载伏笔失败: {e}")
    
    # ============ 依赖创建 ============
    
    def add_dependency(self, source: str, target: str, 
                      dep_type: DependencyType,
                      description: str,
                      strength: int = 5,
                      is_hard: bool = True) -> str:
        """
        添加依赖关系
        """
        dep_id = f"dep_{source}_{target}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        dependency = Dependency(
            id=dep_id,
            type=dep_type,
            source=source,
            target=target,
            description=description,
            strength=strength,
            is_hard=is_hard
        )
        
        # 检查是否会造成循环依赖
        if self._would_create_cycle(source, target):
            raise ValueError(f"添加依赖会造成循环: {source} -> {target}")
        
        # 添加到图
        self.dependency_graph.add_edge(source, target, dependency=dependency)
        self.dependencies[dep_id] = dependency
        
        # 更新章节依赖列表
        if target.startswith("chapter_"):
            chapter_num = int(target.split("_")[1])
            if chapter_num not in self.chapter_dependencies:
                self.chapter_dependencies[chapter_num] = []
            self.chapter_dependencies[chapter_num].append(dep_id)
        
        logger.info(f"添加依赖: {source} -> {target} ({dep_type.value})")
        self._save_dependencies()
        
        return dep_id
    
    def add_foreshadowing(self, name: str, description: str,
                         setup_chapter: int,
                         payoff_chapter: Optional[int] = None,
                         importance: int = 5) -> str:
        """
        添加伏笔
        """
        fs_id = f"fs_{setup_chapter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        foreshadowing = Foreshadowing(
            id=fs_id,
            name=name,
            description=description,
            setup_chapter=setup_chapter,
            payoff_chapter=payoff_chapter,
            importance=importance
        )
        
        self.foreshadowings[fs_id] = foreshadowing
        
        # 如果有回收章节，创建依赖
        if payoff_chapter:
            self.add_dependency(
                source=f"chapter_{setup_chapter}",
                target=f"chapter_{payoff_chapter}",
                dep_type=DependencyType.FORESHADOWING,
                description=f"伏笔'{name}'的铺设与回收",
                strength=importance,
                is_hard=True
            )
        
        logger.info(f"添加伏笔: {name} (第{setup_chapter}章铺设)")
        self._save_foreshadowings()
        
        return fs_id
    
    # ============ 依赖查询 ============
    
    def get_chapter_dependencies(self, chapter_num: int) -> List[Dependency]:
        """
        获取章节的所有依赖
        """
        chapter_id = f"chapter_{chapter_num}"
        dependencies = []
        
        # 获取所有指向该章节的依赖
        if chapter_id in self.dependency_graph:
            for source in self.dependency_graph.predecessors(chapter_id):
                edge_data = self.dependency_graph[source][chapter_id]
                if "dependency" in edge_data:
                    dependencies.append(edge_data["dependency"])
        
        return dependencies
    
    def get_chapter_dependents(self, chapter_num: int) -> List[Dependency]:
        """
        获取依赖于该章节的所有章节
        """
        chapter_id = f"chapter_{chapter_num}"
        dependents = []
        
        # 获取该章节指向的所有依赖
        if chapter_id in self.dependency_graph:
            for target in self.dependency_graph.successors(chapter_id):
                edge_data = self.dependency_graph[chapter_id][target]
                if "dependency" in edge_data:
                    dependents.append(edge_data["dependency"])
        
        return dependents
    
    def get_unresolved_foreshadowings(self) -> List[Foreshadowing]:
        """
        获取未回收的伏笔
        """
        return [
            fs for fs in self.foreshadowings.values()
            if fs.status in ["setup", "active"]
        ]
    
    def get_chapter_foreshadowings(self, chapter_num: int) -> Dict[str, List[Foreshadowing]]:
        """
        获取章节相关的伏笔
        """
        result = {
            "setup": [],    # 本章铺设的伏笔
            "payoff": [],   # 本章回收的伏笔
            "active": []    # 本章需要维持的伏笔
        }
        
        for fs in self.foreshadowings.values():
            if fs.setup_chapter == chapter_num:
                result["setup"].append(fs)
            elif fs.payoff_chapter == chapter_num:
                result["payoff"].append(fs)
            elif (fs.setup_chapter < chapter_num and 
                  (fs.payoff_chapter is None or fs.payoff_chapter > chapter_num)):
                result["active"].append(fs)
        
        return result
    
    # ============ 依赖验证 ============
    
    def validate_chapter_ready(self, chapter_num: int) -> Tuple[bool, List[str]]:
        """
        验证章节是否准备好生成
        检查所有硬依赖是否满足
        """
        dependencies = self.get_chapter_dependencies(chapter_num)
        unmet_dependencies = []
        
        for dep in dependencies:
            if dep.is_hard and not dep.resolved:
                unmet_dependencies.append(
                    f"{dep.type.value}: {dep.description}"
                )
        
        is_ready = len(unmet_dependencies) == 0
        return is_ready, unmet_dependencies
    
    def _would_create_cycle(self, source: str, target: str) -> bool:
        """
        检查添加边是否会创建循环
        """
        if target == source:
            return True
        
        # 临时添加边
        temp_graph = self.dependency_graph.copy()
        temp_graph.add_edge(source, target)
        
        # 检查是否有循环
        try:
            cycles = list(nx.simple_cycles(temp_graph))
            return len(cycles) > 0
        except:
            return False
    
    def get_execution_order(self, chapters: List[int]) -> List[int]:
        """
        根据依赖关系获取章节执行顺序
        使用拓扑排序
        """
        # 创建子图只包含指定章节
        subgraph = nx.DiGraph()
        
        for chapter in chapters:
            chapter_id = f"chapter_{chapter}"
            subgraph.add_node(chapter_id)
        
        # 添加相关的边
        for chapter in chapters:
            chapter_id = f"chapter_{chapter}"
            deps = self.get_chapter_dependencies(chapter)
            
            for dep in deps:
                if dep.source in subgraph and dep.target in subgraph:
                    subgraph.add_edge(dep.source, dep.target)
        
        # 拓扑排序
        try:
            sorted_nodes = list(nx.topological_sort(subgraph))
            # 转换回章节号
            sorted_chapters = []
            for node in sorted_nodes:
                if node.startswith("chapter_"):
                    chapter_num = int(node.split("_")[1])
                    if chapter_num in chapters:
                        sorted_chapters.append(chapter_num)
            
            # 添加未在图中的章节（没有依赖关系的）
            for chapter in chapters:
                if chapter not in sorted_chapters:
                    sorted_chapters.append(chapter)
            
            return sorted_chapters
        except nx.NetworkXError as e:
            logger.error(f"无法排序，存在循环依赖: {e}")
            return chapters  # 返回原始顺序
    
    # ============ 依赖解决 ============
    
    def resolve_dependency(self, dep_id: str, note: str = ""):
        """
        标记依赖为已解决
        """
        if dep_id not in self.dependencies:
            logger.warning(f"依赖不存在: {dep_id}")
            return
        
        dependency = self.dependencies[dep_id]
        dependency.resolved = True
        dependency.resolution_note = note
        
        logger.info(f"依赖已解决: {dep_id}")
        self._save_dependencies()
    
    def resolve_foreshadowing(self, fs_id: str, payoff_chapter: int,
                            note: str = ""):
        """
        标记伏笔为已回收
        """
        if fs_id not in self.foreshadowings:
            logger.warning(f"伏笔不存在: {fs_id}")
            return
        
        foreshadowing = self.foreshadowings[fs_id]
        foreshadowing.status = "resolved"
        foreshadowing.payoff_chapter = payoff_chapter
        foreshadowing.resolved_at = datetime.now()
        foreshadowing.notes.append(note)
        
        logger.info(f"伏笔已回收: {foreshadowing.name} (第{payoff_chapter}章)")
        self._save_foreshadowings()
    
    # ============ 可视化 ============
    
    def generate_dependency_report(self) -> str:
        """
        生成依赖关系报告
        """
        report = []
        report.append("# 📊 依赖关系报告")
        report.append("")
        
        # 统计信息
        total_deps = len(self.dependencies)
        resolved_deps = len([d for d in self.dependencies.values() if d.resolved])
        total_fs = len(self.foreshadowings)
        resolved_fs = len([f for f in self.foreshadowings.values() 
                         if f.status == "resolved"])
        
        report.append("## 📈 统计概览")
        report.append(f"- 总依赖数: {total_deps}")
        report.append(f"- 已解决: {resolved_deps}/{total_deps}")
        report.append(f"- 伏笔总数: {total_fs}")
        report.append(f"- 已回收: {resolved_fs}/{total_fs}")
        report.append("")
        
        # 按类型统计依赖
        report.append("## 🔗 依赖类型分布")
        type_counts = {}
        for dep in self.dependencies.values():
            type_name = dep.type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        for dep_type, count in sorted(type_counts.items()):
            report.append(f"- {dep_type}: {count}个")
        report.append("")
        
        # 未解决的依赖
        unresolved = [d for d in self.dependencies.values() if not d.resolved]
        if unresolved:
            report.append("## ⚠️ 未解决的依赖")
            for dep in unresolved[:10]:  # 最多显示10个
                report.append(f"- {dep.source} → {dep.target}")
                report.append(f"  类型: {dep.type.value}")
                report.append(f"  描述: {dep.description}")
                report.append("")
        
        # 未回收的伏笔
        unresolved_fs = self.get_unresolved_foreshadowings()
        if unresolved_fs:
            report.append("## 📌 未回收的伏笔")
            for fs in unresolved_fs[:10]:  # 最多显示10个
                report.append(f"- {fs.name}")
                report.append(f"  铺设: 第{fs.setup_chapter}章")
                report.append(f"  重要性: {fs.importance}/10")
                report.append(f"  描述: {fs.description}")
                report.append("")
        
        # 章节依赖复杂度
        report.append("## 🔀 章节依赖复杂度")
        chapter_complexity = []
        for i in range(1, 21):  # 假设最多20章
            deps_in = len(self.get_chapter_dependencies(i))
            deps_out = len(self.get_chapter_dependents(i))
            if deps_in > 0 or deps_out > 0:
                chapter_complexity.append((i, deps_in + deps_out))
        
        chapter_complexity.sort(key=lambda x: x[1], reverse=True)
        for chapter_num, complexity in chapter_complexity[:5]:
            report.append(f"- 第{chapter_num}章: 复杂度{complexity}")
        
        return "\n".join(report)
    
    def visualize_dependency_graph(self) -> str:
        """
        生成依赖图的文本可视化
        """
        viz = []
        viz.append("```mermaid")
        viz.append("graph TD")
        
        # 添加节点
        for node in self.dependency_graph.nodes():
            if node.startswith("chapter_"):
                chapter_num = node.split("_")[1]
                viz.append(f"    {node}[第{chapter_num}章]")
        
        # 添加边
        for source, target in self.dependency_graph.edges():
            edge_data = self.dependency_graph[source][target]
            if "dependency" in edge_data:
                dep = edge_data["dependency"]
                label = dep.type.value[:4]  # 缩短标签
                if dep.resolved:
                    viz.append(f"    {source} -->|{label}| {target}")
                else:
                    viz.append(f"    {source} -.->|{label}| {target}")
        
        viz.append("```")
        return "\n".join(viz)
    
    # ============ 持久化 ============
    
    def _save_dependencies(self):
        """保存依赖关系"""
        deps_data = {
            "dependencies": [
                {
                    "id": dep.id,
                    "type": dep.type.value,
                    "source": dep.source,
                    "target": dep.target,
                    "description": dep.description,
                    "strength": dep.strength,
                    "is_hard": dep.is_hard,
                    "resolved": dep.resolved,
                    "resolution_note": dep.resolution_note,
                    "created_at": dep.created_at.isoformat()
                }
                for dep in self.dependencies.values()
            ]
        }
        
        deps_file = self.project_dir / "dependencies.json"
        with open(deps_file, 'w', encoding='utf-8') as f:
            json.dump(deps_data, f, ensure_ascii=False, indent=2)
    
    def _save_foreshadowings(self):
        """保存伏笔"""
        fs_data = {
            "foreshadowings": [
                {
                    "id": fs.id,
                    "name": fs.name,
                    "description": fs.description,
                    "setup_chapter": fs.setup_chapter,
                    "payoff_chapter": fs.payoff_chapter,
                    "importance": fs.importance,
                    "status": fs.status,
                    "created_at": fs.created_at.isoformat(),
                    "notes": fs.notes
                }
                for fs in self.foreshadowings.values()
            ]
        }
        
        fs_file = self.project_dir / "foreshadowings.json"
        with open(fs_file, 'w', encoding='utf-8') as f:
            json.dump(fs_data, f, ensure_ascii=False, indent=2)


# 使用示例
if __name__ == "__main__":
    # 创建依赖管理器
    dep_manager = DependencyManager()
    
    # 添加伏笔
    fs1 = dep_manager.add_foreshadowing(
        name="神秘徽章",
        description="主角发现一个神秘的徽章，不知其含义",
        setup_chapter=1,
        payoff_chapter=5,
        importance=8
    )
    
    fs2 = dep_manager.add_foreshadowing(
        name="梦境预言",
        description="主角做了一个奇怪的梦",
        setup_chapter=2,
        payoff_chapter=8,
        importance=6
    )
    
    # 添加情节依赖
    dep_manager.add_dependency(
        source="chapter_1",
        target="chapter_3",
        dep_type=DependencyType.PLOT,
        description="第1章的事件直接导致第3章的冲突",
        strength=9,
        is_hard=True
    )
    
    # 添加角色依赖
    dep_manager.add_dependency(
        source="chapter_2",
        target="chapter_4",
        dep_type=DependencyType.CHARACTER,
        description="配角A在第2章出现，第4章成为关键",
        strength=7,
        is_hard=False
    )
    
    # 检查章节是否准备好
    ready, unmet = dep_manager.validate_chapter_ready(3)
    print(f"第3章准备状态: {ready}")
    if not ready:
        print(f"未满足的依赖: {unmet}")
    
    # 获取执行顺序
    chapters = [1, 2, 3, 4, 5]
    order = dep_manager.get_execution_order(chapters)
    print(f"建议执行顺序: {order}")
    
    # 生成报告
    report = dep_manager.generate_dependency_report()
    print("\n" + report)
    
    # 可视化依赖图
    viz = dep_manager.visualize_dependency_graph()
    print("\n" + viz)