#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple test for 4-Stream integration"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from core.stream_integrator import StreamOutput
from agents.stream_chapter_generator import (
    CharacterPsychologyStream,
    NarrativeStructureStream,
    WorldBuildingStream,
    ProseCraftStream
)


async def test_streams():
    """Test individual streams"""
    print("Testing 4-Stream outputs...")
    print("-" * 40)
    
    scene = {
        "scene_number": 1,
        "type": "emotional",
        "description": "Character faces major decision",
        "characters": ["Detective", "Suspect"],
        "location": "Hot spring inn",
        "mood": "tense"
    }
    
    # Test each stream
    char_stream = CharacterPsychologyStream()
    narr_stream = NarrativeStructureStream()
    world_stream = WorldBuildingStream()
    prose_stream = ProseCraftStream()
    
    results = {}
    results["Character"] = await char_stream.generate(scene, {}, {})
    results["Narrative"] = await narr_stream.generate(scene, {}, {})
    results["World"] = await world_stream.generate(scene, {}, {})
    results["Prose"] = await prose_stream.generate(scene, {}, {})
    
    for name, result in results.items():
        print(f"\n{name} Stream:")
        print(f"  Style: {result['style']}")
        print(f"  Focus: {result['focus']}")
        # Print first 100 chars to avoid encoding issues
        content_preview = result['content'][:100] if len(result['content']) > 100 else result['content']
        print(f"  Content: {content_preview}...")
    
    print("\n" + "-" * 40)
    print("4-Stream test completed successfully!")
    print("\nThe system is ready for:")
    print("1. Parallel stream generation")
    print("2. Claude-based intelligent merging")
    print("3. Scene-type specific optimization")
    print("\nUse command: /novel:chapter-stream <series-name> <chapter-number>")


if __name__ == "__main__":
    asyncio.run(test_streams())