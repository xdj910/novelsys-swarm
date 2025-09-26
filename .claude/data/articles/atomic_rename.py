import os
import shutil

# Atomic rename operation for Windows
temp_file = r"D:\NOVELSYS-SWARM\.claude\data\articles\registry.json.tmp"
target_file = r"D:\NOVELSYS-SWARM\.claude\data\articles\registry.json"

try:
    # Perform atomic rename
    shutil.move(temp_file, target_file)
    print("Registry updated successfully")
except Exception as e:
    print(f"Error during atomic rename: {e}")