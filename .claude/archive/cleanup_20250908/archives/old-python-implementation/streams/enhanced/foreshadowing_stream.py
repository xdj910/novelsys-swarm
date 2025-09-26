"""
ForeshadowingStream - 伏笔管理大师
精确控制伏笔的植入、呼应和揭示
Quality Target: 100% foreshadowing completion rate
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import math


class ForeshadowType(Enum):
    """伏笔类型枚举"""
    PLOT_TWIST = "plot_twist"          # 情节转折
    CHARACTER_SECRET = "char_secret"    # 角色秘密
    WORLD_MYSTERY = "world_mystery"     # 世界谜团
    ITEM_SIGNIFICANCE = "item_sig"      # 物品意义
    RELATIONSHIP = "relationship"       # 关系真相
    PROPHECY = "prophecy"               # 预言暗示
    SYMBOLIC = "symbolic"               # 象征隐喻


class ForeshadowVisibility(Enum):
    """伏笔可见度级别"""
    INVISIBLE = 0.0      # 完全隐藏
    SUBLIMINAL = 0.2     # 潜意识级
    SUBTLE = 0.4         # 细微暗示
    NOTICEABLE = 0.6     # 可察觉
    OBVIOUS = 0.8        # 明显提示
    EXPLICIT = 1.0       # 明确展示


@dataclass
class Foreshadow:
    """伏笔数据类"""
    id: str
    type: ForeshadowType
    content: str
    plant_location: str
    reveal_location: str
    visibility: float
    importance: str  # critical/high/medium/low
    echo_points: List[str] = None
    dependencies: List[str] = None
    planted: bool = False
    echoed: List[str] = None
    revealed: bool = False
    
    def __post_init__(self):
        if self.echo_points is None:
            self.echo_points = []
        if self.dependencies is None:
            self.dependencies = []
        if self.echoed is None:
            self.echoed = []


class ForeshadowingStream:
    """
    伏笔管理Stream
    负责伏笔的全生命周期管理
    """
    
    def __init__(self):
        self.foreshadow_registry = {}  # 所有伏笔注册表
        self.active_shadows = []        # 活跃的伏笔
        self.revealed_shadows = []      # 已揭示的伏笔
        self.shadow_network = {}        # 伏笔关系网络
        self.timing_calculator = ForeshadowTimingCalculator()
        self.visibility_controller = VisibilityController()
        
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景的伏笔管理
        
        Args:
            scene: 场景信息
            context: 上下文信息，包含Bible和前文
            
        Returns:
            伏笔管理内容
        """
        scene_id = scene.get('id', '')
        
        # 1. 分析当前场景的伏笔需求
        shadow_requirements = await self._analyze_shadow_requirements(scene, context)
        
        # 2. 检查需要植入的伏笔
        shadows_to_plant = await self._get_shadows_to_plant(scene_id, context)
        
        # 3. 检查需要呼应的伏笔
        shadows_to_echo = await self._get_shadows_to_echo(scene_id)
        
        # 4. 检查需要揭示的伏笔
        shadows_to_reveal = await self._get_shadows_to_reveal(scene_id, context)
        
        # 5. 生成伏笔内容
        foreshadow_content = await self._generate_foreshadow_content(
            shadows_to_plant, shadows_to_echo, shadows_to_reveal, scene, context
        )
        
        # 6. 更新伏笔状态
        await self._update_shadow_states(scene_id, shadows_to_plant, shadows_to_echo, shadows_to_reveal)
        
        # 7. 验证伏笔完整性
        integrity_check = await self._verify_shadow_integrity()
        
        return {
            'requirements': shadow_requirements,
            'planting': foreshadow_content['plant'],
            'echoing': foreshadow_content['echo'],
            'revealing': foreshadow_content['reveal'],
            'subtle_hints': foreshadow_content['hints'],
            'symbolic_elements': foreshadow_content['symbols'],
            'integrity': integrity_check,
            'active_shadows': len(self.active_shadows),
            'completion_rate': self._calculate_completion_rate()
        }
    
    async def _analyze_shadow_requirements(self, scene: Dict, context: Dict) -> Dict:
        """分析场景的伏笔需求"""
        requirements = {
            'new_shadows_needed': [],
            'existing_shadows_relevant': [],
            'timing_optimal_for': [],
            'thematic_shadows': []
        }
        
        # 基于Bible分析需要的新伏笔
        bible = context.get('bible', {})
        plot_chain = bible.get('plot_chain', {})
        
        # 检查当前场景是否是关键植入点
        for shadow_key, shadow_info in plot_chain.get('foreshadowing_network', {}).items():
            if shadow_info['plant']['location'] == scene.get('id'):
                requirements['new_shadows_needed'].append({
                    'id': shadow_key,
                    'type': self._determine_shadow_type(shadow_info),
                    'content': shadow_info['plant']['content'],
                    'visibility': shadow_info['plant']['visibility']
                })
        
        # 分析主题相关的伏笔机会
        themes = bible.get('series_info', {}).get('themes', [])
        for theme in themes:
            if self._scene_matches_theme(scene, theme):
                requirements['thematic_shadows'].append({
                    'theme': theme,
                    'suggested_symbolism': self._generate_theme_symbolism(theme)
                })
        
        # 检查现有伏笔的相关性
        for shadow_id, shadow in self.foreshadow_registry.items():
            if shadow.planted and not shadow.revealed:
                relevance = self._calculate_shadow_relevance(shadow, scene, context)
                if relevance > 0.5:
                    requirements['existing_shadows_relevant'].append({
                        'id': shadow_id,
                        'relevance': relevance,
                        'suggested_echo': self._suggest_echo_approach(shadow, relevance)
                    })
        
        # 时机分析
        chapter_progress = context.get('chapter_progress', 0.0)
        for shadow in self.active_shadows:
            if self.timing_calculator.is_optimal_time(shadow, chapter_progress):
                requirements['timing_optimal_for'].append(shadow.id)
        
        return requirements
    
    async def _get_shadows_to_plant(self, scene_id: str, context: Dict) -> List[Foreshadow]:
        """获取需要植入的伏笔"""
        shadows_to_plant = []
        
        # 从Bible中获取计划的伏笔
        bible = context.get('bible', {})
        plot_chain = bible.get('plot_chain', {})
        
        for shadow_key, shadow_info in plot_chain.get('foreshadowing_network', {}).items():
            plant_location = shadow_info['plant']['location']
            
            # 检查是否是当前场景
            if plant_location == scene_id:
                # 创建伏笔对象
                shadow = Foreshadow(
                    id=shadow_key,
                    type=self._determine_shadow_type(shadow_info),
                    content=shadow_info['plant']['content'],
                    plant_location=plant_location,
                    reveal_location=shadow_info.get('reveal', {}).get('location', ''),
                    visibility=shadow_info['plant']['visibility'],
                    importance=shadow_info.get('importance', 'medium'),
                    echo_points=[e['location'] for e in shadow_info.get('echo', [])]
                )
                
                # 检查依赖
                if self._dependencies_satisfied(shadow, context):
                    shadows_to_plant.append(shadow)
                    
        # 动态生成的伏笔（基于故事发展）
        dynamic_shadows = await self._generate_dynamic_shadows(scene_id, context)
        shadows_to_plant.extend(dynamic_shadows)
        
        return shadows_to_plant
    
    async def _get_shadows_to_echo(self, scene_id: str) -> List[Tuple[Foreshadow, float]]:
        """获取需要呼应的伏笔"""
        shadows_to_echo = []
        
        for shadow in self.active_shadows:
            # 检查是否是计划的呼应点
            if scene_id in shadow.echo_points:
                echo_strength = self._calculate_echo_strength(shadow, scene_id)
                shadows_to_echo.append((shadow, echo_strength))
            
            # 检查是否需要自然呼应（即使不是计划点）
            elif self._should_naturally_echo(shadow, scene_id):
                echo_strength = 0.3  # 自然呼应较弱
                shadows_to_echo.append((shadow, echo_strength))
        
        # 按重要性排序
        shadows_to_echo.sort(key=lambda x: x[0].importance == 'critical', reverse=True)
        
        return shadows_to_echo
    
    async def _get_shadows_to_reveal(self, scene_id: str, context: Dict) -> List[Foreshadow]:
        """获取需要揭示的伏笔"""
        shadows_to_reveal = []
        
        for shadow in self.active_shadows:
            # 检查是否是计划的揭示点
            if shadow.reveal_location == scene_id:
                shadows_to_reveal.append(shadow)
            
            # 检查是否满足提前揭示条件
            elif self._can_reveal_early(shadow, scene_id, context):
                shadows_to_reveal.append(shadow)
        
        return shadows_to_reveal
    
    async def _generate_foreshadow_content(
        self, to_plant: List[Foreshadow], 
        to_echo: List[Tuple[Foreshadow, float]],
        to_reveal: List[Foreshadow],
        scene: Dict, context: Dict
    ) -> Dict:
        """生成具体的伏笔内容"""
        content = {
            'plant': [],
            'echo': [],
            'reveal': [],
            'hints': [],
            'symbols': []
        }
        
        # 生成植入内容
        for shadow in to_plant:
            plant_content = await self._create_plant_content(shadow, scene, context)
            content['plant'].append({
                'shadow_id': shadow.id,
                'type': shadow.type.value,
                'visibility': shadow.visibility,
                'content': plant_content['text'],
                'placement': plant_content['placement'],
                'technique': plant_content['technique']
            })
            
            # 添加相关暗示
            if plant_content.get('hints'):
                content['hints'].extend(plant_content['hints'])
        
        # 生成呼应内容
        for shadow, strength in to_echo:
            echo_content = await self._create_echo_content(shadow, strength, scene)
            content['echo'].append({
                'shadow_id': shadow.id,
                'strength': strength,
                'content': echo_content['text'],
                'technique': echo_content['technique'],
                'connection': echo_content['connection']
            })
        
        # 生成揭示内容
        for shadow in to_reveal:
            reveal_content = await self._create_reveal_content(shadow, scene, context)
            content['reveal'].append({
                'shadow_id': shadow.id,
                'impact': reveal_content['impact'],
                'content': reveal_content['text'],
                'revelation_style': reveal_content['style'],
                'character_reactions': reveal_content['reactions']
            })
        
        # 生成象征元素
        symbols = await self._generate_symbolic_elements(scene, context)
        content['symbols'] = symbols
        
        return content
    
    async def _create_plant_content(self, shadow: Foreshadow, scene: Dict, context: Dict) -> Dict:
        """创建伏笔植入内容"""
        content = {
            'text': '',
            'placement': '',
            'technique': '',
            'hints': []
        }
        
        # 根据可见度选择植入技巧
        if shadow.visibility <= 0.2:  # 几乎不可见
            content['technique'] = 'subliminal'
            content['placement'] = 'background_detail'
            content['text'] = self._generate_subliminal_hint(shadow)
            
        elif shadow.visibility <= 0.4:  # 细微
            content['technique'] = 'subtle_mention'
            content['placement'] = 'passing_reference'
            content['text'] = self._generate_subtle_reference(shadow)
            
        elif shadow.visibility <= 0.6:  # 可察觉
            content['technique'] = 'embedded_clue'
            content['placement'] = 'dialogue_subtext'
            content['text'] = self._generate_embedded_clue(shadow)
            content['hints'].append(self._create_supporting_hint(shadow))
            
        elif shadow.visibility <= 0.8:  # 明显
            content['technique'] = 'direct_hint'
            content['placement'] = 'prominent_mention'
            content['text'] = self._generate_direct_hint(shadow)
            
        else:  # 明确
            content['technique'] = 'explicit_setup'
            content['placement'] = 'focal_point'
            content['text'] = self._generate_explicit_setup(shadow)
        
        # 根据伏笔类型调整内容
        content = self._adjust_for_shadow_type(content, shadow)
        
        return content
    
    async def _create_echo_content(self, shadow: Foreshadow, strength: float, scene: Dict) -> Dict:
        """创建伏笔呼应内容"""
        content = {
            'text': '',
            'technique': '',
            'connection': ''
        }
        
        if strength <= 0.3:  # 弱呼应
            content['technique'] = 'parallel_structure'
            content['connection'] = 'thematic'
            content['text'] = f"[细微呼应{shadow.id}：使用相似的描述或情境]"
            
        elif strength <= 0.6:  # 中等呼应
            content['technique'] = 'callback'
            content['connection'] = 'direct_reference'
            content['text'] = f"[中度呼应{shadow.id}：角色回忆或提及相关内容]"
            
        else:  # 强呼应
            content['technique'] = 'amplification'
            content['connection'] = 'development'
            content['text'] = f"[强烈呼应{shadow.id}：深化或扩展原始伏笔]"
        
        return content
    
    async def _create_reveal_content(self, shadow: Foreshadow, scene: Dict, context: Dict) -> Dict:
        """创建伏笔揭示内容"""
        impact_level = self._calculate_reveal_impact(shadow)
        
        content = {
            'impact': impact_level,
            'text': '',
            'style': '',
            'reactions': []
        }
        
        if impact_level == 'minor':
            content['style'] = 'casual_revelation'
            content['text'] = f"[轻微揭示{shadow.id}：自然流露真相]"
            
        elif impact_level == 'moderate':
            content['style'] = 'dramatic_reveal'
            content['text'] = f"[中度揭示{shadow.id}：戏剧性展现真相]"
            content['reactions'] = ['surprise', 'understanding']
            
        elif impact_level == 'major':
            content['style'] = 'shocking_twist'
            content['text'] = f"[重大揭示{shadow.id}：震撼性转折]"
            content['reactions'] = ['shock', 'disbelief', 'realization']
            
        else:  # critical
            content['style'] = 'paradigm_shift'
            content['text'] = f"[关键揭示{shadow.id}：颠覆性真相]"
            content['reactions'] = ['devastation', 'epiphany', 'transformation']
        
        # 添加角色反应描述
        content['character_reactions'] = self._generate_character_reactions(
            shadow, impact_level, scene
        )
        
        return content
    
    async def _update_shadow_states(
        self, scene_id: str,
        planted: List[Foreshadow],
        echoed: List[Tuple[Foreshadow, float]],
        revealed: List[Foreshadow]
    ):
        """更新伏笔状态"""
        # 更新植入状态
        for shadow in planted:
            shadow.planted = True
            self.foreshadow_registry[shadow.id] = shadow
            self.active_shadows.append(shadow)
        
        # 更新呼应状态
        for shadow, strength in echoed:
            if scene_id not in shadow.echoed:
                shadow.echoed.append(scene_id)
        
        # 更新揭示状态
        for shadow in revealed:
            shadow.revealed = True
            if shadow in self.active_shadows:
                self.active_shadows.remove(shadow)
            self.revealed_shadows.append(shadow)
    
    async def _verify_shadow_integrity(self) -> Dict:
        """验证伏笔完整性"""
        integrity = {
            'complete_chains': [],
            'broken_chains': [],
            'orphaned_shadows': [],
            'missing_reveals': [],
            'timing_issues': []
        }
        
        for shadow_id, shadow in self.foreshadow_registry.items():
            # 检查完整链条
            if shadow.planted and shadow.revealed:
                if len(shadow.echoed) >= len(shadow.echo_points) * 0.7:
                    integrity['complete_chains'].append(shadow_id)
                else:
                    integrity['broken_chains'].append({
                        'id': shadow_id,
                        'missing_echoes': set(shadow.echo_points) - set(shadow.echoed)
                    })
            
            # 检查孤立伏笔
            elif shadow.planted and not shadow.reveal_location:
                integrity['orphaned_shadows'].append(shadow_id)
            
            # 检查缺失揭示
            elif shadow.planted and shadow.reveal_location and not shadow.revealed:
                integrity['missing_reveals'].append({
                    'id': shadow_id,
                    'expected_location': shadow.reveal_location
                })
        
        integrity['integrity_score'] = self._calculate_integrity_score(integrity)
        
        return integrity
    
    def _calculate_completion_rate(self) -> float:
        """计算伏笔完成率"""
        if not self.foreshadow_registry:
            return 1.0
        
        total = len(self.foreshadow_registry)
        completed = len([s for s in self.revealed_shadows if s.id in self.foreshadow_registry])
        
        return completed / total if total > 0 else 0.0
    
    # 辅助方法
    def _determine_shadow_type(self, shadow_info: Dict) -> ForeshadowType:
        """确定伏笔类型"""
        content = shadow_info.get('plant', {}).get('content', '')
        
        if 'character' in content or 'identity' in content:
            return ForeshadowType.CHARACTER_SECRET
        elif 'item' in content or 'object' in content:
            return ForeshadowType.ITEM_SIGNIFICANCE
        elif 'prophecy' in content or 'prediction' in content:
            return ForeshadowType.PROPHECY
        elif 'symbol' in content:
            return ForeshadowType.SYMBOLIC
        elif 'relationship' in content:
            return ForeshadowType.RELATIONSHIP
        elif 'world' in content or 'mystery' in content:
            return ForeshadowType.WORLD_MYSTERY
        else:
            return ForeshadowType.PLOT_TWIST
    
    def _dependencies_satisfied(self, shadow: Foreshadow, context: Dict) -> bool:
        """检查伏笔依赖是否满足"""
        for dep in shadow.dependencies:
            if dep not in self.revealed_shadows:
                return False
        return True
    
    def _calculate_shadow_relevance(self, shadow: Foreshadow, scene: Dict, context: Dict) -> float:
        """计算伏笔与场景的相关性"""
        relevance = 0.0
        
        # 检查场景类型匹配
        if self._shadow_matches_scene_type(shadow, scene):
            relevance += 0.3
        
        # 检查角色相关性
        if self._shadow_relates_to_characters(shadow, scene):
            relevance += 0.3
        
        # 检查主题相关性
        if self._shadow_matches_themes(shadow, context):
            relevance += 0.2
        
        # 时间距离因素
        time_factor = self._calculate_time_factor(shadow, context)
        relevance += time_factor * 0.2
        
        return min(relevance, 1.0)
    
    def _suggest_echo_approach(self, shadow: Foreshadow, relevance: float) -> str:
        """建议呼应方式"""
        if relevance > 0.8:
            return "direct_callback"
        elif relevance > 0.6:
            return "thematic_parallel"
        elif relevance > 0.4:
            return "subtle_reminder"
        else:
            return "atmospheric_echo"
    
    def _calculate_echo_strength(self, shadow: Foreshadow, scene_id: str) -> float:
        """计算呼应强度"""
        # 基于伏笔重要性和场景位置
        base_strength = 0.5
        
        if shadow.importance == 'critical':
            base_strength += 0.3
        elif shadow.importance == 'high':
            base_strength += 0.2
        
        # 检查是否接近揭示点
        if self._near_reveal_point(shadow, scene_id):
            base_strength += 0.2
        
        return min(base_strength, 1.0)
    
    def _should_naturally_echo(self, shadow: Foreshadow, scene_id: str) -> bool:
        """判断是否应该自然呼应"""
        # 基于随机性和重要性
        import random
        threshold = 0.7 if shadow.importance == 'critical' else 0.9
        return random.random() > threshold
    
    def _can_reveal_early(self, shadow: Foreshadow, scene_id: str, context: Dict) -> bool:
        """检查是否可以提前揭示"""
        # 某些条件下可以提前揭示
        if context.get('tension_level', 0) > 0.9 and shadow.importance != 'critical':
            return True
        return False
    
    def _calculate_reveal_impact(self, shadow: Foreshadow) -> str:
        """计算揭示影响等级"""
        if shadow.importance == 'critical':
            return 'critical'
        elif shadow.importance == 'high':
            return 'major'
        elif shadow.importance == 'medium':
            return 'moderate'
        else:
            return 'minor'
    
    def _generate_character_reactions(self, shadow: Foreshadow, impact: str, scene: Dict) -> List[Dict]:
        """生成角色反应"""
        reactions = []
        
        for character in scene.get('characters', []):
            reaction = {
                'character': character['name'],
                'emotional_response': self._get_emotional_response(impact),
                'physical_response': self._get_physical_response(impact),
                'verbal_response': self._get_verbal_response(impact)
            }
            reactions.append(reaction)
        
        return reactions
    
    def _scene_matches_theme(self, scene: Dict, theme: str) -> bool:
        """检查场景是否匹配主题"""
        # 简化实现
        return theme.lower() in str(scene).lower()
    
    def _generate_theme_symbolism(self, theme: str) -> str:
        """生成主题象征"""
        symbolism_map = {
            'truth': '镜子、光明、揭开的面纱',
            'betrayal': '影子、碎裂的镜子、双面',
            'power': '高处、王冠、掌控',
            'love': '温暖、连接、牺牲',
            'justice': '天平、剑、盲目'
        }
        
        for key, symbol in symbolism_map.items():
            if key in theme.lower():
                return symbol
        
        return '象征元素'
    
    async def _generate_dynamic_shadows(self, scene_id: str, context: Dict) -> List[Foreshadow]:
        """动态生成伏笔"""
        # 基于故事发展动态创建新伏笔
        dynamic_shadows = []
        
        # 简化实现，实际应该基于复杂逻辑
        if context.get('chapter_number', 0) == 1 and 'sc1' in scene_id:
            shadow = Foreshadow(
                id='dynamic_shadow_1',
                type=ForeshadowType.CHARACTER_SECRET,
                content='角色隐藏的过去',
                plant_location=scene_id,
                reveal_location='ch5_sc3',
                visibility=0.3,
                importance='high'
            )
            dynamic_shadows.append(shadow)
        
        return dynamic_shadows
    
    async def _generate_symbolic_elements(self, scene: Dict, context: Dict) -> List[Dict]:
        """生成象征元素"""
        symbols = []
        
        # 基于场景和主题生成象征
        themes = context.get('bible', {}).get('series_info', {}).get('themes', [])
        
        for theme in themes:
            symbol = {
                'theme': theme,
                'element': self._generate_theme_symbolism(theme),
                'placement': 'environmental_detail',
                'intensity': 0.5
            }
            symbols.append(symbol)
        
        return symbols
    
    # 内容生成方法
    def _generate_subliminal_hint(self, shadow: Foreshadow) -> str:
        """生成潜意识级暗示"""
        return f"[几乎不可见的暗示：在背景中轻微提及与{shadow.content}相关的细节]"
    
    def _generate_subtle_reference(self, shadow: Foreshadow) -> str:
        """生成细微引用"""
        return f"[细微暗示：通过环境描写或次要对话间接提及{shadow.content}]"
    
    def _generate_embedded_clue(self, shadow: Foreshadow) -> str:
        """生成嵌入式线索"""
        return f"[嵌入线索：在对话或描述中自然融入{shadow.content}的线索]"
    
    def _generate_direct_hint(self, shadow: Foreshadow) -> str:
        """生成直接暗示"""
        return f"[明显暗示：直接但不完全地展示{shadow.content}]"
    
    def _generate_explicit_setup(self, shadow: Foreshadow) -> str:
        """生成明确铺垫"""
        return f"[明确铺垫：清晰地建立{shadow.content}的期待]"
    
    def _create_supporting_hint(self, shadow: Foreshadow) -> str:
        """创建支持性暗示"""
        return f"[辅助暗示：强化{shadow.id}的额外细节]"
    
    def _adjust_for_shadow_type(self, content: Dict, shadow: Foreshadow) -> Dict:
        """根据伏笔类型调整内容"""
        if shadow.type == ForeshadowType.CHARACTER_SECRET:
            content['text'] += " [通过行为细节或对话停顿暗示]"
        elif shadow.type == ForeshadowType.ITEM_SIGNIFICANCE:
            content['text'] += " [通过特殊描述或角色反应暗示]"
        elif shadow.type == ForeshadowType.PROPHECY:
            content['text'] += " [通过隐喻或梦境暗示]"
        
        return content
    
    def _shadow_matches_scene_type(self, shadow: Foreshadow, scene: Dict) -> bool:
        """检查伏笔是否匹配场景类型"""
        # 简化实现
        return True
    
    def _shadow_relates_to_characters(self, shadow: Foreshadow, scene: Dict) -> bool:
        """检查伏笔是否与场景角色相关"""
        # 简化实现
        return len(scene.get('characters', [])) > 0
    
    def _shadow_matches_themes(self, shadow: Foreshadow, context: Dict) -> bool:
        """检查伏笔是否匹配主题"""
        # 简化实现
        return True
    
    def _calculate_time_factor(self, shadow: Foreshadow, context: Dict) -> float:
        """计算时间因素"""
        # 简化实现
        return 0.5
    
    def _near_reveal_point(self, shadow: Foreshadow, scene_id: str) -> bool:
        """检查是否接近揭示点"""
        # 简化实现
        return False
    
    def _get_emotional_response(self, impact: str) -> str:
        """获取情感反应"""
        responses = {
            'minor': 'curiosity',
            'moderate': 'surprise',
            'major': 'shock',
            'critical': 'devastation'
        }
        return responses.get(impact, 'neutral')
    
    def _get_physical_response(self, impact: str) -> str:
        """获取身体反应"""
        responses = {
            'minor': 'raised_eyebrow',
            'moderate': 'step_back',
            'major': 'gasp',
            'critical': 'collapse'
        }
        return responses.get(impact, 'stillness')
    
    def _get_verbal_response(self, impact: str) -> str:
        """获取语言反应"""
        responses = {
            'minor': 'interesting',
            'moderate': 'what',
            'major': 'impossible',
            'critical': 'silence'
        }
        return responses.get(impact, 'acknowledgment')
    
    def _calculate_integrity_score(self, integrity: Dict) -> float:
        """计算完整性分数"""
        total = len(self.foreshadow_registry)
        if total == 0:
            return 1.0
        
        complete = len(integrity['complete_chains'])
        broken = len(integrity['broken_chains'])
        orphaned = len(integrity['orphaned_shadows'])
        
        score = (complete * 1.0 - broken * 0.3 - orphaned * 0.5) / total
        
        return max(0.0, min(1.0, score))


class ForeshadowTimingCalculator:
    """伏笔时机计算器"""
    
    def is_optimal_time(self, shadow: Foreshadow, progress: float) -> bool:
        """判断是否是最佳时机"""
        # 基于伏笔类型和故事进度
        if shadow.importance == 'critical':
            # 关键伏笔需要在特定时机
            return abs(progress - 0.7) < 0.1
        elif shadow.importance == 'high':
            return 0.3 < progress < 0.8
        else:
            return True


class VisibilityController:
    """可见度控制器"""
    
    def adjust_visibility(self, base_visibility: float, context: Dict) -> float:
        """调整可见度"""
        adjusted = base_visibility
        
        # 基于读者注意力调整
        attention_level = context.get('reader_attention', 0.5)
        if attention_level > 0.8:
            adjusted *= 0.8  # 降低可见度
        elif attention_level < 0.3:
            adjusted *= 1.2  # 提高可见度
        
        return max(0.0, min(1.0, adjusted))


# 测试函数
async def test_foreshadowing_stream():
    """测试伏笔管理Stream"""
    stream = ForeshadowingStream()
    
    # 测试场景
    test_scene = {
        'id': 'ch1_sc2',
        'type': 'mystery_introduction',
        'characters': [
            {'name': '李明'},
            {'name': '神秘人'}
        ]
    }
    
    # 测试上下文
    test_context = {
        'bible': {
            'series_info': {
                'themes': ['truth', 'betrayal', 'justice']
            },
            'plot_chain': {
                'foreshadowing_network': {
                    'shadow_1': {
                        'plant': {
                            'location': 'ch1_sc2',
                            'content': 'character_secret',
                            'visibility': 0.3
                        },
                        'echo': [
                            {'location': 'ch3_sc1', 'strength': 0.5}
                        ],
                        'reveal': {
                            'location': 'ch5_sc3',
                            'impact': 'major'
                        },
                        'importance': 'high'
                    }
                }
            }
        },
        'chapter_number': 1,
        'chapter_progress': 0.2
    }
    
    # 运行测试
    result = await stream.generate(test_scene, test_context)
    
    print("伏笔管理结果：")
    print(f"活跃伏笔数: {result['active_shadows']}")
    print(f"完成率: {result['completion_rate']:.2%}")
    print(f"植入内容: {json.dumps(result['planting'], indent=2, ensure_ascii=False)}")
    print(f"完整性检查: {json.dumps(result['integrity'], indent=2, ensure_ascii=False)}")
    
    return result


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_foreshadowing_stream())