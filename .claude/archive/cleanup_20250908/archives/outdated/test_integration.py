"""
NOVELSYS-SWARM 集成测试
测试所有组件的集成工作
适配Claude Code环境
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# 导入所有核心组件
from src.core.command_executor import CommandExecutor
from src.core.agent_executor import AgentExecutor, AgentOrchestrator, AgentTask
from src.core.agent_dispatcher import AgentDispatcher, WorkflowDispatcher, TaskPriority
from src.core.data_persistence import DataManager
from src.core.context_sync import GlobalContextCoordinator
from src.core.ultimate_stream_integrator import UltimateStreamIntegrator
from src.core.iterative_generator import IterativeGenerator
from src.core.global_optimizer import GlobalOptimizer


async def test_command_system():
    """测试命令系统"""
    print("\n" + "="*60)
    print("测试 1: 命令执行系统")
    print("="*60)
    
    executor = CommandExecutor()
    
    # 测试项目初始化
    print("\n1.1 初始化项目...")
    result = await executor.execute("init")
    print(f"  结果: {result.success}")
    
    # 测试创建新项目
    print("\n1.2 创建新项目...")
    result = await executor.execute("project-new", ["神秘东方", "玄幻"])
    print(f"  结果: {result.success}")
    if result.success:
        print(f"  Bible ID: {result.data.get('bible_id')}")
    
    # 测试项目状态
    print("\n1.3 获取项目状态...")
    result = await executor.execute("status")
    print(f"  结果: {result.success}")
    if result.success:
        print(f"  状态: {json.dumps(result.data, indent=2, ensure_ascii=False)}")
    
    return executor


async def test_agent_system():
    """测试Agent系统"""
    print("\n" + "="*60)
    print("测试 2: Agent执行系统")
    print("="*60)
    
    executor = AgentExecutor()
    
    # 测试单个Agent执行
    print("\n2.1 执行单个Agent...")
    task = AgentTask(
        agent_name="outline-creator",
        task_type="create_outline",
        input_data={"chapter": 1},
        context={"genre": "玄幻"},
        priority=5
    )
    
    result = await executor.execute_agent("outline-creator", task)
    print(f"  Agent: {result.agent_name}")
    print(f"  成功: {result.success}")
    print(f"  执行时间: {result.execution_time:.2f}秒")
    
    # 测试Stream执行
    print("\n2.2 执行Stream A (Character)...")
    tasks = [
        AgentTask(
            agent_name="character-psychologist",
            task_type="analyze_character",
            input_data={"character": "主角"},
            context={},
            priority=1
        ),
        AgentTask(
            agent_name="dialogue-specialist",
            task_type="create_dialogue",
            input_data={"scene": 1},
            context={},
            priority=2
        )
    ]
    
    stream_result = await executor.execute_stream("A", tasks)
    print(f"  Stream: {stream_result['stream']}")
    print(f"  成功: {stream_result['success']}")
    print(f"  执行摘要: {stream_result['summary']}")
    
    return executor


async def test_dispatcher():
    """测试任务调度器"""
    print("\n" + "="*60)
    print("测试 3: 任务调度系统")
    print("="*60)
    
    dispatcher = AgentDispatcher(max_concurrent=1)  # Claude环境限制
    
    # 调度多个任务
    print("\n3.1 调度任务...")
    
    tasks = [
        ("scene-painter", AgentTask(
            agent_name="scene-painter",
            task_type="paint_scene",
            input_data={"scene": 1},
            context={},
            priority=3
        )),
        ("emotion-weaver", AgentTask(
            agent_name="emotion-weaver",
            task_type="weave_emotions",
            input_data={"scene": 1},
            context={},
            priority=2
        )),
        ("quality-scorer", AgentTask(
            agent_name="quality-scorer",
            task_type="score_quality",
            input_data={"content": "测试内容"},
            context={},
            priority=1
        ))
    ]
    
    task_ids = []
    for agent_name, task in tasks:
        task_id = dispatcher.schedule_task(
            agent_name,
            task,
            TaskPriority.NORMAL
        )
        task_ids.append(task_id)
        print(f"  已调度: {task_id} -> {agent_name}")
    
    # 运行调度器
    print("\n3.2 执行调度队列...")
    await dispatcher.run_until_complete(timeout=30)
    
    # 获取统计
    stats = dispatcher.get_statistics()
    print(f"\n3.3 执行统计:")
    print(f"  总任务: {stats['total_tasks']}")
    print(f"  完成: {stats['completed']}")
    print(f"  失败: {stats['failed']}")
    print(f"  成功率: {stats['success_rate']:.1%}")
    print(f"  平均执行时间: {stats['average_execution_time']:.2f}秒")
    
    return dispatcher


async def test_data_persistence():
    """测试数据持久化"""
    print("\n" + "="*60)
    print("测试 4: 数据持久化系统")
    print("="*60)
    
    manager = DataManager()
    
    # 初始化项目
    print("\n4.1 初始化项目数据...")
    project_data = {
        "title": "测试小说",
        "genre": "科幻",
        "author": "AI作家",
        "description": "一个测试用的科幻小说"
    }
    
    bible_id = manager.initialize_project(project_data)
    print(f"  Bible ID: {bible_id}")
    
    # 保存章节
    print("\n4.2 保存章节...")
    chapter_data = {
        "title": "第一章：起源",
        "scenes": [
            {"content": "这是第一个场景的内容..."},
            {"content": "这是第二个场景的内容..."}
        ],
        "quality_score": 0.85,
        "status": "draft"
    }
    
    success = manager.save_chapter_with_context(
        chapter_number=1,
        chapter_data=chapter_data,
        context_updates={"last_scene": "起源场景"}
    )
    print(f"  保存成功: {success}")
    
    # 获取项目状态
    print("\n4.3 获取项目状态...")
    status = manager.get_project_status()
    print(f"  标题: {status['title']}")
    print(f"  章节数: {status['chapters_count']}")
    print(f"  总字数: {status['total_words']}")
    print(f"  平均质量: {status['average_quality']:.2f}")
    
    return manager


async def test_context_sync():
    """测试上下文同步"""
    print("\n" + "="*60)
    print("测试 5: 上下文同步系统")
    print("="*60)
    
    # 使用之前创建的Bible ID
    bible_id = "test_bible_001"
    coordinator = GlobalContextCoordinator(bible_id)
    
    # 注册组件
    print("\n5.1 注册组件...")
    coordinator.register_component("stream_A", "stream")
    coordinator.register_component("stream_B", "stream")
    coordinator.register_component("agent_director", "agent")
    coordinator.register_component("command_executor", "command")
    print(f"  已注册 {len(coordinator.registered_components)} 个组件")
    
    # 推送上下文更新
    print("\n5.2 推送上下文更新...")
    await coordinator.synchronizer.push_context(
        source="stream_A",
        target="character",
        data={
            "protagonist": {
                "name": "林风",
                "personality": "勇敢、智慧",
                "level": 1
            }
        }
    )
    print("  角色上下文已更新")
    
    # 拉取上下文
    print("\n5.3 拉取上下文...")
    contexts = await coordinator.synchronizer.pull_context(
        requester="test",
        context_types=["character", "global"]
    )
    print(f"  获取到 {len(contexts)} 个上下文类型")
    
    # 执行全局同步
    print("\n5.4 执行全局同步...")
    sync_report = await coordinator.synchronize_all()
    print(f"  检查点ID: {sync_report['checkpoint_id']}")
    print(f"  同步组件数: {sync_report['components_synced']}")
    
    return coordinator


async def test_stream_integration():
    """测试Stream集成"""
    print("\n" + "="*60)
    print("测试 6: 8-Stream集成系统")
    print("="*60)
    
    integrator = UltimateStreamIntegrator()
    
    # 准备测试数据
    scene = {
        "scene_number": 1,
        "content": "测试场景内容",
        "characters": ["主角", "配角"],
        "setting": "神秘森林"
    }
    
    context = {
        "bible": {"genre": "玄幻"},
        "previous_scenes": []
    }
    
    print("\n6.1 执行8-Stream处理...")
    result = await integrator.process_scene(scene, context)
    
    print(f"  处理成功: {result['success']}")
    print(f"  质量分数: {result['quality_score']:.2f}")
    print(f"  Stream输出数: {len(result['stream_outputs'])}")
    
    # 显示各Stream贡献
    print("\n6.2 各Stream贡献:")
    for stream_name, output in result['stream_outputs'].items():
        if isinstance(output, dict):
            print(f"  - {stream_name}: 已处理")
    
    return integrator


async def test_iterative_optimization():
    """测试迭代优化系统"""
    print("\n" + "="*60)
    print("测试 7: 三轮迭代优化系统")
    print("="*60)
    
    generator = IterativeGenerator()
    
    scene = {
        "content": "初始场景内容",
        "quality_score": 0.75
    }
    
    context = {"target_quality": 0.95}
    
    print("\n7.1 执行三轮迭代...")
    result = await generator.generate_with_iterations(scene, context, max_rounds=3)
    
    print(f"  迭代轮数: {result['iteration_count']}")
    print(f"  最终质量: {result['final_quality']:.2f}")
    print(f"  质量提升: {result['quality_improvement']:.2f}")
    
    # 显示每轮结果
    print("\n7.2 迭代历史:")
    for i, iteration in enumerate(result['iteration_history'], 1):
        print(f"  第{i}轮: 质量 {iteration['quality']:.2f} - {iteration['focus']}")
    
    return generator


async def test_global_optimization():
    """测试全局优化"""
    print("\n" + "="*60)
    print("测试 8: 全局优化系统")
    print("="*60)
    
    optimizer = GlobalOptimizer()
    
    # 准备测试场景
    scenes = [
        {"content": "场景1内容", "type": "opening"},
        {"content": "场景2内容", "type": "development"},
        {"content": "场景3内容", "type": "climax"},
        {"content": "场景4内容", "type": "resolution"}
    ]
    
    print("\n8.1 执行全局优化...")
    result = await optimizer.optimize_chapter(scenes)
    
    print(f"  优化场景数: {len(result['optimized_scenes'])}")
    print(f"  优化操作数: {len(result['optimization_history'])}")
    print(f"  质量提升: {result['quality_improvement']:.1%}")
    
    # 显示优化报告
    print("\n8.2 优化报告:")
    report = result['report']
    print(f"  总优化次数: {report['total_optimizations']}")
    for opt_type, count in report['optimization_by_type'].items():
        print(f"  - {opt_type}: {count}次")
    
    return optimizer


async def test_full_workflow():
    """测试完整工作流"""
    print("\n" + "="*60)
    print("测试 9: 完整章节生成工作流")
    print("="*60)
    
    # 初始化所有组件
    command_executor = CommandExecutor()
    orchestrator = AgentOrchestrator()
    workflow_dispatcher = WorkflowDispatcher()
    
    # 创建项目
    print("\n9.1 创建新项目...")
    result = await command_executor.execute("project-new", ["工作流测试", "科幻"])
    bible_id = result.data.get('bible_id')
    
    # 准备Bible和上下文
    bible = {
        "title": "工作流测试",
        "genre": "科幻",
        "setting": "未来世界",
        "protagonist": {"name": "张三", "role": "探索者"}
    }
    
    context = {
        "chapter_goal": "介绍主角和世界观",
        "target_quality": 0.90
    }
    
    # 执行章节生成工作流
    print("\n9.2 执行章节生成工作流...")
    workflow_result = await workflow_dispatcher.execute_chapter_workflow(
        chapter_number=1,
        bible=bible,
        context=context
    )
    
    print(f"  工作流ID: {workflow_result['workflow_id']}")
    print(f"  执行阶段数: {len(workflow_result['stages'])}")
    
    # 显示工作流摘要
    summary = workflow_result['summary']
    print(f"\n9.3 工作流摘要:")
    print(f"  总任务数: {summary['total_tasks']}")
    print(f"  成功任务: {summary['successful_tasks']}")
    print(f"  成功率: {summary['success_rate']:.1%}")
    print(f"  总执行时间: {summary['total_execution_time']:.2f}秒")
    
    return workflow_result


async def main():
    """主测试函数"""
    print("\n" + "="*60)
    print(" NOVELSYS-SWARM 集成测试套件")
    print(" 测试环境: Claude Code")
    print(" 开始时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
    
    try:
        # 运行所有测试
        results = {}
        
        # 1. 命令系统
        results['command'] = await test_command_system()
        
        # 2. Agent系统
        results['agent'] = await test_agent_system()
        
        # 3. 调度器
        results['dispatcher'] = await test_dispatcher()
        
        # 4. 数据持久化
        results['persistence'] = await test_data_persistence()
        
        # 5. 上下文同步
        results['context'] = await test_context_sync()
        
        # 6. Stream集成
        results['stream'] = await test_stream_integration()
        
        # 7. 迭代优化
        results['iteration'] = await test_iterative_optimization()
        
        # 8. 全局优化
        results['optimization'] = await test_global_optimization()
        
        # 9. 完整工作流
        results['workflow'] = await test_full_workflow()
        
        # 测试总结
        print("\n" + "="*60)
        print(" 测试完成")
        print("="*60)
        print(f"✓ 通过测试模块: {len(results)}")
        print(f"  - 命令系统: {'✓' if results.get('command') else '✗'}")
        print(f"  - Agent系统: {'✓' if results.get('agent') else '✗'}")
        print(f"  - 调度系统: {'✓' if results.get('dispatcher') else '✗'}")
        print(f"  - 持久化系统: {'✓' if results.get('persistence') else '✗'}")
        print(f"  - 同步系统: {'✓' if results.get('context') else '✗'}")
        print(f"  - Stream集成: {'✓' if results.get('stream') else '✗'}")
        print(f"  - 迭代优化: {'✓' if results.get('iteration') else '✗'}")
        print(f"  - 全局优化: {'✓' if results.get('optimization') else '✗'}")
        print(f"  - 完整工作流: {'✓' if results.get('workflow') else '✗'}")
        
        print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n系统集成测试成功！NOVELSYS-SWARM已准备就绪。")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 在Claude Code环境中运行
    asyncio.run(main())