"""
测试项目管理系统
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from commands.command_router import CommandRouter


async def test_project_management():
    """测试项目管理功能"""
    print("="*60)
    print("Project Management System Test")
    print("="*60)
    
    router = CommandRouter()
    
    # 1. 创建系列小说项目
    print("\n1. Creating series project...")
    result = await router.route_command(
        "/novel:project-new",
        ["detective-series"],
        {
            "type": "series",
            "genre": "mystery",
            "audience": "adult",
            "books": "5"
        }
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Message: {result.get('message')}")
    
    # 2. 创建单本小说项目
    print("\n2. Creating standalone project...")
    result = await router.route_command(
        "/novel:project-new",
        ["the-final-day"],
        {
            "type": "standalone",
            "genre": "thriller",
            "chapters": "30",
            "words": "120000"
        }
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Message: {result.get('message')}")
    
    # 3. 创建短篇集项目
    print("\n3. Creating collection project...")
    result = await router.route_command(
        "/novel:project-new",
        ["ghost-stories"],
        {
            "type": "collection",
            "genre": "horror",
            "stories": "12"
        }
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Message: {result.get('message')}")
    
    # 4. 列出所有项目
    print("\n4. Listing all projects...")
    result = await router.route_command(
        "/novel:project-list",
        [],
        {}
    )
    print(f"   Total projects: {result.get('count')}")
    for project in result.get('projects', []):
        print(f"   - {project['name']} ({project['type']})")
    
    # 5. 列出系列项目
    print("\n5. Listing series projects only...")
    result = await router.route_command(
        "/novel:project-list",
        [],
        {"type": "series"}
    )
    print(f"   Series projects: {result.get('count')}")
    
    # 6. 获取项目信息
    print("\n6. Getting project info...")
    result = await router.route_command(
        "/novel:project-info",
        ["detective-series"],
        {}
    )
    if result.get('status') == 'success':
        info = result.get('project_info', {})
        print(f"   Name: {info.get('name')}")
        print(f"   Type: {info.get('type')}")
        print(f"   Books: {info.get('books_count', 0)}")
    
    # 7. 向系列添加第一本书
    print("\n7. Adding book to series...")
    result = await router.route_command(
        "/novel:project-add-book",
        ["detective-series", "1", "温泉旅馆谜案"],
        {}
    )
    print(f"   Status: {result.get('status')}")
    print(f"   Message: {result.get('message')}")
    
    # 8. 再次获取系列信息
    print("\n8. Getting updated series info...")
    result = await router.route_command(
        "/novel:project-info",
        ["detective-series"],
        {}
    )
    if result.get('status') == 'success':
        info = result.get('project_info', {})
        print(f"   Books count: {info.get('books_count', 0)}")
        print(f"   Books: {info.get('books', [])}")
    
    print("\n" + "="*60)
    print("Project management test completed!")
    print("="*60)


async def test_integrated_workflow():
    """测试集成工作流程"""
    print("\n" + "="*60)
    print("Integrated Workflow Test")
    print("="*60)
    
    router = CommandRouter()
    
    # 1. 创建系列项目
    print("\n1. Creating a new mystery series project...")
    result = await router.route_command(
        "/novel:project-new",
        ["夜雨推理系列"],
        {
            "type": "series",
            "genre": "mystery",
            "audience": "young-adult",
            "books": "3"
        }
    )
    print(f"   Created: {result.get('message')}")
    
    # 2. 添加第一本书
    print("\n2. Adding first book to series...")
    result = await router.route_command(
        "/novel:project-add-book",
        ["夜雨推理系列", "1", "雨夜的秘密"],
        {}
    )
    print(f"   Added: {result.get('message')}")
    
    # 3. 查看项目结构
    print("\n3. Checking project structure...")
    project_path = Path("D:/NOVELSYS-SWARM/projects/夜雨推理系列")
    if project_path.exists():
        print("   Project structure created:")
        for item in project_path.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(project_path)
                print(f"     - {relative_path}")
                if len(str(relative_path)) < 50:  # 只显示短路径
                    continue
    
    print("\n" + "="*60)
    print("All tests completed successfully!")
    print("="*60)


async def main():
    """运行所有测试"""
    try:
        # 测试项目管理
        await test_project_management()
        
        # 测试集成工作流
        await test_integrated_workflow()
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())