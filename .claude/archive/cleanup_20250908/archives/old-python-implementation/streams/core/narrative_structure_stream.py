"""
Narrative Structure Stream
叙事结构Stream - 极致品质系统核心组件
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime
import json

class NarrativePhase(Enum):
    """叙事阶段"""
    EXPOSITION = "exposition"          # 开端/背景介绍
    RISING_ACTION = "rising_action"    # 上升动作
    CLIMAX = "climax"                  # 高潮
    FALLING_ACTION = "falling_action"  # 下降动作
    RESOLUTION = "resolution"          # 结局
    DENOUEMENT = "denouement"         # 尾声

class PlotType(Enum):
    """情节类型"""
    OVERCOMING_MONSTER = "overcoming_monster"  # 战胜怪物
    RAGS_TO_RICHES = "rags_to_riches"         # 麻雀变凤凰
    QUEST = "quest"                            # 探索追寻
    VOYAGE_AND_RETURN = "voyage_and_return"    # 远航归来
    COMEDY = "comedy"                          # 喜剧
    TRAGEDY = "tragedy"                        # 悲剧
    REBIRTH = "rebirth"                        # 重生

class ConflictType(Enum):
    """冲突类型"""
    MAN_VS_MAN = "man_vs_man"          # 人与人
    MAN_VS_SELF = "man_vs_self"        # 人与自我
    MAN_VS_NATURE = "man_vs_nature"    # 人与自然
    MAN_VS_SOCIETY = "man_vs_society"  # 人与社会
    MAN_VS_FATE = "man_vs_fate"        # 人与命运
    MAN_VS_TECHNOLOGY = "man_vs_technology"  # 人与科技

@dataclass
class StoryBeat:
    """故事节拍"""
    beat_id: str
    type: str  # opening_image, setup, catalyst, debate, etc.
    description: str
    target_percentage: float  # 在故事中的位置百分比
    actual_percentage: float = 0.0
    completed: bool = False
    quality_score: float = 0.0

@dataclass
class PlotThread:
    """情节线"""
    thread_id: str
    thread_type: str  # main, subplot, parallel
    description: str
    start_chapter: int
    target_end_chapter: int
    current_status: str = "active"  # active, resolved, suspended
    tension_curve: List[float] = field(default_factory=list)
    key_events: List[Dict] = field(default_factory=list)
    resolution: Optional[str] = None

@dataclass
class NarrativeStructure:
    """叙事结构模型"""
    structure_type: str  # linear, non-linear, circular, frame
    plot_type: PlotType
    current_phase: NarrativePhase
    
    # 三幕结构
    acts: Dict[str, Dict] = field(default_factory=dict)
    
    # 故事节拍
    story_beats: List[StoryBeat] = field(default_factory=list)
    
    # 情节线管理
    plot_threads: Dict[str, PlotThread] = field(default_factory=dict)
    main_thread: Optional[str] = None
    
    # 冲突系统
    central_conflict: ConflictType = ConflictType.MAN_VS_MAN
    active_conflicts: List[Dict] = field(default_factory=list)
    
    # 张力曲线
    tension_curve: List[float] = field(default_factory=list)
    current_tension: float = 0.3
    target_tension: float = 0.5
    
    # 节奏控制
    pacing: str = "moderate"  # slow, moderate, fast, variable
    scene_rhythm: List[str] = field(default_factory=list)  # action, dialogue, description, reflection
    
    # 主题深度
    themes: List[str] = field(default_factory=list)
    motifs: List[str] = field(default_factory=list)
    symbols: Dict[str, str] = field(default_factory=dict)

class NarrativeStructureStream:
    """
    叙事结构Stream
    - 情节架构管理
    - 节奏控制
    - 张力曲线
    - 主题深化
    """
    
    def __init__(self):
        self.stream_id = "narrative_structure"
        self.weight = 0.125
        self.narrative_model: Optional[NarrativeStructure] = None
        self.scene_sequence: List[Dict] = []
        self.chapter_structures: Dict[int, Dict] = {}
        
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景，返回叙事结构建议
        """
        try:
            # 1. 初始化或更新叙事模型
            await self._initialize_narrative_model(context)
            
            # 2. 分析当前叙事位置
            narrative_position = await self._analyze_narrative_position(
                scene, context
            )
            
            # 3. 评估情节进展
            plot_progression = await self._evaluate_plot_progression(
                scene, narrative_position, context
            )
            
            # 4. 管理张力曲线
            tension_management = await self._manage_tension_curve(
                scene, narrative_position
            )
            
            # 5. 控制叙事节奏
            pacing_control = await self._control_pacing(
                scene, narrative_position
            )
            
            # 6. 深化主题元素
            thematic_elements = await self._deepen_themes(
                scene, context
            )
            
            # 7. 协调情节线
            plot_coordination = await self._coordinate_plot_threads(
                scene, context
            )
            
            # 8. 生成结构建议
            structural_suggestions = await self._generate_structural_suggestions(
                narrative_position, plot_progression, tension_management
            )
            
            return {
                'stream_id': self.stream_id,
                'weight': self.weight,
                'narrative_position': narrative_position,
                'plot_progression': plot_progression,
                'tension_management': tension_management,
                'pacing_control': pacing_control,
                'thematic_elements': thematic_elements,
                'plot_coordination': plot_coordination,
                'structural_suggestions': structural_suggestions,
                'quality_metrics': await self._calculate_structure_quality(
                    narrative_position, plot_progression
                )
            }
            
        except Exception as e:
            return {
                'stream_id': self.stream_id,
                'error': str(e),
                'fallback': await self._generate_fallback(scene)
            }
    
    async def _initialize_narrative_model(self, context: Dict):
        """初始化叙事模型"""
        if not self.narrative_model:
            bible = context.get('bible', {})
            
            # 确定情节类型
            plot_type_str = bible.get('plot_type', 'QUEST')
            plot_type = PlotType[plot_type_str.upper()] if plot_type_str.upper() in PlotType.__members__ else PlotType.QUEST
            
            # 创建叙事结构
            self.narrative_model = NarrativeStructure(
                structure_type=bible.get('structure_type', 'linear'),
                plot_type=plot_type,
                current_phase=NarrativePhase.EXPOSITION,
                central_conflict=ConflictType[
                    bible.get('central_conflict', 'MAN_VS_MAN').upper()
                ],
                themes=bible.get('themes', []),
                motifs=bible.get('motifs', []),
                pacing=bible.get('pacing', 'moderate')
            )
            
            # 初始化三幕结构
            await self._setup_three_act_structure(bible)
            
            # 初始化故事节拍
            await self._setup_story_beats(bible)
            
            # 初始化情节线
            await self._setup_plot_threads(bible)
    
    async def _setup_three_act_structure(self, bible: Dict):
        """设置三幕结构"""
        total_chapters = bible.get('total_chapters', 30)
        
        self.narrative_model.acts = {
            'act_1': {
                'name': '设置',
                'chapters': list(range(1, int(total_chapters * 0.25) + 1)),
                'purpose': '介绍世界、角色、建立冲突',
                'key_points': ['开场形象', '主题陈述', '催化事件', '辩论']
            },
            'act_2a': {
                'name': '对抗',
                'chapters': list(range(int(total_chapters * 0.25) + 1, int(total_chapters * 0.5) + 1)),
                'purpose': '探索新世界、遭遇挫折',
                'key_points': ['B故事', '趣味游戏', '中点']
            },
            'act_2b': {
                'name': '加速',
                'chapters': list(range(int(total_chapters * 0.5) + 1, int(total_chapters * 0.75) + 1)),
                'purpose': '提升赌注、逼近危机',
                'key_points': ['坏人逼近', '一无所有', '灵魂暗夜']
            },
            'act_3': {
                'name': '解决',
                'chapters': list(range(int(total_chapters * 0.75) + 1, total_chapters + 1)),
                'purpose': '最终对决、解决冲突',
                'key_points': ['第三幕转折', '决战', '最终形象']
            }
        }
    
    async def _setup_story_beats(self, bible: Dict):
        """设置故事节拍（Save the Cat结构）"""
        beats = [
            StoryBeat('opening_image', 'opening_image', '开场形象', 0.01),
            StoryBeat('theme_stated', 'theme_stated', '主题陈述', 0.05),
            StoryBeat('setup', 'setup', '设置', 0.10),
            StoryBeat('catalyst', 'catalyst', '催化事件', 0.12),
            StoryBeat('debate', 'debate', '辩论', 0.25),
            StoryBeat('break_into_2', 'break_into_2', '进入第二幕', 0.25),
            StoryBeat('b_story', 'b_story', 'B故事', 0.30),
            StoryBeat('fun_and_games', 'fun_and_games', '趣味游戏', 0.50),
            StoryBeat('midpoint', 'midpoint', '中点', 0.50),
            StoryBeat('bad_guys_close_in', 'bad_guys_close_in', '坏人逼近', 0.62),
            StoryBeat('all_is_lost', 'all_is_lost', '一无所有', 0.75),
            StoryBeat('dark_night', 'dark_night', '灵魂暗夜', 0.80),
            StoryBeat('break_into_3', 'break_into_3', '进入第三幕', 0.85),
            StoryBeat('finale', 'finale', '决战', 0.95),
            StoryBeat('final_image', 'final_image', '最终形象', 0.99)
        ]
        
        self.narrative_model.story_beats = beats
    
    async def _setup_plot_threads(self, bible: Dict):
        """设置情节线"""
        # 主线
        main_thread = PlotThread(
            thread_id='main_plot',
            thread_type='main',
            description=bible.get('main_plot', '主角的核心冲突与成长'),
            start_chapter=1,
            target_end_chapter=bible.get('total_chapters', 30)
        )
        
        self.narrative_model.plot_threads['main_plot'] = main_thread
        self.narrative_model.main_thread = 'main_plot'
        
        # 副线
        subplots = bible.get('subplots', [])
        for i, subplot in enumerate(subplots):
            thread = PlotThread(
                thread_id=f'subplot_{i}',
                thread_type='subplot',
                description=subplot.get('description', ''),
                start_chapter=subplot.get('start_chapter', 3),
                target_end_chapter=subplot.get('end_chapter', 25)
            )
            self.narrative_model.plot_threads[f'subplot_{i}'] = thread
    
    async def _analyze_narrative_position(
        self, scene: Dict, context: Dict
    ) -> Dict:
        """分析当前叙事位置"""
        chapter = context.get('current_chapter', 1)
        total_chapters = context.get('total_chapters', 30)
        progress = chapter / total_chapters
        
        # 确定当前阶段
        current_phase = NarrativePhase.EXPOSITION
        if progress < 0.10:
            current_phase = NarrativePhase.EXPOSITION
        elif progress < 0.25:
            current_phase = NarrativePhase.RISING_ACTION
        elif progress < 0.75:
            current_phase = NarrativePhase.RISING_ACTION
        elif progress < 0.85:
            current_phase = NarrativePhase.CLIMAX
        elif progress < 0.95:
            current_phase = NarrativePhase.FALLING_ACTION
        else:
            current_phase = NarrativePhase.RESOLUTION
        
        self.narrative_model.current_phase = current_phase
        
        # 确定当前幕
        current_act = None
        for act_name, act_info in self.narrative_model.acts.items():
            if chapter in act_info['chapters']:
                current_act = act_name
                break
        
        # 找到最近的故事节拍
        nearest_beat = None
        for beat in self.narrative_model.story_beats:
            if not beat.completed and progress >= beat.target_percentage:
                nearest_beat = beat
                beat.actual_percentage = progress
                break
        
        return {
            'chapter': chapter,
            'progress': progress,
            'current_phase': current_phase.value,
            'current_act': current_act,
            'nearest_beat': nearest_beat.type if nearest_beat else None,
            'act_purpose': self.narrative_model.acts.get(current_act, {}).get('purpose') if current_act else None
        }
    
    async def _evaluate_plot_progression(
        self, scene: Dict, position: Dict, context: Dict
    ) -> Dict:
        """评估情节进展"""
        progression = {
            'main_plot_status': 'on_track',
            'subplot_statuses': {},
            'conflict_evolution': [],
            'momentum': 0.0,
            'complications': []
        }
        
        # 评估主线进展
        main_thread = self.narrative_model.plot_threads.get(self.narrative_model.main_thread)
        if main_thread:
            # 检查关键事件
            expected_events = await self._get_expected_events(position['progress'])
            actual_events = main_thread.key_events
            
            if len(actual_events) < len(expected_events) * position['progress']:
                progression['main_plot_status'] = 'behind_schedule'
            elif len(actual_events) > len(expected_events) * position['progress'] * 1.2:
                progression['main_plot_status'] = 'rushing'
        
        # 评估副线进展
        for thread_id, thread in self.narrative_model.plot_threads.items():
            if thread.thread_type == 'subplot':
                status = 'active' if thread.current_status == 'active' else thread.current_status
                progression['subplot_statuses'][thread_id] = status
        
        # 评估冲突演化
        for conflict in self.narrative_model.active_conflicts:
            evolution = await self._assess_conflict_evolution(conflict, position)
            progression['conflict_evolution'].append(evolution)
        
        # 计算叙事动量
        progression['momentum'] = await self._calculate_momentum(scene, position)
        
        return progression
    
    async def _manage_tension_curve(
        self, scene: Dict, position: Dict
    ) -> Dict:
        """管理张力曲线"""
        # 计算理想张力
        ideal_tension = self._calculate_ideal_tension(position['progress'])
        
        # 评估当前张力
        current_tension = await self._evaluate_scene_tension(scene)
        
        # 更新张力曲线
        self.narrative_model.tension_curve.append(current_tension)
        self.narrative_model.current_tension = current_tension
        self.narrative_model.target_tension = ideal_tension
        
        # 生成张力调整建议
        adjustment_needed = ideal_tension - current_tension
        
        tension_management = {
            'current_tension': current_tension,
            'ideal_tension': ideal_tension,
            'adjustment_needed': adjustment_needed,
            'tension_curve': self.narrative_model.tension_curve[-10:],  # 最近10个点
            'suggestions': []
        }
        
        if adjustment_needed > 0.2:
            tension_management['suggestions'].extend([
                '增加冲突强度',
                '引入时间压力',
                '提升赌注'
            ])
        elif adjustment_needed < -0.2:
            tension_management['suggestions'].extend([
                '给予喘息空间',
                '加入轻松时刻',
                '展现角色关系'
            ])
        
        return tension_management
    
    async def _control_pacing(self, scene: Dict, position: Dict) -> Dict:
        """控制叙事节奏"""
        # 分析场景类型
        scene_type = await self._classify_scene_type(scene)
        
        # 更新节奏序列
        self.narrative_model.scene_rhythm.append(scene_type)
        
        # 评估节奏平衡
        recent_rhythm = self.narrative_model.scene_rhythm[-5:]
        rhythm_balance = {
            'action': recent_rhythm.count('action') / max(len(recent_rhythm), 1),
            'dialogue': recent_rhythm.count('dialogue') / max(len(recent_rhythm), 1),
            'description': recent_rhythm.count('description') / max(len(recent_rhythm), 1),
            'reflection': recent_rhythm.count('reflection') / max(len(recent_rhythm), 1)
        }
        
        # 生成节奏建议
        pacing_suggestions = []
        
        # 检查节奏单调
        if max(rhythm_balance.values()) > 0.6:
            dominant_type = max(rhythm_balance, key=rhythm_balance.get)
            if dominant_type == 'action':
                pacing_suggestions.append('加入对话或反思场景以平衡节奏')
            elif dominant_type == 'dialogue':
                pacing_suggestions.append('加入动作场景以增加动感')
        
        # 根据叙事位置调整节奏
        if position['current_phase'] == NarrativePhase.CLIMAX.value:
            if scene_type != 'action':
                pacing_suggestions.append('高潮阶段应以动作场景为主')
        elif position['current_phase'] == NarrativePhase.EXPOSITION.value:
            if scene_type == 'action':
                pacing_suggestions.append('开端阶段不宜过早进入激烈动作')
        
        return {
            'current_pacing': self.narrative_model.pacing,
            'scene_type': scene_type,
            'rhythm_balance': rhythm_balance,
            'recent_rhythm': recent_rhythm,
            'suggestions': pacing_suggestions
        }
    
    async def _deepen_themes(self, scene: Dict, context: Dict) -> Dict:
        """深化主题元素"""
        thematic_elements = {
            'active_themes': [],
            'motif_appearances': [],
            'symbolic_elements': [],
            'thematic_resonance': 0.0
        }
        
        # 识别场景中的主题
        scene_content = scene.get('content', '')
        for theme in self.narrative_model.themes:
            if await self._detect_theme_presence(theme, scene_content):
                thematic_elements['active_themes'].append(theme)
        
        # 识别母题出现
        for motif in self.narrative_model.motifs:
            if await self._detect_motif(motif, scene_content):
                thematic_elements['motif_appearances'].append({
                    'motif': motif,
                    'context': await self._extract_motif_context(motif, scene_content)
                })
        
        # 识别象征元素
        for symbol, meaning in self.narrative_model.symbols.items():
            if symbol.lower() in scene_content.lower():
                thematic_elements['symbolic_elements'].append({
                    'symbol': symbol,
                    'meaning': meaning,
                    'usage': await self._analyze_symbol_usage(symbol, scene_content)
                })
        
        # 计算主题共鸣度
        thematic_elements['thematic_resonance'] = len(thematic_elements['active_themes']) * 0.3 + \
                                                  len(thematic_elements['motif_appearances']) * 0.2 + \
                                                  len(thematic_elements['symbolic_elements']) * 0.1
        
        return thematic_elements
    
    async def _coordinate_plot_threads(self, scene: Dict, context: Dict) -> Dict:
        """协调情节线"""
        coordination = {
            'active_threads': [],
            'thread_intersections': [],
            'thread_priorities': {},
            'weaving_pattern': []
        }
        
        chapter = context.get('current_chapter', 1)
        
        # 识别活跃线程
        for thread_id, thread in self.narrative_model.plot_threads.items():
            if thread.start_chapter <= chapter <= thread.target_end_chapter:
                if thread.current_status == 'active':
                    coordination['active_threads'].append(thread_id)
                    
                    # 计算优先级
                    priority = await self._calculate_thread_priority(
                        thread, chapter, context
                    )
                    coordination['thread_priorities'][thread_id] = priority
        
        # 识别线程交叉点
        if len(coordination['active_threads']) > 1:
            for i, thread1 in enumerate(coordination['active_threads']):
                for thread2 in coordination['active_threads'][i+1:]:
                    if await self._detect_thread_intersection(thread1, thread2, scene):
                        coordination['thread_intersections'].append({
                            'threads': [thread1, thread2],
                            'type': 'convergence',
                            'impact': 'high'
                        })
        
        # 生成编织模式
        coordination['weaving_pattern'] = await self._generate_weaving_pattern(
            coordination['active_threads'],
            coordination['thread_priorities']
        )
        
        return coordination
    
    async def _generate_structural_suggestions(
        self, position: Dict, progression: Dict, tension: Dict
    ) -> List[str]:
        """生成结构建议"""
        suggestions = []
        
        # 基于位置的建议
        if position['nearest_beat']:
            beat_suggestions = {
                'catalyst': '确保催化事件足够强烈以推动故事前进',
                'midpoint': '中点应该是假胜利或假失败，改变故事方向',
                'all_is_lost': '主角应该到达最低点，似乎一切都失去了',
                'finale': '确保所有线索都得到解决'
            }
            if position['nearest_beat'] in beat_suggestions:
                suggestions.append(beat_suggestions[position['nearest_beat']])
        
        # 基于进展的建议
        if progression['main_plot_status'] == 'behind_schedule':
            suggestions.append('主线情节进展缓慢，考虑加快节奏')
        elif progression['main_plot_status'] == 'rushing':
            suggestions.append('主线推进过快，增加细节和角色发展')
        
        # 基于张力的建议
        if tension['adjustment_needed'] > 0.3:
            suggestions.append('当前张力不足，需要增加冲突或提升赌注')
        elif tension['adjustment_needed'] < -0.3:
            suggestions.append('张力过高，给予角色和读者喘息空间')
        
        return suggestions
    
    def _calculate_ideal_tension(self, progress: float) -> float:
        """计算理想张力值"""
        # 使用修改的正弦曲线模拟张力变化
        import math
        
        # 基础张力曲线
        base_tension = 0.3 + 0.4 * math.sin(progress * math.pi)
        
        # 在关键点增加张力峰值
        if 0.23 < progress < 0.27:  # 第一幕转折
            base_tension += 0.2
        elif 0.48 < progress < 0.52:  # 中点
            base_tension += 0.25
        elif 0.73 < progress < 0.77:  # 一无所有
            base_tension += 0.3
        elif 0.83 < progress < 0.87:  # 进入第三幕
            base_tension += 0.35
        
        return min(max(base_tension, 0.0), 1.0)
    
    async def _evaluate_scene_tension(self, scene: Dict) -> float:
        """评估场景张力"""
        tension = 0.3  # 基础张力
        
        content = scene.get('content', '').lower()
        
        # 冲突指标
        conflict_words = ['斗争', '对抗', '冲突', '危险', '威胁', '紧张']
        for word in conflict_words:
            if word in content:
                tension += 0.1
        
        # 情感强度
        intense_emotions = ['愤怒', '恐惧', '绝望', '狂喜', '震惊']
        for emotion in intense_emotions:
            if emotion in content:
                tension += 0.08
        
        # 时间压力
        time_pressure = ['立即', '马上', '来不及', '最后机会', '倒计时']
        for phrase in time_pressure:
            if phrase in content:
                tension += 0.12
        
        # 对话密度（快速对话增加张力）
        dialogue_lines = scene.get('dialogue', [])
        if len(dialogue_lines) > 10:
            tension += 0.1
        
        return min(tension, 1.0)
    
    async def _classify_scene_type(self, scene: Dict) -> str:
        """分类场景类型"""
        content = scene.get('content', '')
        dialogue = scene.get('dialogue', [])
        
        # 计算各类型的权重
        weights = {
            'action': 0,
            'dialogue': 0,
            'description': 0,
            'reflection': 0
        }
        
        # 动作场景标志
        action_indicators = ['冲', '跑', '打', '逃', '追', '跳', '攻击', '战斗']
        for indicator in action_indicators:
            if indicator in content:
                weights['action'] += 1
        
        # 对话权重
        if len(dialogue) > 5:
            weights['dialogue'] = len(dialogue) / 3
        
        # 描述权重
        description_indicators = ['景色', '环境', '氛围', '外貌', '装饰']
        for indicator in description_indicators:
            if indicator in content:
                weights['description'] += 1
        
        # 反思权重
        reflection_indicators = ['想起', '回忆', '思考', '意识到', '明白']
        for indicator in reflection_indicators:
            if indicator in content:
                weights['reflection'] += 1
        
        # 返回权重最高的类型
        return max(weights, key=weights.get)
    
    async def _get_expected_events(self, progress: float) -> List[str]:
        """获取预期事件"""
        events = []
        
        if progress > 0.12:
            events.append('catalyst')
        if progress > 0.25:
            events.append('break_into_act2')
        if progress > 0.50:
            events.append('midpoint')
        if progress > 0.75:
            events.append('all_is_lost')
        if progress > 0.85:
            events.append('break_into_act3')
        
        return events
    
    async def _assess_conflict_evolution(
        self, conflict: Dict, position: Dict
    ) -> Dict:
        """评估冲突演化"""
        evolution = {
            'conflict_id': conflict.get('id'),
            'intensity': conflict.get('intensity', 0.5),
            'stage': 'developing',
            'resolution_proximity': 0.0
        }
        
        # 根据叙事位置判断冲突阶段
        if position['progress'] < 0.25:
            evolution['stage'] = 'introducing'
        elif position['progress'] < 0.75:
            evolution['stage'] = 'escalating'
        elif position['progress'] < 0.90:
            evolution['stage'] = 'climaxing'
        else:
            evolution['stage'] = 'resolving'
            evolution['resolution_proximity'] = (position['progress'] - 0.90) * 10
        
        return evolution
    
    async def _calculate_momentum(self, scene: Dict, position: Dict) -> float:
        """计算叙事动量"""
        momentum = 0.5
        
        # 接近关键节拍时增加动量
        if position['nearest_beat']:
            key_beats = ['catalyst', 'midpoint', 'all_is_lost', 'finale']
            if position['nearest_beat'] in key_beats:
                momentum += 0.2
        
        # 在上升动作阶段增加动量
        if position['current_phase'] == NarrativePhase.RISING_ACTION.value:
            momentum += 0.15
        
        # 场景中有重要事件增加动量
        if 'major_event' in scene or 'revelation' in scene:
            momentum += 0.25
        
        return min(momentum, 1.0)
    
    async def _detect_theme_presence(self, theme: str, content: str) -> bool:
        """检测主题存在"""
        theme_keywords = {
            '爱情': ['爱', '情', '心动', '吸引'],
            '成长': ['成长', '改变', '学习', '领悟'],
            '牺牲': ['牺牲', '付出', '奉献', '舍弃'],
            '救赎': ['救赎', '原谅', '弥补', '重生'],
            '权力': ['权力', '控制', '支配', '统治']
        }
        
        keywords = theme_keywords.get(theme, [theme])
        return any(keyword in content for keyword in keywords)
    
    async def _detect_motif(self, motif: str, content: str) -> bool:
        """检测母题"""
        return motif.lower() in content.lower()
    
    async def _extract_motif_context(self, motif: str, content: str) -> str:
        """提取母题上下文"""
        index = content.lower().find(motif.lower())
        if index != -1:
            start = max(0, index - 50)
            end = min(len(content), index + len(motif) + 50)
            return content[start:end]
        return ""
    
    async def _analyze_symbol_usage(self, symbol: str, content: str) -> str:
        """分析象征使用"""
        count = content.lower().count(symbol.lower())
        if count > 3:
            return "频繁出现，强化象征意义"
        elif count > 1:
            return "多次出现，建立联系"
        else:
            return "单次出现，引入象征"
    
    async def _calculate_thread_priority(
        self, thread: PlotThread, chapter: int, context: Dict
    ) -> float:
        """计算线程优先级"""
        priority = 0.5
        
        # 主线始终高优先级
        if thread.thread_type == 'main':
            priority = 0.9
        
        # 接近解决的副线提高优先级
        if thread.thread_type == 'subplot':
            progress = (chapter - thread.start_chapter) / \
                      (thread.target_end_chapter - thread.start_chapter)
            if progress > 0.8:
                priority += 0.3
        
        return min(priority, 1.0)
    
    async def _detect_thread_intersection(
        self, thread1: str, thread2: str, scene: Dict
    ) -> bool:
        """检测线程交叉"""
        # 简化实现：检查场景是否同时涉及两个线程的元素
        thread1_present = thread1 in str(scene)
        thread2_present = thread2 in str(scene)
        return thread1_present and thread2_present
    
    async def _generate_weaving_pattern(
        self, active_threads: List[str], priorities: Dict[str, float]
    ) -> List[str]:
        """生成编织模式"""
        # 按优先级排序线程
        sorted_threads = sorted(
            active_threads,
            key=lambda x: priorities.get(x, 0),
            reverse=True
        )
        
        # 生成交织建议
        pattern = []
        if len(sorted_threads) > 0:
            pattern.append(f"主导线程: {sorted_threads[0]}")
        if len(sorted_threads) > 1:
            pattern.append(f"支撑线程: {', '.join(sorted_threads[1:])}")
        
        return pattern
    
    async def _calculate_structure_quality(
        self, position: Dict, progression: Dict
    ) -> Dict:
        """计算结构质量"""
        metrics = {
            'structure_coherence': 0.0,
            'pacing_quality': 0.0,
            'tension_management': 0.0,
            'thematic_depth': 0.0,
            'overall_score': 0.0
        }
        
        # 结构连贯性
        if position['current_act'] and position['nearest_beat']:
            metrics['structure_coherence'] = 0.8
        elif position['current_act']:
            metrics['structure_coherence'] = 0.6
        else:
            metrics['structure_coherence'] = 0.3
        
        # 节奏质量
        if self.narrative_model.pacing in ['moderate', 'variable']:
            metrics['pacing_quality'] = 0.7
        else:
            metrics['pacing_quality'] = 0.5
        
        # 张力管理
        tension_variance = abs(self.narrative_model.current_tension - 
                              self.narrative_model.target_tension)
        metrics['tension_management'] = max(0, 1.0 - tension_variance)
        
        # 主题深度
        metrics['thematic_depth'] = min(len(self.narrative_model.themes) * 0.2, 0.8)
        
        # 总分
        metrics['overall_score'] = sum(metrics.values()) / (len(metrics) - 1)
        
        return metrics
    
    async def _generate_fallback(self, scene: Dict) -> Dict:
        """生成降级方案"""
        return {
            'narrative_position': {'progress': 0.0, 'current_phase': 'unknown'},
            'suggestions': ['继续推进故事'],
            'message': 'Using simplified narrative structure'
        }