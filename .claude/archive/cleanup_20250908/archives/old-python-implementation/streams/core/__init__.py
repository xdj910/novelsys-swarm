"""
Core Streams for Ultimate Quality System
8-Stream架构的核心Stream模块
"""

from .character_psychology_stream import CharacterPsychologyStream
from .narrative_structure_stream import NarrativeStructureStream
from .world_building_stream import WorldBuildingStream
from .prose_craft_stream import ProseCraftStream

# 导出所有Stream类
__all__ = [
    'CharacterPsychologyStream',
    'NarrativeStructureStream',
    'WorldBuildingStream',
    'ProseCraftStream'
]

# Stream配置
STREAM_CONFIG = {
    'character_psychology': {
        'class': 'CharacterPsychologyStream',
        'weight': 0.125,
        'priority': 'critical',
        'description': '角色心理深度分析，动机链追踪'
    },
    'narrative_structure': {
        'class': 'NarrativeStructureStream',
        'weight': 0.125,
        'priority': 'critical',
        'description': '叙事结构管理，节奏控制与张力曲线'
    },
    'world_building': {
        'class': 'WorldBuildingStream',
        'weight': 0.125,
        'priority': 'high',
        'description': '世界构建，环境描写与感官细节'
    },
    'prose_craft': {
        'class': 'ProseCraftStream',
        'weight': 0.125,
        'priority': 'medium',
        'description': '文笔工艺，语言优化与风格一致性'
    }
}