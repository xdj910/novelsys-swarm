"""
Five-Stage Standardized Workflow
5阶段规范化创作流程
借鉴CCPM的PRD→Epic→Task→Issue→Code流程
适配为：概念→Bible→章节→场景→成稿
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class WorkflowStage(Enum):
    """工作流阶段"""
    CONCEPT = "concept"      # 概念构思（对应PRD）
    BIBLE = "bible"          # Bible规划（对应Epic）
    CHAPTER = "chapter"      # 章节分解（对应Task）
    SCENE = "scene"          # 场景生成（对应Issue）
    MANUSCRIPT = "manuscript" # 成稿润色（对应Code）


@dataclass
class StageDocument:
    """阶段文档"""
    stage: WorkflowStage
    title: str
    content: Dict
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"  # draft, review, approved, published
    quality_score: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class FiveStageWorkflow:
    """
    5阶段工作流管理器
    确保每个阶段规范执行，可追溯
    """
    
    def __init__(self, project_dir: str = "data/workflow"):
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # 各阶段目录
        self.stage_dirs = {
            WorkflowStage.CONCEPT: self.project_dir / "1_concepts",
            WorkflowStage.BIBLE: self.project_dir / "2_bibles",
            WorkflowStage.CHAPTER: self.project_dir / "3_chapters",
            WorkflowStage.SCENE: self.project_dir / "4_scenes",
            WorkflowStage.MANUSCRIPT: self.project_dir / "5_manuscripts"
        }
        
        # 创建目录
        for stage_dir in self.stage_dirs.values():
            stage_dir.mkdir(parents=True, exist_ok=True)
        
        # 当前工作流状态
        self.current_stage = None
        self.documents = {}
        
        # 加载已有文档
        self._load_documents()
    
    def _load_documents(self):
        """加载已有的工作流文档"""
        for stage, stage_dir in self.stage_dirs.items():
            for file_path in stage_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        doc_id = file_path.stem
                        self.documents[doc_id] = StageDocument(
                            stage=stage,
                            title=data.get('title', ''),
                            content=data.get('content', {}),
                            status=data.get('status', 'draft'),
                            quality_score=data.get('quality_score'),
                            dependencies=data.get('dependencies', []),
                            outputs=data.get('outputs', [])
                        )
                except Exception as e:
                    logger.error(f"加载文档失败 {file_path}: {e}")
    
    # ============ Stage 1: CONCEPT (概念构思) ============
    
    def create_concept(self, title: str, genre: str, 
                      themes: List[str], target_audience: str) -> str:
        """
        Stage 1: 创建概念文档（类似PRD）
        定义小说的核心概念和目标
        """
        logger.info(f"Stage 1: 创建概念文档 - {title}")
        
        concept = {
            "title": title,
            "genre": genre,
            "themes": themes,
            "target_audience": target_audience,
            "core_conflict": "",
            "unique_selling_points": [],
            "success_criteria": {
                "word_count": 100000,
                "quality_score": 98,
                "reader_engagement": "high",
                "completion_time": "3 months"
            },
            "constraints": {
                "content_rating": "PG-13",
                "cultural_sensitivity": True,
                "avoid_topics": []
            },
            "inspiration": {
                "similar_works": [],
                "references": [],
                "mood_board": []
            }
        }
        
        # 头脑风暴补充内容
        concept = self._brainstorm_concept(concept)
        
        # 创建文档
        doc_id = f"concept_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        document = StageDocument(
            stage=WorkflowStage.CONCEPT,
            title=title,
            content=concept,
            status="draft"
        )
        
        # 保存
        self._save_document(doc_id, document)
        self.documents[doc_id] = document
        
        logger.info(f"概念文档创建完成: {doc_id}")
        return doc_id
    
    def _brainstorm_concept(self, concept: Dict) -> Dict:
        """概念头脑风暴"""
        # 这里应该调用AI进行头脑风暴
        # 简化实现
        concept["core_conflict"] = "个人vs社会，理想vs现实"
        concept["unique_selling_points"] = [
            "独特的魔法系统",
            "复杂的人物关系",
            "意想不到的反转"
        ]
        return concept
    
    # ============ Stage 2: BIBLE (Bible规划) ============
    
    def create_bible(self, concept_id: str) -> str:
        """
        Stage 2: 基于概念创建Bible（类似Epic）
        定义完整的世界观、角色、情节
        """
        if concept_id not in self.documents:
            raise ValueError(f"概念文档不存在: {concept_id}")
        
        concept = self.documents[concept_id]
        logger.info(f"Stage 2: 创建Bible - 基于{concept.title}")
        
        bible = {
            "concept_id": concept_id,
            "world_setting": {
                "time_period": "",
                "location": "",
                "society": "",
                "technology_level": "",
                "magic_system": {}
            },
            "characters": {
                "protagonist": {},
                "antagonist": {},
                "supporting": []
            },
            "plot_structure": {
                "three_acts": {
                    "act1": {"chapters": [1, 2, 3], "purpose": "Setup"},
                    "act2": {"chapters": [4, 5, 6, 7, 8], "purpose": "Confrontation"},
                    "act3": {"chapters": [9, 10], "purpose": "Resolution"}
                },
                "key_events": [],
                "turning_points": []
            },
            "themes_exploration": {},
            "style_guide": {
                "narrative_voice": "third_person_limited",
                "tone": "serious_with_humor",
                "pacing": "moderate",
                "description_density": "balanced"
            }
        }
        
        # 基于概念扩展Bible
        bible = self._expand_bible(bible, concept.content)
        
        # 创建文档
        doc_id = f"bible_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        document = StageDocument(
            stage=WorkflowStage.BIBLE,
            title=f"Bible: {concept.title}",
            content=bible,
            status="draft",
            dependencies=[concept_id]
        )
        
        # 保存
        self._save_document(doc_id, document)
        self.documents[doc_id] = document
        
        # 更新概念文档的输出
        concept.outputs.append(doc_id)
        self._save_document(concept_id, concept)
        
        logger.info(f"Bible创建完成: {doc_id}")
        return doc_id
    
    def _expand_bible(self, bible: Dict, concept: Dict) -> Dict:
        """扩展Bible内容"""
        # 基于概念填充Bible
        bible["world_setting"]["time_period"] = "近未来2050年"
        bible["world_setting"]["location"] = "新东京"
        
        bible["characters"]["protagonist"] = {
            "name": "林凯",
            "age": 25,
            "occupation": "异能觉醒者",
            "motivation": "寻找真相",
            "arc": "从怀疑到接受到超越"
        }
        
        bible["themes_exploration"] = {
            theme: f"通过主角的成长探索{theme}"
            for theme in concept.get("themes", [])
        }
        
        return bible
    
    # ============ Stage 3: CHAPTER (章节分解) ============
    
    def create_chapters(self, bible_id: str) -> List[str]:
        """
        Stage 3: 基于Bible创建章节大纲（类似Task）
        分解为具体的章节任务
        """
        if bible_id not in self.documents:
            raise ValueError(f"Bible文档不存在: {bible_id}")
        
        bible = self.documents[bible_id]
        logger.info(f"Stage 3: 创建章节大纲 - 基于{bible.title}")
        
        chapter_ids = []
        plot_structure = bible.content.get("plot_structure", {})
        
        # 为每个章节创建大纲
        total_chapters = 10  # 从Bible中获取
        for chapter_num in range(1, total_chapters + 1):
            chapter = {
                "bible_id": bible_id,
                "chapter_num": chapter_num,
                "title": f"第{chapter_num}章",
                "purpose": self._get_chapter_purpose(chapter_num, plot_structure),
                "outline": {
                    "opening": "",
                    "development": "",
                    "climax": "",
                    "resolution": ""
                },
                "key_events": [],
                "character_focus": [],
                "word_count_target": 3000,
                "dependencies": [],  # 依赖的前置章节
                "foreshadowing": {
                    "setup": [],     # 本章铺设的伏笔
                    "payoff": []     # 本章回收的伏笔
                }
            }
            
            # 生成章节大纲
            chapter = self._generate_chapter_outline(chapter, bible.content)
            
            # 创建文档
            doc_id = f"chapter_{chapter_num:03d}_{datetime.now().strftime('%Y%m%d')}"
            document = StageDocument(
                stage=WorkflowStage.CHAPTER,
                title=chapter["title"],
                content=chapter,
                status="draft",
                dependencies=[bible_id]
            )
            
            # 设置章节依赖
            if chapter_num > 1:
                document.dependencies.append(chapter_ids[-1])  # 依赖前一章
            
            # 保存
            self._save_document(doc_id, document)
            self.documents[doc_id] = document
            chapter_ids.append(doc_id)
        
        # 更新Bible的输出
        bible.outputs.extend(chapter_ids)
        self._save_document(bible_id, bible)
        
        logger.info(f"创建了{len(chapter_ids)}个章节大纲")
        return chapter_ids
    
    def _get_chapter_purpose(self, chapter_num: int, plot_structure: Dict) -> str:
        """获取章节目的"""
        three_acts = plot_structure.get("three_acts", {})
        
        for act_name, act_info in three_acts.items():
            if chapter_num in act_info.get("chapters", []):
                return f"{act_name}: {act_info.get('purpose', '')}"
        
        return "Development"
    
    def _generate_chapter_outline(self, chapter: Dict, bible: Dict) -> Dict:
        """生成章节大纲"""
        chapter_num = chapter["chapter_num"]
        
        # 简化的大纲生成
        chapter["outline"]["opening"] = f"第{chapter_num}章开场，承接前文"
        chapter["outline"]["development"] = f"展开第{chapter_num}章的主要情节"
        chapter["outline"]["climax"] = f"第{chapter_num}章的高潮部分"
        chapter["outline"]["resolution"] = f"第{chapter_num}章的收尾，引出下文"
        
        chapter["key_events"] = [
            f"事件{chapter_num}.1: 触发事件",
            f"事件{chapter_num}.2: 发展冲突",
            f"事件{chapter_num}.3: 解决或悬念"
        ]
        
        return chapter
    
    # ============ Stage 4: SCENE (场景生成) ============
    
    def create_scenes(self, chapter_id: str) -> List[str]:
        """
        Stage 4: 基于章节创建场景（类似Issue）
        分解为可并行执行的场景
        """
        if chapter_id not in self.documents:
            raise ValueError(f"章节文档不存在: {chapter_id}")
        
        chapter = self.documents[chapter_id]
        logger.info(f"Stage 4: 创建场景 - {chapter.title}")
        
        scene_ids = []
        
        # 通常一章3-5个场景
        num_scenes = 3
        for scene_num in range(1, num_scenes + 1):
            scene = {
                "chapter_id": chapter_id,
                "scene_num": scene_num,
                "type": self._determine_scene_type(scene_num),
                "location": "",
                "time": "",
                "characters": [],
                "purpose": "",
                "content_requirements": {
                    "mood": "",
                    "tension_level": 5,
                    "pov_character": "",
                    "key_dialogue": [],
                    "key_actions": [],
                    "sensory_details": []
                },
                "word_count_target": 1000,
                "parallel_executable": True,  # 是否可并行生成
                "stream_allocation": []  # 分配给哪些Stream处理
            }
            
            # 生成场景详情
            scene = self._generate_scene_details(scene, chapter.content)
            
            # 创建文档
            doc_id = f"scene_{chapter.content['chapter_num']:03d}_{scene_num:02d}"
            document = StageDocument(
                stage=WorkflowStage.SCENE,
                title=f"场景{scene_num}",
                content=scene,
                status="draft",
                dependencies=[chapter_id]
            )
            
            # 保存
            self._save_document(doc_id, document)
            self.documents[doc_id] = document
            scene_ids.append(doc_id)
        
        # 更新章节的输出
        chapter.outputs.extend(scene_ids)
        self._save_document(chapter_id, chapter)
        
        logger.info(f"创建了{len(scene_ids)}个场景")
        return scene_ids
    
    def _determine_scene_type(self, scene_num: int) -> str:
        """确定场景类型"""
        types = ["opening", "development", "climax", "transition", "closing"]
        if scene_num == 1:
            return "opening"
        elif scene_num == 3:
            return "climax"
        else:
            return "development"
    
    def _generate_scene_details(self, scene: Dict, chapter: Dict) -> Dict:
        """生成场景详情"""
        scene["location"] = "城市街道"
        scene["time"] = "傍晚"
        scene["characters"] = ["主角", "配角A"]
        scene["purpose"] = f"推进章节{chapter['chapter_num']}的情节"
        
        scene["content_requirements"]["mood"] = "紧张而神秘"
        scene["content_requirements"]["pov_character"] = "主角"
        
        # 分配Stream
        scene["stream_allocation"] = [
            "Character Psychology",
            "Narrative Structure",
            "World Building",
            "Dialogue Master"
        ]
        
        return scene
    
    # ============ Stage 5: MANUSCRIPT (成稿润色) ============
    
    def create_manuscript(self, scene_ids: List[str]) -> str:
        """
        Stage 5: 基于场景创建成稿（类似Code）
        整合场景，润色成最终稿件
        """
        if not scene_ids:
            raise ValueError("没有场景可以生成成稿")
        
        logger.info(f"Stage 5: 创建成稿 - 基于{len(scene_ids)}个场景")
        
        # 收集所有场景
        scenes = [self.documents[scene_id] for scene_id in scene_ids]
        
        manuscript = {
            "scene_ids": scene_ids,
            "content": "",
            "word_count": 0,
            "quality_metrics": {
                "character_depth": 0,
                "plot_coherence": 0,
                "prose_quality": 0,
                "dialogue_naturalness": 0,
                "world_building": 0,
                "emotional_impact": 0,
                "overall": 0
            },
            "revision_notes": [],
            "final_polish": {
                "grammar_check": False,
                "style_consistency": False,
                "fact_check": False,
                "sensitivity_review": False
            }
        }
        
        # 整合场景内容
        manuscript = self._integrate_scenes(manuscript, scenes)
        
        # 质量评估
        manuscript = self._assess_manuscript_quality(manuscript)
        
        # 创建文档
        doc_id = f"manuscript_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        document = StageDocument(
            stage=WorkflowStage.MANUSCRIPT,
            title="成稿",
            content=manuscript,
            status="draft",
            quality_score=manuscript["quality_metrics"]["overall"],
            dependencies=scene_ids
        )
        
        # 保存
        self._save_document(doc_id, document)
        self.documents[doc_id] = document
        
        # 更新场景的输出
        for scene_id in scene_ids:
            if scene_id in self.documents:
                self.documents[scene_id].outputs.append(doc_id)
        
        logger.info(f"成稿创建完成: {doc_id}, 质量分: {document.quality_score}")
        return doc_id
    
    def _integrate_scenes(self, manuscript: Dict, scenes: List[StageDocument]) -> Dict:
        """整合场景内容"""
        content_parts = []
        
        for scene in scenes:
            # 这里应该读取实际生成的场景内容
            content_parts.append(f"[场景{scene.content.get('scene_num', '')}内容]")
        
        manuscript["content"] = "\n\n".join(content_parts)
        manuscript["word_count"] = len(manuscript["content"])
        
        return manuscript
    
    def _assess_manuscript_quality(self, manuscript: Dict) -> Dict:
        """评估成稿质量"""
        # 简化的质量评估
        metrics = manuscript["quality_metrics"]
        metrics["character_depth"] = 92
        metrics["plot_coherence"] = 95
        metrics["prose_quality"] = 90
        metrics["dialogue_naturalness"] = 93
        metrics["world_building"] = 91
        metrics["emotional_impact"] = 89
        
        # 计算总分
        metrics["overall"] = int(sum([
            metrics["character_depth"],
            metrics["plot_coherence"],
            metrics["prose_quality"],
            metrics["dialogue_naturalness"],
            metrics["world_building"],
            metrics["emotional_impact"]
        ]) / 6)
        
        return manuscript
    
    # ============ 工作流管理 ============
    
    def validate_stage_transition(self, from_stage: WorkflowStage, 
                                 to_stage: WorkflowStage) -> bool:
        """
        验证阶段转换是否合法
        """
        valid_transitions = {
            WorkflowStage.CONCEPT: [WorkflowStage.BIBLE],
            WorkflowStage.BIBLE: [WorkflowStage.CHAPTER],
            WorkflowStage.CHAPTER: [WorkflowStage.SCENE],
            WorkflowStage.SCENE: [WorkflowStage.MANUSCRIPT],
            WorkflowStage.MANUSCRIPT: []
        }
        
        return to_stage in valid_transitions.get(from_stage, [])
    
    def get_stage_documents(self, stage: WorkflowStage, 
                           status: str = None) -> List[StageDocument]:
        """
        获取特定阶段的文档
        """
        documents = []
        
        for doc in self.documents.values():
            if doc.stage == stage:
                if status is None or doc.status == status:
                    documents.append(doc)
        
        return documents
    
    def approve_document(self, doc_id: str) -> bool:
        """
        批准文档，允许进入下一阶段
        """
        if doc_id not in self.documents:
            return False
        
        document = self.documents[doc_id]
        
        # 检查依赖是否都已批准
        for dep_id in document.dependencies:
            if dep_id in self.documents:
                if self.documents[dep_id].status != "approved":
                    logger.warning(f"依赖文档{dep_id}未批准")
                    return False
        
        # 批准文档
        document.status = "approved"
        document.updated_at = datetime.now()
        self._save_document(doc_id, document)
        
        logger.info(f"文档{doc_id}已批准")
        return True
    
    def get_workflow_status(self) -> Dict:
        """
        获取整体工作流状态
        """
        status = {
            "total_documents": len(self.documents),
            "stages": {}
        }
        
        for stage in WorkflowStage:
            stage_docs = self.get_stage_documents(stage)
            status["stages"][stage.value] = {
                "total": len(stage_docs),
                "draft": len([d for d in stage_docs if d.status == "draft"]),
                "review": len([d for d in stage_docs if d.status == "review"]),
                "approved": len([d for d in stage_docs if d.status == "approved"]),
                "published": len([d for d in stage_docs if d.status == "published"])
            }
        
        return status
    
    def _save_document(self, doc_id: str, document: StageDocument):
        """保存文档到文件"""
        file_path = self.stage_dirs[document.stage] / f"{doc_id}.json"
        
        data = {
            "title": document.title,
            "content": document.content,
            "created_at": document.created_at.isoformat(),
            "updated_at": document.updated_at.isoformat(),
            "status": document.status,
            "quality_score": document.quality_score,
            "dependencies": document.dependencies,
            "outputs": document.outputs,
            "metadata": document.metadata
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_traceability_report(self) -> str:
        """
        生成可追溯性报告
        显示从概念到成稿的完整链条
        """
        report = []
        report.append("# 📊 5阶段工作流追溯报告")
        report.append("")
        
        # 找到所有概念文档
        concepts = self.get_stage_documents(WorkflowStage.CONCEPT)
        
        for concept in concepts:
            report.append(f"## 📝 概念: {concept.title}")
            report.append(f"- 状态: {concept.status}")
            report.append(f"- 创建: {concept.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            # 追踪Bible
            for bible_id in concept.outputs:
                if bible_id in self.documents:
                    bible = self.documents[bible_id]
                    report.append(f"\n### 📚 Bible: {bible.title}")
                    report.append(f"- 状态: {bible.status}")
                    
                    # 追踪章节
                    chapters = [self.documents[cid] for cid in bible.outputs 
                              if cid in self.documents]
                    report.append(f"\n#### 📖 章节 ({len(chapters)}个)")
                    
                    for chapter in chapters[:3]:  # 只显示前3章
                        report.append(f"- {chapter.title}: {chapter.status}")
                        
                        # 追踪场景
                        scenes = [self.documents[sid] for sid in chapter.outputs 
                                if sid in self.documents]
                        if scenes:
                            report.append(f"  - 场景: {len(scenes)}个")
                        
                        # 追踪成稿
                        for scene in scenes:
                            for manuscript_id in scene.outputs:
                                if manuscript_id in self.documents:
                                    ms = self.documents[manuscript_id]
                                    report.append(f"    - 成稿: 质量{ms.quality_score}分")
            
            report.append("")
            report.append("---")
            report.append("")
        
        # 统计摘要
        status = self.get_workflow_status()
        report.append("## 📈 统计摘要")
        report.append(f"- 总文档数: {status['total_documents']}")
        for stage_name, stage_data in status["stages"].items():
            report.append(f"- {stage_name}: {stage_data['total']}个文档")
            if stage_data['approved'] > 0:
                report.append(f"  - 已批准: {stage_data['approved']}")
        
        return "\n".join(report)


# 使用示例
if __name__ == "__main__":
    # 创建工作流管理器
    workflow = FiveStageWorkflow()
    
    # Stage 1: 创建概念
    concept_id = workflow.create_concept(
        title="量子觉醒",
        genre="科幻",
        themes=["人性", "科技", "自由意志"],
        target_audience="青年读者"
    )
    print(f"创建概念: {concept_id}")
    
    # Stage 2: 创建Bible
    bible_id = workflow.create_bible(concept_id)
    print(f"创建Bible: {bible_id}")
    
    # Stage 3: 创建章节
    chapter_ids = workflow.create_chapters(bible_id)
    print(f"创建{len(chapter_ids)}个章节")
    
    # Stage 4: 创建场景（第一章）
    scene_ids = workflow.create_scenes(chapter_ids[0])
    print(f"创建{len(scene_ids)}个场景")
    
    # Stage 5: 创建成稿
    manuscript_id = workflow.create_manuscript(scene_ids)
    print(f"创建成稿: {manuscript_id}")
    
    # 生成追溯报告
    report = workflow.generate_traceability_report()
    print("\n" + report)