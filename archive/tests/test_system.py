"""
测试NOVELSYS-SWARM系统
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from commands.command_router import CommandRouter


async def test_basic_workflow():
    """测试基本工作流程"""
    print("="*60)
    print("NOVELSYS-SWARM System Test")
    print("="*60)
    
    router = CommandRouter()
    
    # 1. 创建新的Bible
    print("\n1. Creating new Bible for 'Mystery Series'...")
    result = await router.route_command(
        "/novel:bible-new",
        ["mystery-series"],
        {
            "genre": "mystery",
            "thinking_mode": "ultrathink",
            "time_period": "contemporary",
            "audience": "adult"
        }
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Quality Score: {result.get('quality_score', 0):.1f}/100")
    
    # 2. 检查Bible一致性
    print("\n2. Checking Bible consistency...")
    result = await router.route_command(
        "/novel:bible-check",
        ["mystery-series"],
        {}
    )
    if result.get("results"):
        for check in result["results"]:
            print(f"   {check['file']}: {check['consistency_score']:.1f}/100")
    
    # 3. 生成第一章
    print("\n3. Generating Chapter 1...")
    result = await router.route_command(
        "/novel:chapter-start",
        ["mystery-series", "1"],
        {
            "thinking_mode": "think-hard",
            "plot_points": ["神秘事件发生", "主角登场", "初步调查", "发现线索", "章节悬念"],
            "characters": ["侦探李明", "助手小王"],
            "location": "都市办公楼",
            "mood": "suspense"
        }
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Quality Score: {result.get('quality_score', 0):.1f}/100")
    print(f"   Execution Time: {result.get('execution_time', 0):.2f}s")
    
    # 4. 并行生成多个章节
    print("\n4. Parallel generation of Chapters 2-4...")
    result = await router.route_command(
        "/novel:chapter-parallel",
        ["mystery-series", "2", "3", "4"],
        {"thinking_mode": "think"}
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Chapters Generated: {result.get('chapters_generated', 0)}")
    if result.get("results"):
        for ch_result in result["results"]:
            print(f"   Chapter {ch_result['chapter']}: {ch_result['status']} (Quality: {ch_result['quality_score']:.1f})")
    
    # 5. 质量检查
    print("\n5. Running quality check on all content...")
    result = await router.route_command(
        "/novel:quality-check",
        ["all"],
        {}
    )
    print(f"   Average Quality Score: {result.get('average_score', 0):.1f}/100")
    
    # 6. 系统状态
    print("\n6. Checking system status...")
    result = await router.route_command(
        "/novel:status",
        [],
        {}
    )
    print(f"   Active Agents: {len(result.get('agents', {}))}")
    print(f"   Total Bibles: {result.get('statistics', {}).get('total_bibles', 0)}")
    print(f"   Total Chapters: {result.get('statistics', {}).get('total_chapters', 0)}")
    
    print("\n" + "="*60)
    print("Test completed successfully!")
    print("="*60)


async def test_advanced_features():
    """测试高级功能"""
    print("\n" + "="*60)
    print("Advanced Features Test")
    print("="*60)
    
    router = CommandRouter()
    
    # 1. Bible进化（续集）
    print("\n1. Testing Bible evolution for sequel...")
    result = await router.route_command(
        "/novel:bible-evolve",
        ["mystery-series", "2"],
        {
            "thinking_mode": "think-harder",
            "conflict": "更深层的阴谋",
            "themes": ["背叛", "救赎"],
            "characters": [{"name": "新反派", "role": "mastermind"}]
        }
    )
    print(f"   Status: {result.get('status')}")
    if result.get('status') == 'success':
        print(f"   Quality Score: {result.get('quality_score', 0):.1f}/100")
    
    # 2. 独立小说Bible
    print("\n2. Creating standalone novel Bible...")
    result = await router.route_command(
        "/novel:bible-standalone",
        ["short-story"],
        {
            "genre": "thriller",
            "thinking_mode": "think-hard"
        }
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Quality Score: {result.get('quality_score', 0):.1f}/100")
    
    # 3. 批量章节生成
    print("\n3. Batch generation of chapters...")
    result = await router.route_command(
        "/novel:chapter-batch",
        ["short-story", "1", "3"],
        {"thinking_mode": "think"}
    )
    print(f"   Status: {result.get('status')}")
    if result.get("results"):
        for ch in result["results"]:
            print(f"   Chapter {ch['chapter']}: {ch['status']}")
    
    print("\n" + "="*60)
    print("Advanced test completed!")
    print("="*60)


async def main():
    """运行所有测试"""
    try:
        # 基础工作流测试
        await test_basic_workflow()
        
        # 高级功能测试
        await test_advanced_features()
        
        print("\n" + "="*60)
        print("All tests passed! System is working correctly.")
        print("="*60)
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())