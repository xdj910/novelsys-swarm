"""
NOVELSYS-SWARM 主程序
AI驱动的小说创作系统
"""

import asyncio
import sys
import argparse
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from commands.command_router import CommandRouter


class NovelSystemSwarm:
    """NOVELSYS-SWARM主系统"""
    
    def __init__(self):
        self.router = CommandRouter()
        self.running = True
    
    async def process_command(self, command_line: str):
        """处理命令行输入"""
        if not command_line.strip():
            return
        
        # 解析命令
        parts = command_line.split()
        command = parts[0]
        args = []
        options = {}
        
        # 解析参数和选项
        for part in parts[1:]:
            if part.startswith("--"):
                # 选项
                if "=" in part:
                    key, value = part[2:].split("=", 1)
                    options[key] = value
                else:
                    options[part[2:]] = True
            else:
                # 参数
                args.append(part)
        
        # 特殊命令处理
        if command == "exit" or command == "quit":
            self.running = False
            return {"message": "Goodbye!"}
        
        # 路由命令
        try:
            result = await self.router.route_command(command, args, options)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def interactive_mode(self):
        """交互模式"""
        print("="*60)
        print("NOVELSYS-SWARM - AI Novel Creation System")
        print("Version 1.0.0 | Based on CCPM Architecture")
        print("="*60)
        print("Type 'help' for available commands, 'exit' to quit")
        print()
        
        while self.running:
            try:
                # 获取用户输入
                command_line = input("novel> ").strip()
                
                if not command_line:
                    continue
                
                # 处理命令
                result = await self.process_command(command_line)
                
                # 显示结果
                if result:
                    if "error" in result:
                        print(f"Error: {result['error']}")
                    elif "message" in result:
                        print(result["message"])
                    else:
                        # 格式化输出
                        for key, value in result.items():
                            if key not in ["status"]:
                                print(f"{key}: {value}")
                print()
                
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Unexpected error: {e}")
    
    async def batch_mode(self, script_file: str):
        """批处理模式 - 从文件执行命令"""
        script_path = Path(script_file)
        
        if not script_path.exists():
            print(f"Script file not found: {script_file}")
            return
        
        with open(script_path, 'r', encoding='utf-8') as f:
            commands = f.readlines()
        
        print(f"Executing {len(commands)} commands from {script_file}")
        
        for i, command_line in enumerate(commands, 1):
            command_line = command_line.strip()
            
            # 跳过空行和注释
            if not command_line or command_line.startswith("#"):
                continue
            
            print(f"\n[{i}] Executing: {command_line}")
            result = await self.process_command(command_line)
            
            if result:
                if "error" in result:
                    print(f"Error: {result['error']}")
                    break  # 出错停止
                elif "message" in result:
                    print(result["message"])
    
    async def run(self, mode="interactive", script=None):
        """运行系统"""
        if mode == "batch" and script:
            await self.batch_mode(script)
        else:
            await self.interactive_mode()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="NOVELSYS-SWARM Novel Creation System")
    parser.add_argument("--mode", choices=["interactive", "batch"], default="interactive",
                       help="Execution mode")
    parser.add_argument("--script", help="Script file for batch mode")
    parser.add_argument("--command", help="Execute single command")
    
    args = parser.parse_args()
    
    # 创建系统实例
    system = NovelSystemSwarm()
    
    # 运行系统
    if args.command:
        # 单命令模式
        asyncio.run(system.process_command(args.command))
    else:
        # 交互或批处理模式
        asyncio.run(system.run(mode=args.mode, script=args.script))


if __name__ == "__main__":
    main()