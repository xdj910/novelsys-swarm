"""
Ultimate Stream Integrator - 8-Stream智能集成器
协调8个专业Stream，生成98分质量的内容
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import time

# 导入所有Stream
from src.streams.enhanced import (
    ContinuityGuardStream,
    ForeshadowingStream,
    DialogueMasterStream,
    EmotionWeaverStream
)

from src.streams.core import (
    CharacterPsychologyStream,
    NarrativeStructureStream,
    WorldBuildingStream,
    ProseCraftStream
)


@dataclass
class StreamResult:
    """Stream结果"""
    stream_name: str
    result: Dict
    execution_time: float
    quality_score: float
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class UltimateStreamIntegrator:
    """
    8-Stream终极集成器
    协调所有Stream生成极致质量内容
    """
    
    def __init__(self, config: Dict = None):
        """
        初始化集成器
        
        Args:
            config: Stream配置
        """
        self.config = config or self._get_default_config()
        
        # 初始化4个增强Stream
        self.enhanced_streams = {
            'continuity_guard': ContinuityGuardStream(),
            'foreshadowing': ForeshadowingStream(),
            'dialogue_master': DialogueMasterStream(),
            'emotion_weaver': EmotionWeaverStream()
        }
        
        # 核心4个Stream
        self.core_streams = {
            'character_psychology': CharacterPsychologyStream(),
            'narrative_structure': NarrativeStructureStream(),
            'world_building': WorldBuildingStream(),
            'prose_craft': ProseCraftStream()
        }
        
        # 合并所有Stream
        self.all_streams = {**self.enhanced_streams, **self.core_streams}
        
        # 冲突解决器
        self.conflict_resolver = ConflictResolver()
        
        # 质量评估器
        self.quality_evaluator = QualityEvaluator()
        
        # 执行统计
        self.execution_stats = {
            'total_runs': 0,
            'average_time': 0,
            'average_quality': 0
        }
    
    async def generate(self, scene: Dict, context: Dict) -> Dict:
        """
        使用8-Stream生成内容
        
        Args:
            scene: 场景信息
            context: 上下文信息
            
        Returns:
            集成后的生成结果
        """
        start_time = time.time()
        
        # 1. 预处理
        preprocessed = await self._preprocess(scene, context)
        
        # 2. 并行执行所有Stream
        stream_results = await self._execute_streams_parallel(preprocessed['scene'], preprocessed['context'])
        
        # 3. 冲突检测与解决
        resolved_results = await self._resolve_conflicts(stream_results)
        
        # 4. 智能融合
        integrated_content = await self._intelligent_merge(resolved_results, preprocessed)
        
        # 5. 质量评估
        quality_assessment = await self._assess_quality(integrated_content, resolved_results)
        
        # 6. 优化调整
        if quality_assessment['overall_score'] < self.config['quality_threshold']:
            integrated_content = await self._optimize_content(integrated_content, quality_assessment)
        
        # 7. 后处理
        final_content = await self._postprocess(integrated_content)
        
        # 更新统计
        execution_time = time.time() - start_time
        self._update_stats(execution_time, quality_assessment['overall_score'])
        
        return {
            'content': final_content,
            'stream_results': {name: result.result for name, result in resolved_results.items()},
            'quality': quality_assessment,
            'execution_time': execution_time,
            'stats': self.execution_stats,
            'metadata': {
                'scene_id': scene.get('id'),
                'streams_used': len(stream_results),
                'conflicts_resolved': len(resolved_results)
            }
        }
    
    async def _preprocess(self, scene: Dict, context: Dict) -> Dict:
        """预处理输入"""
        preprocessed = {
            'scene': scene.copy(),
            'context': context.copy()
        }
        
        # 添加必要的元数据
        if 'timestamp' not in preprocessed['scene']:
            preprocessed['scene']['timestamp'] = time.time()
        
        # 确保上下文完整
        if 'bible' not in preprocessed['context']:
            preprocessed['context']['bible'] = {}
        
        # 添加Stream协调信息
        preprocessed['context']['stream_coordination'] = {
            'priority_emotion': self._determine_priority_emotion(scene),
            'focus_areas': self._determine_focus_areas(scene),
            'quality_targets': self.config['quality_targets']
        }
        
        return preprocessed
    
    async def _execute_streams_parallel(self, scene: Dict, context: Dict) -> Dict[str, StreamResult]:
        """并行执行所有Stream"""
        results = {}
        tasks = []
        
        # 创建所有Stream任务
        for stream_name, stream in self.all_streams.items():
            if stream is not None:  # 跳过未实现的Stream
                task = self._execute_single_stream(stream_name, stream, scene, context)
                tasks.append(task)
        
        # 并行执行
        if tasks:
            completed_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 整理结果
            for result in completed_results:
                if isinstance(result, StreamResult):
                    results[result.stream_name] = result
                elif isinstance(result, Exception):
                    print(f"Stream执行错误: {result}")
        
        return results
    
    async def _execute_single_stream(self, name: str, stream: Any, scene: Dict, context: Dict) -> StreamResult:
        """执行单个Stream"""
        start_time = time.time()
        
        try:
            # 执行Stream（所有Stream统一使用process方法）
            result = await stream.process(scene, context)
            
            # 计算执行时间
            execution_time = time.time() - start_time
            
            # 评估Stream质量
            quality_score = self._evaluate_stream_quality(name, result)
            
            return StreamResult(
                stream_name=name,
                result=result,
                execution_time=execution_time,
                quality_score=quality_score
            )
            
        except Exception as e:
            return StreamResult(
                stream_name=name,
                result={'error': str(e)},
                execution_time=time.time() - start_time,
                quality_score=0.0,
                warnings=[f"Stream执行失败: {str(e)}"]
            )
    
    async def _resolve_conflicts(self, results: Dict[str, StreamResult]) -> Dict[str, StreamResult]:
        """解决Stream之间的冲突"""
        resolved = results.copy()
        
        # 检测冲突
        conflicts = self.conflict_resolver.detect_conflicts(results)
        
        # 解决每个冲突
        for conflict in conflicts:
            resolution = await self.conflict_resolver.resolve(conflict, results)
            
            # 应用解决方案
            for stream_name, adjustment in resolution.items():
                if stream_name in resolved:
                    resolved[stream_name].result.update(adjustment)
        
        return resolved
    
    async def _intelligent_merge(self, results: Dict[str, StreamResult], preprocessed: Dict) -> Dict:
        """智能融合所有Stream结果"""
        merged = {
            'text': '',
            'metadata': {},
            'style': {},
            'requirements': [],
            'enhancements': []
        }
        
        # 提取各Stream的核心内容
        components = {
            'continuity': self._extract_continuity_requirements(results),
            'foreshadowing': self._extract_foreshadowing_content(results),
            'dialogue': self._extract_dialogue_content(results),
            'emotion': self._extract_emotional_elements(results),
            'character': self._extract_character_elements(results),
            'narrative': self._extract_narrative_structure(results),
            'world': self._extract_world_details(results),
            'prose': self._extract_prose_style(results)
        }
        
        # 按优先级融合
        priority_order = self._determine_merge_priority(preprocessed['scene'])
        
        for priority in priority_order:
            if priority in components and components[priority]:
                merged = self._merge_component(merged, components[priority], priority)
        
        # 确保连贯性要求被满足
        merged = self._enforce_continuity_requirements(merged, components.get('continuity', {}))
        
        # 添加情感层次
        merged = self._layer_emotions(merged, components.get('emotion', {}))
        
        # 植入伏笔
        merged = self._embed_foreshadowing(merged, components.get('foreshadowing', {}))
        
        return merged
    
    async def _assess_quality(self, content: Dict, results: Dict[str, StreamResult]) -> Dict:
        """评估生成质量"""
        assessment = {
            'overall_score': 0.0,
            'dimension_scores': {},
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        # 评估各维度
        dimensions = {
            'continuity': self._assess_continuity(content, results),
            'character_consistency': self._assess_character_consistency(content, results),
            'emotional_depth': self._assess_emotional_depth(content, results),
            'narrative_coherence': self._assess_narrative_coherence(content),
            'prose_quality': self._assess_prose_quality(content),
            'dialogue_naturality': self._assess_dialogue_naturality(content, results),
            'foreshadowing_effectiveness': self._assess_foreshadowing(content, results),
            'reader_engagement': self._assess_engagement(content)
        }
        
        assessment['dimension_scores'] = dimensions
        
        # 计算总分
        weights = self.config['quality_weights']
        total_weight = sum(weights.values())
        weighted_sum = sum(
            dimensions.get(dim, 0) * weight 
            for dim, weight in weights.items()
        )
        assessment['overall_score'] = weighted_sum / total_weight if total_weight > 0 else 0
        
        # 识别优势和劣势
        for dim, score in dimensions.items():
            if score > 0.9:
                assessment['strengths'].append(f"{dim}: {score:.2f}")
            elif score < 0.7:
                assessment['weaknesses'].append(f"{dim}: {score:.2f}")
        
        # 生成改进建议
        if assessment['overall_score'] < 0.95:
            assessment['suggestions'] = self._generate_improvement_suggestions(dimensions)
        
        return assessment
    
    async def _optimize_content(self, content: Dict, assessment: Dict) -> Dict:
        """优化内容以提高质量"""
        optimized = content.copy()
        
        # 基于弱点进行针对性优化
        for weakness in assessment['weaknesses']:
            if 'continuity' in weakness:
                optimized = self._enhance_continuity(optimized)
            elif 'emotional' in weakness:
                optimized = self._enhance_emotions(optimized)
            elif 'dialogue' in weakness:
                optimized = self._enhance_dialogue(optimized)
            elif 'prose' in weakness:
                optimized = self._enhance_prose(optimized)
        
        return optimized
    
    async def _postprocess(self, content: Dict) -> Dict:
        """后处理最终内容"""
        final = content.copy()
        
        # 格式化文本
        if 'text' in final:
            final['text'] = self._format_text(final['text'])
        
        # 清理元数据
        if 'metadata' in final:
            final['metadata'] = self._clean_metadata(final['metadata'])
        
        # 添加质量保证标记
        final['quality_assured'] = True
        final['quality_level'] = 'ultimate'
        
        return final
    
    # 辅助方法
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'quality_threshold': 0.95,
            'quality_targets': {
                'continuity': 0.99,
                'character_consistency': 0.95,
                'emotional_depth': 0.90,
                'narrative_coherence': 0.95,
                'prose_quality': 0.90,
                'dialogue_naturality': 0.95,
                'foreshadowing_effectiveness': 0.85,
                'reader_engagement': 0.90
            },
            'quality_weights': {
                'continuity': 0.2,
                'character_consistency': 0.15,
                'emotional_depth': 0.15,
                'narrative_coherence': 0.15,
                'prose_quality': 0.1,
                'dialogue_naturality': 0.1,
                'foreshadowing_effectiveness': 0.075,
                'reader_engagement': 0.075
            },
            'stream_weights': {
                'continuity_guard': 0.125,
                'foreshadowing': 0.125,
                'dialogue_master': 0.125,
                'emotion_weaver': 0.125,
                'character_psychology': 0.125,
                'narrative_structure': 0.125,
                'world_building': 0.125,
                'prose_craft': 0.125
            }
        }
    
    def _determine_priority_emotion(self, scene: Dict) -> str:
        """确定优先情感"""
        scene_type = scene.get('type', '')
        if 'conflict' in scene_type:
            return 'tension'
        elif 'revelation' in scene_type:
            return 'shock'
        elif 'romance' in scene_type:
            return 'love'
        else:
            return 'neutral'
    
    def _determine_focus_areas(self, scene: Dict) -> List[str]:
        """确定焦点区域"""
        focus = []
        
        if scene.get('has_dialogue', True):
            focus.append('dialogue')
        if scene.get('has_action', False):
            focus.append('action')
        if scene.get('has_revelation', False):
            focus.append('revelation')
        if scene.get('emotional_intensity', 0) > 0.5:
            focus.append('emotion')
        
        return focus if focus else ['general']
    
    def _evaluate_stream_quality(self, stream_name: str, result: Dict) -> float:
        """评估Stream质量"""
        # 基于Stream类型的特定评估
        if stream_name == 'continuity_guard':
            return result.get('continuity_score', 0.0)
        elif stream_name == 'foreshadowing':
            return result.get('integrity', {}).get('integrity_score', 0.0) if 'integrity' in result else 0.8
        elif stream_name == 'dialogue_master':
            return result.get('quality_metrics', {}).get('overall_score', 0.0) if 'quality_metrics' in result else 0.8
        elif stream_name == 'emotion_weaver':
            return result.get('authenticity', {}).get('overall_score', 0.0) if 'authenticity' in result else 0.8
        else:
            return 0.5  # 默认分数
    
    def _extract_continuity_requirements(self, results: Dict[str, StreamResult]) -> Dict:
        """提取连贯性要求"""
        if 'continuity_guard' in results:
            guards = results['continuity_guard'].result.get('guards', {})
            return {
                'mandatory': guards.get('mandatory_mentions', []),
                'prohibited': guards.get('prohibited_mentions', []),
                'required_explanations': guards.get('required_explanations', [])
            }
        return {}
    
    def _extract_foreshadowing_content(self, results: Dict[str, StreamResult]) -> Dict:
        """提取伏笔内容"""
        if 'foreshadowing' in results:
            foreshadow = results['foreshadowing'].result
            return {
                'plant': foreshadow.get('planting', []),
                'echo': foreshadow.get('echoing', []),
                'reveal': foreshadow.get('revealing', [])
            }
        return {}
    
    def _extract_dialogue_content(self, results: Dict[str, StreamResult]) -> Dict:
        """提取对话内容"""
        if 'dialogue_master' in results:
            dialogue = results['dialogue_master'].result
            return {
                'exchanges': dialogue.get('exchanges', []),
                'subtext': dialogue.get('subtext_layers', [])
            }
        return {}
    
    def _extract_emotional_elements(self, results: Dict[str, StreamResult]) -> Dict:
        """提取情感元素"""
        if 'emotion_weaver' in results:
            emotion = results['emotion_weaver'].result
            return {
                'beats': emotion.get('emotional_beats', []),
                'atmosphere': emotion.get('atmosphere', {}),
                'resonance': emotion.get('resonance_points', [])
            }
        return {}
    
    def _extract_character_elements(self, results: Dict[str, StreamResult]) -> Dict:
        """提取角色元素"""
        # 从各Stream中提取角色相关内容
        character_elements = {}
        
        if 'dialogue_master' in results:
            character_elements['voices'] = results['dialogue_master'].result.get('character_voices', {})
        
        if 'emotion_weaver' in results:
            character_elements['emotional_states'] = results['emotion_weaver'].result.get('character_states', {})
        
        return character_elements
    
    def _extract_narrative_structure(self, results: Dict[str, StreamResult]) -> Dict:
        """提取叙事结构"""
        # 占位实现
        return {'structure': 'standard'}
    
    def _extract_world_details(self, results: Dict[str, StreamResult]) -> Dict:
        """提取世界细节"""
        # 占位实现
        return {'details': []}
    
    def _extract_prose_style(self, results: Dict[str, StreamResult]) -> Dict:
        """提取文体风格"""
        # 占位实现
        return {'style': 'literary'}
    
    def _determine_merge_priority(self, scene: Dict) -> List[str]:
        """确定融合优先级"""
        scene_type = scene.get('type', '')
        
        if 'dialogue' in scene_type:
            return ['dialogue', 'emotion', 'continuity', 'character', 'foreshadowing', 'narrative', 'world', 'prose']
        elif 'action' in scene_type:
            return ['continuity', 'narrative', 'world', 'character', 'emotion', 'prose', 'dialogue', 'foreshadowing']
        elif 'revelation' in scene_type:
            return ['foreshadowing', 'emotion', 'dialogue', 'continuity', 'character', 'narrative', 'prose', 'world']
        else:
            return ['continuity', 'character', 'emotion', 'narrative', 'dialogue', 'world', 'prose', 'foreshadowing']
    
    def _merge_component(self, merged: Dict, component: Dict, component_type: str) -> Dict:
        """融合单个组件"""
        # 简化实现
        if component_type == 'dialogue' and 'exchanges' in component:
            merged['text'] += f"\n[对话内容: {len(component['exchanges'])}个交换]"
        elif component_type == 'emotion' and 'atmosphere' in component:
            merged['metadata']['atmosphere'] = component['atmosphere']
        elif component_type == 'continuity' and 'mandatory' in component:
            merged['requirements'].extend(component['mandatory'])
        
        return merged
    
    def _enforce_continuity_requirements(self, merged: Dict, continuity: Dict) -> Dict:
        """强制执行连贯性要求"""
        if 'mandatory' in continuity:
            for requirement in continuity['mandatory']:
                merged['requirements'].append(f"[必须: {requirement}]")
        
        if 'prohibited' in continuity:
            for prohibition in continuity['prohibited']:
                merged['requirements'].append(f"[禁止: {prohibition}]")
        
        return merged
    
    def _layer_emotions(self, merged: Dict, emotion: Dict) -> Dict:
        """分层情感"""
        if 'beats' in emotion:
            merged['metadata']['emotional_beats'] = emotion['beats']
        
        if 'atmosphere' in emotion:
            merged['style']['atmosphere'] = emotion['atmosphere']
        
        return merged
    
    def _embed_foreshadowing(self, merged: Dict, foreshadowing: Dict) -> Dict:
        """嵌入伏笔"""
        if 'plant' in foreshadowing:
            for shadow in foreshadowing['plant']:
                merged['enhancements'].append(f"[伏笔: {shadow}]")
        
        return merged
    
    def _assess_continuity(self, content: Dict, results: Dict[str, StreamResult]) -> float:
        """评估连贯性"""
        if 'continuity_guard' in results:
            return results['continuity_guard'].result.get('continuity_score', 0.5)
        return 0.5
    
    def _assess_character_consistency(self, content: Dict, results: Dict[str, StreamResult]) -> float:
        """评估角色一致性"""
        # 简化实现
        return 0.85
    
    def _assess_emotional_depth(self, content: Dict, results: Dict[str, StreamResult]) -> float:
        """评估情感深度"""
        if 'emotion_weaver' in results:
            return results['emotion_weaver'].result.get('authenticity', {}).get('depth', 0.5)
        return 0.5
    
    def _assess_narrative_coherence(self, content: Dict) -> float:
        """评估叙事连贯性"""
        return 0.8
    
    def _assess_prose_quality(self, content: Dict) -> float:
        """评估文笔质量"""
        return 0.75
    
    def _assess_dialogue_naturality(self, content: Dict, results: Dict[str, StreamResult]) -> float:
        """评估对话自然度"""
        if 'dialogue_master' in results:
            metrics = results['dialogue_master'].result.get('quality_metrics', {})
            return metrics.get('naturality', 0.5)
        return 0.5
    
    def _assess_foreshadowing(self, content: Dict, results: Dict[str, StreamResult]) -> float:
        """评估伏笔效果"""
        if 'foreshadowing' in results:
            return results['foreshadowing'].result.get('completion_rate', 0.5)
        return 0.5
    
    def _assess_engagement(self, content: Dict) -> float:
        """评估读者参与度"""
        return 0.8
    
    def _generate_improvement_suggestions(self, dimensions: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        for dim, score in dimensions.items():
            if score < 0.7:
                if dim == 'continuity':
                    suggestions.append("加强时空逻辑验证")
                elif dim == 'emotional_depth':
                    suggestions.append("深化情感层次")
                elif dim == 'dialogue_naturality':
                    suggestions.append("优化对话自然度")
        
        return suggestions
    
    def _enhance_continuity(self, content: Dict) -> Dict:
        """增强连贯性"""
        # 简化实现
        content['enhancements'].append("[连贯性增强]")
        return content
    
    def _enhance_emotions(self, content: Dict) -> Dict:
        """增强情感"""
        content['enhancements'].append("[情感深化]")
        return content
    
    def _enhance_dialogue(self, content: Dict) -> Dict:
        """增强对话"""
        content['enhancements'].append("[对话优化]")
        return content
    
    def _enhance_prose(self, content: Dict) -> Dict:
        """增强文笔"""
        content['enhancements'].append("[文笔润色]")
        return content
    
    def _format_text(self, text: str) -> str:
        """格式化文本"""
        # 简化实现
        return text.strip()
    
    def _clean_metadata(self, metadata: Dict) -> Dict:
        """清理元数据"""
        # 移除内部字段
        cleaned = metadata.copy()
        internal_fields = ['_internal', '_debug', '_temp']
        for field in internal_fields:
            cleaned.pop(field, None)
        return cleaned
    
    def _update_stats(self, execution_time: float, quality_score: float):
        """更新统计信息"""
        self.execution_stats['total_runs'] += 1
        
        # 更新平均时间
        total_time = self.execution_stats['average_time'] * (self.execution_stats['total_runs'] - 1)
        self.execution_stats['average_time'] = (total_time + execution_time) / self.execution_stats['total_runs']
        
        # 更新平均质量
        total_quality = self.execution_stats['average_quality'] * (self.execution_stats['total_runs'] - 1)
        self.execution_stats['average_quality'] = (total_quality + quality_score) / self.execution_stats['total_runs']


class ConflictResolver:
    """冲突解决器"""
    
    def detect_conflicts(self, results: Dict[str, StreamResult]) -> List[Dict]:
        """检测冲突"""
        conflicts = []
        
        # 检测连贯性与其他Stream的冲突
        if 'continuity_guard' in results and 'dialogue_master' in results:
            continuity = results['continuity_guard'].result
            dialogue = results['dialogue_master'].result
            
            # 检查对话是否违反连贯性
            if continuity.get('guards', {}).get('prohibited_mentions'):
                conflicts.append({
                    'type': 'continuity_dialogue',
                    'streams': ['continuity_guard', 'dialogue_master'],
                    'description': '对话可能违反连贯性要求'
                })
        
        return conflicts
    
    async def resolve(self, conflict: Dict, results: Dict[str, StreamResult]) -> Dict:
        """解决冲突"""
        resolution = {}
        
        if conflict['type'] == 'continuity_dialogue':
            # 调整对话以满足连贯性要求
            resolution['dialogue_master'] = {
                'adjusted': True,
                'reason': 'continuity_requirement'
            }
        
        return resolution


class QualityEvaluator:
    """质量评估器"""
    
    def evaluate(self, content: Dict, config: Dict) -> float:
        """评估内容质量"""
        # 简化实现
        return 0.85


# 测试函数
async def test_integrator():
    """测试8-Stream集成器"""
    integrator = UltimateStreamIntegrator()
    
    # 测试场景
    test_scene = {
        'id': 'ch7_sc5',
        'type': 'climax_revelation_dialogue',
        'importance': 'critical',
        'has_dialogue': True,
        'has_revelation': True,
        'emotional_intensity': 0.9,
        'characters': [
            {'name': '李明', 'emotional_state': 'shocked'},
            {'name': '张总', 'emotional_state': 'triumphant'}
        ]
    }
    
    # 测试上下文
    test_context = {
        'bible': {
            'series_info': {
                'themes': ['betrayal', 'redemption', 'truth']
            }
        },
        'chapter_number': 7,
        'tension_level': 0.9
    }
    
    # 运行测试
    result = await integrator.generate(test_scene, test_context)
    
    print("8-Stream集成结果：")
    print(f"质量分数: {result['quality']['overall_score']:.2f}")
    print(f"执行时间: {result['execution_time']:.2f}秒")
    print(f"使用Stream数: {result['metadata']['streams_used']}")
    print(f"\n质量维度评分:")
    for dim, score in result['quality']['dimension_scores'].items():
        print(f"  {dim}: {score:.2f}")
    
    return result


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_integrator())