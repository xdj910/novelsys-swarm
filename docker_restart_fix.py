#!/usr/bin/env python3
"""
Docker Restart Script to Fix ImportError
Stop existing container, rebuild with fixed code, and start new one
"""
import subprocess
import sys
import os
import time

def run_command(cmd, cwd=None):
    """Run command and return result"""
    print(f"Executing: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    docker_dir = r"D:\NOVELSYS-SWARM\.claude\docker\docling"

    print("=== Docker Container Restart to Fix ImportError ===")

    # 1. Stop existing containers
    print("\n1. Stopping existing containers...")
    run_command("docker stop docling-granite")
    run_command("docker rm docling-granite")

    # 2. Check if images need to be removed
    print("\n2. Checking for existing images...")
    run_command("docker images | grep docling")

    # 3. Rebuild container with fixed code
    print("\n3. Rebuilding container with fixed ImportError...")
    if not run_command("docker-compose build --no-cache", cwd=docker_dir):
        print("Build failed! Check the error messages above.")
        return False

    # 4. Start new container
    print("\n4. Starting new container...")
    if not run_command("docker-compose up -d", cwd=docker_dir):
        print("Container start failed! Check the error messages above.")
        return False

    # 5. Wait and check status
    print("\n5. Waiting for container to start...")
    time.sleep(5)

    # 6. Check logs
    print("\n6. Checking container logs...")
    run_command("docker logs docling-granite")

    # 7. Test endpoint
    print("\n7. Testing API endpoint...")
    try:
        import requests
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print("SUCCESS: API is responding!")
            print(f"Response: {response.json()}")
        else:
            print(f"API returned status: {response.status_code}")
    except ImportError:
        print("Install requests to test API: pip install requests")
    except Exception as e:
        print(f"API test failed: {e}")

    print("\n=== Restart Complete ===")
    print("Check logs above for any errors.")
    print("If successful, API should be available at: http://localhost:8000")

    return True

if __name__ == "__main__":
    main()