"""
Character Psychology Stream
角色心理深度分析Stream - 极致品质系统核心组件
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime
import json

class PsychologicalState(Enum):
    """心理状态枚举"""
    STABLE = "stable"
    STRESSED = "stressed"
    CONFLICTED = "conflicted"
    BREAKING = "breaking"
    TRANSFORMED = "transformed"
    ENLIGHTENED = "enlightened"

class MotivationType(Enum):
    """动机类型"""
    SURVIVAL = "survival"          # 生存动机
    SECURITY = "security"          # 安全动机
    BELONGING = "belonging"        # 归属动机
    ESTEEM = "esteem"             # 尊重动机
    SELF_ACTUALIZATION = "self_actualization"  # 自我实现
    TRANSCENDENCE = "transcendence"  # 超越自我

@dataclass
class CharacterPsyche:
    """角色心理模型"""
    character_id: str
    
    # 核心人格
    personality_traits: Dict[str, float] = field(default_factory=dict)  # Big Five
    values: List[str] = field(default_factory=list)
    beliefs: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    desires: List[str] = field(default_factory=list)
    
    # 动态心理状态
    current_state: PsychologicalState = PsychologicalState.STABLE
    stress_level: float = 0.0  # 0-1
    emotional_stability: float = 0.8  # 0-1
    
    # 认知模式
    cognitive_biases: List[str] = field(default_factory=list)
    defense_mechanisms: List[str] = field(default_factory=list)
    coping_strategies: List[str] = field(default_factory=list)
    
    # 动机系统
    primary_motivation: MotivationType = MotivationType.BELONGING
    secondary_motivations: List[MotivationType] = field(default_factory=list)
    current_goals: List[Dict[str, Any]] = field(default_factory=list)
    
    # 关系心理
    attachment_style: str = "secure"
    trust_levels: Dict[str, float] = field(default_factory=dict)  # 对其他角色的信任度
    relationship_patterns: List[str] = field(default_factory=list)
    
    # 创伤与成长
    traumas: List[Dict[str, Any]] = field(default_factory=list)
    growth_experiences: List[Dict[str, Any]] = field(default_factory=list)
    unresolved_conflicts: List[Dict[str, Any]] = field(default_factory=list)
    
    # 决策模式
    decision_style: str = "rational"  # rational, intuitive, dependent, avoidant, spontaneous
    risk_tolerance: float = 0.5  # 0-1
    moral_flexibility: float = 0.3  # 0-1

@dataclass
class PsychologicalDynamics:
    """心理动态变化"""
    trigger: str
    response: str
    impact: Dict[str, float]
    duration: str
    recovery_conditions: List[str]

class CharacterPsychologyStream:
    """
    角色心理Stream
    - 深度心理建模
    - 动机链追踪
    - 行为预测
    - 心理转变弧线
    """
    
    def __init__(self):
        self.stream_id = "character_psychology"
        self.weight = 0.125
        self.character_models: Dict[str, CharacterPsyche] = {}
        self.interaction_history: List[Dict] = []
        self.psychological_arcs: Dict[str, List] = {}
        
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景，返回心理分析结果
        """
        try:
            # 1. 初始化或更新角色心理模型
            characters = await self._identify_characters(scene, context)
            await self._update_character_models(characters, context)
            
            # 2. 分析当前心理状态
            psychological_states = await self._analyze_psychological_states(
                characters, scene, context
            )
            
            # 3. 预测行为倾向
            behavior_predictions = await self._predict_behaviors(
                psychological_states, scene, context
            )
            
            # 4. 生成内心活动
            inner_monologues = await self._generate_inner_monologues(
                psychological_states, scene
            )
            
            # 5. 评估心理冲突
            psychological_conflicts = await self._assess_conflicts(
                psychological_states, context
            )
            
            # 6. 追踪心理弧线
            arc_progression = await self._track_psychological_arcs(
                characters, psychological_states
            )
            
            return {
                'stream_id': self.stream_id,
                'weight': self.weight,
                'psychological_states': psychological_states,
                'behavior_predictions': behavior_predictions,
                'inner_monologues': inner_monologues,
                'psychological_conflicts': psychological_conflicts,
                'arc_progression': arc_progression,
                'recommendations': await self._generate_recommendations(
                    psychological_states, behavior_predictions
                ),
                'quality_score': await self._calculate_quality_score(
                    psychological_states, arc_progression
                )
            }
            
        except Exception as e:
            return {
                'stream_id': self.stream_id,
                'error': str(e),
                'fallback': await self._generate_fallback(scene)
            }
    
    async def _identify_characters(self, scene: Dict, context: Dict) -> List[str]:
        """识别场景中的角色"""
        characters = []
        
        # 从场景描述中提取
        if 'characters' in scene:
            characters.extend(scene['characters'])
        
        # 从对话中提取
        if 'dialogue' in scene:
            for line in scene['dialogue']:
                if 'speaker' in line and line['speaker'] not in characters:
                    characters.append(line['speaker'])
        
        # 从上下文中补充
        if 'active_characters' in context:
            for char in context['active_characters']:
                if char not in characters:
                    characters.append(char)
        
        return characters
    
    async def _update_character_models(self, characters: List[str], context: Dict):
        """更新角色心理模型"""
        for char_id in characters:
            if char_id not in self.character_models:
                # 创建新模型
                self.character_models[char_id] = await self._create_character_model(
                    char_id, context
                )
            else:
                # 更新现有模型
                await self._evolve_character_model(
                    self.character_models[char_id], context
                )
    
    async def _create_character_model(self, char_id: str, context: Dict) -> CharacterPsyche:
        """创建角色心理模型"""
        # 从context中获取角色信息
        char_info = context.get('characters', {}).get(char_id, {})
        
        model = CharacterPsyche(
            character_id=char_id,
            personality_traits={
                'openness': char_info.get('openness', 0.5),
                'conscientiousness': char_info.get('conscientiousness', 0.5),
                'extraversion': char_info.get('extraversion', 0.5),
                'agreeableness': char_info.get('agreeableness', 0.5),
                'neuroticism': char_info.get('neuroticism', 0.5)
            },
            values=char_info.get('values', []),
            beliefs=char_info.get('beliefs', []),
            fears=char_info.get('fears', []),
            desires=char_info.get('desires', []),
            primary_motivation=MotivationType[
                char_info.get('motivation', 'BELONGING').upper()
            ],
            attachment_style=char_info.get('attachment_style', 'secure'),
            decision_style=char_info.get('decision_style', 'rational')
        )
        
        return model
    
    async def _evolve_character_model(self, model: CharacterPsyche, context: Dict):
        """演化角色心理模型"""
        # 基于最近事件调整
        recent_events = context.get('recent_events', [])
        
        for event in recent_events:
            if event.get('character_id') == model.character_id:
                # 调整压力水平
                if event.get('type') == 'conflict':
                    model.stress_level = min(1.0, model.stress_level + 0.1)
                elif event.get('type') == 'resolution':
                    model.stress_level = max(0.0, model.stress_level - 0.15)
                
                # 更新情绪稳定性
                if event.get('emotional_impact'):
                    impact = event['emotional_impact']
                    model.emotional_stability = max(0.0, min(1.0,
                        model.emotional_stability - impact * 0.1
                    ))
                
                # 记录创伤或成长
                if event.get('significance') == 'high':
                    if event.get('valence') == 'negative':
                        model.traumas.append(event)
                    else:
                        model.growth_experiences.append(event)
    
    async def _analyze_psychological_states(
        self, characters: List[str], scene: Dict, context: Dict
    ) -> Dict[str, Dict]:
        """分析角色心理状态"""
        states = {}
        
        for char_id in characters:
            model = self.character_models.get(char_id)
            if not model:
                continue
            
            # 分析当前状态
            state_analysis = {
                'character_id': char_id,
                'psychological_state': model.current_state.value,
                'stress_level': model.stress_level,
                'emotional_stability': model.emotional_stability,
                'active_motivations': [model.primary_motivation.value],
                'dominant_emotions': await self._identify_dominant_emotions(
                    model, scene
                ),
                'cognitive_state': await self._assess_cognitive_state(model),
                'behavioral_tendency': await self._determine_behavioral_tendency(
                    model, scene
                ),
                'defense_mechanisms_active': await self._identify_active_defenses(
                    model, scene
                )
            }
            
            states[char_id] = state_analysis
        
        return states
    
    async def _predict_behaviors(
        self, states: Dict, scene: Dict, context: Dict
    ) -> Dict[str, List]:
        """预测角色行为"""
        predictions = {}
        
        for char_id, state in states.items():
            model = self.character_models.get(char_id)
            if not model:
                continue
            
            # 基于心理状态预测行为
            likely_behaviors = []
            
            # 高压力下的行为
            if state['stress_level'] > 0.7:
                if 'fight' in model.coping_strategies:
                    likely_behaviors.append({
                        'type': 'confrontation',
                        'probability': 0.7,
                        'description': '可能采取对抗行为'
                    })
                elif 'flight' in model.coping_strategies:
                    likely_behaviors.append({
                        'type': 'avoidance',
                        'probability': 0.8,
                        'description': '可能逃避或撤退'
                    })
            
            # 基于动机的行为
            if model.primary_motivation == MotivationType.SURVIVAL:
                likely_behaviors.append({
                    'type': 'self_preservation',
                    'probability': 0.9,
                    'description': '优先考虑自身安全'
                })
            elif model.primary_motivation == MotivationType.BELONGING:
                likely_behaviors.append({
                    'type': 'connection_seeking',
                    'probability': 0.75,
                    'description': '寻求他人支持或认同'
                })
            
            predictions[char_id] = likely_behaviors
        
        return predictions
    
    async def _generate_inner_monologues(
        self, states: Dict, scene: Dict
    ) -> Dict[str, str]:
        """生成内心独白"""
        monologues = {}
        
        for char_id, state in states.items():
            model = self.character_models.get(char_id)
            if not model:
                continue
            
            # 基于心理状态生成内心活动
            thoughts = []
            
            # 压力思维
            if state['stress_level'] > 0.5:
                thoughts.append(f"压力让思维变得混乱")
            
            # 情绪思维
            if 'fear' in state['dominant_emotions']:
                if model.fears:
                    thoughts.append(f"恐惧{model.fears[0]}的感觉再次袭来")
            
            # 动机思维
            if model.current_goals:
                thoughts.append(f"必须{model.current_goals[0].get('description', '达成目标')}")
            
            monologues[char_id] = '，'.join(thoughts) if thoughts else "内心一片平静"
        
        return monologues
    
    async def _assess_conflicts(
        self, states: Dict, context: Dict
    ) -> List[Dict]:
        """评估心理冲突"""
        conflicts = []
        
        for char_id, state in states.items():
            model = self.character_models.get(char_id)
            if not model:
                continue
            
            # 内部冲突
            if len(model.unresolved_conflicts) > 0:
                conflicts.append({
                    'type': 'internal',
                    'character': char_id,
                    'nature': model.unresolved_conflicts[0],
                    'intensity': state['stress_level'],
                    'resolution_path': await self._suggest_resolution(
                        model.unresolved_conflicts[0]
                    )
                })
            
            # 价值观冲突
            if model.moral_flexibility < 0.3 and state['stress_level'] > 0.6:
                conflicts.append({
                    'type': 'moral',
                    'character': char_id,
                    'description': '道德准则与现实压力的冲突',
                    'intensity': 0.8
                })
        
        return conflicts
    
    async def _track_psychological_arcs(
        self, characters: List[str], states: Dict
    ) -> Dict[str, Dict]:
        """追踪心理弧线"""
        arc_data = {}
        
        for char_id in characters:
            if char_id not in self.psychological_arcs:
                self.psychological_arcs[char_id] = []
            
            # 记录当前状态点
            current_point = {
                'timestamp': datetime.now().isoformat(),
                'state': states.get(char_id, {}),
                'chapter': states.get('chapter', 1)
            }
            
            self.psychological_arcs[char_id].append(current_point)
            
            # 分析弧线进展
            arc_analysis = await self._analyze_arc_progression(
                self.psychological_arcs[char_id]
            )
            
            arc_data[char_id] = arc_analysis
        
        return arc_data
    
    async def _analyze_arc_progression(self, arc_points: List[Dict]) -> Dict:
        """分析心理弧线进展"""
        if len(arc_points) < 2:
            return {'status': 'beginning', 'progression': 0.0}
        
        # 分析变化趋势
        first = arc_points[0]
        latest = arc_points[-1]
        
        progression = {
            'status': 'developing',
            'progression': len(arc_points) / 20,  # 假设20个点完成一个弧
            'stress_trend': latest.get('state', {}).get('stress_level', 0) - 
                           first.get('state', {}).get('stress_level', 0),
            'stability_trend': latest.get('state', {}).get('emotional_stability', 0) - 
                              first.get('state', {}).get('emotional_stability', 0),
            'transformation_indicators': []
        }
        
        # 检测转变指标
        if abs(progression['stress_trend']) > 0.3:
            progression['transformation_indicators'].append('significant_stress_change')
        if abs(progression['stability_trend']) > 0.3:
            progression['transformation_indicators'].append('stability_shift')
        
        return progression
    
    async def _identify_dominant_emotions(
        self, model: CharacterPsyche, scene: Dict
    ) -> List[str]:
        """识别主导情绪"""
        emotions = []
        
        # 基于压力水平
        if model.stress_level > 0.7:
            emotions.append('anxiety')
        elif model.stress_level > 0.4:
            emotions.append('tension')
        
        # 基于情绪稳定性
        if model.emotional_stability < 0.3:
            emotions.append('volatile')
        elif model.emotional_stability > 0.7:
            emotions.append('calm')
        
        # 基于场景内容
        scene_content = scene.get('content', '').lower()
        if 'danger' in scene_content or 'threat' in scene_content:
            emotions.append('fear')
        if 'loss' in scene_content or 'gone' in scene_content:
            emotions.append('grief')
        
        return emotions[:3]  # 返回前3个主导情绪
    
    async def _assess_cognitive_state(self, model: CharacterPsyche) -> str:
        """评估认知状态"""
        if model.stress_level > 0.8:
            return 'impaired'  # 认知受损
        elif model.emotional_stability < 0.3:
            return 'distorted'  # 认知扭曲
        elif model.stress_level < 0.3 and model.emotional_stability > 0.7:
            return 'clear'  # 清晰
        else:
            return 'functional'  # 正常运作
    
    async def _determine_behavioral_tendency(
        self, model: CharacterPsyche, scene: Dict
    ) -> str:
        """确定行为倾向"""
        # 基于决策风格和当前状态
        if model.decision_style == 'avoidant' and model.stress_level > 0.5:
            return 'withdrawal'
        elif model.decision_style == 'spontaneous' and model.emotional_stability < 0.5:
            return 'impulsive'
        elif model.decision_style == 'rational' and model.stress_level < 0.4:
            return 'analytical'
        elif model.risk_tolerance > 0.7:
            return 'risk_taking'
        else:
            return 'cautious'
    
    async def _identify_active_defenses(
        self, model: CharacterPsyche, scene: Dict
    ) -> List[str]:
        """识别活跃的防御机制"""
        active_defenses = []
        
        if model.stress_level > 0.6:
            if 'denial' in model.defense_mechanisms:
                active_defenses.append('denial')
            if 'projection' in model.defense_mechanisms:
                active_defenses.append('projection')
        
        if model.emotional_stability < 0.4:
            if 'rationalization' in model.defense_mechanisms:
                active_defenses.append('rationalization')
        
        return active_defenses
    
    async def _suggest_resolution(self, conflict: Dict) -> str:
        """建议冲突解决路径"""
        conflict_type = conflict.get('type', 'unknown')
        
        resolutions = {
            'value_conflict': '通过自我反思重新评估价值观',
            'goal_conflict': '确定优先级并做出选择',
            'relationship_conflict': '开放沟通和相互理解',
            'identity_conflict': '接纳多面性的自我',
            'unknown': '深入探索冲突根源'
        }
        
        return resolutions.get(conflict_type, resolutions['unknown'])
    
    async def _generate_recommendations(
        self, states: Dict, predictions: Dict
    ) -> List[str]:
        """生成心理层面的写作建议"""
        recommendations = []
        
        # 检查心理深度
        has_depth = any(
            state.get('stress_level', 0) > 0.3 or 
            len(state.get('dominant_emotions', [])) > 1
            for state in states.values()
        )
        
        if not has_depth:
            recommendations.append("增加角色的内心冲突以提升心理深度")
        
        # 检查行为一致性
        for char_id, prediction in predictions.items():
            if prediction and len(prediction) > 0:
                model = self.character_models.get(char_id)
                if model and prediction[0]['type'] not in ['confrontation', 'avoidance']:
                    if model.decision_style == 'avoidant':
                        recommendations.append(
                            f"{char_id}的行为应更符合回避型人格"
                        )
        
        return recommendations
    
    async def _calculate_quality_score(
        self, states: Dict, arc_progression: Dict
    ) -> float:
        """计算心理刻画质量分数"""
        score = 0.0
        
        # 心理复杂度 (30%)
        complexity = sum(
            len(state.get('dominant_emotions', [])) * 0.1 +
            state.get('stress_level', 0) * 0.1 +
            (1 - state.get('emotional_stability', 1)) * 0.1
            for state in states.values()
        ) / max(len(states), 1)
        score += min(complexity, 0.3)
        
        # 心理一致性 (30%)
        consistency = sum(
            0.3 if state.get('behavioral_tendency') else 0.0
            for state in states.values()
        ) / max(len(states), 1)
        score += consistency
        
        # 心理弧线 (20%)
        arc_score = sum(
            min(arc.get('progression', 0), 1.0) * 0.2
            for arc in arc_progression.values()
        ) / max(len(arc_progression), 1)
        score += arc_score
        
        # 内心活动深度 (20%)
        has_inner_depth = any(
            len(state.get('defense_mechanisms_active', [])) > 0
            for state in states.values()
        )
        if has_inner_depth:
            score += 0.2
        
        return min(score, 1.0)
    
    async def _generate_fallback(self, scene: Dict) -> Dict:
        """生成降级方案"""
        return {
            'psychological_states': {},
            'behavior_predictions': {},
            'inner_monologues': {},
            'message': 'Using simplified psychological model'
        }