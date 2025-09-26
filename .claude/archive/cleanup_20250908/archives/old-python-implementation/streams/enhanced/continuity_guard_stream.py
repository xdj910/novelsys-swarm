"""
ContinuityGuardStream - 守护连贯性的核心Stream
确保时间、空间、状态、知识的完美连续性
Quality Target: 99% continuity accuracy
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class SceneState:
    """场景状态数据类"""
    scene_id: str
    timestamp: str
    location: str
    characters_present: List[str]
    objects_present: List[str]
    character_states: Dict[str, Dict]
    knowledge_states: Dict[str, List[str]]
    weather: Optional[str] = None
    time_of_day: Optional[str] = None


class ContinuityGuardStream:
    """
    连贯性守护Stream
    负责追踪和验证所有状态的连续性
    """
    
    def __init__(self):
        self.global_state = {
            'timeline': [],
            'character_positions': {},
            'character_possessions': {},
            'character_knowledge': {},
            'character_injuries': {},
            'location_states': {},
            'object_locations': {},
            'revealed_information': set(),
            'active_mysteries': set(),
            'relationship_matrix': {}
        }
        self.validation_errors = []
        self.continuity_score = 1.0
    
    async def process(self, scene: Dict, context: Dict) -> Dict:
        """
        处理场景的连贯性保障
        
        Args:
            scene: 场景信息
            context: 上下文信息
            
        Returns:
            连贯性检查结果和修正建议
        """
        # 1. 验证入场条件
        entry_validation = await self._validate_entry_conditions(scene, context)
        
        # 2. 追踪状态变化
        state_changes = await self._track_state_changes(scene)
        
        # 3. 预测出场状态
        exit_state = await self._predict_exit_state(scene, state_changes)
        
        # 4. 生成连贯性保障
        continuity_content = await self._generate_continuity_guards(
            scene, entry_validation, state_changes, exit_state
        )
        
        # 5. 更新全局状态
        await self._update_global_state(exit_state)
        
        return {
            'continuity_score': self.continuity_score,
            'entry_validation': entry_validation,
            'state_tracking': state_changes,
            'exit_state': exit_state,
            'guards': continuity_content,
            'errors': self.validation_errors,
            'suggestions': await self._generate_suggestions()
        }
    
    async def _validate_entry_conditions(self, scene: Dict, context: Dict) -> Dict:
        """验证场景入场条件"""
        validations = {
            'time_continuity': await self._check_time_continuity(scene, context),
            'space_continuity': await self._check_space_continuity(scene, context),
            'character_continuity': await self._check_character_continuity(scene, context),
            'object_continuity': await self._check_object_continuity(scene, context),
            'knowledge_continuity': await self._check_knowledge_continuity(scene, context)
        }
        
        # 计算总体连贯性分数
        scores = [v['score'] for v in validations.values()]
        self.continuity_score = sum(scores) / len(scores)
        
        # 记录错误
        for check_name, result in validations.items():
            if result['score'] < 0.9:
                self.validation_errors.append({
                    'type': check_name,
                    'severity': 'critical' if result['score'] < 0.7 else 'warning',
                    'details': result['issues']
                })
        
        return validations
    
    async def _check_time_continuity(self, scene: Dict, context: Dict) -> Dict:
        """检查时间连续性"""
        issues = []
        score = 1.0
        
        # 获取前一场景的时间
        if context.get('previous_scene'):
            prev_time = context['previous_scene'].get('end_time')
            curr_time = scene.get('start_time')
            
            if prev_time and curr_time:
                # 检查时间是否合理
                if curr_time < prev_time:
                    issues.append("时间倒流：当前场景时间早于前一场景")
                    score = 0.0
                elif self._time_gap_unreasonable(prev_time, curr_time, scene):
                    issues.append("时间跳跃过大或过小")
                    score = 0.7
        
        # 检查时间与场景描述的一致性
        if scene.get('time_of_day'):
            if not self._time_matches_description(scene['start_time'], scene['time_of_day']):
                issues.append("时间与场景描述不符")
                score = min(score, 0.8)
        
        return {
            'score': score,
            'issues': issues,
            'validated_time': scene.get('start_time')
        }
    
    async def _check_space_continuity(self, scene: Dict, context: Dict) -> Dict:
        """检查空间连续性"""
        issues = []
        score = 1.0
        
        # 检查角色位置转换的合理性
        for character in scene.get('characters', []):
            char_name = character['name']
            current_location = scene.get('location')
            
            if char_name in self.global_state['character_positions']:
                prev_location = self.global_state['character_positions'][char_name]
                
                # 检查位置转换是否合理
                if not self._location_transition_valid(
                    prev_location, current_location, 
                    context.get('time_elapsed', 0)
                ):
                    issues.append(f"{char_name}的位置转换不合理：从{prev_location}到{current_location}")
                    score = min(score, 0.5)
        
        # 检查物品位置
        for obj in scene.get('objects', []):
            if obj in self.global_state['object_locations']:
                prev_obj_location = self.global_state['object_locations'][obj]
                if prev_obj_location != scene.get('location'):
                    # 检查是否有角色携带
                    if not self._object_carried_by_character(obj, scene):
                        issues.append(f"物品{obj}出现位置异常")
                        score = min(score, 0.7)
        
        return {
            'score': score,
            'issues': issues,
            'validated_locations': {
                'scene': scene.get('location'),
                'characters': {c['name']: scene.get('location') for c in scene.get('characters', [])}
            }
        }
    
    async def _check_character_continuity(self, scene: Dict, context: Dict) -> Dict:
        """检查角色连续性"""
        issues = []
        score = 1.0
        
        for character in scene.get('characters', []):
            char_name = character['name']
            
            # 检查角色状态连续性
            if char_name in self.global_state['character_injuries']:
                injuries = self.global_state['character_injuries'][char_name]
                if injuries and not self._injuries_mentioned_or_healed(injuries, scene):
                    issues.append(f"{char_name}的伤势未被提及或解释")
                    score = min(score, 0.8)
            
            # 检查角色物品连续性
            if char_name in self.global_state['character_possessions']:
                possessions = self.global_state['character_possessions'][char_name]
                current_possessions = character.get('possessions', [])
                
                # 检查丢失的物品
                lost_items = set(possessions) - set(current_possessions)
                if lost_items and not self._items_loss_explained(lost_items, scene):
                    issues.append(f"{char_name}的物品{lost_items}消失未解释")
                    score = min(score, 0.7)
                
                # 检查新增的物品
                new_items = set(current_possessions) - set(possessions)
                if new_items and not self._items_gain_explained(new_items, scene):
                    issues.append(f"{char_name}的新物品{new_items}来源未解释")
                    score = min(score, 0.7)
        
        return {
            'score': score,
            'issues': issues,
            'character_states': {c['name']: c for c in scene.get('characters', [])}
        }
    
    async def _check_knowledge_continuity(self, scene: Dict, context: Dict) -> Dict:
        """检查知识状态连续性"""
        issues = []
        score = 1.0
        
        for character in scene.get('characters', []):
            char_name = character['name']
            
            # 检查角色是否使用了不应知道的信息
            if char_name in self.global_state['character_knowledge']:
                known_info = self.global_state['character_knowledge'][char_name]
                used_info = self._extract_used_information(character, scene)
                
                unknown_used = set(used_info) - set(known_info)
                if unknown_used:
                    issues.append(f"{char_name}使用了未知信息：{unknown_used}")
                    score = min(score, 0.3)  # 知识错误是严重问题
            
            # 检查角色是否忽略了应该知道的关键信息
            critical_known = self._get_critical_known_info(char_name)
            if critical_known and not self._info_properly_used(critical_known, character, scene):
                issues.append(f"{char_name}忽略了关键已知信息")
                score = min(score, 0.6)
        
        return {
            'score': score,
            'issues': issues,
            'knowledge_states': {
                c['name']: self.global_state['character_knowledge'].get(c['name'], [])
                for c in scene.get('characters', [])
            }
        }
    
    async def _check_object_continuity(self, scene: Dict, context: Dict) -> Dict:
        """检查物品连续性"""
        issues = []
        score = 1.0
        
        scene_objects = scene.get('objects', [])
        
        for obj in scene_objects:
            # 检查物品是否应该存在于此场景
            if obj in self.global_state['object_locations']:
                expected_location = self.global_state['object_locations'][obj]
                current_location = scene.get('location')
                
                if expected_location != current_location:
                    # 检查是否被角色携带
                    if not self._object_carried_by_character(obj, scene):
                        issues.append(f"物品{obj}不应出现在{current_location}")
                        score = min(score, 0.6)
        
        # 检查应该存在但缺失的物品
        expected_objects = self._get_expected_objects(scene.get('location'))
        missing_objects = set(expected_objects) - set(scene_objects)
        if missing_objects:
            issues.append(f"场景缺少预期物品：{missing_objects}")
            score = min(score, 0.8)
        
        return {
            'score': score,
            'issues': issues,
            'object_locations': {obj: scene.get('location') for obj in scene_objects}
        }
    
    async def _track_state_changes(self, scene: Dict) -> Dict:
        """追踪场景中的状态变化"""
        changes = {
            'position_changes': {},
            'possession_changes': {},
            'knowledge_changes': {},
            'relationship_changes': {},
            'injury_changes': {},
            'revelation_changes': []
        }
        
        # 追踪位置变化
        for character in scene.get('characters', []):
            char_name = character['name']
            new_position = scene.get('location')
            if char_name in self.global_state['character_positions']:
                old_position = self.global_state['character_positions'][char_name]
                if old_position != new_position:
                    changes['position_changes'][char_name] = {
                        'from': old_position,
                        'to': new_position
                    }
        
        # 追踪物品变化
        for character in scene.get('characters', []):
            char_name = character['name']
            new_possessions = set(character.get('possessions', []))
            if char_name in self.global_state['character_possessions']:
                old_possessions = set(self.global_state['character_possessions'][char_name])
                if old_possessions != new_possessions:
                    changes['possession_changes'][char_name] = {
                        'gained': list(new_possessions - old_possessions),
                        'lost': list(old_possessions - new_possessions)
                    }
        
        # 追踪知识变化
        new_revelations = scene.get('revelations', [])
        for revelation in new_revelations:
            changes['revelation_changes'].append(revelation)
            # 更新角色知识状态
            for char_name in revelation.get('known_by', []):
                if char_name not in changes['knowledge_changes']:
                    changes['knowledge_changes'][char_name] = []
                changes['knowledge_changes'][char_name].append(revelation['content'])
        
        return changes
    
    async def _predict_exit_state(self, scene: Dict, changes: Dict) -> SceneState:
        """预测场景结束时的状态"""
        # 构建退场状态
        exit_state = SceneState(
            scene_id=scene.get('id', 'unknown'),
            timestamp=scene.get('end_time', ''),
            location=scene.get('location', ''),
            characters_present=[c['name'] for c in scene.get('characters', [])],
            objects_present=scene.get('objects', []),
            character_states={},
            knowledge_states={}
        )
        
        # 更新角色状态
        for character in scene.get('characters', []):
            char_name = character['name']
            exit_state.character_states[char_name] = {
                'position': scene.get('location'),
                'possessions': character.get('possessions', []),
                'injuries': character.get('injuries', []),
                'emotional_state': character.get('emotional_state', 'neutral')
            }
            
            # 更新知识状态
            current_knowledge = self.global_state['character_knowledge'].get(char_name, [])
            new_knowledge = changes['knowledge_changes'].get(char_name, [])
            exit_state.knowledge_states[char_name] = current_knowledge + new_knowledge
        
        return exit_state
    
    async def _generate_continuity_guards(
        self, scene: Dict, entry_validation: Dict,
        state_changes: Dict, exit_state: SceneState
    ) -> Dict:
        """生成连贯性保障内容"""
        guards = {
            'mandatory_mentions': [],
            'prohibited_mentions': [],
            'required_explanations': [],
            'state_confirmations': [],
            'transition_guides': []
        }
        
        # 基于验证结果生成必要提及
        for validation_type, result in entry_validation.items():
            if result['issues']:
                for issue in result['issues']:
                    guards['required_explanations'].append({
                        'type': validation_type,
                        'explanation_needed': issue,
                        'suggested_approach': self._suggest_explanation(issue)
                    })
        
        # 生成状态确认要求
        guards['state_confirmations'] = [
            f"确认{char}在{loc}"
            for char, loc in exit_state.character_states.items()
        ]
        
        # 生成过渡指导
        if state_changes['position_changes']:
            for char, change in state_changes['position_changes'].items():
                guards['transition_guides'].append(
                    f"描述{char}从{change['from']}到{change['to']}的过程"
                )
        
        # 生成必须提及的内容
        critical_items = self._identify_critical_items(scene)
        guards['mandatory_mentions'].extend(critical_items)
        
        # 生成禁止提及的内容（角色不应知道的信息）
        for char_name in exit_state.characters_present:
            unknown_info = self._get_unknown_info(char_name)
            if unknown_info:
                guards['prohibited_mentions'].append({
                    'character': char_name,
                    'prohibited_info': unknown_info
                })
        
        return guards
    
    async def _update_global_state(self, exit_state: SceneState):
        """更新全局状态"""
        # 更新时间线
        self.global_state['timeline'].append({
            'scene_id': exit_state.scene_id,
            'timestamp': exit_state.timestamp
        })
        
        # 更新角色位置
        for char_name in exit_state.characters_present:
            self.global_state['character_positions'][char_name] = exit_state.location
        
        # 更新角色物品
        for char_name, state in exit_state.character_states.items():
            self.global_state['character_possessions'][char_name] = state['possessions']
            self.global_state['character_injuries'][char_name] = state.get('injuries', [])
        
        # 更新角色知识
        for char_name, knowledge in exit_state.knowledge_states.items():
            self.global_state['character_knowledge'][char_name] = knowledge
        
        # 更新物品位置
        for obj in exit_state.objects_present:
            self.global_state['object_locations'][obj] = exit_state.location
    
    async def _generate_suggestions(self) -> List[Dict]:
        """生成改进建议"""
        suggestions = []
        
        if self.continuity_score < 0.9:
            suggestions.append({
                'priority': 'high',
                'type': 'continuity_fix',
                'suggestion': '建议重新生成场景以修复连贯性问题',
                'specific_fixes': [
                    error['details'] for error in self.validation_errors
                    if error['severity'] == 'critical'
                ]
            })
        
        # 生成具体修复建议
        for error in self.validation_errors:
            if error['type'] == 'time_continuity':
                suggestions.append({
                    'priority': 'medium',
                    'type': 'time_fix',
                    'suggestion': '调整时间描述或添加时间过渡说明'
                })
            elif error['type'] == 'knowledge_continuity':
                suggestions.append({
                    'priority': 'high',
                    'type': 'knowledge_fix',
                    'suggestion': '修改角色对话，避免使用未知信息'
                })
        
        return suggestions
    
    # 辅助方法
    def _time_gap_unreasonable(self, prev_time: str, curr_time: str, scene: Dict) -> bool:
        """检查时间间隔是否合理"""
        # 实现时间间隔逻辑
        # 这里简化处理，实际需要解析时间并计算
        return False
    
    def _time_matches_description(self, timestamp: str, time_of_day: str) -> bool:
        """检查时间是否与描述匹配"""
        # 实现时间匹配逻辑
        return True
    
    def _location_transition_valid(self, from_loc: str, to_loc: str, time_elapsed: float) -> bool:
        """检查位置转换是否合理"""
        # 实现位置转换验证逻辑
        # 考虑距离和时间
        return True
    
    def _object_carried_by_character(self, obj: str, scene: Dict) -> bool:
        """检查物品是否被角色携带"""
        for character in scene.get('characters', []):
            if obj in character.get('possessions', []):
                return True
        return False
    
    def _injuries_mentioned_or_healed(self, injuries: List[str], scene: Dict) -> bool:
        """检查伤势是否被提及或治愈"""
        # 实现伤势检查逻辑
        return True
    
    def _items_loss_explained(self, lost_items: set, scene: Dict) -> bool:
        """检查物品丢失是否有解释"""
        # 实现物品丢失解释检查
        return False
    
    def _items_gain_explained(self, new_items: set, scene: Dict) -> bool:
        """检查新物品是否有来源解释"""
        # 实现新物品来源检查
        return False
    
    def _extract_used_information(self, character: Dict, scene: Dict) -> List[str]:
        """提取角色使用的信息"""
        # 实现信息提取逻辑
        return []
    
    def _get_critical_known_info(self, char_name: str) -> List[str]:
        """获取角色应该知道的关键信息"""
        # 实现关键信息获取
        return []
    
    def _info_properly_used(self, info: List[str], character: Dict, scene: Dict) -> bool:
        """检查信息是否被恰当使用"""
        # 实现信息使用检查
        return True
    
    def _get_expected_objects(self, location: str) -> List[str]:
        """获取场景预期物品"""
        # 基于场景类型返回预期物品
        return []
    
    def _suggest_explanation(self, issue: str) -> str:
        """建议解释方式"""
        if "时间" in issue:
            return "添加时间过渡描述，如'几小时后'或'第二天早晨'"
        elif "位置" in issue:
            return "描述角色的移动过程或使用场景转换"
        elif "物品" in issue:
            return "解释物品的获得或丢失过程"
        else:
            return "添加必要的解释或过渡描述"
    
    def _identify_critical_items(self, scene: Dict) -> List[str]:
        """识别必须提及的关键内容"""
        critical = []
        
        # 关键物品
        if scene.get('key_items'):
            critical.extend([f"提及{item}" for item in scene['key_items']])
        
        # 重要伤势
        for char in scene.get('characters', []):
            if char.get('injuries'):
                critical.append(f"提及{char['name']}的伤势")
        
        return critical
    
    def _get_unknown_info(self, char_name: str) -> List[str]:
        """获取角色不应知道的信息"""
        all_revealed = self.global_state['revealed_information']
        char_known = set(self.global_state['character_knowledge'].get(char_name, []))
        return list(all_revealed - char_known)


# 测试函数
async def test_continuity_guard():
    """测试连贯性守护Stream"""
    stream = ContinuityGuardStream()
    
    # 测试场景
    test_scene = {
        'id': 'ch1_sc2',
        'start_time': '09:00',
        'end_time': '09:30',
        'location': '办公室',
        'characters': [
            {
                'name': '李明',
                'possessions': ['手机', '钱包', '笔记本'],
                'emotional_state': '焦虑'
            }
        ],
        'objects': ['电脑', '咖啡杯'],
        'revelations': [
            {
                'content': '发现重要线索',
                'known_by': ['李明']
            }
        ]
    }
    
    test_context = {
        'previous_scene': {
            'end_time': '08:45',
            'location': '家中'
        }
    }
    
    # 运行测试
    result = await stream.generate(test_scene, test_context)
    
    print("连贯性检查结果：")
    print(f"连贯性分数: {result['continuity_score']}")
    print(f"验证结果: {json.dumps(result['entry_validation'], indent=2, ensure_ascii=False)}")
    print(f"状态追踪: {json.dumps(result['state_tracking'], indent=2, ensure_ascii=False)}")
    print(f"保障措施: {json.dumps(result['guards'], indent=2, ensure_ascii=False)}")
    
    return result


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_continuity_guard())