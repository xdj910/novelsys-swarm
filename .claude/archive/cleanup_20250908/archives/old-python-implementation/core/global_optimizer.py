"""
全局优化器
对整章内容进行全局优化，确保连贯性和一致性
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
import re

@dataclass 
class OptimizationResult:
    """优化结果"""
    optimization_type: str
    original_content: Any
    optimized_content: Any
    changes_made: List[str]
    improvement_score: float


class GlobalOptimizer:
    """
    全局优化器
    负责章节级别的整体优化
    """
    
    def __init__(self):
        """初始化全局优化器"""
        self.optimization_history = []
        self.style_analyzer = StyleAnalyzer()
        self.pacing_controller = PacingController()
        self.transition_smoother = TransitionSmoother()
        self.consistency_enforcer = ConsistencyEnforcer()
        
    async def optimize_chapter(self, scenes: List[Dict]) -> Dict:
        """
        优化整个章节
        
        Args:
            scenes: 场景列表
            
        Returns:
            优化后的章节内容
        """
        print("\n=== 开始全局优化 ===")
        self.optimization_history = []
        
        # 1. 场景过渡优化
        scenes = await self.smooth_transitions(scenes)
        
        # 2. 风格统一化
        scenes = await self.unify_style(scenes)
        
        # 3. 节奏调整
        scenes = await self.adjust_pacing(scenes)
        
        # 4. 情感曲线微调
        scenes = await self.tune_emotional_arc(scenes)
        
        # 5. 伏笔验证与补充
        scenes = await self.verify_foreshadowing(scenes)
        
        # 6. 全局一致性检查
        scenes = await self.ensure_global_consistency(scenes)
        
        # 生成优化报告
        optimization_report = self._generate_optimization_report()
        
        return {
            'optimized_scenes': scenes,
            'optimization_history': self.optimization_history,
            'report': optimization_report,
            'quality_improvement': self._calculate_improvement()
        }
    
    async def smooth_transitions(self, scenes: List[Dict]) -> List[Dict]:
        """
        优化场景间过渡
        
        Args:
            scenes: 场景列表
            
        Returns:
            优化后的场景列表
        """
        print("  优化场景过渡...")
        optimized_scenes = []
        
        for i, scene in enumerate(scenes):
            optimized_scene = scene.copy()
            
            if i > 0:
                # 检查与前一场景的连接
                prev_scene = scenes[i-1]
                transition_quality = await self.transition_smoother.evaluate(
                    prev_scene, scene
                )
                
                if transition_quality < 0.8:
                    # 需要优化过渡
                    optimized_scene = await self.transition_smoother.smooth(
                        prev_scene, scene
                    )
                    
                    self._record_optimization(
                        'transition',
                        f"场景{i-1}到场景{i}的过渡",
                        ['添加过渡句', '调整时间连续性', '补充空间转换说明']
                    )
            
            optimized_scenes.append(optimized_scene)
        
        return optimized_scenes
    
    async def unify_style(self, scenes: List[Dict]) -> List[Dict]:
        """
        统一文体风格
        
        Args:
            scenes: 场景列表
            
        Returns:
            风格统一的场景列表
        """
        print("  统一文体风格...")
        
        # 分析整体风格
        overall_style = await self.style_analyzer.analyze_overall(scenes)
        
        optimized_scenes = []
        for i, scene in enumerate(scenes):
            scene_style = await self.style_analyzer.analyze_scene(scene)
            
            if not self.style_analyzer.is_consistent(scene_style, overall_style):
                # 调整场景风格
                optimized_scene = await self.style_analyzer.adjust_style(
                    scene, overall_style
                )
                
                self._record_optimization(
                    'style',
                    f"场景{i}风格调整",
                    ['统一句式结构', '调整词汇选择', '保持语气一致']
                )
            else:
                optimized_scene = scene
            
            optimized_scenes.append(optimized_scene)
        
        return optimized_scenes
    
    async def adjust_pacing(self, scenes: List[Dict]) -> List[Dict]:
        """
        调整叙事节奏
        
        Args:
            scenes: 场景列表
            
        Returns:
            节奏优化的场景列表
        """
        print("  调整叙事节奏...")
        
        # 分析当前节奏
        pacing_analysis = await self.pacing_controller.analyze(scenes)
        
        optimized_scenes = []
        for i, scene in enumerate(scenes):
            scene_pacing = pacing_analysis['scene_pacing'][i]
            ideal_pacing = pacing_analysis['ideal_curve'][i]
            
            if abs(scene_pacing - ideal_pacing) > 0.2:
                # 需要调整节奏
                if scene_pacing < ideal_pacing:
                    # 加快节奏
                    optimized_scene = await self.pacing_controller.accelerate(scene)
                    changes = ['缩短描写', '使用短句', '增加动作']
                else:
                    # 放慢节奏
                    optimized_scene = await self.pacing_controller.decelerate(scene)
                    changes = ['增加细节描写', '使用长句', '加入内心活动']
                
                self._record_optimization('pacing', f"场景{i}节奏调整", changes)
            else:
                optimized_scene = scene
            
            optimized_scenes.append(optimized_scene)
        
        return optimized_scenes
    
    async def tune_emotional_arc(self, scenes: List[Dict]) -> List[Dict]:
        """
        微调情感曲线
        
        Args:
            scenes: 场景列表
            
        Returns:
            情感优化的场景列表
        """
        print("  微调情感曲线...")
        
        # 分析整体情感弧
        emotional_arc = self._analyze_emotional_arc(scenes)
        ideal_arc = self._generate_ideal_arc(len(scenes))
        
        optimized_scenes = []
        for i, scene in enumerate(scenes):
            current_emotion = emotional_arc[i]
            ideal_emotion = ideal_arc[i]
            
            if abs(current_emotion - ideal_emotion) > 0.15:
                # 调整情感强度
                optimized_scene = await self._adjust_emotional_intensity(
                    scene, ideal_emotion
                )
                
                self._record_optimization(
                    'emotion',
                    f"场景{i}情感调整",
                    ['调整情感词汇', '修改情感描写', '优化氛围营造']
                )
            else:
                optimized_scene = scene
            
            optimized_scenes.append(optimized_scene)
        
        return optimized_scenes
    
    async def verify_foreshadowing(self, scenes: List[Dict]) -> List[Dict]:
        """
        验证和补充伏笔
        
        Args:
            scenes: 场景列表
            
        Returns:
            伏笔完善的场景列表
        """
        print("  验证伏笔完整性...")
        
        # 收集所有伏笔
        foreshadows = self._collect_foreshadows(scenes)
        
        # 检查伏笔链条
        incomplete_chains = self._check_foreshadow_chains(foreshadows)
        
        optimized_scenes = scenes.copy()
        
        for chain in incomplete_chains:
            if chain['type'] == 'missing_plant':
                # 缺少埋设，需要补充
                target_scene = chain['suggested_scene']
                optimized_scenes[target_scene] = await self._add_foreshadow_plant(
                    optimized_scenes[target_scene], chain['foreshadow']
                )
                
                self._record_optimization(
                    'foreshadow',
                    f"场景{target_scene}补充伏笔",
                    ['添加伏笔埋设']
                )
                
            elif chain['type'] == 'missing_payoff':
                # 缺少回收，需要补充
                target_scene = chain['suggested_scene']
                optimized_scenes[target_scene] = await self._add_foreshadow_payoff(
                    optimized_scenes[target_scene], chain['foreshadow']
                )
                
                self._record_optimization(
                    'foreshadow',
                    f"场景{target_scene}回收伏笔",
                    ['添加伏笔揭示']
                )
        
        return optimized_scenes
    
    async def ensure_global_consistency(self, scenes: List[Dict]) -> List[Dict]:
        """
        确保全局一致性
        
        Args:
            scenes: 场景列表
            
        Returns:
            一致性优化的场景列表
        """
        print("  检查全局一致性...")
        
        # 检查各类一致性
        consistency_issues = await self.consistency_enforcer.check_all(scenes)
        
        optimized_scenes = scenes.copy()
        
        for issue in consistency_issues:
            scene_idx = issue['scene_index']
            issue_type = issue['type']
            
            if issue_type == 'character_inconsistency':
                optimized_scenes[scene_idx] = await self.consistency_enforcer.fix_character(
                    optimized_scenes[scene_idx], issue['details']
                )
            elif issue_type == 'timeline_inconsistency':
                optimized_scenes[scene_idx] = await self.consistency_enforcer.fix_timeline(
                    optimized_scenes[scene_idx], issue['details']
                )
            elif issue_type == 'setting_inconsistency':
                optimized_scenes[scene_idx] = await self.consistency_enforcer.fix_setting(
                    optimized_scenes[scene_idx], issue['details']
                )
            
            self._record_optimization(
                'consistency',
                f"场景{scene_idx}一致性修复",
                [f"修复{issue_type}"]
            )
        
        return optimized_scenes
    
    def _record_optimization(
        self, 
        opt_type: str, 
        description: str, 
        changes: List[str]
    ):
        """记录优化操作"""
        self.optimization_history.append({
            'type': opt_type,
            'description': description,
            'changes': changes,
            'timestamp': asyncio.get_event_loop().time()
        })
    
    def _analyze_emotional_arc(self, scenes: List[Dict]) -> List[float]:
        """分析情感弧线"""
        arc = []
        for scene in scenes:
            # 简化的情感强度计算
            emotion_words = ['爱', '恨', '怒', '喜', '悲', '恐', '惊']
            content = scene.get('content', '')
            intensity = sum(content.count(word) for word in emotion_words) / max(len(content), 1) * 10
            arc.append(min(intensity, 1.0))
        return arc
    
    def _generate_ideal_arc(self, num_scenes: int) -> List[float]:
        """生成理想情感弧线"""
        # 简化的三幕情感曲线
        arc = []
        for i in range(num_scenes):
            progress = i / max(num_scenes - 1, 1)
            if progress < 0.25:  # 第一幕
                intensity = 0.3 + progress * 0.8
            elif progress < 0.75:  # 第二幕
                intensity = 0.5 + 0.3 * ((progress - 0.25) * 2)
            else:  # 第三幕
                intensity = 0.8 + 0.2 * ((progress - 0.75) * 4)
            arc.append(min(intensity, 1.0))
        return arc
    
    async def _adjust_emotional_intensity(
        self, 
        scene: Dict, 
        target_intensity: float
    ) -> Dict:
        """调整情感强度"""
        # 简化实现
        adjusted_scene = scene.copy()
        adjusted_scene['emotional_intensity'] = target_intensity
        return adjusted_scene
    
    def _collect_foreshadows(self, scenes: List[Dict]) -> List[Dict]:
        """收集所有伏笔"""
        foreshadows = []
        for i, scene in enumerate(scenes):
            if 'foreshadows' in scene:
                for fs in scene['foreshadows']:
                    fs['scene_index'] = i
                    foreshadows.append(fs)
        return foreshadows
    
    def _check_foreshadow_chains(self, foreshadows: List[Dict]) -> List[Dict]:
        """检查伏笔链条完整性"""
        incomplete = []
        # 简化实现：检查是否有未回收的伏笔
        for fs in foreshadows:
            if fs.get('planted') and not fs.get('revealed'):
                incomplete.append({
                    'type': 'missing_payoff',
                    'foreshadow': fs,
                    'suggested_scene': -1  # 最后一个场景
                })
        return incomplete
    
    async def _add_foreshadow_plant(self, scene: Dict, foreshadow: Dict) -> Dict:
        """添加伏笔埋设"""
        enhanced_scene = scene.copy()
        if 'foreshadows' not in enhanced_scene:
            enhanced_scene['foreshadows'] = []
        enhanced_scene['foreshadows'].append(foreshadow)
        return enhanced_scene
    
    async def _add_foreshadow_payoff(self, scene: Dict, foreshadow: Dict) -> Dict:
        """添加伏笔回收"""
        enhanced_scene = scene.copy()
        enhanced_scene['foreshadow_payoff'] = foreshadow
        return enhanced_scene
    
    def _generate_optimization_report(self) -> Dict:
        """生成优化报告"""
        report = {
            'total_optimizations': len(self.optimization_history),
            'optimization_by_type': {},
            'major_changes': []
        }
        
        # 按类型统计
        for opt in self.optimization_history:
            opt_type = opt['type']
            if opt_type not in report['optimization_by_type']:
                report['optimization_by_type'][opt_type] = 0
            report['optimization_by_type'][opt_type] += 1
            
            # 记录主要改动
            if len(opt['changes']) > 2:
                report['major_changes'].append(opt['description'])
        
        return report
    
    def _calculate_improvement(self) -> float:
        """计算改进程度"""
        # 基于优化次数的简单计算
        base_improvement = min(len(self.optimization_history) * 0.02, 0.2)
        
        # 根据优化类型加权
        type_weights = {
            'transition': 0.15,
            'style': 0.20,
            'pacing': 0.15,
            'emotion': 0.20,
            'foreshadow': 0.15,
            'consistency': 0.15
        }
        
        weighted_improvement = 0
        for opt in self.optimization_history:
            weighted_improvement += type_weights.get(opt['type'], 0.1) / 10
        
        return min(base_improvement + weighted_improvement, 0.3)


# 辅助类（简化实现）

class StyleAnalyzer:
    """风格分析器"""
    
    async def analyze_overall(self, scenes: List[Dict]) -> Dict:
        """分析整体风格"""
        return {'voice': 'neutral', 'tone': 'balanced', 'pace': 'moderate'}
    
    async def analyze_scene(self, scene: Dict) -> Dict:
        """分析场景风格"""
        return {'voice': 'neutral', 'tone': 'balanced', 'pace': 'moderate'}
    
    def is_consistent(self, scene_style: Dict, overall_style: Dict) -> bool:
        """检查风格一致性"""
        return scene_style == overall_style
    
    async def adjust_style(self, scene: Dict, target_style: Dict) -> Dict:
        """调整风格"""
        adjusted = scene.copy()
        adjusted['style'] = target_style
        return adjusted


class PacingController:
    """节奏控制器"""
    
    async def analyze(self, scenes: List[Dict]) -> Dict:
        """分析节奏"""
        return {
            'scene_pacing': [0.5] * len(scenes),
            'ideal_curve': [0.5] * len(scenes)
        }
    
    async def accelerate(self, scene: Dict) -> Dict:
        """加快节奏"""
        return scene
    
    async def decelerate(self, scene: Dict) -> Dict:
        """放慢节奏"""
        return scene


class TransitionSmoother:
    """过渡平滑器"""
    
    async def evaluate(self, prev_scene: Dict, next_scene: Dict) -> float:
        """评估过渡质量"""
        return 0.85
    
    async def smooth(self, prev_scene: Dict, next_scene: Dict) -> Dict:
        """平滑过渡"""
        return next_scene


class ConsistencyEnforcer:
    """一致性执行器"""
    
    async def check_all(self, scenes: List[Dict]) -> List[Dict]:
        """检查所有一致性"""
        return []
    
    async def fix_character(self, scene: Dict, details: Dict) -> Dict:
        """修复角色一致性"""
        return scene
    
    async def fix_timeline(self, scene: Dict, details: Dict) -> Dict:
        """修复时间线一致性"""
        return scene
    
    async def fix_setting(self, scene: Dict, details: Dict) -> Dict:
        """修复设定一致性"""
        return scene