import os
import sys
import time
import pyautogui
import subprocess
import psutil

# ✅ Allow imports from root folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from file_manager import (
    create_folder, create_file, delete_file, delete_folder
)

print("\n=== 🧠 TESTING FULL FILE EXPLORER WORKFLOW ===")

# 🗂️ Step 1: Define paths
downloads = os.path.join(os.path.expanduser("~"), "Downloads")
test_folder = os.path.join(downloads, "Jarvis_test")
test_file = os.path.join(test_folder, "test.txt")
renamed_file = os.path.join(test_folder, "test1.txt")

# 🪄 Step 2: Open Downloads folder first (so you can see creation)
print("📂 Opening Downloads folder in File Explorer...")
subprocess.Popen(f'explorer "{downloads}"', shell=True)
time.sleep(3)  # wait for File Explorer to open

# 🪄 Step 3: Create new folder
print("🧱 Creating folder inside Downloads...")
print(create_folder(test_folder))
time.sleep(2)

# 🧭 Step 4: Open the new folder (navigate inside it)
print("📁 Opening the new folder in File Explorer...")
subprocess.Popen(f'explorer "{test_folder}"', shell=True)
time.sleep(2)

# 📝 Step 5: Create and open test.txt file
print("📝 Creating file test.txt...")
print(create_file(test_file, "Hello World"))
time.sleep(2)

print("📝 Opening file in Notepad...")
subprocess.Popen(f'notepad "{test_file}"', shell=True)
time.sleep(3)

# 💾 Step 6: Add content, save, and close Notepad
pyautogui.typewrite(" - Added by JARVIS automation.", interval=0.05)
time.sleep(1)
pyautogui.hotkey("ctrl", "s")  # Save file
time.sleep(1)
pyautogui.hotkey("alt", "f4")  # Close Notepad
time.sleep(1)

# ✏️ Step 7: Rename the file
print(f"🔤 Renaming {test_file} to {renamed_file}")
os.rename(test_file, renamed_file)
time.sleep(1)

# 🗑️ Step 8: Delete the file and folder
print(delete_file(renamed_file))
time.sleep(1)
print(delete_folder(test_folder))
time.sleep(1)

# 🚪 Step 9: Close all File Explorer windows
print("🚪 Closing all File Explorer windows...")
for proc in psutil.process_iter(["pid", "name"]):
    try:
        if "explorer.exe" in proc.info["name"].lower():
            proc.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

print("✅ Full file workflow test completed successfully!")
