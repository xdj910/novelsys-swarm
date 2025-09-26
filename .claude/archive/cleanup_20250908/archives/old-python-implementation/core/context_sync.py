"""
上下文同步系统
负责在Streams、Agents和持久化层之间同步上下文
适配Claude Code环境的顺序执行特性
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import json
import asyncio
from pathlib import Path

from .data_persistence import ContextStorage


@dataclass
class ContextUpdate:
    """上下文更新记录"""
    source: str  # 更新来源 (agent/stream/command)
    target: str  # 更新目标 (global/chapter/character/scene)
    timestamp: str
    data: Dict
    operation: str  # add/update/delete
    
    
@dataclass
class SyncEvent:
    """同步事件"""
    event_id: str
    event_type: str  # push/pull/merge/conflict
    source: str
    target: str
    data: Dict
    timestamp: str
    status: str  # pending/processing/completed/failed


class ContextSynchronizer:
    """上下文同步器"""
    
    def __init__(self, bible_id: str, base_path: str = "D:\\NOVELSYS-SWARM\\data"):
        """
        初始化同步器
        
        Args:
            bible_id: Bible ID
            base_path: 数据存储路径
        """
        self.bible_id = bible_id
        self.storage = ContextStorage(base_path)
        
        # 内存中的上下文缓存
        self.contexts = {
            'global': {},
            'chapter': {},
            'character': {},
            'scene': {},
            'stream': {}  # Stream专用上下文
        }
        
        # 同步队列
        self.sync_queue = []
        self.pending_updates = []
        
        # 版本控制
        self.versions = {}
        
        # 锁机制（虽然Claude是顺序执行，但保留以防将来扩展）
        self.locks = {}
        
        # 初始化时加载持久化的上下文
        self._load_persisted_contexts()
        
    def _load_persisted_contexts(self):
        """加载持久化的上下文"""
        for ctx_type in ['global', 'chapter', 'character', 'scene']:
            context = self.storage.read_context(self.bible_id, ctx_type)
            if context:
                self.contexts[ctx_type] = context
                self.versions[ctx_type] = context.get('_version', 1)
    
    async def push_context(
        self,
        source: str,
        target: str,
        data: Dict,
        merge_strategy: str = 'update'
    ) -> bool:
        """
        推送上下文更新
        
        Args:
            source: 更新来源
            target: 目标上下文类型
            data: 更新数据
            merge_strategy: 合并策略 (update/replace/merge)
            
        Returns:
            是否成功
        """
        # 创建更新记录
        update = ContextUpdate(
            source=source,
            target=target,
            timestamp=datetime.now().isoformat(),
            data=data,
            operation=merge_strategy
        )
        
        # 添加到队列
        self.pending_updates.append(update)
        
        # 执行同步
        return await self._process_update(update)
    
    async def pull_context(
        self,
        requester: str,
        context_types: List[str] = None
    ) -> Dict:
        """
        拉取上下文
        
        Args:
            requester: 请求者标识
            context_types: 需要的上下文类型
            
        Returns:
            请求的上下文数据
        """
        if context_types is None:
            context_types = ['global', 'chapter', 'character', 'scene']
        
        result = {}
        
        for ctx_type in context_types:
            if ctx_type in self.contexts:
                # 克隆数据避免直接引用
                result[ctx_type] = self.contexts[ctx_type].copy()
        
        # 记录访问
        self._log_access(requester, context_types)
        
        return result
    
    async def merge_contexts(
        self,
        contexts_to_merge: List[Dict],
        target: str,
        strategy: str = 'deep'
    ) -> Dict:
        """
        合并多个上下文
        
        Args:
            contexts_to_merge: 要合并的上下文列表
            target: 目标上下文类型
            strategy: 合并策略 (deep/shallow/custom)
            
        Returns:
            合并后的上下文
        """
        if target not in self.contexts:
            self.contexts[target] = {}
        
        base_context = self.contexts[target].copy()
        
        if strategy == 'deep':
            merged = self._deep_merge(base_context, *contexts_to_merge)
        elif strategy == 'shallow':
            merged = self._shallow_merge(base_context, *contexts_to_merge)
        else:
            merged = self._custom_merge(base_context, contexts_to_merge)
        
        # 更新版本
        self.versions[target] = self.versions.get(target, 0) + 1
        merged['_version'] = self.versions[target]
        
        # 更新内存和持久化
        self.contexts[target] = merged
        await self._persist_context(target, merged)
        
        return merged
    
    async def sync_stream_context(
        self,
        stream_id: str,
        stream_data: Dict
    ) -> bool:
        """
        同步Stream上下文
        
        Args:
            stream_id: Stream标识 (A/B/C/D)
            stream_data: Stream数据
            
        Returns:
            是否成功
        """
        if 'stream' not in self.contexts:
            self.contexts['stream'] = {}
        
        # 更新Stream特定上下文
        self.contexts['stream'][stream_id] = {
            'data': stream_data,
            'updated_at': datetime.now().isoformat()
        }
        
        # 提取需要同步到全局的信息
        global_updates = self._extract_global_updates(stream_id, stream_data)
        
        if global_updates:
            await self.push_context(
                source=f'stream_{stream_id}',
                target='global',
                data=global_updates
            )
        
        return True
    
    async def sync_agent_context(
        self,
        agent_name: str,
        agent_output: Dict
    ) -> bool:
        """
        同步Agent上下文
        
        Args:
            agent_name: Agent名称
            agent_output: Agent输出
            
        Returns:
            是否成功
        """
        # 根据Agent类型决定更新哪个上下文
        context_mapping = {
            'character-psychologist': 'character',
            'world-builder': 'scene',
            'outline-creator': 'chapter',
            'director': 'global'
        }
        
        target_context = context_mapping.get(agent_name, 'global')
        
        return await self.push_context(
            source=f'agent_{agent_name}',
            target=target_context,
            data=agent_output
        )
    
    async def resolve_conflicts(
        self,
        conflicts: List[Dict]
    ) -> List[Dict]:
        """
        解决上下文冲突
        
        Args:
            conflicts: 冲突列表
            
        Returns:
            解决方案列表
        """
        resolutions = []
        
        for conflict in conflicts:
            resolution = await self._resolve_single_conflict(conflict)
            resolutions.append(resolution)
        
        return resolutions
    
    async def create_checkpoint(self) -> str:
        """
        创建上下文检查点
        
        Returns:
            检查点ID
        """
        checkpoint_id = self.storage.create_snapshot(self.bible_id)
        
        # 记录检查点信息
        checkpoint_info = {
            'id': checkpoint_id,
            'created_at': datetime.now().isoformat(),
            'versions': self.versions.copy(),
            'contexts_included': list(self.contexts.keys())
        }
        
        # 保存检查点元信息
        self._save_checkpoint_info(checkpoint_info)
        
        return checkpoint_id
    
    async def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """
        恢复到检查点
        
        Args:
            checkpoint_id: 检查点ID
            
        Returns:
            是否成功
        """
        success = self.storage.restore_snapshot(self.bible_id, checkpoint_id)
        
        if success:
            # 重新加载上下文
            self._load_persisted_contexts()
        
        return success
    
    async def _process_update(self, update: ContextUpdate) -> bool:
        """处理上下文更新"""
        target = update.target
        
        if target not in self.contexts:
            self.contexts[target] = {}
        
        # 根据操作类型处理
        if update.operation == 'replace':
            self.contexts[target] = update.data
        elif update.operation == 'update':
            self.contexts[target].update(update.data)
        elif update.operation == 'merge':
            self.contexts[target] = self._deep_merge(
                self.contexts[target], 
                update.data
            )
        
        # 更新版本
        self.versions[target] = self.versions.get(target, 0) + 1
        self.contexts[target]['_version'] = self.versions[target]
        
        # 持久化
        return await self._persist_context(target, self.contexts[target])
    
    async def _persist_context(self, context_type: str, data: Dict) -> bool:
        """持久化上下文"""
        return self.storage.save_context(self.bible_id, context_type, data)
    
    def _deep_merge(self, base: Dict, *others: Dict) -> Dict:
        """深度合并字典"""
        result = base.copy()
        
        for other in others:
            for key, value in other.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._deep_merge(result[key], value)
                else:
                    result[key] = value
        
        return result
    
    def _shallow_merge(self, base: Dict, *others: Dict) -> Dict:
        """浅合并字典"""
        result = base.copy()
        for other in others:
            result.update(other)
        return result
    
    def _custom_merge(self, base: Dict, others: List[Dict]) -> Dict:
        """自定义合并策略"""
        # 可以根据具体需求实现复杂的合并逻辑
        return self._deep_merge(base, *others)
    
    def _extract_global_updates(self, stream_id: str, stream_data: Dict) -> Dict:
        """从Stream数据中提取全局更新"""
        global_updates = {}
        
        # 提取重要的全局信息
        if 'plot_points' in stream_data:
            global_updates['latest_plot_points'] = stream_data['plot_points']
        
        if 'character_developments' in stream_data:
            global_updates['character_updates'] = stream_data['character_developments']
        
        return global_updates
    
    async def _resolve_single_conflict(self, conflict: Dict) -> Dict:
        """解决单个冲突"""
        # 简单的冲突解决策略：后来者优先
        resolution = {
            'conflict_id': conflict.get('id'),
            'resolution_strategy': 'latest_wins',
            'chosen_value': conflict.get('new_value'),
            'resolved_at': datetime.now().isoformat()
        }
        
        return resolution
    
    def _log_access(self, requester: str, context_types: List[str]):
        """记录上下文访问"""
        # 可以用于监控和优化
        pass
    
    def _save_checkpoint_info(self, info: Dict):
        """保存检查点信息"""
        checkpoints_dir = Path(f"D:\\NOVELSYS-SWARM\\data\\bibles\\{self.bible_id}\\checkpoints")
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        
        info_file = checkpoints_dir / f"{info['id']}_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)


class StreamContextManager:
    """Stream上下文管理器"""
    
    def __init__(self, synchronizer: ContextSynchronizer):
        """
        初始化Stream上下文管理器
        
        Args:
            synchronizer: 上下文同步器
        """
        self.synchronizer = synchronizer
        self.stream_buffers = {
            'A': [],  # Character Stream
            'B': [],  # Narrative Stream
            'C': [],  # World Stream
            'D': []   # Prose Stream
        }
        
    async def collect_stream_output(
        self,
        stream_id: str,
        output: Dict
    ):
        """
        收集Stream输出
        
        Args:
            stream_id: Stream标识
            output: Stream输出
        """
        if stream_id in self.stream_buffers:
            self.stream_buffers[stream_id].append({
                'output': output,
                'timestamp': datetime.now().isoformat()
            })
    
    async def flush_to_context(self) -> Dict:
        """
        将缓冲的Stream输出刷新到上下文
        
        Returns:
            合并后的上下文
        """
        merged_context = {}
        
        for stream_id, buffer in self.stream_buffers.items():
            if buffer:
                # 合并同一Stream的所有输出
                stream_context = self._merge_stream_buffer(stream_id, buffer)
                
                # 同步到主上下文
                await self.synchronizer.sync_stream_context(stream_id, stream_context)
                
                merged_context[f'stream_{stream_id}'] = stream_context
                
                # 清空缓冲
                self.stream_buffers[stream_id] = []
        
        return merged_context
    
    def _merge_stream_buffer(self, stream_id: str, buffer: List[Dict]) -> Dict:
        """合并Stream缓冲区"""
        merged = {
            'stream_id': stream_id,
            'outputs': [],
            'summary': {}
        }
        
        for item in buffer:
            merged['outputs'].append(item['output'])
        
        # 根据Stream类型生成摘要
        if stream_id == 'A':  # Character
            merged['summary'] = self._summarize_character_outputs(merged['outputs'])
        elif stream_id == 'B':  # Narrative
            merged['summary'] = self._summarize_narrative_outputs(merged['outputs'])
        elif stream_id == 'C':  # World
            merged['summary'] = self._summarize_world_outputs(merged['outputs'])
        elif stream_id == 'D':  # Prose
            merged['summary'] = self._summarize_prose_outputs(merged['outputs'])
        
        return merged
    
    def _summarize_character_outputs(self, outputs: List[Dict]) -> Dict:
        """总结角色相关输出"""
        return {
            'character_count': len(outputs),
            'key_developments': [],
            'emotional_states': []
        }
    
    def _summarize_narrative_outputs(self, outputs: List[Dict]) -> Dict:
        """总结叙事相关输出"""
        return {
            'plot_points': [],
            'tension_level': 0,
            'pacing': 'moderate'
        }
    
    def _summarize_world_outputs(self, outputs: List[Dict]) -> Dict:
        """总结世界构建输出"""
        return {
            'locations': [],
            'atmosphere': '',
            'cultural_elements': []
        }
    
    def _summarize_prose_outputs(self, outputs: List[Dict]) -> Dict:
        """总结文笔相关输出"""
        return {
            'style_consistency': 0.9,
            'voice_strength': 0.85,
            'quality_score': 0.88
        }


class GlobalContextCoordinator:
    """全局上下文协调器"""
    
    def __init__(self, bible_id: str):
        """
        初始化全局协调器
        
        Args:
            bible_id: Bible ID
        """
        self.bible_id = bible_id
        self.synchronizer = ContextSynchronizer(bible_id)
        self.stream_manager = StreamContextManager(self.synchronizer)
        
        # 注册的组件
        self.registered_components = {}
        
    def register_component(self, component_id: str, component_type: str):
        """
        注册组件
        
        Args:
            component_id: 组件ID
            component_type: 组件类型 (stream/agent/command)
        """
        self.registered_components[component_id] = {
            'type': component_type,
            'registered_at': datetime.now().isoformat(),
            'last_sync': None
        }
    
    async def broadcast_update(
        self,
        source: str,
        update_data: Dict,
        target_components: List[str] = None
    ):
        """
        广播上下文更新
        
        Args:
            source: 更新源
            update_data: 更新数据
            target_components: 目标组件列表
        """
        if target_components is None:
            target_components = list(self.registered_components.keys())
        
        for component_id in target_components:
            if component_id != source:  # 不发送给自己
                await self._send_update_to_component(component_id, update_data)
    
    async def _send_update_to_component(self, component_id: str, data: Dict):
        """发送更新到组件"""
        # 在Claude环境中，这里只是更新内存中的数据
        # 实际组件会在需要时拉取
        if component_id in self.registered_components:
            self.registered_components[component_id]['last_sync'] = datetime.now().isoformat()
    
    async def synchronize_all(self) -> Dict:
        """
        执行全局同步
        
        Returns:
            同步报告
        """
        # 刷新所有Stream缓冲
        stream_context = await self.stream_manager.flush_to_context()
        
        # 获取所有上下文
        all_contexts = await self.synchronizer.pull_context('global_coordinator')
        
        # 创建检查点
        checkpoint_id = await self.synchronizer.create_checkpoint()
        
        return {
            'synchronized_at': datetime.now().isoformat(),
            'checkpoint_id': checkpoint_id,
            'components_synced': len(self.registered_components),
            'contexts': list(all_contexts.keys())
        }


# 导出主要类
__all__ = [
    'ContextSynchronizer',
    'StreamContextManager',
    'GlobalContextCoordinator',
    'ContextUpdate',
    'SyncEvent'
]