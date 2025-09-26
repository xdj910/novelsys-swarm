"""
World Building Stream
世界构建Stream - 极致品质系统核心组件
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime
import json

class LocationType(Enum):
    """地点类型"""
    URBAN = "urban"              # 城市
    RURAL = "rural"              # 乡村
    WILDERNESS = "wilderness"    # 荒野
    INTERIOR = "interior"        # 室内
    TRANSITIONAL = "transitional"  # 过渡空间
    VIRTUAL = "virtual"          # 虚拟空间
    DREAMSCAPE = "dreamscape"    # 梦境

class TimeOfDay(Enum):
    """时间段"""
    DAWN = "dawn"          # 黎明
    MORNING = "morning"    # 早晨
    NOON = "noon"          # 正午
    AFTERNOON = "afternoon"  # 下午
    DUSK = "dusk"          # 黄昏
    EVENING = "evening"    # 傍晚
    NIGHT = "night"        # 夜晚
    MIDNIGHT = "midnight"  # 午夜

class WeatherCondition(Enum):
    """天气状况"""
    CLEAR = "clear"          # 晴朗
    CLOUDY = "cloudy"        # 多云
    RAINY = "rainy"          # 雨天
    STORMY = "stormy"        # 暴风雨
    SNOWY = "snowy"          # 雪天
    FOGGY = "foggy"          # 雾天
    WINDY = "windy"          # 大风

@dataclass
class Location:
    """地点模型"""
    location_id: str
    name: str
    type: LocationType
    description: str
    
    # 物理属性
    size: str = "medium"  # small, medium, large, vast
    layout: Dict[str, Any] = field(default_factory=dict)
    landmarks: List[str] = field(default_factory=list)
    
    # 感官细节
    visual_details: List[str] = field(default_factory=list)
    sounds: List[str] = field(default_factory=list)
    smells: List[str] = field(default_factory=list)
    textures: List[str] = field(default_factory=list)
    temperature: str = "moderate"
    
    # 氛围与情绪
    atmosphere: str = "neutral"
    emotional_tone: str = "neutral"
    symbolic_meaning: Optional[str] = None
    
    # 历史与文化
    history: List[str] = field(default_factory=list)
    cultural_significance: Optional[str] = None
    local_customs: List[str] = field(default_factory=list)
    
    # 连接关系
    connected_locations: List[str] = field(default_factory=list)
    travel_times: Dict[str, float] = field(default_factory=dict)  # 到其他地点的时间
    
    # 居民与活动
    inhabitants: List[str] = field(default_factory=list)
    typical_activities: List[str] = field(default_factory=list)
    
    # 时间变化
    time_variations: Dict[TimeOfDay, Dict] = field(default_factory=dict)
    seasonal_changes: Dict[str, str] = field(default_factory=dict)

@dataclass
class WorldState:
    """世界状态"""
    current_time: datetime
    time_of_day: TimeOfDay
    weather: WeatherCondition
    season: str
    
    # 社会状态
    political_climate: str = "stable"
    economic_situation: str = "moderate"
    social_tensions: List[str] = field(default_factory=list)
    current_events: List[str] = field(default_factory=list)
    
    # 文化背景
    cultural_context: Dict[str, Any] = field(default_factory=dict)
    prevailing_beliefs: List[str] = field(default_factory=list)
    taboos: List[str] = field(default_factory=list)
    
    # 技术水平
    technology_level: str = "contemporary"
    available_tech: List[str] = field(default_factory=list)
    communication_methods: List[str] = field(default_factory=list)
    
    # 全局事件
    ongoing_conflicts: List[Dict] = field(default_factory=list)
    recent_disasters: List[Dict] = field(default_factory=list)
    celebrations: List[Dict] = field(default_factory=list)

@dataclass
class SensoryLayer:
    """感官层次"""
    dominant_sense: str  # visual, auditory, olfactory, tactile, gustatory
    intensity: float  # 0-1
    details: List[str]
    emotional_impact: str

class WorldBuildingStream:
    """
    世界构建Stream
    - 环境描写
    - 感官细节
    - 时空连续性
    - 文化背景
    """
    
    def __init__(self):
        self.stream_id = "world_building"
        self.weight = 0.125
        self.locations: Dict[str, Location] = {}
        self.world_state: Optional[WorldState] = None
        self.location_graph: Dict[str, List[str]] = {}  # 地点连接图
        self.time_tracker: Dict[str, datetime] = {}  # 角色时间追踪
        
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景，返回世界构建结果
        """
        try:
            # 1. 初始化或更新世界状态
            await self._update_world_state(scene, context)
            
            # 2. 确定场景地点
            location_info = await self._determine_location(scene, context)
            
            # 3. 构建环境细节
            environmental_details = await self._build_environment(
                location_info, scene, context
            )
            
            # 4. 生成感官层次
            sensory_layers = await self._generate_sensory_layers(
                location_info, environmental_details, scene
            )
            
            # 5. 维护时空连续性
            spatiotemporal_continuity = await self._maintain_continuity(
                location_info, scene, context
            )
            
            # 6. 融入文化元素
            cultural_elements = await self._integrate_culture(
                location_info, scene, context
            )
            
            # 7. 创建氛围渲染
            atmosphere_rendering = await self._render_atmosphere(
                location_info, environmental_details, sensory_layers
            )
            
            # 8. 生成世界细节建议
            world_suggestions = await self._generate_world_suggestions(
                location_info, spatiotemporal_continuity
            )
            
            return {
                'stream_id': self.stream_id,
                'weight': self.weight,
                'location': location_info,
                'environment': environmental_details,
                'sensory_layers': sensory_layers,
                'continuity': spatiotemporal_continuity,
                'cultural_elements': cultural_elements,
                'atmosphere': atmosphere_rendering,
                'suggestions': world_suggestions,
                'quality_metrics': await self._calculate_world_quality(
                    environmental_details, sensory_layers, spatiotemporal_continuity
                )
            }
            
        except Exception as e:
            return {
                'stream_id': self.stream_id,
                'error': str(e),
                'fallback': await self._generate_fallback(scene)
            }
    
    async def _update_world_state(self, scene: Dict, context: Dict):
        """更新世界状态"""
        if not self.world_state:
            # 初始化世界状态
            self.world_state = WorldState(
                current_time=datetime.now(),
                time_of_day=TimeOfDay.MORNING,
                weather=WeatherCondition.CLEAR,
                season=context.get('season', 'spring'),
                technology_level=context.get('technology_level', 'contemporary'),
                political_climate=context.get('political_climate', 'stable')
            )
        
        # 更新时间
        if 'time' in scene:
            self.world_state.current_time = scene['time']
            self.world_state.time_of_day = await self._determine_time_of_day(scene['time'])
        
        # 更新天气
        if 'weather' in scene:
            self.world_state.weather = WeatherCondition[scene['weather'].upper()]
        
        # 更新社会事件
        if 'current_events' in context:
            self.world_state.current_events = context['current_events']
    
    async def _determine_location(self, scene: Dict, context: Dict) -> Dict:
        """确定场景地点"""
        location_id = scene.get('location_id', 'unknown')
        
        # 如果是新地点，创建它
        if location_id not in self.locations:
            location = await self._create_location(location_id, scene, context)
            self.locations[location_id] = location
        else:
            location = self.locations[location_id]
        
        # 更新地点信息
        if 'location_updates' in scene:
            await self._update_location(location, scene['location_updates'])
        
        return {
            'id': location_id,
            'name': location.name,
            'type': location.type.value,
            'description': location.description,
            'atmosphere': location.atmosphere,
            'current_activity': await self._determine_current_activity(location, scene)
        }
    
    async def _create_location(
        self, location_id: str, scene: Dict, context: Dict
    ) -> Location:
        """创建新地点"""
        location_info = context.get('locations', {}).get(location_id, {})
        
        location = Location(
            location_id=location_id,
            name=location_info.get('name', f'Location_{location_id}'),
            type=LocationType[location_info.get('type', 'INTERIOR').upper()],
            description=location_info.get('description', ''),
            size=location_info.get('size', 'medium'),
            atmosphere=location_info.get('atmosphere', 'neutral'),
            emotional_tone=location_info.get('emotional_tone', 'neutral')
        )
        
        # 添加感官细节
        if 'sensory' in location_info:
            location.visual_details = location_info['sensory'].get('visual', [])
            location.sounds = location_info['sensory'].get('sounds', [])
            location.smells = location_info['sensory'].get('smells', [])
            location.textures = location_info['sensory'].get('textures', [])
        
        # 添加文化历史
        if 'culture' in location_info:
            location.history = location_info['culture'].get('history', [])
            location.cultural_significance = location_info['culture'].get('significance')
            location.local_customs = location_info['culture'].get('customs', [])
        
        return location
    
    async def _build_environment(
        self, location: Dict, scene: Dict, context: Dict
    ) -> Dict:
        """构建环境细节"""
        environment = {
            'physical_setting': {},
            'weather_effects': {},
            'lighting': {},
            'spatial_relations': {},
            'interactive_elements': []
        }
        
        # 物理设置
        location_obj = self.locations.get(location['id'])
        if location_obj:
            environment['physical_setting'] = {
                'size': location_obj.size,
                'layout': location_obj.layout,
                'landmarks': location_obj.landmarks,
                'boundaries': await self._determine_boundaries(location_obj)
            }
        
        # 天气影响
        environment['weather_effects'] = await self._calculate_weather_effects(
            self.world_state.weather, location
        )
        
        # 光照条件
        environment['lighting'] = await self._determine_lighting(
            self.world_state.time_of_day,
            self.world_state.weather,
            location
        )
        
        # 空间关系
        environment['spatial_relations'] = await self._map_spatial_relations(
            location, scene
        )
        
        # 可交互元素
        environment['interactive_elements'] = await self._identify_interactive_elements(
            location, scene
        )
        
        return environment
    
    async def _generate_sensory_layers(
        self, location: Dict, environment: Dict, scene: Dict
    ) -> List[SensoryLayer]:
        """生成感官层次"""
        layers = []
        
        location_obj = self.locations.get(location['id'])
        if not location_obj:
            return layers
        
        # 视觉层
        visual_layer = SensoryLayer(
            dominant_sense='visual',
            intensity=0.8,
            details=location_obj.visual_details + 
                   await self._generate_visual_details(environment),
            emotional_impact=await self._assess_visual_impact(location_obj)
        )
        layers.append(visual_layer)
        
        # 听觉层
        auditory_layer = SensoryLayer(
            dominant_sense='auditory',
            intensity=0.6,
            details=location_obj.sounds + 
                   await self._generate_ambient_sounds(environment, scene),
            emotional_impact=await self._assess_auditory_impact(location_obj)
        )
        layers.append(auditory_layer)
        
        # 嗅觉层
        if location_obj.smells:
            olfactory_layer = SensoryLayer(
                dominant_sense='olfactory',
                intensity=0.4,
                details=location_obj.smells,
                emotional_impact=await self._assess_olfactory_impact(location_obj)
            )
            layers.append(olfactory_layer)
        
        # 触觉层
        if location_obj.textures or environment.get('weather_effects'):
            tactile_layer = SensoryLayer(
                dominant_sense='tactile',
                intensity=0.3,
                details=location_obj.textures + 
                       await self._generate_tactile_sensations(environment),
                emotional_impact='grounding'
            )
            layers.append(tactile_layer)
        
        # 根据场景需要调整感官强度
        await self._adjust_sensory_intensity(layers, scene)
        
        return layers
    
    async def _maintain_continuity(
        self, location: Dict, scene: Dict, context: Dict
    ) -> Dict:
        """维护时空连续性"""
        continuity = {
            'spatial_consistency': True,
            'temporal_consistency': True,
            'travel_feasibility': True,
            'issues': [],
            'corrections': []
        }
        
        # 检查空间连续性
        previous_location = context.get('previous_location')
        if previous_location:
            # 检查是否可以从前一个地点到达当前地点
            if not await self._check_spatial_connection(
                previous_location, location['id']
            ):
                continuity['spatial_consistency'] = False
                continuity['issues'].append(
                    f"从{previous_location}到{location['id']}的路径不明确"
                )
                continuity['corrections'].append(
                    "添加过渡场景或说明移动方式"
                )
        
        # 检查时间连续性
        previous_time = context.get('previous_time')
        current_time = scene.get('time', self.world_state.current_time)
        
        if previous_time and current_time:
            time_gap = await self._calculate_time_gap(previous_time, current_time)
            travel_time = await self._estimate_travel_time(
                previous_location, location['id']
            )
            
            if travel_time and time_gap < travel_time:
                continuity['temporal_consistency'] = False
                continuity['issues'].append(
                    f"时间间隔({time_gap}分钟)小于所需行程时间({travel_time}分钟)"
                )
                continuity['corrections'].append(
                    "调整时间设定或使用更快的交通方式"
                )
        
        # 检查角色位置追踪
        character_locations = await self._track_character_locations(scene, context)
        for char_id, char_location in character_locations.items():
            if char_location != location['id']:
                continuity['issues'].append(
                    f"{char_id}的位置不一致"
                )
        
        return continuity
    
    async def _integrate_culture(
        self, location: Dict, scene: Dict, context: Dict
    ) -> Dict:
        """融入文化元素"""
        cultural_elements = {
            'customs': [],
            'beliefs': [],
            'social_norms': [],
            'language_patterns': [],
            'cultural_artifacts': []
        }
        
        location_obj = self.locations.get(location['id'])
        if not location_obj:
            return cultural_elements
        
        # 地方习俗
        cultural_elements['customs'] = location_obj.local_customs
        
        # 信仰体系
        cultural_elements['beliefs'] = self.world_state.prevailing_beliefs
        
        # 社会规范
        cultural_elements['social_norms'] = await self._identify_social_norms(
            location_obj, self.world_state
        )
        
        # 语言模式
        cultural_elements['language_patterns'] = await self._generate_language_patterns(
            location_obj, context.get('culture', {})
        )
        
        # 文化物品
        cultural_elements['cultural_artifacts'] = await self._identify_artifacts(
            location_obj, scene
        )
        
        return cultural_elements
    
    async def _render_atmosphere(
        self, location: Dict, environment: Dict, sensory_layers: List[SensoryLayer]
    ) -> Dict:
        """渲染氛围"""
        atmosphere = {
            'overall_mood': '',
            'emotional_tone': '',
            'tension_level': 0.0,
            'immersion_elements': [],
            'suggested_descriptions': []
        }
        
        location_obj = self.locations.get(location['id'])
        if not location_obj:
            return atmosphere
        
        # 确定整体情绪
        atmosphere['overall_mood'] = location_obj.atmosphere
        atmosphere['emotional_tone'] = location_obj.emotional_tone
        
        # 计算紧张度
        atmosphere['tension_level'] = await self._calculate_atmospheric_tension(
            location_obj, environment, sensory_layers
        )
        
        # 沉浸元素
        for layer in sensory_layers:
            if layer.intensity > 0.5:
                atmosphere['immersion_elements'].extend(layer.details[:2])
        
        # 生成描述建议
        atmosphere['suggested_descriptions'] = await self._generate_atmospheric_descriptions(
            location_obj, environment, atmosphere['overall_mood']
        )
        
        return atmosphere
    
    async def _generate_world_suggestions(
        self, location: Dict, continuity: Dict
    ) -> List[str]:
        """生成世界构建建议"""
        suggestions = []
        
        # 基于连续性问题的建议
        if not continuity['spatial_consistency']:
            suggestions.append("注意保持空间连续性，确保地点转换合理")
        
        if not continuity['temporal_consistency']:
            suggestions.append("检查时间流逝是否符合逻辑")
        
        # 基于地点类型的建议
        location_obj = self.locations.get(location['id'])
        if location_obj:
            if location_obj.type == LocationType.URBAN:
                suggestions.append("加入城市噪音和人群活动细节")
            elif location_obj.type == LocationType.WILDERNESS:
                suggestions.append("强调自然声音和原始环境")
            elif location_obj.type == LocationType.INTERIOR:
                suggestions.append("描述室内陈设和光线变化")
        
        # 基于时间的建议
        if self.world_state.time_of_day == TimeOfDay.DAWN:
            suggestions.append("利用黎明的特殊光线营造氛围")
        elif self.world_state.time_of_day == TimeOfDay.NIGHT:
            suggestions.append("运用阴影和有限视野增加神秘感")
        
        # 基于天气的建议
        if self.world_state.weather == WeatherCondition.RAINY:
            suggestions.append("描写雨水对环境和人物的影响")
        elif self.world_state.weather == WeatherCondition.FOGGY:
            suggestions.append("利用雾气限制视野，增加不确定性")
        
        return suggestions
    
    async def _determine_time_of_day(self, time: datetime) -> TimeOfDay:
        """确定一天中的时间段"""
        hour = time.hour
        
        if 5 <= hour < 7:
            return TimeOfDay.DAWN
        elif 7 <= hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= hour < 14:
            return TimeOfDay.NOON
        elif 14 <= hour < 17:
            return TimeOfDay.AFTERNOON
        elif 17 <= hour < 19:
            return TimeOfDay.DUSK
        elif 19 <= hour < 22:
            return TimeOfDay.EVENING
        elif 22 <= hour < 24 or 0 <= hour < 2:
            return TimeOfDay.NIGHT
        else:
            return TimeOfDay.MIDNIGHT
    
    async def _determine_current_activity(
        self, location: Location, scene: Dict
    ) -> str:
        """确定当前活动"""
        # 基于时间和地点类型推断活动
        if self.world_state.time_of_day == TimeOfDay.MORNING:
            if location.type == LocationType.URBAN:
                return "早高峰通勤"
            elif location.type == LocationType.RURAL:
                return "晨间劳作"
        elif self.world_state.time_of_day == TimeOfDay.NIGHT:
            if location.type == LocationType.URBAN:
                return "夜生活"
            else:
                return "安静休息"
        
        # 使用地点的典型活动
        if location.typical_activities:
            return location.typical_activities[0]
        
        return "日常活动"
    
    async def _update_location(self, location: Location, updates: Dict):
        """更新地点信息"""
        for key, value in updates.items():
            if hasattr(location, key):
                setattr(location, key, value)
    
    async def _determine_boundaries(self, location: Location) -> List[str]:
        """确定边界"""
        boundaries = []
        
        if location.type == LocationType.INTERIOR:
            boundaries = ["墙壁", "门", "窗户"]
        elif location.type == LocationType.URBAN:
            boundaries = ["街道", "建筑", "十字路口"]
        elif location.type == LocationType.WILDERNESS:
            boundaries = ["地平线", "山脉", "河流"]
        
        return boundaries
    
    async def _calculate_weather_effects(
        self, weather: WeatherCondition, location: Dict
    ) -> Dict:
        """计算天气影响"""
        effects = {
            'visibility': 1.0,
            'movement_speed': 1.0,
            'comfort_level': 'comfortable',
            'environmental_hazards': []
        }
        
        if weather == WeatherCondition.FOGGY:
            effects['visibility'] = 0.3
            effects['environmental_hazards'].append('能见度低')
        elif weather == WeatherCondition.STORMY:
            effects['visibility'] = 0.5
            effects['movement_speed'] = 0.6
            effects['comfort_level'] = 'uncomfortable'
            effects['environmental_hazards'].extend(['强风', '雷电'])
        elif weather == WeatherCondition.SNOWY:
            effects['movement_speed'] = 0.7
            effects['comfort_level'] = 'cold'
            effects['environmental_hazards'].append('路面湿滑')
        
        return effects
    
    async def _determine_lighting(
        self, time_of_day: TimeOfDay, weather: WeatherCondition, location: Dict
    ) -> Dict:
        """确定光照条件"""
        lighting = {
            'natural_light': 0.5,
            'artificial_light': 0.0,
            'shadows': 'moderate',
            'color_temperature': 'neutral',
            'special_effects': []
        }
        
        # 根据时间调整自然光
        time_lighting = {
            TimeOfDay.DAWN: (0.3, 'long', 'warm', ['金色晨光']),
            TimeOfDay.MORNING: (0.7, 'moderate', 'cool', []),
            TimeOfDay.NOON: (1.0, 'short', 'neutral', ['强烈日光']),
            TimeOfDay.AFTERNOON: (0.8, 'moderate', 'warm', []),
            TimeOfDay.DUSK: (0.4, 'long', 'golden', ['夕阳余晖']),
            TimeOfDay.EVENING: (0.2, 'deep', 'blue', ['暮色']),
            TimeOfDay.NIGHT: (0.1, 'deep', 'cool', ['月光']),
            TimeOfDay.MIDNIGHT: (0.05, 'complete', 'cold', ['星光'])
        }
        
        if time_of_day in time_lighting:
            light_data = time_lighting[time_of_day]
            lighting['natural_light'] = light_data[0]
            lighting['shadows'] = light_data[1]
            lighting['color_temperature'] = light_data[2]
            lighting['special_effects'] = light_data[3]
        
        # 天气影响
        if weather in [WeatherCondition.CLOUDY, WeatherCondition.RAINY]:
            lighting['natural_light'] *= 0.6
            lighting['color_temperature'] = 'gray'
        elif weather == WeatherCondition.FOGGY:
            lighting['natural_light'] *= 0.4
            lighting['special_effects'].append('漫射光')
        
        # 室内需要人工光源
        location_obj = self.locations.get(location['id'])
        if location_obj and location_obj.type == LocationType.INTERIOR:
            if lighting['natural_light'] < 0.5:
                lighting['artificial_light'] = 0.8
        
        return lighting
    
    async def _map_spatial_relations(self, location: Dict, scene: Dict) -> Dict:
        """映射空间关系"""
        relations = {
            'character_positions': {},
            'object_locations': {},
            'distances': {},
            'orientations': {}
        }
        
        # 角色位置
        if 'characters' in scene:
            for char in scene['characters']:
                relations['character_positions'][char] = 'present'
        
        # 物体位置
        if 'objects' in scene:
            for obj in scene['objects']:
                relations['object_locations'][obj] = 'visible'
        
        return relations
    
    async def _identify_interactive_elements(
        self, location: Dict, scene: Dict
    ) -> List[str]:
        """识别可交互元素"""
        elements = []
        
        location_obj = self.locations.get(location['id'])
        if not location_obj:
            return elements
        
        # 基于地点类型的常见元素
        if location_obj.type == LocationType.INTERIOR:
            elements.extend(['门', '窗', '家具'])
        elif location_obj.type == LocationType.URBAN:
            elements.extend(['车辆', '路标', '商店'])
        
        # 场景特定元素
        if 'interactive' in scene:
            elements.extend(scene['interactive'])
        
        return elements
    
    async def _generate_visual_details(self, environment: Dict) -> List[str]:
        """生成视觉细节"""
        details = []
        
        # 基于光照生成细节
        lighting = environment.get('lighting', {})
        if lighting.get('natural_light', 0) < 0.3:
            details.append('朦胧的轮廓')
        elif lighting.get('natural_light', 0) > 0.8:
            details.append('清晰的细节')
        
        if lighting.get('shadows') == 'long':
            details.append('拉长的影子')
        
        return details
    
    async def _generate_ambient_sounds(
        self, environment: Dict, scene: Dict
    ) -> List[str]:
        """生成环境声音"""
        sounds = []
        
        # 天气声音
        weather_effects = environment.get('weather_effects', {})
        if 'strong_wind' in weather_effects.get('environmental_hazards', []):
            sounds.append('呼啸的风声')
        
        # 基于时间的声音
        if self.world_state.time_of_day == TimeOfDay.MORNING:
            sounds.append('鸟鸣')
        elif self.world_state.time_of_day == TimeOfDay.NIGHT:
            sounds.append('虫鸣')
        
        return sounds
    
    async def _generate_tactile_sensations(self, environment: Dict) -> List[str]:
        """生成触觉感受"""
        sensations = []
        
        weather_effects = environment.get('weather_effects', {})
        if weather_effects.get('comfort_level') == 'cold':
            sensations.append('刺骨的寒冷')
        elif weather_effects.get('comfort_level') == 'uncomfortable':
            sensations.append('潮湿的空气')
        
        return sensations
    
    async def _assess_visual_impact(self, location: Location) -> str:
        """评估视觉影响"""
        if location.emotional_tone == 'oppressive':
            return 'overwhelming'
        elif location.emotional_tone == 'peaceful':
            return 'calming'
        else:
            return 'neutral'
    
    async def _assess_auditory_impact(self, location: Location) -> str:
        """评估听觉影响"""
        if len(location.sounds) > 5:
            return 'chaotic'
        elif len(location.sounds) == 0:
            return 'eerie'
        else:
            return 'ambient'
    
    async def _assess_olfactory_impact(self, location: Location) -> str:
        """评估嗅觉影响"""
        if any('腐' in smell or '臭' in smell for smell in location.smells):
            return 'repulsive'
        elif any('香' in smell or '花' in smell for smell in location.smells):
            return 'pleasant'
        else:
            return 'neutral'
    
    async def _adjust_sensory_intensity(
        self, layers: List[SensoryLayer], scene: Dict
    ):
        """调整感官强度"""
        # 动作场景强化视觉
        if 'action' in scene.get('tags', []):
            for layer in layers:
                if layer.dominant_sense == 'visual':
                    layer.intensity = min(1.0, layer.intensity * 1.3)
        
        # 亲密场景强化触觉和嗅觉
        if 'intimate' in scene.get('tags', []):
            for layer in layers:
                if layer.dominant_sense in ['tactile', 'olfactory']:
                    layer.intensity = min(1.0, layer.intensity * 1.5)
    
    async def _check_spatial_connection(
        self, from_location: str, to_location: str
    ) -> bool:
        """检查空间连接"""
        # 检查地点图中的连接
        if from_location in self.location_graph:
            return to_location in self.location_graph[from_location]
        
        # 如果没有明确连接，检查地点对象
        from_loc = self.locations.get(from_location)
        if from_loc:
            return to_location in from_loc.connected_locations
        
        return False
    
    async def _calculate_time_gap(
        self, previous_time: datetime, current_time: datetime
    ) -> float:
        """计算时间间隔（分钟）"""
        gap = current_time - previous_time
        return gap.total_seconds() / 60
    
    async def _estimate_travel_time(
        self, from_location: str, to_location: str
    ) -> Optional[float]:
        """估算行程时间（分钟）"""
        from_loc = self.locations.get(from_location)
        if from_loc and to_location in from_loc.travel_times:
            return from_loc.travel_times[to_location]
        
        # 默认估算
        return 15.0  # 默认15分钟
    
    async def _track_character_locations(
        self, scene: Dict, context: Dict
    ) -> Dict[str, str]:
        """追踪角色位置"""
        character_locations = {}
        
        for char in scene.get('characters', []):
            # 假设所有出现的角色都在当前地点
            character_locations[char] = scene.get('location_id', 'unknown')
        
        return character_locations
    
    async def _identify_social_norms(
        self, location: Location, world_state: WorldState
    ) -> List[str]:
        """识别社会规范"""
        norms = []
        
        # 基于地点类型
        if location.type == LocationType.URBAN:
            norms.append('保持适当的社交距离')
        elif location.type == LocationType.RURAL:
            norms.append('邻里互助')
        
        # 基于文化背景
        if world_state.technology_level == 'medieval':
            norms.append('等级分明')
        elif world_state.technology_level == 'futuristic':
            norms.append('数字礼仪')
        
        return norms
    
    async def _generate_language_patterns(
        self, location: Location, culture: Dict
    ) -> List[str]:
        """生成语言模式"""
        patterns = []
        
        # 基于地点
        if location.type == LocationType.RURAL:
            patterns.append('方言土语')
        elif location.type == LocationType.URBAN:
            patterns.append('都市俚语')
        
        # 基于文化
        if culture.get('formality') == 'high':
            patterns.append('敬语')
        
        return patterns
    
    async def _identify_artifacts(
        self, location: Location, scene: Dict
    ) -> List[str]:
        """识别文化物品"""
        artifacts = []
        
        # 从场景中提取
        if 'artifacts' in scene:
            artifacts.extend(scene['artifacts'])
        
        # 基于地点历史
        if location.history:
            artifacts.append('历史遗迹')
        
        return artifacts
    
    async def _calculate_atmospheric_tension(
        self, location: Location, environment: Dict, sensory_layers: List[SensoryLayer]
    ) -> float:
        """计算氛围紧张度"""
        tension = 0.0
        
        # 基于地点情绪基调
        if location.emotional_tone in ['oppressive', 'threatening']:
            tension += 0.3
        elif location.emotional_tone == 'peaceful':
            tension -= 0.2
        
        # 基于环境危险
        hazards = environment.get('weather_effects', {}).get('environmental_hazards', [])
        tension += len(hazards) * 0.1
        
        # 基于感官强度
        high_intensity_count = sum(1 for layer in sensory_layers if layer.intensity > 0.7)
        tension += high_intensity_count * 0.1
        
        return max(0.0, min(1.0, tension))
    
    async def _generate_atmospheric_descriptions(
        self, location: Location, environment: Dict, mood: str
    ) -> List[str]:
        """生成氛围描述"""
        descriptions = []
        
        # 基于情绪
        mood_descriptions = {
            'oppressive': '空气似乎凝固了，压得人喘不过气',
            'peaceful': '宁静笼罩着一切，时间仿佛放慢了脚步',
            'mysterious': '阴影中似乎隐藏着不为人知的秘密',
            'energetic': '充满活力的氛围让人精神振奋'
        }
        
        if mood in mood_descriptions:
            descriptions.append(mood_descriptions[mood])
        
        # 基于光照
        lighting = environment.get('lighting', {})
        if lighting.get('special_effects'):
            for effect in lighting['special_effects']:
                descriptions.append(f"{effect}洒在{location.name}")
        
        return descriptions
    
    async def _calculate_world_quality(
        self, environment: Dict, sensory_layers: List[SensoryLayer], continuity: Dict
    ) -> Dict:
        """计算世界构建质量"""
        metrics = {
            'environmental_detail': 0.0,
            'sensory_richness': 0.0,
            'continuity_score': 0.0,
            'immersion_level': 0.0,
            'overall_score': 0.0
        }
        
        # 环境细节
        detail_count = sum([
            len(environment.get('physical_setting', {}).get('landmarks', [])),
            len(environment.get('interactive_elements', [])),
            1 if environment.get('weather_effects') else 0
        ])
        metrics['environmental_detail'] = min(detail_count * 0.15, 0.9)
        
        # 感官丰富度
        metrics['sensory_richness'] = min(len(sensory_layers) * 0.2, 0.8)
        
        # 连续性分数
        if continuity['spatial_consistency'] and continuity['temporal_consistency']:
            metrics['continuity_score'] = 0.9
        elif continuity['spatial_consistency'] or continuity['temporal_consistency']:
            metrics['continuity_score'] = 0.5
        else:
            metrics['continuity_score'] = 0.2
        
        # 沉浸度
        high_intensity_layers = sum(1 for layer in sensory_layers if layer.intensity > 0.5)
        metrics['immersion_level'] = min(high_intensity_layers * 0.25, 0.9)
        
        # 总分
        metrics['overall_score'] = sum(metrics.values()) / (len(metrics) - 1)
        
        return metrics
    
    async def _generate_fallback(self, scene: Dict) -> Dict:
        """生成降级方案"""
        return {
            'location': {'id': 'unknown', 'type': 'generic'},
            'environment': {},
            'suggestions': ['添加基本环境描述'],
            'message': 'Using simplified world building'
        }