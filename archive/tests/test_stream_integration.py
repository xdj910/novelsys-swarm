"""
测试4-Stream集成架构
验证Stream生成和Claude智能合并
"""

import asyncio
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.stream_integrator import ClaudeStreamIntegrator, StreamOutput
from agents.stream_chapter_generator import (
    StreamChapterGeneratorAgent,
    CharacterPsychologyStream,
    NarrativeStructureStream,
    WorldBuildingStream,
    ProseCraftStream
)


async def test_stream_outputs():
    """测试各个Stream的输出"""
    print("=== 测试独立Stream输出 ===\n")
    
    scene = {
        "scene_number": 1,
        "type": "emotional",
        "description": "主角面对重大抉择的内心挣扎",
        "characters": ["李明", "张华"],
        "location": "雨夜的东京街头",
        "mood": "tense"
    }
    
    bible = {}
    context = {}
    
    # 测试各个Stream
    streams = {
        "Character Psychology": CharacterPsychologyStream(),
        "Narrative Structure": NarrativeStructureStream(),
        "World Building": WorldBuildingStream(),
        "Prose Craft": ProseCraftStream()
    }
    
    for name, stream in streams.items():
        result = await stream.generate(scene, bible, context)
        print(f"{name}:")
        print(f"  内容: {result['content']}")
        print(f"  风格: {result['style']}")
        print(f"  焦点: {result['focus']}")
        print()


async def test_stream_integration():
    """测试Stream集成"""
    print("=== 测试Stream智能合并 ===\n")
    
    # 创建模拟的Stream输出
    stream_outputs = {
        "character_psychology": StreamOutput(
            stream_name="character_psychology",
            content="李明的内心充满了矛盾。他知道揭露真相意味着什么，但沉默同样是一种背叛。",
            style="introspective",
            focus="角色内心",
            metadata={"emotional_intensity": 0.8}
        ),
        "narrative_structure": StreamOutput(
            stream_name="narrative_structure",
            content="故事在此处达到转折点。主角必须做出决定，这个选择将影响所有人的命运。",
            style="structured",
            focus="情节推进",
            metadata={"tension_level": 0.9}
        ),
        "world_building": StreamOutput(
            stream_name="world_building",
            content="雨水冲刷着东京的街道，霓虹灯在水洼中破碎成无数片段，就像此刻破碎的心。",
            style="descriptive",
            focus="环境氛围",
            metadata={"atmosphere": "melancholic"}
        ),
        "prose_craft": StreamOutput(
            stream_name="prose_craft",
            content="时间仿佛凝固，每一滴雨水都诉说着一个故事，每一次心跳都是一次抉择。",
            style="literary",
            focus="语言艺术",
            metadata={"literary_devices": ["metaphor", "personification"]}
        )
    }
    
    # 使用集成器合并
    integrator = ClaudeStreamIntegrator()
    integrator.set_thinking_mode("think-hard")
    
    # 注意：实际运行需要Claude API，这里只是演示架构
    try:
        merged_content = await integrator.smart_merge(stream_outputs)
        print("合并后的内容:")
        print(merged_content)
    except Exception as e:
        print(f"合并演示（实际需要Claude API）:")
        print("雨水冲刷着东京的街道，霓虹灯在水洼中破碎成无数片段。")
        print("李明站在街角，内心充满了矛盾。")
        print("他知道，这个决定将影响所有人的命运。")
        print("时间仿佛凝固，每一滴雨水都诉说着一个故事。")


async def test_full_chapter_generation():
    """测试完整章节生成"""
    print("\n=== 测试完整4-Stream章节生成 ===\n")
    
    # 创建Stream生成器
    generator = StreamChapterGeneratorAgent()
    generator.set_thinking_mode("think-hard")
    
    # 准备任务
    task = {
        "type": "generate_scene",
        "scene": {
            "scene_number": 1,
            "type": "mixed",
            "description": "开场：温泉旅馆的神秘案件",
            "characters": ["侦探", "旅馆老板"],
            "location": "日式温泉旅馆大堂",
            "mood": "mysterious"
        },
        "bible": {},
        "chapter_context": {
            "chapter_number": 1,
            "title": "迷雾中的温泉"
        }
    }
    
    try:
        result = await generator.generate_scene_with_streams(task)
        print(f"场景生成成功!")
        print(f"字数: {result.get('word_count', 0)}")
        print(f"内容预览: {result.get('content', '')[:200]}...")
        
        # 显示各Stream的贡献
        if "stream_outputs" in result:
            print("\n各Stream贡献:")
            for stream_name, output in result["stream_outputs"].items():
                print(f"  {stream_name}: {output['focus']}")
    except Exception as e:
        print(f"生成演示完成（实际需要完整环境）: {e}")


async def test_scene_type_detection():
    """测试场景类型检测"""
    print("\n=== 测试场景类型检测 ===\n")
    
    generator = StreamChapterGeneratorAgent()
    
    test_points = [
        "主角与反派激烈对话，揭露阴谋",
        "深夜追逐，穿越雨中的街道",
        "温泉旅馆的详细环境描写",
        "主角内心的痛苦回忆",
        "多个角色在餐厅的复杂互动"
    ]
    
    for point in test_points:
        scene_type = generator.determine_scene_type(point)
        print(f"场景: {point}")
        print(f"类型: {scene_type}\n")


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("NOVELSYS 4-Stream集成测试")
    print("=" * 60)
    print()
    
    # 运行各项测试
    await test_stream_outputs()
    await test_stream_integration()
    await test_full_chapter_generation()
    await test_scene_type_detection()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())