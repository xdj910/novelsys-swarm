"""
EmotionWeaverStream - 情感编织大师
多层次情感渲染，创造深度情感体验
Quality Target: 95% emotional resonance
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import math


class EmotionLayer(Enum):
    """情感层次枚举"""
    SURFACE = "surface"           # 表层情感
    UNDERLYING = "underlying"     # 深层情感
    SUBCONSCIOUS = "subconscious" # 潜意识情感
    ATMOSPHERIC = "atmospheric"   # 氛围情感
    READER = "reader"             # 读者情感


class EmotionType(Enum):
    """情感类型枚举"""
    # 基础情感
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    
    # 复杂情感
    LOVE = "love"
    GUILT = "guilt"
    SHAME = "shame"
    PRIDE = "pride"
    ENVY = "envy"
    GRATITUDE = "gratitude"
    HOPE = "hope"
    DESPAIR = "despair"
    NOSTALGIA = "nostalgia"
    MELANCHOLY = "melancholy"
    ANXIETY = "anxiety"
    RELIEF = "relief"


@dataclass
class EmotionalState:
    """情感状态"""
    character: str
    surface_emotion: EmotionType
    surface_intensity: float  # 0-1
    underlying_emotion: Optional[EmotionType] = None
    underlying_intensity: float = 0.0
    triggers: List[str] = None
    duration: str = "moment"  # moment/scene/chapter/arc
    trajectory: str = "stable"  # stable/rising/falling/volatile
    
    def __post_init__(self):
        if self.triggers is None:
            self.triggers = []
    
    def blend_with(self, other: 'EmotionalState') -> 'EmotionalState':
        """混合两个情感状态"""
        # 简化实现：取强度更高的情感
        if self.surface_intensity >= other.surface_intensity:
            primary = self
            secondary = other
        else:
            primary = other
            secondary = self
        
        return EmotionalState(
            character=self.character,
            surface_emotion=primary.surface_emotion,
            surface_intensity=primary.surface_intensity,
            underlying_emotion=secondary.surface_emotion,
            underlying_intensity=secondary.surface_intensity * 0.7,
            triggers=self.triggers + other.triggers,
            duration=primary.duration,
            trajectory=primary.trajectory
        )


@dataclass
class EmotionalBeat:
    """情感节拍"""
    timestamp: str
    emotion_states: Dict[str, EmotionalState]
    atmosphere: Dict[str, float]  # emotion_type -> intensity
    tension: float
    mood_shift: Optional[str] = None
    catalyst: Optional[str] = None


class EmotionWeaverStream:
    """
    情感编织Stream
    负责创造多层次、细腻的情感体验
    """
    
    def __init__(self):
        self.emotional_history = []  # 情感历史
        self.character_baselines = {}  # 角色情感基线
        self.atmosphere_builder = AtmosphereBuilder()
        self.transition_smoother = EmotionTransitionSmoother()
        self.resonance_calculator = ResonanceCalculator()
        self.emotion_mapper = EmotionMapper()
        
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景的情感编织
        
        Args:
            scene: 场景信息
            context: 上下文信息
            
        Returns:
            情感编织结果
        """
        # 1. 分析场景情感需求
        emotional_requirements = await self._analyze_emotional_needs(scene, context)
        
        # 2. 建立角色情感状态
        character_states = await self._establish_character_emotions(scene, context)
        
        # 3. 构建情感层次
        emotion_layers = await self._build_emotion_layers(
            character_states, emotional_requirements, context
        )
        
        # 4. 创建情感节拍
        emotional_beats = await self._create_emotional_beats(
            emotion_layers, scene, context
        )
        
        # 5. 编织氛围
        atmosphere = await self._weave_atmosphere(emotional_beats, scene, context)
        
        # 6. 平滑情感过渡
        smoothed_progression = await self._smooth_transitions(emotional_beats)
        
        # 7. 增强情感共鸣
        resonance_points = await self._enhance_resonance(smoothed_progression, context)
        
        # 8. 生成情感表现
        emotional_expressions = await self._generate_expressions(
            smoothed_progression, atmosphere, resonance_points
        )
        
        # 9. 验证情感真实性
        authenticity_check = await self._validate_emotional_authenticity(emotional_expressions)
        
        return {
            'character_states': character_states,
            'emotion_layers': emotion_layers,
            'emotional_beats': smoothed_progression,
            'atmosphere': atmosphere,
            'resonance_points': resonance_points,
            'expressions': emotional_expressions,
            'authenticity': authenticity_check,
            'emotional_arc': self._extract_emotional_arc(smoothed_progression),
            'mood_summary': self._summarize_mood(atmosphere),
            'impact_prediction': await self._predict_reader_impact(emotional_expressions)
        }
    
    async def _analyze_emotional_needs(self, scene: Dict, context: Dict) -> Dict:
        """分析场景的情感需求"""
        needs = {
            'target_emotions': [],
            'intensity_range': (0.0, 1.0),
            'complexity_level': 'medium',
            'reader_goal': 'engagement',
            'thematic_emotions': [],
            'avoided_emotions': []
        }
        
        # 基于场景类型确定目标情感
        scene_type = scene.get('type', '')
        if 'tragedy' in scene_type:
            needs['target_emotions'] = [EmotionType.SADNESS, EmotionType.DESPAIR]
            needs['reader_goal'] = 'catharsis'
        elif 'victory' in scene_type:
            needs['target_emotions'] = [EmotionType.JOY, EmotionType.PRIDE]
            needs['reader_goal'] = 'celebration'
        elif 'betrayal' in scene_type:
            needs['target_emotions'] = [EmotionType.ANGER, EmotionType.DISGUST]
            needs['reader_goal'] = 'shock'
        elif 'reunion' in scene_type:
            needs['target_emotions'] = [EmotionType.JOY, EmotionType.NOSTALGIA]
            needs['reader_goal'] = 'warmth'
        else:
            needs['target_emotions'] = [EmotionType.ANXIETY]
            needs['reader_goal'] = 'tension'
        
        # 确定强度范围
        importance = scene.get('importance', 'medium')
        if importance == 'critical':
            needs['intensity_range'] = (0.7, 1.0)
            needs['complexity_level'] = 'high'
        elif importance == 'high':
            needs['intensity_range'] = (0.5, 0.9)
            needs['complexity_level'] = 'medium-high'
        else:
            needs['intensity_range'] = (0.3, 0.7)
            needs['complexity_level'] = 'medium'
        
        # 主题相关情感
        themes = context.get('bible', {}).get('series_info', {}).get('themes', [])
        needs['thematic_emotions'] = self._map_themes_to_emotions(themes)
        
        # 避免的情感（基于前文避免情感疲劳）
        recent_emotions = self._get_recent_emotions()
        if recent_emotions.count(EmotionType.SADNESS) > 3:
            needs['avoided_emotions'].append(EmotionType.SADNESS)
        
        return needs
    
    async def _establish_character_emotions(self, scene: Dict, context: Dict) -> Dict[str, EmotionalState]:
        """建立角色情感状态"""
        states = {}
        
        for character in scene.get('characters', []):
            char_name = character['name']
            
            # 获取基线情感
            baseline = self._get_character_baseline(char_name, context)
            
            # 当前场景情感
            current_emotion = self._determine_current_emotion(character, scene, context)
            
            # 创建情感状态
            state = EmotionalState(
                character=char_name,
                surface_emotion=current_emotion['surface'],
                surface_intensity=current_emotion['intensity'],
                underlying_emotion=baseline.get('underlying'),
                underlying_intensity=baseline.get('underlying_intensity', 0.5),
                triggers=self._identify_triggers(character, scene),
                duration=self._estimate_duration(current_emotion),
                trajectory=self._predict_trajectory(character, scene, context)
            )
            
            states[char_name] = state
        
        return states
    
    async def _build_emotion_layers(
        self, character_states: Dict[str, EmotionalState],
        requirements: Dict, context: Dict
    ) -> Dict[str, Dict]:
        """构建情感层次"""
        layers = {
            'surface': {},
            'underlying': {},
            'subconscious': {},
            'atmospheric': {},
            'reader': {}
        }
        
        # 表层情感（角色直接表现）
        for char_name, state in character_states.items():
            layers['surface'][char_name] = {
                'emotion': state.surface_emotion.value,
                'intensity': state.surface_intensity,
                'expression': self._get_expression_mode(state.surface_emotion, state.surface_intensity)
            }
        
        # 深层情感（角色内心）
        for char_name, state in character_states.items():
            if state.underlying_emotion:
                layers['underlying'][char_name] = {
                    'emotion': state.underlying_emotion.value,
                    'intensity': state.underlying_intensity,
                    'hints': self._generate_underlying_hints(state)
                }
        
        # 潜意识情感（角色未意识到的）
        for char_name, state in character_states.items():
            subconscious = self._detect_subconscious_emotion(state, context)
            if subconscious:
                layers['subconscious'][char_name] = subconscious
        
        # 氛围情感（场景整体）
        layers['atmospheric'] = await self.atmosphere_builder.build(
            character_states, requirements, context
        )
        
        # 读者目标情感
        layers['reader'] = {
            'target': [e.value for e in requirements['target_emotions']],
            'intensity': sum(requirements['intensity_range']) / 2,
            'techniques': self._select_reader_techniques(requirements['reader_goal'])
        }
        
        return layers
    
    async def _create_emotional_beats(
        self, layers: Dict, scene: Dict, context: Dict
    ) -> List[EmotionalBeat]:
        """创建情感节拍"""
        beats = []
        
        # 确定节拍数量
        scene_length = scene.get('estimated_length', 1000)  # 字数
        beat_frequency = 200  # 每200字一个节拍
        num_beats = max(3, scene_length // beat_frequency)
        
        # 创建情感进程
        for i in range(num_beats):
            progress = i / (num_beats - 1) if num_beats > 1 else 0.5
            
            # 计算此节拍的情感状态
            beat_states = {}
            for char_name in layers['surface']:
                beat_state = self._interpolate_emotion_state(
                    char_name, progress, layers, context
                )
                beat_states[char_name] = beat_state
            
            # 计算氛围
            beat_atmosphere = self._interpolate_atmosphere(
                progress, layers['atmospheric']
            )
            
            # 计算紧张度
            beat_tension = self._calculate_beat_tension(progress, scene, context)
            
            # 检查情绪转换
            mood_shift = None
            if i > 0 and self._detect_mood_shift(beats[-1], beat_states):
                mood_shift = self._describe_mood_shift(beats[-1], beat_states)
            
            # 识别催化剂
            catalyst = self._identify_catalyst(i, scene) if mood_shift else None
            
            beat = EmotionalBeat(
                timestamp=f"beat_{i}",
                emotion_states=beat_states,
                atmosphere=beat_atmosphere,
                tension=beat_tension,
                mood_shift=mood_shift,
                catalyst=catalyst
            )
            
            beats.append(beat)
        
        return beats
    
    async def _weave_atmosphere(
        self, beats: List[EmotionalBeat], scene: Dict, context: Dict
    ) -> Dict:
        """编织氛围"""
        atmosphere = {
            'dominant_mood': '',
            'mood_layers': [],
            'sensory_elements': {},
            'symbolic_elements': [],
            'intensity_curve': [],
            'color_palette': []
        }
        
        # 确定主导情绪
        mood_counts = {}
        for beat in beats:
            for emotion, intensity in beat.atmosphere.items():
                if emotion not in mood_counts:
                    mood_counts[emotion] = 0
                mood_counts[emotion] += intensity
        
        if mood_counts:
            atmosphere['dominant_mood'] = max(mood_counts, key=mood_counts.get)
        
        # 构建情绪层次
        atmosphere['mood_layers'] = [
            {'primary': atmosphere['dominant_mood'], 'weight': 0.6},
            {'secondary': self._find_complementary_mood(atmosphere['dominant_mood']), 'weight': 0.3},
            {'accent': self._find_accent_mood(scene), 'weight': 0.1}
        ]
        
        # 感官元素
        atmosphere['sensory_elements'] = self._generate_sensory_elements(
            atmosphere['dominant_mood'], scene
        )
        
        # 象征元素
        atmosphere['symbolic_elements'] = self._generate_symbolic_elements(
            atmosphere['dominant_mood'], context
        )
        
        # 强度曲线
        atmosphere['intensity_curve'] = [beat.tension for beat in beats]
        
        # 色彩调色板
        atmosphere['color_palette'] = self._generate_color_palette(atmosphere['dominant_mood'])
        
        return atmosphere
    
    async def _smooth_transitions(self, beats: List[EmotionalBeat]) -> List[EmotionalBeat]:
        """平滑情感过渡"""
        smoothed = self.transition_smoother.smooth(beats)
        
        # 添加过渡描述
        for i in range(1, len(smoothed)):
            prev_beat = smoothed[i-1]
            curr_beat = smoothed[i]
            
            # 检查是否需要过渡
            if self._needs_transition(prev_beat, curr_beat):
                # 插入过渡节拍
                transition_beat = self._create_transition_beat(prev_beat, curr_beat)
                smoothed.insert(i, transition_beat)
        
        return smoothed
    
    async def _enhance_resonance(
        self, beats: List[EmotionalBeat], context: Dict
    ) -> List[Dict]:
        """增强情感共鸣"""
        resonance_points = []
        
        for i, beat in enumerate(beats):
            # 计算共鸣潜力
            resonance_potential = self.resonance_calculator.calculate(beat, context)
            
            if resonance_potential > 0.7:
                # 创建共鸣点
                resonance_point = {
                    'beat_index': i,
                    'type': self._identify_resonance_type(beat),
                    'technique': self._select_resonance_technique(beat, context),
                    'target_emotion': self._get_primary_emotion(beat),
                    'intensity': resonance_potential,
                    'universal_theme': self._map_to_universal_theme(beat)
                }
                
                resonance_points.append(resonance_point)
        
        return resonance_points
    
    async def _generate_expressions(
        self, beats: List[EmotionalBeat],
        atmosphere: Dict,
        resonance_points: List[Dict]
    ) -> Dict:
        """生成情感表现"""
        expressions = {
            'physical': [],
            'verbal': [],
            'environmental': [],
            'narrative': [],
            'symbolic': []
        }
        
        for beat in beats:
            # 身体表现
            for char_name, state in beat.emotion_states.items():
                physical = self._generate_physical_expression(state)
                expressions['physical'].append({
                    'character': char_name,
                    'beat': beat.timestamp,
                    'expression': physical
                })
            
            # 语言表现
            verbal = self._generate_verbal_expression(beat)
            if verbal:
                expressions['verbal'].append(verbal)
            
            # 环境表现
            environmental = self._generate_environmental_expression(beat, atmosphere)
            expressions['environmental'].append(environmental)
        
        # 叙事表现（节奏、句式等）
        expressions['narrative'] = self._generate_narrative_expressions(beats)
        
        # 象征表现
        expressions['symbolic'] = self._generate_symbolic_expressions(
            resonance_points, atmosphere
        )
        
        return expressions
    
    async def _validate_emotional_authenticity(self, expressions: Dict) -> Dict:
        """验证情感真实性"""
        authenticity = {
            'overall_score': 0.0,
            'consistency': 0.0,
            'depth': 0.0,
            'believability': 0.0,
            'impact': 0.0,
            'issues': []
        }
        
        # 一致性检查
        authenticity['consistency'] = self._check_emotional_consistency(expressions)
        
        # 深度检查
        authenticity['depth'] = self._check_emotional_depth(expressions)
        
        # 可信度检查
        authenticity['believability'] = self._check_believability(expressions)
        
        # 影响力检查
        authenticity['impact'] = self._check_emotional_impact(expressions)
        
        # 计算总分
        authenticity['overall_score'] = (
            authenticity['consistency'] * 0.25 +
            authenticity['depth'] * 0.25 +
            authenticity['believability'] * 0.3 +
            authenticity['impact'] * 0.2
        )
        
        # 识别问题
        if authenticity['consistency'] < 0.7:
            authenticity['issues'].append("情感表现不一致")
        if authenticity['depth'] < 0.6:
            authenticity['issues'].append("情感缺乏深度")
        if authenticity['believability'] < 0.7:
            authenticity['issues'].append("情感不够真实")
        
        return authenticity
    
    async def _predict_reader_impact(self, expressions: Dict) -> Dict:
        """预测读者影响"""
        impact = {
            'emotional_engagement': 0.0,
            'likely_reactions': [],
            'memorability': 0.0,
            'discussion_potential': 0.0
        }
        
        # 情感参与度
        impact['emotional_engagement'] = self._calculate_engagement_level(expressions)
        
        # 可能的读者反应
        impact['likely_reactions'] = self._predict_reader_reactions(expressions)
        
        # 记忆度
        impact['memorability'] = self._calculate_memorability(expressions)
        
        # 讨论潜力
        impact['discussion_potential'] = self._calculate_discussion_potential(expressions)
        
        return impact
    
    # 辅助方法
    def _map_themes_to_emotions(self, themes: List[str]) -> List[EmotionType]:
        """将主题映射到情感"""
        emotion_map = {
            'betrayal': EmotionType.ANGER,
            'love': EmotionType.LOVE,
            'loss': EmotionType.SADNESS,
            'hope': EmotionType.HOPE,
            'justice': EmotionType.PRIDE,
            'fear': EmotionType.FEAR,
            'mystery': EmotionType.ANXIETY
        }
        
        emotions = []
        for theme in themes:
            for keyword, emotion in emotion_map.items():
                if keyword in theme.lower():
                    emotions.append(emotion)
        
        return emotions if emotions else [EmotionType.ANXIETY]
    
    def _get_recent_emotions(self) -> List[EmotionType]:
        """获取最近的情感"""
        # 从历史中提取
        recent = []
        for entry in self.emotional_history[-5:]:
            if 'dominant_emotion' in entry:
                recent.append(entry['dominant_emotion'])
        return recent
    
    def _get_character_baseline(self, char_name: str, context: Dict) -> Dict:
        """获取角色情感基线"""
        if char_name in self.character_baselines:
            return self.character_baselines[char_name]
        
        # 从Bible中提取
        char_info = context.get('bible', {}).get('characters', {}).get(char_name, {})
        personality = char_info.get('personality', '')
        
        baseline = {
            'dominant': EmotionType.ANXIETY,  # 默认
            'underlying': None,
            'underlying_intensity': 0.3
        }
        
        if 'optimistic' in personality:
            baseline['dominant'] = EmotionType.HOPE
        elif 'melancholic' in personality:
            baseline['dominant'] = EmotionType.MELANCHOLY
        elif 'angry' in personality:
            baseline['dominant'] = EmotionType.ANGER
        
        self.character_baselines[char_name] = baseline
        return baseline
    
    def _determine_current_emotion(self, character: Dict, scene: Dict, context: Dict) -> Dict:
        """确定当前情感"""
        emotion_state = character.get('emotional_state', 'neutral')
        
        emotion_map = {
            'happy': (EmotionType.JOY, 0.7),
            'sad': (EmotionType.SADNESS, 0.7),
            'angry': (EmotionType.ANGER, 0.8),
            'fearful': (EmotionType.FEAR, 0.8),
            'surprised': (EmotionType.SURPRISE, 0.6),
            'disgusted': (EmotionType.DISGUST, 0.7),
            'anxious': (EmotionType.ANXIETY, 0.6),
            'neutral': (EmotionType.ANXIETY, 0.3)
        }
        
        emotion, intensity = emotion_map.get(emotion_state, (EmotionType.ANXIETY, 0.5))
        
        return {
            'surface': emotion,
            'intensity': intensity
        }
    
    def _identify_triggers(self, character: Dict, scene: Dict) -> List[str]:
        """识别情感触发器"""
        triggers = []
        
        # 场景事件触发
        if scene.get('events'):
            triggers.extend(scene['events'])
        
        # 角色交互触发
        if character.get('interactions'):
            triggers.extend(character['interactions'])
        
        return triggers
    
    def _estimate_duration(self, emotion: Dict) -> str:
        """估计情感持续时间"""
        intensity = emotion.get('intensity', 0.5)
        
        if intensity > 0.8:
            return 'arc'  # 贯穿故事弧
        elif intensity > 0.6:
            return 'chapter'  # 整章
        elif intensity > 0.4:
            return 'scene'  # 整个场景
        else:
            return 'moment'  # 瞬间
    
    def _predict_trajectory(self, character: Dict, scene: Dict, context: Dict) -> str:
        """预测情感轨迹"""
        scene_type = scene.get('type', '')
        
        if 'escalation' in scene_type:
            return 'rising'
        elif 'resolution' in scene_type:
            return 'falling'
        elif 'chaos' in scene_type:
            return 'volatile'
        else:
            return 'stable'
    
    def _get_expression_mode(self, emotion: EmotionType, intensity: float) -> str:
        """获取表达模式"""
        if intensity > 0.8:
            return 'explosive'
        elif intensity > 0.6:
            return 'overt'
        elif intensity > 0.4:
            return 'controlled'
        else:
            return 'subtle'
    
    def _generate_underlying_hints(self, state: EmotionalState) -> List[str]:
        """生成深层情感暗示"""
        hints = []
        
        if state.underlying_emotion == EmotionType.GUILT:
            hints.append("避免眼神接触")
            hints.append("过度解释")
        elif state.underlying_emotion == EmotionType.LOVE:
            hints.append("不自觉的微笑")
            hints.append("寻找接近机会")
        elif state.underlying_emotion == EmotionType.FEAR:
            hints.append("紧张的小动作")
            hints.append("过度警觉")
        
        return hints
    
    def _detect_subconscious_emotion(self, state: EmotionalState, context: Dict) -> Optional[Dict]:
        """检测潜意识情感"""
        # 简化实现
        if state.surface_emotion == EmotionType.ANGER:
            # 愤怒可能掩盖恐惧
            return {
                'emotion': EmotionType.FEAR.value,
                'intensity': 0.4,
                'manifestation': 'defensive_aggression'
            }
        return None
    
    def _select_reader_techniques(self, goal: str) -> List[str]:
        """选择读者情感技巧"""
        techniques_map = {
            'engagement': ['perspective_shift', 'sensory_detail', 'internal_monologue'],
            'catharsis': ['emotional_buildup', 'release_moment', 'reflection'],
            'shock': ['sudden_revelation', 'contrast', 'visceral_description'],
            'tension': ['uncertainty', 'countdown', 'conflicting_emotions'],
            'warmth': ['nostalgia', 'shared_experience', 'gentle_humor']
        }
        
        return techniques_map.get(goal, ['standard_narrative'])
    
    def _interpolate_emotion_state(
        self, char_name: str, progress: float,
        layers: Dict, context: Dict
    ) -> EmotionalState:
        """插值情感状态"""
        # 简化实现：基于进度调整强度
        base_state = EmotionalState(
            character=char_name,
            surface_emotion=EmotionType.ANXIETY,
            surface_intensity=0.5 + progress * 0.3
        )
        
        # 从层次中提取信息
        if char_name in layers['surface']:
            emotion_str = layers['surface'][char_name]['emotion']
            # 转换字符串回枚举
            for e in EmotionType:
                if e.value == emotion_str:
                    base_state.surface_emotion = e
                    break
            
            base_state.surface_intensity = layers['surface'][char_name]['intensity'] * (0.7 + progress * 0.3)
        
        return base_state
    
    def _interpolate_atmosphere(self, progress: float, atmospheric_layer: Dict) -> Dict[str, float]:
        """插值氛围"""
        atmosphere = {}
        
        for emotion, base_intensity in atmospheric_layer.items():
            # 使用正弦波创建起伏
            wave = math.sin(progress * math.pi)
            atmosphere[emotion] = base_intensity * (0.7 + wave * 0.3)
        
        return atmosphere
    
    def _calculate_beat_tension(self, progress: float, scene: Dict, context: Dict) -> float:
        """计算节拍紧张度"""
        base_tension = scene.get('tension_level', 0.5)
        
        # 紧张度曲线
        if scene.get('type') == 'climax':
            # 持续上升
            return min(1.0, base_tension + progress * 0.4)
        elif scene.get('type') == 'resolution':
            # 逐渐下降
            return max(0.1, base_tension * (1 - progress * 0.5))
        else:
            # 波动
            return base_tension + math.sin(progress * math.pi * 2) * 0.2
    
    def _detect_mood_shift(self, prev_beat: EmotionalBeat, current_states: Dict) -> bool:
        """检测情绪转换"""
        # 比较主要角色的情感
        for char_name, curr_state in current_states.items():
            if char_name in prev_beat.emotion_states:
                prev_state = prev_beat.emotion_states[char_name]
                if prev_state.surface_emotion != curr_state.surface_emotion:
                    return True
        return False
    
    def _describe_mood_shift(self, prev_beat: EmotionalBeat, current_states: Dict) -> str:
        """描述情绪转换"""
        # 简化实现
        return "emotional_transition"
    
    def _identify_catalyst(self, beat_index: int, scene: Dict) -> Optional[str]:
        """识别催化剂"""
        events = scene.get('events', [])
        if beat_index < len(events):
            return events[beat_index]
        return None
    
    def _find_complementary_mood(self, dominant: str) -> str:
        """找到互补情绪"""
        complements = {
            'joy': 'melancholy',
            'sadness': 'hope',
            'anger': 'regret',
            'fear': 'courage',
            'love': 'longing'
        }
        return complements.get(dominant, 'neutral')
    
    def _find_accent_mood(self, scene: Dict) -> str:
        """找到点缀情绪"""
        # 基于场景类型
        scene_type = scene.get('type', '')
        if 'mystery' in scene_type:
            return 'curiosity'
        elif 'action' in scene_type:
            return 'excitement'
        else:
            return 'anticipation'
    
    def _generate_sensory_elements(self, mood: str, scene: Dict) -> Dict:
        """生成感官元素"""
        elements = {
            'visual': [],
            'auditory': [],
            'tactile': [],
            'olfactory': [],
            'gustatory': []
        }
        
        mood_sensory = {
            'joy': {
                'visual': ['bright_colors', 'open_spaces'],
                'auditory': ['laughter', 'music'],
                'tactile': ['warmth', 'softness']
            },
            'sadness': {
                'visual': ['muted_colors', 'rain'],
                'auditory': ['silence', 'distant_sounds'],
                'tactile': ['cold', 'heaviness']
            },
            'fear': {
                'visual': ['shadows', 'movement'],
                'auditory': ['whispers', 'creaking'],
                'tactile': ['goosebumps', 'tension']
            }
        }
        
        if mood in mood_sensory:
            for sense, items in mood_sensory[mood].items():
                elements[sense] = items
        
        return elements
    
    def _generate_symbolic_elements(self, mood: str, context: Dict) -> List[str]:
        """生成象征元素"""
        symbols = {
            'joy': ['sunrise', 'flowers_blooming', 'birds_singing'],
            'sadness': ['wilting_flowers', 'setting_sun', 'empty_chair'],
            'fear': ['shadows_lengthening', 'clock_ticking', 'door_creaking'],
            'hope': ['first_light', 'seed_sprouting', 'clearing_sky']
        }
        
        return symbols.get(mood, ['neutral_imagery'])
    
    def _generate_color_palette(self, mood: str) -> List[str]:
        """生成色彩调色板"""
        palettes = {
            'joy': ['golden', 'bright_blue', 'warm_orange'],
            'sadness': ['grey', 'deep_blue', 'muted_purple'],
            'anger': ['red', 'black', 'dark_orange'],
            'fear': ['shadow', 'pale', 'sickly_green'],
            'love': ['soft_pink', 'warm_red', 'gentle_gold']
        }
        
        return palettes.get(mood, ['neutral_tones'])
    
    def _needs_transition(self, prev: EmotionalBeat, curr: EmotionalBeat) -> bool:
        """判断是否需要过渡"""
        # 紧张度差异大
        if abs(prev.tension - curr.tension) > 0.3:
            return True
        
        # 情绪转换剧烈
        if curr.mood_shift and 'dramatic' in curr.mood_shift:
            return True
        
        return False
    
    def _create_transition_beat(self, prev: EmotionalBeat, curr: EmotionalBeat) -> EmotionalBeat:
        """创建过渡节拍"""
        # 混合两个节拍
        transition_states = {}
        for char_name in prev.emotion_states:
            if char_name in curr.emotion_states:
                # 混合情感状态
                transition_states[char_name] = prev.emotion_states[char_name].blend_with(
                    curr.emotion_states[char_name]
                )
        
        return EmotionalBeat(
            timestamp=f"{prev.timestamp}_to_{curr.timestamp}",
            emotion_states=transition_states,
            atmosphere={k: (v + curr.atmosphere.get(k, 0)) / 2 
                        for k, v in prev.atmosphere.items()},
            tension=(prev.tension + curr.tension) / 2,
            mood_shift="transitioning"
        )
    
    def _identify_resonance_type(self, beat: EmotionalBeat) -> str:
        """识别共鸣类型"""
        # 基于情感强度和类型
        primary_emotions = []
        for state in beat.emotion_states.values():
            if state.surface_intensity > 0.7:
                primary_emotions.append(state.surface_emotion)
        
        if EmotionType.LOVE in primary_emotions:
            return 'universal_love'
        elif EmotionType.SADNESS in primary_emotions:
            return 'shared_loss'
        elif EmotionType.FEAR in primary_emotions:
            return 'primal_fear'
        else:
            return 'human_experience'
    
    def _select_resonance_technique(self, beat: EmotionalBeat, context: Dict) -> str:
        """选择共鸣技巧"""
        if beat.tension > 0.8:
            return 'visceral_description'
        elif beat.mood_shift:
            return 'emotional_mirror'
        else:
            return 'subtle_recognition'
    
    def _get_primary_emotion(self, beat: EmotionalBeat) -> str:
        """获取主要情感"""
        # 找到最强烈的情感
        max_emotion = None
        max_intensity = 0
        
        for state in beat.emotion_states.values():
            if state.surface_intensity > max_intensity:
                max_intensity = state.surface_intensity
                max_emotion = state.surface_emotion
        
        return max_emotion.value if max_emotion else 'neutral'
    
    def _map_to_universal_theme(self, beat: EmotionalBeat) -> str:
        """映射到普世主题"""
        primary = self._get_primary_emotion(beat)
        
        universal_themes = {
            'love': 'connection',
            'fear': 'survival',
            'sadness': 'loss',
            'joy': 'celebration',
            'anger': 'injustice'
        }
        
        return universal_themes.get(primary, 'human_condition')
    
    def _generate_physical_expression(self, state: EmotionalState) -> Dict:
        """生成身体表现"""
        expressions = {
            EmotionType.JOY: {'face': 'smile', 'body': 'relaxed', 'gesture': 'open'},
            EmotionType.SADNESS: {'face': 'downcast', 'body': 'slumped', 'gesture': 'withdrawn'},
            EmotionType.ANGER: {'face': 'furrowed', 'body': 'tense', 'gesture': 'clenched'},
            EmotionType.FEAR: {'face': 'wide_eyes', 'body': 'rigid', 'gesture': 'defensive'}
        }
        
        return expressions.get(state.surface_emotion, {'face': 'neutral', 'body': 'normal', 'gesture': 'still'})
    
    def _generate_verbal_expression(self, beat: EmotionalBeat) -> Optional[Dict]:
        """生成语言表现"""
        if beat.tension > 0.7:
            return {
                'style': 'fragmented',
                'pace': 'rapid',
                'volume': 'variable'
            }
        elif beat.tension < 0.3:
            return {
                'style': 'flowing',
                'pace': 'measured',
                'volume': 'soft'
            }
        return None
    
    def _generate_environmental_expression(self, beat: EmotionalBeat, atmosphere: Dict) -> Dict:
        """生成环境表现"""
        return {
            'lighting': 'dim' if beat.tension > 0.6 else 'soft',
            'weather': 'stormy' if beat.tension > 0.8 else 'calm',
            'ambiance': atmosphere.get('dominant_mood', 'neutral')
        }
    
    def _generate_narrative_expressions(self, beats: List[EmotionalBeat]) -> List[Dict]:
        """生成叙事表现"""
        expressions = []
        
        for beat in beats:
            if beat.tension > 0.7:
                expressions.append({
                    'sentence_length': 'short',
                    'paragraph_structure': 'fragmented',
                    'rhythm': 'staccato'
                })
            else:
                expressions.append({
                    'sentence_length': 'varied',
                    'paragraph_structure': 'flowing',
                    'rhythm': 'melodic'
                })
        
        return expressions
    
    def _generate_symbolic_expressions(self, resonance_points: List[Dict], atmosphere: Dict) -> List[Dict]:
        """生成象征表现"""
        expressions = []
        
        for point in resonance_points:
            expressions.append({
                'symbol': self._select_symbol(point['universal_theme']),
                'placement': f"beat_{point['beat_index']}",
                'intensity': point['intensity']
            })
        
        return expressions
    
    def _select_symbol(self, theme: str) -> str:
        """选择象征"""
        symbols = {
            'connection': 'intertwined_paths',
            'survival': 'flickering_flame',
            'loss': 'empty_frame',
            'celebration': 'raised_glass',
            'injustice': 'broken_scales'
        }
        return symbols.get(theme, 'abstract_form')
    
    def _extract_emotional_arc(self, beats: List[EmotionalBeat]) -> List[Tuple[str, float]]:
        """提取情感弧线"""
        arc = []
        for beat in beats:
            primary = self._get_primary_emotion(beat)
            avg_intensity = sum(s.surface_intensity for s in beat.emotion_states.values()) / len(beat.emotion_states) if beat.emotion_states else 0
            arc.append((primary, avg_intensity))
        return arc
    
    def _summarize_mood(self, atmosphere: Dict) -> str:
        """总结情绪"""
        dominant = atmosphere.get('dominant_mood', 'neutral')
        layers = atmosphere.get('mood_layers', [])
        
        if layers:
            secondary = layers[1]['primary'] if len(layers) > 1 else 'none'
            return f"{dominant}_with_{secondary}_undertones"
        
        return dominant
    
    def _check_emotional_consistency(self, expressions: Dict) -> float:
        """检查情感一致性"""
        # 简化实现
        return 0.85
    
    def _check_emotional_depth(self, expressions: Dict) -> float:
        """检查情感深度"""
        # 简化实现
        return 0.8
    
    def _check_believability(self, expressions: Dict) -> float:
        """检查可信度"""
        # 简化实现
        return 0.87
    
    def _check_emotional_impact(self, expressions: Dict) -> float:
        """检查情感影响"""
        # 简化实现
        return 0.9
    
    def _calculate_engagement_level(self, expressions: Dict) -> float:
        """计算参与度"""
        # 简化实现
        return 0.85
    
    def _predict_reader_reactions(self, expressions: Dict) -> List[str]:
        """预测读者反应"""
        # 简化实现
        return ['empathy', 'tension', 'satisfaction']
    
    def _calculate_memorability(self, expressions: Dict) -> float:
        """计算记忆度"""
        # 简化实现
        return 0.75
    
    def _calculate_discussion_potential(self, expressions: Dict) -> float:
        """计算讨论潜力"""
        # 简化实现
        return 0.7


class AtmosphereBuilder:
    """氛围构建器"""
    
    async def build(self, states: Dict, requirements: Dict, context: Dict) -> Dict:
        """构建氛围"""
        atmosphere = {}
        
        # 基于角色情感构建
        emotion_counts = {}
        for state in states.values():
            emotion = state.surface_emotion.value
            if emotion not in emotion_counts:
                emotion_counts[emotion] = 0
            emotion_counts[emotion] += state.surface_intensity
        
        # 标准化
        total = sum(emotion_counts.values())
        if total > 0:
            for emotion, count in emotion_counts.items():
                atmosphere[emotion] = count / total
        
        return atmosphere


class EmotionTransitionSmoother:
    """情感过渡平滑器"""
    
    def smooth(self, beats: List[EmotionalBeat]) -> List[EmotionalBeat]:
        """平滑过渡"""
        # 简化实现
        return beats


class ResonanceCalculator:
    """共鸣计算器"""
    
    def calculate(self, beat: EmotionalBeat, context: Dict) -> float:
        """计算共鸣潜力"""
        # 基于情感强度和普遍性
        max_intensity = max(s.surface_intensity for s in beat.emotion_states.values()) if beat.emotion_states else 0
        
        # 某些情感更容易产生共鸣
        resonant_emotions = [EmotionType.LOVE, EmotionType.SADNESS, EmotionType.FEAR, EmotionType.JOY]
        has_resonant = any(s.surface_emotion in resonant_emotions for s in beat.emotion_states.values())
        
        base_resonance = max_intensity * 0.7
        if has_resonant:
            base_resonance += 0.2
        
        return min(1.0, base_resonance)


class EmotionMapper:
    """情感映射器"""
    
    def map_to_expression(self, emotion: EmotionType, intensity: float) -> str:
        """映射到表达"""
        if intensity > 0.8:
            return f"intense_{emotion.value}"
        elif intensity > 0.5:
            return f"moderate_{emotion.value}"
        else:
            return f"subtle_{emotion.value}"


# 测试函数
async def test_emotion_weaver():
    """测试情感编织Stream"""
    stream = EmotionWeaverStream()
    
    # 测试场景
    test_scene = {
        'id': 'ch5_sc3',
        'type': 'betrayal_revelation',
        'importance': 'critical',
        'estimated_length': 1500,
        'tension_level': 0.8,
        'characters': [
            {'name': '李明', 'emotional_state': 'shocked'},
            {'name': '王伟', 'emotional_state': 'guilty'}
        ],
        'events': ['truth_revealed', 'confrontation', 'breakdown']
    }
    
    # 测试上下文
    test_context = {
        'bible': {
            'series_info': {
                'themes': ['betrayal', 'trust', 'redemption']
            },
            'characters': {
                '李明': {
                    'personality': 'trusting analytical'
                },
                '王伟': {
                    'personality': 'conflicted guilty'
                }
            }
        }
    }
    
    # 运行测试
    result = await stream.generate(test_scene, test_context)
    
    print("情感编织结果：")
    print(f"情感真实性: {result['authenticity']['overall_score']:.2f}")
    print(f"氛围总结: {result['mood_summary']}")
    print(f"情感弧线: {result['emotional_arc']}")
    print(f"读者影响预测: {json.dumps(result['impact_prediction'], indent=2, ensure_ascii=False)}")
    
    return result


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_emotion_weaver())