"""
Prose Craft Stream
文笔工艺Stream - 极致品质系统核心组件
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime
import re

class ProseTechnique(Enum):
    """文笔技巧"""
    METAPHOR = "metaphor"              # 隐喻
    SIMILE = "simile"                  # 明喻
    PERSONIFICATION = "personification"  # 拟人
    SYMBOLISM = "symbolism"            # 象征
    IMAGERY = "imagery"                # 意象
    ALLITERATION = "alliteration"      # 头韵
    ASSONANCE = "assonance"            # 元音韵
    ONOMATOPOEIA = "onomatopoeia"      # 拟声
    PARALLELISM = "parallelism"        # 排比
    REPETITION = "repetition"          # 重复

class SentenceType(Enum):
    """句子类型"""
    SIMPLE = "simple"                  # 简单句
    COMPOUND = "compound"              # 并列句
    COMPLEX = "complex"                # 复合句
    COMPOUND_COMPLEX = "compound_complex"  # 并列复合句
    FRAGMENT = "fragment"              # 句子片段（用于效果）

class ParagraphFunction(Enum):
    """段落功能"""
    EXPOSITION = "exposition"          # 说明
    DESCRIPTION = "description"        # 描写
    NARRATION = "narration"           # 叙述
    DIALOGUE = "dialogue"             # 对话
    TRANSITION = "transition"         # 过渡
    CLIMAX = "climax"                # 高潮
    REFLECTION = "reflection"         # 反思

@dataclass
class StyleProfile:
    """风格配置"""
    voice: str = "neutral"  # formal, casual, poetic, minimalist, ornate
    tone: str = "balanced"  # light, dark, humorous, serious, ironic
    pace: str = "moderate"  # slow, moderate, fast, variable
    
    # 句子结构偏好
    sentence_length_avg: int = 15
    sentence_variety: float = 0.7  # 0-1，句子多样性
    
    # 词汇选择
    vocabulary_level: str = "standard"  # simple, standard, advanced, mixed
    word_precision: float = 0.8  # 0-1，用词精确度
    
    # 修辞密度
    figurative_density: float = 0.3  # 0-1，修辞手法密度
    description_detail: float = 0.6  # 0-1，描写详细度
    
    # 节奏控制
    paragraph_length_avg: int = 100  # 平均段落字数
    dialogue_ratio: float = 0.3  # 对话占比
    
    # 特色元素
    signature_techniques: List[ProseTechnique] = field(default_factory=list)
    avoided_cliches: List[str] = field(default_factory=list)

@dataclass
class ProseElement:
    """文笔元素"""
    text: str
    technique: Optional[ProseTechnique] = None
    effectiveness: float = 0.5  # 0-1
    originality: float = 0.5  # 0-1

@dataclass
class RhythmPattern:
    """节奏模式"""
    sentence_lengths: List[int]
    variation_score: float
    flow_quality: str  # smooth, choppy, varied, monotonous
    tension_curve: List[float]

class ProseCraftStream:
    """
    文笔工艺Stream
    - 语言优化
    - 修辞运用
    - 节奏控制
    - 风格一致性
    """
    
    def __init__(self):
        self.stream_id = "prose_craft"
        self.weight = 0.125
        self.style_profile: Optional[StyleProfile] = None
        self.vocabulary_bank: Dict[str, List[str]] = {}
        self.phrase_patterns: List[str] = []
        self.rhythm_history: List[RhythmPattern] = []
        
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景，返回文笔优化结果
        """
        try:
            # 1. 初始化或更新风格配置
            await self._initialize_style_profile(context)
            
            # 2. 分析当前文本
            text_analysis = await self._analyze_text(scene)
            
            # 3. 优化句子结构
            sentence_optimization = await self._optimize_sentences(
                scene, text_analysis
            )
            
            # 4. 增强描写深度
            description_enhancement = await self._enhance_descriptions(
                scene, context
            )
            
            # 5. 应用修辞技巧
            rhetorical_devices = await self._apply_rhetorical_devices(
                scene, text_analysis
            )
            
            # 6. 控制节奏变化
            rhythm_control = await self._control_rhythm(
                sentence_optimization, scene
            )
            
            # 7. 精炼词汇选择
            vocabulary_refinement = await self._refine_vocabulary(
                scene, context
            )
            
            # 8. 保持风格一致
            style_consistency = await self._ensure_style_consistency(
                scene, text_analysis
            )
            
            # 9. 生成文笔建议
            prose_suggestions = await self._generate_prose_suggestions(
                text_analysis, rhythm_control, style_consistency
            )
            
            return {
                'stream_id': self.stream_id,
                'weight': self.weight,
                'text_analysis': text_analysis,
                'sentence_optimization': sentence_optimization,
                'description_enhancement': description_enhancement,
                'rhetorical_devices': rhetorical_devices,
                'rhythm_control': rhythm_control,
                'vocabulary_refinement': vocabulary_refinement,
                'style_consistency': style_consistency,
                'suggestions': prose_suggestions,
                'quality_metrics': await self._calculate_prose_quality(
                    text_analysis, rhythm_control, rhetorical_devices
                )
            }
            
        except Exception as e:
            return {
                'stream_id': self.stream_id,
                'error': str(e),
                'fallback': await self._generate_fallback(scene)
            }
    
    async def _initialize_style_profile(self, context: Dict):
        """初始化风格配置"""
        if not self.style_profile:
            style_config = context.get('style', {})
            
            self.style_profile = StyleProfile(
                voice=style_config.get('voice', 'neutral'),
                tone=style_config.get('tone', 'balanced'),
                pace=style_config.get('pace', 'moderate'),
                sentence_length_avg=style_config.get('sentence_length', 15),
                vocabulary_level=style_config.get('vocabulary', 'standard'),
                figurative_density=style_config.get('figurative_density', 0.3),
                description_detail=style_config.get('description_detail', 0.6)
            )
            
            # 加载词汇库
            await self._load_vocabulary_bank(context)
            
            # 加载短语模式
            await self._load_phrase_patterns(context)
    
    async def _analyze_text(self, scene: Dict) -> Dict:
        """分析文本"""
        content = scene.get('content', '')
        
        analysis = {
            'total_words': 0,
            'total_sentences': 0,
            'avg_sentence_length': 0,
            'sentence_variety': 0.0,
            'paragraph_count': 0,
            'readability_score': 0.0,
            'cliche_count': 0,
            'passive_voice_count': 0,
            'adverb_density': 0.0,
            'adjective_density': 0.0
        }
        
        if not content:
            return analysis
        
        # 基本统计
        words = content.split()
        analysis['total_words'] = len(words)
        
        # 句子分析
        sentences = await self._split_sentences(content)
        analysis['total_sentences'] = len(sentences)
        
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences]
            analysis['avg_sentence_length'] = sum(sentence_lengths) / len(sentence_lengths)
            analysis['sentence_variety'] = await self._calculate_variety(sentence_lengths)
        
        # 段落统计
        paragraphs = content.split('\n\n')
        analysis['paragraph_count'] = len(paragraphs)
        
        # 可读性评分
        analysis['readability_score'] = await self._calculate_readability(
            analysis['avg_sentence_length'],
            analysis['total_words']
        )
        
        # 陈词滥调检测
        analysis['cliche_count'] = await self._detect_cliches(content)
        
        # 被动语态检测
        analysis['passive_voice_count'] = await self._detect_passive_voice(content)
        
        # 词性密度
        analysis['adverb_density'] = await self._calculate_adverb_density(content)
        analysis['adjective_density'] = await self._calculate_adjective_density(content)
        
        return analysis
    
    async def _optimize_sentences(self, scene: Dict, analysis: Dict) -> Dict:
        """优化句子结构"""
        optimization = {
            'sentence_structures': [],
            'variety_improvements': [],
            'length_adjustments': [],
            'flow_enhancements': []
        }
        
        content = scene.get('content', '')
        sentences = await self._split_sentences(content)
        
        for i, sentence in enumerate(sentences):
            # 分析句子结构
            structure = await self._analyze_sentence_structure(sentence)
            optimization['sentence_structures'].append(structure)
            
            # 如果句子太长，建议拆分
            word_count = len(sentence.split())
            if word_count > self.style_profile.sentence_length_avg * 2:
                optimization['length_adjustments'].append({
                    'sentence_index': i,
                    'current_length': word_count,
                    'suggestion': '考虑拆分这个长句',
                    'proposed_split': await self._suggest_sentence_split(sentence)
                })
            
            # 如果句子太短且连续，建议合并
            elif word_count < self.style_profile.sentence_length_avg * 0.5:
                if i > 0 and len(sentences[i-1].split()) < self.style_profile.sentence_length_avg * 0.5:
                    optimization['flow_enhancements'].append({
                        'sentence_indices': [i-1, i],
                        'suggestion': '考虑合并这些短句',
                        'proposed_merge': await self._suggest_sentence_merge(
                            sentences[i-1], sentence
                        )
                    })
        
        # 提升句子多样性
        if analysis['sentence_variety'] < self.style_profile.sentence_variety:
            optimization['variety_improvements'] = await self._suggest_variety_improvements(
                optimization['sentence_structures']
            )
        
        return optimization
    
    async def _enhance_descriptions(self, scene: Dict, context: Dict) -> Dict:
        """增强描写深度"""
        enhancement = {
            'sensory_details': [],
            'specific_details': [],
            'metaphorical_descriptions': [],
            'atmosphere_building': []
        }
        
        content = scene.get('content', '')
        
        # 识别描写段落
        descriptive_sections = await self._identify_descriptive_sections(content)
        
        for section in descriptive_sections:
            # 检查感官细节
            sensory_coverage = await self._check_sensory_coverage(section)
            if sensory_coverage['missing_senses']:
                enhancement['sensory_details'].append({
                    'section': section[:50] + '...',
                    'missing_senses': sensory_coverage['missing_senses'],
                    'suggestions': await self._suggest_sensory_details(
                        section, sensory_coverage['missing_senses']
                    )
                })
            
            # 检查具体性
            if await self._is_too_generic(section):
                enhancement['specific_details'].append({
                    'section': section[:50] + '...',
                    'issue': '描写过于笼统',
                    'suggestions': await self._suggest_specific_details(section)
                })
            
            # 添加隐喻描写
            if self.style_profile.figurative_density > 0.5:
                metaphor = await self._create_metaphor(section, context)
                if metaphor:
                    enhancement['metaphorical_descriptions'].append(metaphor)
        
        # 氛围营造
        enhancement['atmosphere_building'] = await self._suggest_atmosphere_elements(
            scene, context
        )
        
        return enhancement
    
    async def _apply_rhetorical_devices(self, scene: Dict, analysis: Dict) -> Dict:
        """应用修辞技巧"""
        devices = {
            'applied_techniques': [],
            'suggested_techniques': [],
            'effectiveness_scores': {}
        }
        
        content = scene.get('content', '')
        
        # 检测已使用的技巧
        for technique in ProseTechnique:
            if await self._detect_technique(content, technique):
                devices['applied_techniques'].append(technique.value)
                devices['effectiveness_scores'][technique.value] = \
                    await self._evaluate_technique_effectiveness(content, technique)
        
        # 建议新技巧
        current_density = len(devices['applied_techniques']) / max(analysis['total_sentences'], 1)
        
        if current_density < self.style_profile.figurative_density:
            # 需要更多修辞
            suitable_techniques = await self._select_suitable_techniques(scene)
            
            for technique in suitable_techniques:
                if technique.value not in devices['applied_techniques']:
                    suggestion = await self._create_technique_suggestion(
                        content, technique, scene
                    )
                    if suggestion:
                        devices['suggested_techniques'].append(suggestion)
        
        return devices
    
    async def _control_rhythm(self, sentence_optimization: Dict, scene: Dict) -> Dict:
        """控制节奏变化"""
        rhythm = {
            'current_pattern': None,
            'flow_quality': 'unknown',
            'pacing_adjustments': [],
            'tension_management': []
        }
        
        # 分析当前节奏
        sentence_lengths = [
            struct.get('word_count', 0) 
            for struct in sentence_optimization.get('sentence_structures', [])
        ]
        
        if sentence_lengths:
            rhythm['current_pattern'] = RhythmPattern(
                sentence_lengths=sentence_lengths,
                variation_score=await self._calculate_variety(sentence_lengths),
                flow_quality=await self._assess_flow_quality(sentence_lengths),
                tension_curve=await self._calculate_tension_curve(sentence_lengths)
            )
            
            rhythm['flow_quality'] = rhythm['current_pattern'].flow_quality
            
            # 记录节奏历史
            self.rhythm_history.append(rhythm['current_pattern'])
            
            # 节奏调整建议
            if rhythm['flow_quality'] == 'monotonous':
                rhythm['pacing_adjustments'].append({
                    'issue': '节奏单调',
                    'suggestion': '变化句子长度以创造节奏感',
                    'example': await self._generate_rhythm_example()
                })
            elif rhythm['flow_quality'] == 'choppy':
                rhythm['pacing_adjustments'].append({
                    'issue': '节奏断续',
                    'suggestion': '使用过渡词和复合句改善流畅性',
                    'example': await self._generate_flow_example()
                })
            
            # 张力管理
            scene_type = scene.get('type', 'normal')
            if scene_type == 'action':
                if sum(sentence_lengths) / len(sentence_lengths) > 20:
                    rhythm['tension_management'].append({
                        'issue': '动作场景句子过长',
                        'suggestion': '使用短句增加紧张感和速度感'
                    })
            elif scene_type == 'reflection':
                if sum(sentence_lengths) / len(sentence_lengths) < 10:
                    rhythm['tension_management'].append({
                        'issue': '反思场景句子过短',
                        'suggestion': '使用长句营造沉思氛围'
                    })
        
        return rhythm
    
    async def _refine_vocabulary(self, scene: Dict, context: Dict) -> Dict:
        """精炼词汇选择"""
        refinement = {
            'word_replacements': [],
            'precision_improvements': [],
            'tone_adjustments': [],
            'eliminated_redundancies': []
        }
        
        content = scene.get('content', '')
        words = content.split()
        
        # 词汇替换建议
        for i, word in enumerate(words):
            # 检查词汇级别
            if self.style_profile.vocabulary_level == 'advanced':
                if await self._is_common_word(word):
                    alternatives = await self._find_sophisticated_alternatives(word)
                    if alternatives:
                        refinement['word_replacements'].append({
                            'original': word,
                            'alternatives': alternatives,
                            'context': ' '.join(words[max(0, i-3):min(len(words), i+4)])
                        })
            
            # 精确度改进
            if await self._is_vague_word(word):
                specific_alternatives = await self._find_specific_alternatives(word, context)
                if specific_alternatives:
                    refinement['precision_improvements'].append({
                        'vague_word': word,
                        'specific_alternatives': specific_alternatives
                    })
        
        # 语气调整
        if self.style_profile.tone != await self._detect_tone(content):
            refinement['tone_adjustments'] = await self._suggest_tone_adjustments(
                content, self.style_profile.tone
            )
        
        # 消除冗余
        redundancies = await self._detect_redundancies(content)
        refinement['eliminated_redundancies'] = redundancies
        
        return refinement
    
    async def _ensure_style_consistency(self, scene: Dict, analysis: Dict) -> Dict:
        """确保风格一致性"""
        consistency = {
            'voice_consistency': 0.0,
            'tone_consistency': 0.0,
            'vocabulary_consistency': 0.0,
            'inconsistencies': [],
            'adjustments': []
        }
        
        content = scene.get('content', '')
        
        # 检查语态一致性
        detected_voice = await self._detect_voice(content)
        if detected_voice == self.style_profile.voice:
            consistency['voice_consistency'] = 1.0
        else:
            consistency['voice_consistency'] = 0.5
            consistency['inconsistencies'].append({
                'aspect': 'voice',
                'expected': self.style_profile.voice,
                'detected': detected_voice
            })
        
        # 检查语气一致性
        detected_tone = await self._detect_tone(content)
        if detected_tone == self.style_profile.tone:
            consistency['tone_consistency'] = 1.0
        else:
            consistency['tone_consistency'] = 0.5
            consistency['inconsistencies'].append({
                'aspect': 'tone',
                'expected': self.style_profile.tone,
                'detected': detected_tone
            })
        
        # 检查词汇一致性
        vocabulary_level = await self._assess_vocabulary_level(content)
        if vocabulary_level == self.style_profile.vocabulary_level:
            consistency['vocabulary_consistency'] = 1.0
        else:
            consistency['vocabulary_consistency'] = 0.6
        
        # 生成调整建议
        for inconsistency in consistency['inconsistencies']:
            adjustment = await self._generate_consistency_adjustment(
                inconsistency, content
            )
            consistency['adjustments'].append(adjustment)
        
        return consistency
    
    async def _generate_prose_suggestions(
        self, analysis: Dict, rhythm: Dict, consistency: Dict
    ) -> List[str]:
        """生成文笔建议"""
        suggestions = []
        
        # 基于文本分析的建议
        if analysis['avg_sentence_length'] > 25:
            suggestions.append("考虑缩短句子长度以提高可读性")
        elif analysis['avg_sentence_length'] < 10:
            suggestions.append("适当增加句子复杂度以丰富表达")
        
        if analysis['cliche_count'] > 3:
            suggestions.append("避免使用陈词滥调，寻找新颖表达")
        
        if analysis['passive_voice_count'] > analysis['total_sentences'] * 0.3:
            suggestions.append("减少被动语态使用，让叙述更有力")
        
        if analysis['adverb_density'] > 0.05:
            suggestions.append("精简副词使用，通过动词选择传达含义")
        
        # 基于节奏的建议
        if rhythm.get('flow_quality') == 'monotonous':
            suggestions.append("变化句子结构和长度以改善节奏")
        
        # 基于一致性的建议
        if consistency['voice_consistency'] < 0.8:
            suggestions.append("保持叙述语态的一致性")
        
        return suggestions
    
    async def _load_vocabulary_bank(self, context: Dict):
        """加载词汇库"""
        self.vocabulary_bank = {
            'sophisticated': ['elaborate', 'intricate', 'nuanced', 'sophisticated'],
            'emotional': ['poignant', 'profound', 'stirring', 'evocative'],
            'descriptive': ['vivid', 'striking', 'luminous', 'ethereal'],
            'action': ['surge', 'cascade', 'plunge', 'soar']
        }
        
        # 从context加载自定义词汇
        custom_vocab = context.get('vocabulary', {})
        self.vocabulary_bank.update(custom_vocab)
    
    async def _load_phrase_patterns(self, context: Dict):
        """加载短语模式"""
        self.phrase_patterns = [
            "如...一般",
            "仿佛...似的",
            "像...那样"
        ]
        
        # 从context加载自定义模式
        custom_patterns = context.get('phrase_patterns', [])
        self.phrase_patterns.extend(custom_patterns)
    
    async def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        # 简化的句子分割
        sentences = re.split(r'[。！？.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    async def _calculate_variety(self, lengths: List[int]) -> float:
        """计算多样性分数"""
        if not lengths:
            return 0.0
        
        avg = sum(lengths) / len(lengths)
        if avg == 0:
            return 0.0
        
        variance = sum((x - avg) ** 2 for x in lengths) / len(lengths)
        std_dev = variance ** 0.5
        
        # 变异系数
        cv = std_dev / avg
        return min(cv, 1.0)
    
    async def _calculate_readability(self, avg_sentence_length: float, total_words: int) -> float:
        """计算可读性分数"""
        # 简化的可读性计算
        if avg_sentence_length < 10:
            return 0.9
        elif avg_sentence_length < 20:
            return 0.7
        elif avg_sentence_length < 30:
            return 0.5
        else:
            return 0.3
    
    async def _detect_cliches(self, text: str) -> int:
        """检测陈词滥调"""
        cliches = [
            '一见钟情', '命中注定', '缘分天定',
            '岁月如梭', '时光飞逝', '转眼之间'
        ]
        
        count = 0
        for cliche in cliches:
            count += text.count(cliche)
        
        return count
    
    async def _detect_passive_voice(self, text: str) -> int:
        """检测被动语态"""
        # 简化的被动语态检测
        passive_markers = ['被', '受到', '遭到', '得到']
        count = 0
        for marker in passive_markers:
            count += text.count(marker)
        return count
    
    async def _calculate_adverb_density(self, text: str) -> float:
        """计算副词密度"""
        # 简化的副词检测
        adverb_endings = ['地', '然', '极了', '很', '非常', '十分']
        word_count = len(text.split())
        adverb_count = sum(text.count(ending) for ending in adverb_endings)
        
        return adverb_count / max(word_count, 1)
    
    async def _calculate_adjective_density(self, text: str) -> float:
        """计算形容词密度"""
        # 简化的形容词检测
        adjective_patterns = ['的', '般的', '样的']
        word_count = len(text.split())
        adj_count = sum(text.count(pattern) for pattern in adjective_patterns)
        
        return adj_count / max(word_count, 1)
    
    async def _analyze_sentence_structure(self, sentence: str) -> Dict:
        """分析句子结构"""
        structure = {
            'type': SentenceType.SIMPLE.value,
            'word_count': len(sentence.split()),
            'clause_count': 1,
            'has_subordinate': False
        }
        
        # 检测复合句标志
        if '，' in sentence and ('但' in sentence or '而' in sentence):
            structure['type'] = SentenceType.COMPOUND.value
            structure['clause_count'] = sentence.count('，') + 1
        elif '因为' in sentence or '如果' in sentence or '虽然' in sentence:
            structure['type'] = SentenceType.COMPLEX.value
            structure['has_subordinate'] = True
        
        return structure
    
    async def _suggest_sentence_split(self, sentence: str) -> List[str]:
        """建议句子拆分"""
        # 在逗号处寻找拆分点
        parts = sentence.split('，')
        if len(parts) > 2:
            mid = len(parts) // 2
            return [
                '，'.join(parts[:mid]) + '。',
                '，'.join(parts[mid:])
            ]
        return [sentence]
    
    async def _suggest_sentence_merge(self, sent1: str, sent2: str) -> str:
        """建议句子合并"""
        # 简单合并建议
        if sent1.endswith('。'):
            sent1 = sent1[:-1]
        return f"{sent1}，{sent2}"
    
    async def _suggest_variety_improvements(self, structures: List[Dict]) -> List[str]:
        """建议句子多样性改进"""
        improvements = []
        
        # 检查连续相同结构
        for i in range(len(structures) - 2):
            if structures[i]['type'] == structures[i+1]['type'] == structures[i+2]['type']:
                improvements.append(
                    f"第{i+1}-{i+3}句结构相同，建议变化句式"
                )
        
        return improvements
    
    async def _identify_descriptive_sections(self, text: str) -> List[str]:
        """识别描写段落"""
        paragraphs = text.split('\n\n')
        descriptive = []
        
        for para in paragraphs:
            # 简单判断：对话少、描写词多
            if para.count('"') < 2 and ('景' in para or '色' in para or '光' in para):
                descriptive.append(para)
        
        return descriptive
    
    async def _check_sensory_coverage(self, section: str) -> Dict:
        """检查感官覆盖"""
        coverage = {
            'visual': '看' in section or '色' in section or '光' in section,
            'auditory': '声' in section or '听' in section or '音' in section,
            'olfactory': '味' in section or '香' in section or '臭' in section,
            'tactile': '触' in section or '感' in section or '温' in section,
            'gustatory': '尝' in section or '甜' in section or '苦' in section
        }
        
        missing = [sense for sense, present in coverage.items() if not present]
        
        return {
            'coverage': coverage,
            'missing_senses': missing
        }
    
    async def _suggest_sensory_details(self, section: str, missing_senses: List[str]) -> List[str]:
        """建议感官细节"""
        suggestions = {
            'visual': '添加视觉细节：颜色、光影、形状',
            'auditory': '添加听觉细节：声音、音调、节奏',
            'olfactory': '添加嗅觉细节：气味、香味、空气质感',
            'tactile': '添加触觉细节：质地、温度、触感',
            'gustatory': '添加味觉细节：味道、口感'
        }
        
        return [suggestions.get(sense, '') for sense in missing_senses if sense in suggestions]
    
    async def _is_too_generic(self, section: str) -> bool:
        """判断是否过于笼统"""
        generic_words = ['东西', '很多', '有些', '一些', '大概', '可能']
        generic_count = sum(section.count(word) for word in generic_words)
        return generic_count > 3
    
    async def _suggest_specific_details(self, section: str) -> List[str]:
        """建议具体细节"""
        return [
            "用具体数字代替'很多'、'一些'",
            "用具体名词代替'东西'",
            "用准确描述代替'大概'、'可能'"
        ]
    
    async def _create_metaphor(self, section: str, context: Dict) -> Optional[Dict]:
        """创建隐喻"""
        # 简化的隐喻生成
        if '光' in section:
            return {
                'original': '光线',
                'metaphor': '如流水般的光线',
                'type': 'visual'
            }
        return None
    
    async def _suggest_atmosphere_elements(self, scene: Dict, context: Dict) -> List[str]:
        """建议氛围元素"""
        suggestions = []
        
        scene_type = scene.get('type', 'normal')
        if scene_type == 'tense':
            suggestions.append("使用短促的句子和不完整的思维营造紧张感")
        elif scene_type == 'romantic':
            suggestions.append("使用柔和的词汇和流畅的节奏营造浪漫氛围")
        elif scene_type == 'mysterious':
            suggestions.append("使用模糊的描述和省略营造神秘感")
        
        return suggestions
    
    async def _detect_technique(self, text: str, technique: ProseTechnique) -> bool:
        """检测修辞技巧"""
        technique_markers = {
            ProseTechnique.METAPHOR: ['是', '如同', '仿佛是'],
            ProseTechnique.SIMILE: ['像', '如', '好像'],
            ProseTechnique.PERSONIFICATION: ['他' in text and not '人' in text],
            ProseTechnique.REPETITION: any(text.count(word) > 2 for word in text.split())
        }
        
        if technique in technique_markers:
            if isinstance(technique_markers[technique], bool):
                return technique_markers[technique]
            return any(marker in text for marker in technique_markers[technique])
        
        return False
    
    async def _evaluate_technique_effectiveness(self, text: str, technique: ProseTechnique) -> float:
        """评估技巧效果"""
        # 简化的效果评估
        return 0.7  # 默认中等效果
    
    async def _select_suitable_techniques(self, scene: Dict) -> List[ProseTechnique]:
        """选择合适的技巧"""
        suitable = []
        
        scene_type = scene.get('type', 'normal')
        if scene_type == 'descriptive':
            suitable.extend([ProseTechnique.IMAGERY, ProseTechnique.METAPHOR])
        elif scene_type == 'action':
            suitable.extend([ProseTechnique.ONOMATOPOEIA, ProseTechnique.PARALLELISM])
        elif scene_type == 'emotional':
            suitable.extend([ProseTechnique.REPETITION, ProseTechnique.SYMBOLISM])
        
        return suitable
    
    async def _create_technique_suggestion(
        self, content: str, technique: ProseTechnique, scene: Dict
    ) -> Optional[Dict]:
        """创建技巧建议"""
        suggestions = {
            ProseTechnique.METAPHOR: {
                'technique': 'metaphor',
                'suggestion': '添加隐喻增强表现力',
                'example': '时间如流水般逝去'
            },
            ProseTechnique.PARALLELISM: {
                'technique': 'parallelism',
                'suggestion': '使用排比增强气势',
                'example': '他跑过街道，跑过广场，跑过记忆'
            }
        }
        
        return suggestions.get(technique)
    
    async def _assess_flow_quality(self, sentence_lengths: List[int]) -> str:
        """评估流畅质量"""
        if not sentence_lengths:
            return 'unknown'
        
        variety = await self._calculate_variety(sentence_lengths)
        
        if variety < 0.2:
            return 'monotonous'
        elif variety > 0.8:
            return 'choppy'
        elif 0.4 <= variety <= 0.6:
            return 'smooth'
        else:
            return 'varied'
    
    async def _calculate_tension_curve(self, sentence_lengths: List[int]) -> List[float]:
        """计算张力曲线"""
        if not sentence_lengths:
            return []
        
        max_length = max(sentence_lengths)
        if max_length == 0:
            return [0.0] * len(sentence_lengths)
        
        # 短句张力高，长句张力低
        return [1.0 - (length / max_length) for length in sentence_lengths]
    
    async def _generate_rhythm_example(self) -> str:
        """生成节奏示例"""
        return "短句急促。稍长的句子缓和节奏。然后一个更长的句子，如涓涓细流，慢慢展开叙述。又短。变化。"
    
    async def _generate_flow_example(self) -> str:
        """生成流畅示例"""
        return "使用过渡词如'然而'、'因此'、'与此同时'连接句子，创造流畅的阅读体验。"
    
    async def _is_common_word(self, word: str) -> bool:
        """判断是否常用词"""
        common_words = ['说', '走', '看', '想', '好', '大', '小']
        return word in common_words
    
    async def _find_sophisticated_alternatives(self, word: str) -> List[str]:
        """寻找高级替代词"""
        alternatives = {
            '说': ['诉说', '陈述', '表达', '倾诉'],
            '走': ['漫步', '踱步', '疾行', '徜徉'],
            '看': ['凝视', '眺望', '审视', '端详']
        }
        
        return alternatives.get(word, [])
    
    async def _is_vague_word(self, word: str) -> bool:
        """判断是否模糊词"""
        vague_words = ['东西', '事情', '地方', '有些', '很多']
        return word in vague_words
    
    async def _find_specific_alternatives(self, word: str, context: Dict) -> List[str]:
        """寻找具体替代词"""
        alternatives = {
            '东西': ['物品', '器具', '工具'],
            '地方': ['场所', '地点', '区域'],
            '很多': ['众多', '大量', '无数']
        }
        
        return alternatives.get(word, [])
    
    async def _detect_tone(self, text: str) -> str:
        """检测语气"""
        # 简化的语气检测
        if '!' in text or '激动' in text:
            return 'energetic'
        elif '?' in text or '疑惑' in text:
            return 'questioning'
        elif '悲' in text or '哀' in text:
            return 'melancholic'
        else:
            return 'balanced'
    
    async def _suggest_tone_adjustments(self, content: str, target_tone: str) -> List[str]:
        """建议语气调整"""
        adjustments = {
            'light': ['使用轻松的词汇', '加入幽默元素'],
            'dark': ['使用沉重的意象', '强调阴影和黑暗'],
            'serious': ['使用正式词汇', '避免口语化表达']
        }
        
        return adjustments.get(target_tone, [])
    
    async def _detect_redundancies(self, text: str) -> List[str]:
        """检测冗余"""
        redundancies = []
        
        # 简单的冗余模式
        redundant_patterns = [
            ('完全彻底', '完全'),
            ('非常极其', '非常'),
            ('大约左右', '大约')
        ]
        
        for pattern, replacement in redundant_patterns:
            if pattern in text:
                redundancies.append(f"'{pattern}' 可简化为 '{replacement}'")
        
        return redundancies
    
    async def _detect_voice(self, text: str) -> str:
        """检测语态"""
        # 简化的语态检测
        if '我' in text[:20]:
            return 'first_person'
        elif '你' in text[:20]:
            return 'second_person'
        else:
            return 'third_person'
    
    async def _assess_vocabulary_level(self, text: str) -> str:
        """评估词汇水平"""
        # 简化的词汇水平评估
        sophisticated_count = sum(
            text.count(word) 
            for word in self.vocabulary_bank.get('sophisticated', [])
        )
        
        if sophisticated_count > 5:
            return 'advanced'
        elif sophisticated_count > 2:
            return 'standard'
        else:
            return 'simple'
    
    async def _generate_consistency_adjustment(self, inconsistency: Dict, content: str) -> Dict:
        """生成一致性调整"""
        return {
            'aspect': inconsistency['aspect'],
            'current': inconsistency['detected'],
            'target': inconsistency['expected'],
            'suggestion': f"调整{inconsistency['aspect']}从{inconsistency['detected']}到{inconsistency['expected']}"
        }
    
    async def _calculate_prose_quality(
        self, analysis: Dict, rhythm: Dict, devices: Dict
    ) -> Dict:
        """计算文笔质量"""
        metrics = {
            'clarity': 0.0,
            'elegance': 0.0,
            'rhythm_quality': 0.0,
            'originality': 0.0,
            'overall_score': 0.0
        }
        
        # 清晰度
        metrics['clarity'] = analysis['readability_score']
        
        # 优雅度
        if analysis['sentence_variety'] > 0.5:
            metrics['elegance'] += 0.3
        if len(devices.get('applied_techniques', [])) > 2:
            metrics['elegance'] += 0.3
        if analysis['passive_voice_count'] < analysis['total_sentences'] * 0.2:
            metrics['elegance'] += 0.3
        
        # 节奏质量
        if rhythm.get('flow_quality') == 'smooth':
            metrics['rhythm_quality'] = 0.9
        elif rhythm.get('flow_quality') == 'varied':
            metrics['rhythm_quality'] = 0.7
        else:
            metrics['rhythm_quality'] = 0.4
        
        # 原创性
        metrics['originality'] = max(0, 1.0 - (analysis['cliche_count'] * 0.1))
        
        # 总分
        metrics['overall_score'] = sum(metrics.values()) / (len(metrics) - 1)
        
        return metrics
    
    async def _generate_fallback(self, scene: Dict) -> Dict:
        """生成降级方案"""
        return {
            'suggestions': ['保持清晰简洁的表达'],
            'message': 'Using simplified prose analysis'
        }