"""
三轮迭代生成系统
实现从85分到98分的渐进式质量提升
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
import time

@dataclass
class IterationResult:
    """迭代结果"""
    round: int
    content: Dict
    quality_score: float
    problems: List[Dict]
    improvements: List[str]
    execution_time: float


class IterativeGenerator:
    """
    三轮迭代生成器
    通过逐步优化达到98分质量目标
    """
    
    def __init__(self, stream_integrator):
        """
        初始化迭代生成器
        
        Args:
            stream_integrator: 8-Stream集成器实例
        """
        self.integrator = stream_integrator
        self.iteration_history = []
        
        # 质量目标（每轮递进）
        self.quality_targets = {
            1: 0.85,  # 第一轮：基础生成
            2: 0.92,  # 第二轮：问题修复
            3: 0.98   # 第三轮：精雕细琢
        }
    
    async def generate_with_iterations(
        self, 
        scene: Dict, 
        context: Dict,
        max_rounds: int = 3
    ) -> Dict:
        """
        执行三轮迭代生成
        
        Args:
            scene: 场景信息
            context: 上下文信息
            max_rounds: 最大迭代轮数
            
        Returns:
            最终生成结果
        """
        start_time = time.time()
        self.iteration_history = []
        
        current_result = None
        current_scene = scene.copy()
        current_context = context.copy()
        
        for round_num in range(1, max_rounds + 1):
            print(f"\n=== 第{round_num}轮迭代 ===")
            
            # 执行当前轮次生成
            iteration_result = await self._execute_iteration(
                round_num,
                current_scene,
                current_context,
                current_result
            )
            
            self.iteration_history.append(iteration_result)
            current_result = iteration_result.content
            
            # 检查是否达到质量目标
            if iteration_result.quality_score >= self.quality_targets[round_num]:
                print(f"第{round_num}轮达到质量目标: {iteration_result.quality_score:.2f}")
                
                # 如果已达到最终目标，提前结束
                if iteration_result.quality_score >= 0.98:
                    print(f"提前达到98分目标，结束迭代")
                    break
            else:
                print(f"第{round_num}轮质量分数: {iteration_result.quality_score:.2f}, 继续优化")
            
            # 为下一轮准备
            if round_num < max_rounds:
                current_scene, current_context = await self._prepare_next_iteration(
                    iteration_result,
                    current_scene,
                    current_context
                )
        
        # 生成最终报告
        final_result = {
            'final_content': current_result,
            'iterations': self.iteration_history,
            'total_rounds': len(self.iteration_history),
            'final_quality': self.iteration_history[-1].quality_score,
            'total_time': time.time() - start_time,
            'quality_improvement': self._calculate_improvement()
        }
        
        return final_result
    
    async def _execute_iteration(
        self,
        round_num: int,
        scene: Dict,
        context: Dict,
        previous_result: Optional[Dict]
    ) -> IterationResult:
        """
        执行单轮迭代
        
        Args:
            round_num: 轮次编号
            scene: 场景信息
            context: 上下文信息
            previous_result: 上一轮结果
            
        Returns:
            迭代结果
        """
        round_start = time.time()
        
        if round_num == 1:
            # 第一轮：基础生成
            result = await self._round1_basic_generation(scene, context)
        elif round_num == 2:
            # 第二轮：问题修复
            result = await self._round2_problem_fixing(
                scene, context, previous_result
            )
        else:
            # 第三轮：精雕细琢
            result = await self._round3_fine_tuning(
                scene, context, previous_result
            )
        
        # 识别问题
        problems = await self._identify_problems(result, round_num)
        
        # 计算质量分数
        quality_score = result.get('quality', {}).get('overall_score', 0.0)
        
        return IterationResult(
            round=round_num,
            content=result,
            quality_score=quality_score,
            problems=problems,
            improvements=await self._identify_improvements(result, previous_result),
            execution_time=time.time() - round_start
        )
    
    async def _round1_basic_generation(self, scene: Dict, context: Dict) -> Dict:
        """
        第一轮：基础生成（目标85分）
        重点：完整性、基本连贯性
        """
        # 强调基础要求
        enhanced_context = context.copy()
        enhanced_context['iteration_round'] = 1
        enhanced_context['focus_areas'] = [
            'completeness',      # 内容完整性
            'basic_coherence',   # 基本连贯性
            'character_basics',  # 角色基础
            'plot_progression'   # 情节推进
        ]
        
        # 使用8-Stream生成
        result = await self.integrator.generate(scene, enhanced_context)
        
        return result
    
    async def _round2_problem_fixing(
        self, 
        scene: Dict, 
        context: Dict,
        previous_result: Dict
    ) -> Dict:
        """
        第二轮：问题修复（目标92分）
        重点：修复明显问题、增强深度
        """
        # 分析第一轮的问题
        problems = previous_result.get('quality', {}).get('weaknesses', [])
        
        # 针对性增强
        enhanced_context = context.copy()
        enhanced_context['iteration_round'] = 2
        enhanced_context['previous_result'] = previous_result
        enhanced_context['fix_targets'] = problems
        enhanced_context['focus_areas'] = [
            'fix_continuity',    # 修复连贯性问题
            'deepen_character',  # 深化角色
            'enhance_emotion',   # 增强情感
            'improve_dialogue'   # 改进对话
        ]
        
        # 增强场景信息
        enhanced_scene = scene.copy()
        enhanced_scene['refinement_mode'] = True
        
        # 再次生成
        result = await self.integrator.generate(enhanced_scene, enhanced_context)
        
        return result
    
    async def _round3_fine_tuning(
        self,
        scene: Dict,
        context: Dict,
        previous_result: Dict
    ) -> Dict:
        """
        第三轮：精雕细琢（目标98分）
        重点：文学性、艺术性、完美度
        """
        # 最高标准要求
        enhanced_context = context.copy()
        enhanced_context['iteration_round'] = 3
        enhanced_context['previous_result'] = previous_result
        enhanced_context['quality_mode'] = 'ultimate'
        enhanced_context['focus_areas'] = [
            'literary_quality',   # 文学质量
            'artistic_value',     # 艺术价值
            'emotional_impact',   # 情感冲击力
            'reader_experience',  # 阅读体验
            'subtle_details',     # 细节雕琢
            'prose_elegance'      # 文笔优雅
        ]
        
        # 极致场景要求
        enhanced_scene = scene.copy()
        enhanced_scene['quality_level'] = 'masterpiece'
        enhanced_scene['polish_mode'] = True
        
        # 最终生成
        result = await self.integrator.generate(enhanced_scene, enhanced_context)
        
        return result
    
    async def _identify_problems(self, result: Dict, round_num: int) -> List[Dict]:
        """
        识别当前结果的问题
        
        Args:
            result: 生成结果
            round_num: 当前轮次
            
        Returns:
            问题列表
        """
        problems = []
        quality = result.get('quality', {})
        
        # 根据轮次设置不同的问题识别标准
        if round_num == 1:
            # 第一轮：关注基础问题
            threshold = 0.8
        elif round_num == 2:
            # 第二轮：关注中级问题
            threshold = 0.9
        else:
            # 第三轮：关注细节问题
            threshold = 0.95
        
        # 检查各维度
        for dimension, score in quality.get('dimension_scores', {}).items():
            if score < threshold:
                problems.append({
                    'dimension': dimension,
                    'score': score,
                    'severity': self._classify_severity(score, threshold),
                    'description': f"{dimension}得分{score:.2f}，低于标准{threshold}"
                })
        
        return problems
    
    async def _identify_improvements(
        self,
        current_result: Dict,
        previous_result: Optional[Dict]
    ) -> List[str]:
        """
        识别相对上一轮的改进
        
        Args:
            current_result: 当前结果
            previous_result: 上一轮结果
            
        Returns:
            改进列表
        """
        if not previous_result:
            return ["初始生成完成"]
        
        improvements = []
        
        # 比较质量分数
        current_score = current_result.get('quality', {}).get('overall_score', 0)
        previous_score = previous_result.get('quality', {}).get('overall_score', 0)
        
        if current_score > previous_score:
            improvements.append(
                f"整体质量提升: {previous_score:.2f} → {current_score:.2f}"
            )
        
        # 比较各维度
        current_dims = current_result.get('quality', {}).get('dimension_scores', {})
        previous_dims = previous_result.get('quality', {}).get('dimension_scores', {})
        
        for dim in current_dims:
            if dim in previous_dims:
                if current_dims[dim] > previous_dims[dim]:
                    improvements.append(
                        f"{dim}: {previous_dims[dim]:.2f} → {current_dims[dim]:.2f}"
                    )
        
        return improvements
    
    async def _prepare_next_iteration(
        self,
        last_result: IterationResult,
        scene: Dict,
        context: Dict
    ) -> tuple[Dict, Dict]:
        """
        为下一轮迭代准备输入
        
        Args:
            last_result: 上一轮结果
            scene: 场景信息
            context: 上下文信息
            
        Returns:
            更新后的场景和上下文
        """
        # 保留原始信息
        new_scene = scene.copy()
        new_context = context.copy()
        
        # 添加迭代信息
        new_context['iteration_history'] = [
            {
                'round': h.round,
                'quality': h.quality_score,
                'problems': h.problems
            }
            for h in self.iteration_history
        ]
        
        # 添加上轮问题作为重点
        new_context['problems_to_fix'] = last_result.problems
        
        return new_scene, new_context
    
    def _classify_severity(self, score: float, threshold: float) -> str:
        """
        分类问题严重程度
        
        Args:
            score: 实际分数
            threshold: 阈值
            
        Returns:
            严重程度
        """
        gap = threshold - score
        if gap > 0.2:
            return 'critical'
        elif gap > 0.1:
            return 'major'
        elif gap > 0.05:
            return 'minor'
        else:
            return 'trivial'
    
    def _calculate_improvement(self) -> Dict:
        """
        计算整体改进情况
        
        Returns:
            改进统计
        """
        if not self.iteration_history:
            return {}
        
        first_score = self.iteration_history[0].quality_score
        final_score = self.iteration_history[-1].quality_score
        
        return {
            'initial_score': first_score,
            'final_score': final_score,
            'total_improvement': final_score - first_score,
            'improvement_percentage': ((final_score - first_score) / first_score * 100) 
                                     if first_score > 0 else 0,
            'rounds_used': len(self.iteration_history)
        }


# 测试函数
async def test_iterative_generator():
    """测试三轮迭代生成器"""
    from ultimate_stream_integrator import UltimateStreamIntegrator
    
    # 创建集成器和迭代生成器
    integrator = UltimateStreamIntegrator()
    generator = IterativeGenerator(integrator)
    
    # 测试场景
    test_scene = {
        'id': 'test_scene',
        'type': 'emotional_climax',
        'content': '关键情感场景'
    }
    
    test_context = {
        'chapter': 7,
        'bible': {}
    }
    
    # 执行三轮迭代
    result = await generator.generate_with_iterations(test_scene, test_context)
    
    print(f"\n=== 迭代完成 ===")
    print(f"最终质量: {result['final_quality']:.2f}")
    print(f"总用时: {result['total_time']:.2f}秒")
    print(f"质量提升: {result['quality_improvement']['total_improvement']:.2f}")
    
    return result


if __name__ == "__main__":
    asyncio.run(test_iterative_generator())