"""
Enhanced Streams for Ultimate Quality System
8-Stream架构的增强Stream模块
"""

from .continuity_guard_stream import ContinuityGuardStream
from .foreshadowing_stream import ForeshadowingStream
from .dialogue_master_stream import DialogueMasterStream
from .emotion_weaver_stream import EmotionWeaverStream

# 导出所有Stream类
__all__ = [
    'ContinuityGuardStream',
    'DialogueMasterStream',
    'ForeshadowingStream', 
    'EmotionWeaverStream'
]

# Stream配置
STREAM_CONFIG = {
    'continuity_guard': {
        'class': 'ContinuityGuardStream',
        'weight': 0.125,
        'priority': 'critical',
        'description': '守护连贯性，确保时空逻辑完美'
    },
    'dialogue_master': {
        'class': 'DialogueMasterStream',
        'weight': 0.125,
        'priority': 'high',
        'description': '对话大师，生成自然富有潜台词的对话'
    },
    'foreshadowing': {
        'class': 'ForeshadowingStream',
        'weight': 0.125,
        'priority': 'high',
        'description': '伏笔管理，精确控制铺垫与揭示'
    },
    'emotion_weaver': {
        'class': 'EmotionWeaverStream',
        'weight': 0.125,
        'priority': 'medium',
        'description': '情感编织，多层次情感渲染'
    }
}