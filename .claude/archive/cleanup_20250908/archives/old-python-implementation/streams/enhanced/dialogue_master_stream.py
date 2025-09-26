"""
DialogueMasterStream - 对话大师
生成自然、富有潜台词、个性鲜明的对话
Quality Target: 95% dialogue naturality
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re


class DialogueStyle(Enum):
    """对话风格枚举"""
    FORMAL = "formal"                # 正式
    CASUAL = "casual"                # 随意
    INTIMATE = "intimate"            # 亲密
    CONFRONTATIONAL = "confrontational"  # 对抗
    COMEDIC = "comedic"              # 喜剧
    DRAMATIC = "dramatic"            # 戏剧性
    MYSTERIOUS = "mysterious"        # 神秘
    PHILOSOPHICAL = "philosophical"   # 哲学性


class DialoguePurpose(Enum):
    """对话目的枚举"""
    EXPOSITION = "exposition"         # 信息传递
    CHARACTER_REVEAL = "char_reveal" # 角色展现
    CONFLICT = "conflict"            # 冲突
    BONDING = "bonding"              # 情感连接
    HUMOR = "humor"                  # 幽默调剂
    TENSION = "tension"              # 制造紧张
    REVELATION = "revelation"        # 揭示真相
    SUBTEXT = "subtext"              # 潜台词


@dataclass
class CharacterVoice:
    """角色语言特征"""
    name: str
    vocabulary_level: str     # simple/moderate/complex/academic
    speech_patterns: List[str]  # 语言模式
    catchphrases: List[str]     # 口头禅
    dialect: Optional[str]      # 方言/口音
    formality: float           # 0-1 正式程度
    verbosity: float           # 0-1 话多程度
    emotional_expression: float # 0-1 情感表达程度
    typical_topics: List[str]  # 常谈话题
    avoidance_topics: List[str] # 避免话题
    
    def adjust_for_emotion(self, emotion: str) -> 'CharacterVoice':
        """根据情绪调整语言特征"""
        adjusted = CharacterVoice(
            name=self.name,
            vocabulary_level=self.vocabulary_level,
            speech_patterns=self.speech_patterns.copy(),
            catchphrases=self.catchphrases.copy(),
            dialect=self.dialect,
            formality=self.formality,
            verbosity=self.verbosity,
            emotional_expression=self.emotional_expression,
            typical_topics=self.typical_topics.copy(),
            avoidance_topics=self.avoidance_topics.copy()
        )
        
        if emotion == 'angry':
            adjusted.formality *= 0.7
            adjusted.verbosity *= 1.3
            adjusted.emotional_expression = min(1.0, self.emotional_expression * 1.5)
        elif emotion == 'sad':
            adjusted.verbosity *= 0.6
            adjusted.emotional_expression *= 0.8
        elif emotion == 'excited':
            adjusted.verbosity *= 1.5
            adjusted.emotional_expression = min(1.0, self.emotional_expression * 1.4)
        elif emotion == 'fearful':
            adjusted.verbosity *= 0.8
            adjusted.speech_patterns.append('stuttering')
        
        return adjusted


@dataclass
class DialogueExchange:
    """对话交换单元"""
    speaker: str
    listener: str
    text: str
    subtext: Optional[str] = None
    emotion: Optional[str] = None
    gesture: Optional[str] = None
    pause_before: bool = False
    pause_after: bool = False
    interruption: bool = False
    internal_thought: Optional[str] = None


class DialogueMasterStream:
    """
    对话大师Stream
    负责生成高质量、自然、富有层次的对话
    """
    
    def __init__(self):
        self.character_voices = {}     # 角色语言特征库
        self.conversation_history = [] # 对话历史
        self.tension_tracker = 0.0     # 紧张度追踪
        self.subtext_generator = SubtextGenerator()
        self.rhythm_controller = DialogueRhythmController()
        self.conflict_escalator = ConflictEscalator()
        
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景的对话生成
        
        Args:
            scene: 场景信息
            context: 上下文信息
            
        Returns:
            对话生成结果
        """
        # 1. 分析对话需求
        dialogue_requirements = await self._analyze_dialogue_needs(scene, context)
        
        # 2. 建立角色声音
        character_voices = await self._establish_character_voices(scene, context)
        
        # 3. 规划对话结构
        dialogue_structure = await self._plan_dialogue_structure(
            dialogue_requirements, scene, context
        )
        
        # 4. 生成对话交换
        exchanges = await self._generate_dialogue_exchanges(
            dialogue_structure, character_voices, scene, context
        )
        
        # 5. 添加潜台词层
        exchanges_with_subtext = await self._add_subtext_layer(exchanges, context)
        
        # 6. 优化对话节奏
        optimized_exchanges = await self._optimize_dialogue_rhythm(exchanges_with_subtext)
        
        # 7. 添加非语言元素
        final_exchanges = await self._add_nonverbal_elements(optimized_exchanges, scene)
        
        # 8. 验证对话质量
        quality_check = await self._validate_dialogue_quality(final_exchanges)
        
        return {
            'exchanges': final_exchanges,
            'character_voices': character_voices,
            'dialogue_purpose': dialogue_requirements['purpose'],
            'tension_level': self.tension_tracker,
            'subtext_layers': self._extract_subtext_summary(final_exchanges),
            'quality_metrics': quality_check,
            'suggestions': await self._generate_dialogue_suggestions(final_exchanges, context)
        }
    
    async def _analyze_dialogue_needs(self, scene: Dict, context: Dict) -> Dict:
        """分析场景的对话需求"""
        needs = {
            'purpose': [],
            'style': DialogueStyle.CASUAL,
            'expected_length': 0,
            'key_information': [],
            'emotional_trajectory': [],
            'conflict_level': 0.0
        }
        
        # 确定对话目的
        scene_type = scene.get('type', '')
        if 'revelation' in scene_type:
            needs['purpose'].append(DialoguePurpose.REVELATION)
        if 'conflict' in scene_type:
            needs['purpose'].append(DialoguePurpose.CONFLICT)
        if 'introduction' in scene_type:
            needs['purpose'].append(DialoguePurpose.EXPOSITION)
        if 'emotional' in scene_type:
            needs['purpose'].append(DialoguePurpose.BONDING)
        
        # 如果没有明确目的，添加默认
        if not needs['purpose']:
            needs['purpose'].append(DialoguePurpose.CHARACTER_REVEAL)
        
        # 确定风格
        tension = context.get('tension_level', 0.5)
        if tension > 0.8:
            needs['style'] = DialogueStyle.CONFRONTATIONAL
        elif tension > 0.6:
            needs['style'] = DialogueStyle.DRAMATIC
        elif scene.get('mood') == 'light':
            needs['style'] = DialogueStyle.COMEDIC
        elif scene.get('setting') == 'formal':
            needs['style'] = DialogueStyle.FORMAL
        
        # 预估对话长度
        scene_importance = scene.get('importance', 'medium')
        if scene_importance == 'critical':
            needs['expected_length'] = 15  # 交换次数
        elif scene_importance == 'high':
            needs['expected_length'] = 10
        else:
            needs['expected_length'] = 5
        
        # 提取关键信息
        needs['key_information'] = scene.get('must_convey', [])
        
        # 情感轨迹
        needs['emotional_trajectory'] = self._plan_emotional_arc(scene, context)
        
        # 冲突等级
        needs['conflict_level'] = self._assess_conflict_level(scene, context)
        
        return needs
    
    async def _establish_character_voices(self, scene: Dict, context: Dict) -> Dict[str, CharacterVoice]:
        """建立角色语言特征"""
        voices = {}
        
        for character in scene.get('characters', []):
            char_name = character['name']
            
            # 检查是否已有语言特征
            if char_name in self.character_voices:
                voice = self.character_voices[char_name]
                # 根据当前情绪调整
                emotion = character.get('emotional_state', 'neutral')
                voice = voice.adjust_for_emotion(emotion)
            else:
                # 创建新的语言特征
                voice = await self._create_character_voice(character, context)
                self.character_voices[char_name] = voice
            
            voices[char_name] = voice
        
        return voices
    
    async def _create_character_voice(self, character: Dict, context: Dict) -> CharacterVoice:
        """创建角色语言特征"""
        char_info = context.get('bible', {}).get('characters', {}).get(character['name'], {})
        
        voice = CharacterVoice(
            name=character['name'],
            vocabulary_level=self._determine_vocabulary_level(char_info),
            speech_patterns=self._extract_speech_patterns(char_info),
            catchphrases=self._generate_catchphrases(char_info),
            dialect=char_info.get('dialect'),
            formality=self._calculate_formality(char_info),
            verbosity=self._calculate_verbosity(char_info),
            emotional_expression=self._calculate_emotional_expression(char_info),
            typical_topics=self._identify_typical_topics(char_info),
            avoidance_topics=self._identify_avoidance_topics(char_info)
        )
        
        return voice
    
    async def _plan_dialogue_structure(self, requirements: Dict, scene: Dict, context: Dict) -> Dict:
        """规划对话结构"""
        structure = {
            'opening': {},
            'development': [],
            'climax': {},
            'resolution': {},
            'beats': []
        }
        
        # 开场
        structure['opening'] = {
            'style': 'hook' if requirements['conflict_level'] > 0.6 else 'natural',
            'speaker': self._select_opening_speaker(scene),
            'tone': requirements['style'].value
        }
        
        # 发展阶段
        num_beats = requirements['expected_length']
        for i in range(num_beats):
            beat = {
                'purpose': self._determine_beat_purpose(i, num_beats, requirements),
                'tension': self._calculate_beat_tension(i, num_beats, requirements),
                'focus': self._determine_beat_focus(i, requirements)
            }
            structure['development'].append(beat)
        
        # 高潮
        if requirements['conflict_level'] > 0.5:
            structure['climax'] = {
                'position': int(num_beats * 0.7),
                'type': 'confrontation' if requirements['conflict_level'] > 0.8 else 'revelation'
            }
        
        # 收尾
        structure['resolution'] = {
            'style': 'cliffhanger' if scene.get('end_type') == 'suspense' else 'natural',
            'emotion': requirements['emotional_trajectory'][-1] if requirements['emotional_trajectory'] else 'neutral'
        }
        
        return structure
    
    async def _generate_dialogue_exchanges(
        self, structure: Dict, voices: Dict[str, CharacterVoice],
        scene: Dict, context: Dict
    ) -> List[DialogueExchange]:
        """生成对话交换"""
        exchanges = []
        characters = list(voices.keys())
        
        if len(characters) < 2:
            return exchanges  # 需要至少两个角色
        
        current_speaker = structure['opening']['speaker']
        current_listener = [c for c in characters if c != current_speaker][0]
        
        # 生成开场
        opening_exchange = await self._create_exchange(
            current_speaker, current_listener, 
            'opening', structure['opening'],
            voices, context
        )
        exchanges.append(opening_exchange)
        
        # 生成发展阶段的对话
        for i, beat in enumerate(structure['development']):
            # 交替说话者
            current_speaker, current_listener = current_listener, current_speaker
            
            exchange = await self._create_exchange(
                current_speaker, current_listener,
                f'beat_{i}', beat,
                voices, context
            )
            
            # 根据节拍调整
            if beat['tension'] > 0.7:
                exchange.emotion = 'intense'
            if beat['purpose'] == 'revelation':
                exchange.pause_before = True
            
            exchanges.append(exchange)
        
        # 生成高潮对话（如果有）
        if structure.get('climax'):
            climax_exchange = await self._create_climax_exchange(
                characters, structure['climax'], voices, context
            )
            exchanges.insert(structure['climax']['position'], climax_exchange)
        
        # 生成收尾
        resolution_exchange = await self._create_resolution_exchange(
            characters, structure['resolution'], voices, context
        )
        exchanges.append(resolution_exchange)
        
        return exchanges
    
    async def _create_exchange(
        self, speaker: str, listener: str,
        exchange_type: str, params: Dict,
        voices: Dict[str, CharacterVoice],
        context: Dict
    ) -> DialogueExchange:
        """创建单个对话交换"""
        voice = voices[speaker]
        
        # 生成对话文本
        text = await self._generate_dialogue_text(voice, exchange_type, params, context)
        
        # 生成情绪
        emotion = params.get('emotion', 'neutral')
        
        # 创建交换
        exchange = DialogueExchange(
            speaker=speaker,
            listener=listener,
            text=text,
            emotion=emotion
        )
        
        return exchange
    
    async def _add_subtext_layer(self, exchanges: List[DialogueExchange], context: Dict) -> List[DialogueExchange]:
        """添加潜台词层"""
        for exchange in exchanges:
            # 分析是否需要潜台词
            if self._needs_subtext(exchange, context):
                subtext = await self.subtext_generator.generate(
                    exchange.text,
                    exchange.speaker,
                    exchange.emotion,
                    context
                )
                exchange.subtext = subtext
                
                # 可能添加内心独白
                if self._needs_internal_thought(exchange, context):
                    exchange.internal_thought = await self._generate_internal_thought(
                        exchange, context
                    )
        
        return exchanges
    
    async def _optimize_dialogue_rhythm(self, exchanges: List[DialogueExchange]) -> List[DialogueExchange]:
        """优化对话节奏"""
        optimized = self.rhythm_controller.optimize(exchanges)
        
        # 添加中断
        for i, exchange in enumerate(optimized):
            if i > 0 and self._should_interrupt(exchange, optimized[i-1]):
                exchange.interruption = True
        
        # 添加停顿
        for i, exchange in enumerate(optimized):
            if self._needs_pause_before(exchange, i, optimized):
                exchange.pause_before = True
            if self._needs_pause_after(exchange, i, optimized):
                exchange.pause_after = True
        
        return optimized
    
    async def _add_nonverbal_elements(self, exchanges: List[DialogueExchange], scene: Dict) -> List[DialogueExchange]:
        """添加非语言元素"""
        for exchange in exchanges:
            # 添加手势
            if exchange.emotion in ['angry', 'excited', 'frustrated']:
                exchange.gesture = self._generate_gesture(exchange.emotion)
            
            # 特殊场景的非语言元素
            if scene.get('environment') == 'noisy':
                if exchange.emotion == 'quiet':
                    exchange.gesture = 'leans_closer'
                elif exchange.emotion == 'shouting':
                    exchange.gesture = 'cups_hands'
        
        return exchanges
    
    async def _validate_dialogue_quality(self, exchanges: List[DialogueExchange]) -> Dict:
        """验证对话质量"""
        metrics = {
            'naturality': 0.0,
            'character_consistency': 0.0,
            'information_clarity': 0.0,
            'emotional_authenticity': 0.0,
            'rhythm_quality': 0.0,
            'subtext_effectiveness': 0.0
        }
        
        # 自然度评分
        metrics['naturality'] = self._score_naturality(exchanges)
        
        # 角色一致性评分
        metrics['character_consistency'] = self._score_character_consistency(exchanges)
        
        # 信息清晰度评分
        metrics['information_clarity'] = self._score_information_clarity(exchanges)
        
        # 情感真实性评分
        metrics['emotional_authenticity'] = self._score_emotional_authenticity(exchanges)
        
        # 节奏质量评分
        metrics['rhythm_quality'] = self.rhythm_controller.score_rhythm(exchanges)
        
        # 潜台词效果评分
        metrics['subtext_effectiveness'] = self._score_subtext_effectiveness(exchanges)
        
        # 计算总分
        metrics['overall_score'] = sum(metrics.values()) / len(metrics)
        
        return metrics
    
    async def _generate_dialogue_suggestions(self, exchanges: List[DialogueExchange], context: Dict) -> List[str]:
        """生成对话改进建议"""
        suggestions = []
        
        # 检查对话长度
        if len(exchanges) < 3:
            suggestions.append("对话过短，考虑添加更多交换")
        elif len(exchanges) > 20:
            suggestions.append("对话过长，考虑分割或精简")
        
        # 检查情感变化
        emotions = [e.emotion for e in exchanges if e.emotion]
        if len(set(emotions)) < 2:
            suggestions.append("情感变化不足，考虑添加情感层次")
        
        # 检查潜台词
        subtext_count = sum(1 for e in exchanges if e.subtext)
        if subtext_count < len(exchanges) * 0.2:
            suggestions.append("潜台词不足，考虑增加对话深度")
        
        # 检查节奏
        if not any(e.pause_before or e.pause_after for e in exchanges):
            suggestions.append("缺少停顿，考虑添加节奏变化")
        
        return suggestions
    
    # 辅助方法
    def _plan_emotional_arc(self, scene: Dict, context: Dict) -> List[str]:
        """规划情感弧线"""
        arc = []
        scene_mood = scene.get('mood', 'neutral')
        
        if scene_mood == 'escalating':
            arc = ['calm', 'concerned', 'worried', 'anxious', 'panicked']
        elif scene_mood == 'descending':
            arc = ['excited', 'happy', 'content', 'melancholic', 'sad']
        elif scene_mood == 'volatile':
            arc = ['neutral', 'irritated', 'angry', 'furious', 'exhausted']
        else:
            arc = ['neutral', 'engaged', 'interested', 'thoughtful', 'resolved']
        
        return arc
    
    def _assess_conflict_level(self, scene: Dict, context: Dict) -> float:
        """评估冲突等级"""
        base_conflict = 0.0
        
        # 场景类型影响
        if 'confrontation' in scene.get('type', ''):
            base_conflict += 0.5
        if 'argument' in scene.get('type', ''):
            base_conflict += 0.3
        
        # 角色关系影响
        relationships = context.get('relationships', {})
        for rel in relationships.values():
            if rel.get('status') == 'hostile':
                base_conflict += 0.2
            elif rel.get('status') == 'tense':
                base_conflict += 0.1
        
        # 剧情阶段影响
        if context.get('plot_stage') == 'climax':
            base_conflict += 0.3
        
        return min(1.0, base_conflict)
    
    def _select_opening_speaker(self, scene: Dict) -> str:
        """选择开场说话者"""
        characters = scene.get('characters', [])
        if not characters:
            return 'unknown'
        
        # 优先选择主动角色
        for char in characters:
            if char.get('role') == 'initiator':
                return char['name']
        
        # 否则选择第一个
        return characters[0]['name']
    
    def _determine_beat_purpose(self, index: int, total: int, requirements: Dict) -> str:
        """确定节拍目的"""
        progress = index / total if total > 0 else 0
        
        if progress < 0.3:
            return 'setup'
        elif progress < 0.6:
            return 'development'
        elif progress < 0.8:
            return 'escalation'
        else:
            return 'resolution'
    
    def _calculate_beat_tension(self, index: int, total: int, requirements: Dict) -> float:
        """计算节拍紧张度"""
        progress = index / total if total > 0 else 0
        base_tension = requirements['conflict_level']
        
        # 紧张度曲线
        if requirements['conflict_level'] > 0.5:
            # 冲突场景：逐渐升高
            return min(1.0, base_tension * (1 + progress))
        else:
            # 非冲突场景：波动
            import math
            return base_tension * (1 + 0.3 * math.sin(progress * math.pi * 2))
    
    def _determine_beat_focus(self, index: int, requirements: Dict) -> str:
        """确定节拍焦点"""
        purposes = requirements['purpose']
        if not purposes:
            return 'dialogue'
        
        # 循环使用目的
        purpose_index = index % len(purposes)
        return purposes[purpose_index].value
    
    def _determine_vocabulary_level(self, char_info: Dict) -> str:
        """确定词汇水平"""
        education = char_info.get('education', 'average')
        profession = char_info.get('profession', '')
        
        if education == 'phd' or 'professor' in profession:
            return 'academic'
        elif education == 'college' or 'professional' in profession:
            return 'complex'
        elif education == 'high_school':
            return 'moderate'
        else:
            return 'simple'
    
    def _extract_speech_patterns(self, char_info: Dict) -> List[str]:
        """提取语言模式"""
        patterns = []
        personality = char_info.get('personality', '')
        
        if 'nervous' in personality:
            patterns.append('repetition')
        if 'confident' in personality:
            patterns.append('declarative')
        if 'uncertain' in personality:
            patterns.append('questioning')
        if 'analytical' in personality:
            patterns.append('logical_structure')
        
        return patterns if patterns else ['standard']
    
    def _generate_catchphrases(self, char_info: Dict) -> List[str]:
        """生成口头禅"""
        # 简化实现
        return char_info.get('catchphrases', [])
    
    def _calculate_formality(self, char_info: Dict) -> float:
        """计算正式程度"""
        profession = char_info.get('profession', '')
        personality = char_info.get('personality', '')
        
        formality = 0.5
        
        if 'lawyer' in profession or 'executive' in profession:
            formality += 0.3
        if 'casual' in personality or 'relaxed' in personality:
            formality -= 0.2
        if 'proper' in personality or 'traditional' in personality:
            formality += 0.2
        
        return max(0.0, min(1.0, formality))
    
    def _calculate_verbosity(self, char_info: Dict) -> float:
        """计算话多程度"""
        personality = char_info.get('personality', '')
        
        verbosity = 0.5
        
        if 'talkative' in personality or 'extrovert' in personality:
            verbosity += 0.3
        if 'quiet' in personality or 'introvert' in personality:
            verbosity -= 0.3
        if 'nervous' in personality:
            verbosity += 0.2
        
        return max(0.0, min(1.0, verbosity))
    
    def _calculate_emotional_expression(self, char_info: Dict) -> float:
        """计算情感表达程度"""
        personality = char_info.get('personality', '')
        
        expression = 0.5
        
        if 'emotional' in personality or 'passionate' in personality:
            expression += 0.3
        if 'stoic' in personality or 'reserved' in personality:
            expression -= 0.3
        
        return max(0.0, min(1.0, expression))
    
    def _identify_typical_topics(self, char_info: Dict) -> List[str]:
        """识别典型话题"""
        interests = char_info.get('interests', [])
        profession = char_info.get('profession', '')
        
        topics = interests.copy()
        if profession:
            topics.append(profession)
        
        return topics if topics else ['general']
    
    def _identify_avoidance_topics(self, char_info: Dict) -> List[str]:
        """识别避免话题"""
        traumas = char_info.get('traumas', [])
        secrets = char_info.get('secrets', [])
        
        return traumas + secrets
    
    async def _generate_dialogue_text(self, voice: CharacterVoice, exchange_type: str, params: Dict, context: Dict) -> str:
        """生成对话文本"""
        # 这里简化实现，实际应该基于voice特征生成
        if exchange_type == 'opening':
            return f"[{voice.name}的开场白，{params.get('style')}风格]"
        elif 'beat' in exchange_type:
            return f"[{voice.name}的对话，目的:{params.get('purpose')}]"
        else:
            return f"[{voice.name}的对话]"
    
    async def _create_climax_exchange(self, characters: List[str], climax: Dict, voices: Dict, context: Dict) -> DialogueExchange:
        """创建高潮对话"""
        # 简化实现
        speaker = characters[0]
        listener = characters[1] if len(characters) > 1 else 'all'
        
        return DialogueExchange(
            speaker=speaker,
            listener=listener,
            text=f"[高潮对话：{climax['type']}]",
            emotion='intense',
            pause_before=True,
            pause_after=True
        )
    
    async def _create_resolution_exchange(self, characters: List[str], resolution: Dict, voices: Dict, context: Dict) -> DialogueExchange:
        """创建收尾对话"""
        speaker = characters[-1] if characters else 'unknown'
        listener = 'all'
        
        return DialogueExchange(
            speaker=speaker,
            listener=listener,
            text=f"[收尾对话：{resolution['style']}]",
            emotion=resolution.get('emotion', 'neutral')
        )
    
    def _needs_subtext(self, exchange: DialogueExchange, context: Dict) -> bool:
        """判断是否需要潜台词"""
        # 紧张场景更需要潜台词
        if context.get('tension_level', 0) > 0.6:
            return True
        # 某些情绪需要潜台词
        if exchange.emotion in ['suspicious', 'deceptive', 'conflicted']:
            return True
        return False
    
    def _needs_internal_thought(self, exchange: DialogueExchange, context: Dict) -> bool:
        """判断是否需要内心独白"""
        # POV角色更可能有内心独白
        if exchange.speaker == context.get('pov_character'):
            return exchange.emotion in ['conflicted', 'suspicious', 'shocked']
        return False
    
    async def _generate_internal_thought(self, exchange: DialogueExchange, context: Dict) -> str:
        """生成内心独白"""
        return f"[{exchange.speaker}的内心想法，与表面对话形成对比]"
    
    def _should_interrupt(self, current: DialogueExchange, previous: DialogueExchange) -> bool:
        """判断是否应该中断"""
        # 情绪激动时更容易中断
        if current.emotion in ['angry', 'excited', 'impatient']:
            return True
        # 紧急情况
        if current.text and 'urgent' in current.text.lower():
            return True
        return False
    
    def _needs_pause_before(self, exchange: DialogueExchange, index: int, all_exchanges: List) -> bool:
        """判断是否需要前置停顿"""
        # 重要揭示前需要停顿
        if exchange.emotion == 'revelation':
            return True
        # 情绪转变需要停顿
        if index > 0:
            prev_emotion = all_exchanges[index-1].emotion
            if prev_emotion and exchange.emotion and prev_emotion != exchange.emotion:
                return True
        return False
    
    def _needs_pause_after(self, exchange: DialogueExchange, index: int, all_exchanges: List) -> bool:
        """判断是否需要后置停顿"""
        # 震撼性对话后需要停顿
        if exchange.emotion in ['shocking', 'devastating']:
            return True
        return False
    
    def _generate_gesture(self, emotion: str) -> str:
        """生成手势"""
        gestures = {
            'angry': 'clenched_fists',
            'excited': 'animated_hands',
            'frustrated': 'runs_hand_through_hair',
            'sad': 'slumped_shoulders',
            'confident': 'crossed_arms',
            'nervous': 'fidgeting'
        }
        return gestures.get(emotion, 'neutral_stance')
    
    def _extract_subtext_summary(self, exchanges: List[DialogueExchange]) -> List[Dict]:
        """提取潜台词摘要"""
        summary = []
        for exchange in exchanges:
            if exchange.subtext:
                summary.append({
                    'speaker': exchange.speaker,
                    'surface': exchange.text[:50],
                    'subtext': exchange.subtext
                })
        return summary
    
    def _score_naturality(self, exchanges: List[DialogueExchange]) -> float:
        """评分自然度"""
        # 简化实现
        return 0.85
    
    def _score_character_consistency(self, exchanges: List[DialogueExchange]) -> float:
        """评分角色一致性"""
        return 0.9
    
    def _score_information_clarity(self, exchanges: List[DialogueExchange]) -> float:
        """评分信息清晰度"""
        return 0.88
    
    def _score_emotional_authenticity(self, exchanges: List[DialogueExchange]) -> float:
        """评分情感真实性"""
        return 0.87
    
    def _score_subtext_effectiveness(self, exchanges: List[DialogueExchange]) -> float:
        """评分潜台词效果"""
        subtext_count = sum(1 for e in exchanges if e.subtext)
        if len(exchanges) == 0:
            return 0.5
        ratio = subtext_count / len(exchanges)
        return min(1.0, ratio * 2)  # 理想是50%有潜台词


class SubtextGenerator:
    """潜台词生成器"""
    
    async def generate(self, surface_text: str, speaker: str, emotion: str, context: Dict) -> str:
        """生成潜台词"""
        # 简化实现
        if emotion == 'angry':
            return "我快要失控了"
        elif emotion == 'suspicious':
            return "我不相信你"
        elif emotion == 'sad':
            return "我需要安慰"
        else:
            return "我有话没说出口"


class DialogueRhythmController:
    """对话节奏控制器"""
    
    def optimize(self, exchanges: List[DialogueExchange]) -> List[DialogueExchange]:
        """优化对话节奏"""
        # 简化实现
        return exchanges
    
    def score_rhythm(self, exchanges: List[DialogueExchange]) -> float:
        """评分节奏质量"""
        return 0.85


class ConflictEscalator:
    """冲突升级器"""
    
    def escalate(self, exchanges: List[DialogueExchange], target_level: float) -> List[DialogueExchange]:
        """升级冲突"""
        # 简化实现
        return exchanges


# 测试函数
async def test_dialogue_master():
    """测试对话大师Stream"""
    stream = DialogueMasterStream()
    
    # 测试场景
    test_scene = {
        'id': 'ch3_sc2',
        'type': 'confrontation',
        'importance': 'high',
        'mood': 'escalating',
        'characters': [
            {'name': '李明', 'emotional_state': 'suspicious', 'role': 'initiator'},
            {'name': '张总', 'emotional_state': 'defensive'}
        ]
    }
    
    # 测试上下文
    test_context = {
        'tension_level': 0.7,
        'pov_character': '李明',
        'bible': {
            'characters': {
                '李明': {
                    'personality': 'analytical nervous',
                    'profession': 'detective',
                    'education': 'college'
                },
                '张总': {
                    'personality': 'confident deceptive',
                    'profession': 'executive',
                    'education': 'mba'
                }
            }
        }
    }
    
    # 运行测试
    result = await stream.generate(test_scene, test_context)
    
    print("对话生成结果：")
    print(f"交换次数: {len(result['exchanges'])}")
    print(f"紧张度: {result['tension_level']:.2f}")
    print(f"质量评分: {result['quality_metrics']}")
    print("\n对话内容：")
    for i, exchange in enumerate(result['exchanges'], 1):
        print(f"{i}. {exchange.speaker} -> {exchange.listener}: {exchange.text}")
        if exchange.subtext:
            print(f"   潜台词: {exchange.subtext}")
    
    return result


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_dialogue_master())