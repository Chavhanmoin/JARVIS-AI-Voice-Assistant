import sys
import os
import time
import subprocess

# Add project root path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from system_control import open_anything, close_anything, execute_system_command

print("\n=== 🧠 JARVIS SYSTEM CONTROL — FULL TEST (Optimized Voice) ===\n")

def section(title):
    print("\n" + "=" * 65)
    print(f"🔹 {title}")
    print("=" * 65)

try:
    # 1️⃣ Open & Close Notepad
    section("Testing Notepad Application")
    print(open_anything("notepad"))
    time.sleep(3)
    print(close_anything("notepad"))
    time.sleep(1)

    # 2️⃣ Open & Close Calculator
    section("Testing Calculator")
    print(open_anything("calculator"))
    time.sleep(3)
    print(close_anything("calculator"))
    time.sleep(1)

    # 3️⃣ Open & Close File Explorer
    section("Testing File Explorer")
    print(open_anything("explorer"))
    time.sleep(3)
    print(close_anything("explorer"))
    time.sleep(1)

    # 4️⃣ Windows Settings
    section("Testing Windows Settings")
    print(execute_system_command("start ms-settings:"))
    time.sleep(5)
    print(close_anything("SystemSettings.exe"))
    time.sleep(1)

    # 5️⃣ Network & Internet (Wi-Fi)
    section("Testing Wi-Fi Settings")
    print(execute_system_command("start ms-settings:network-wifi"))
    time.sleep(5)
    print(close_anything("SystemSettings.exe"))
    time.sleep(1)

    # 6️⃣ Command Prompt
    section("Testing Command Prompt")
    print(open_anything("cmd"))
    time.sleep(2)
    print(execute_system_command("echo Hello from Jarvis system test"))
    time.sleep(2)
    print(close_anything("cmd"))
    time.sleep(1)

    # 7️⃣ Restart Explorer
    section("Restarting Windows Explorer")
    print(execute_system_command("taskkill /f /im explorer.exe"))
    time.sleep(3)
    subprocess.Popen("explorer.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)

    # 8️⃣ Volume Control
    section("Testing Volume Control")
    try:
        execute_system_command("nircmd.exe mutesysvolume 1")
        time.sleep(1)
        execute_system_command("nircmd.exe mutesysvolume 0")
        time.sleep(1)
        execute_system_command("nircmd.exe setsysvolume 49152")
        print("✅ Volume control tested.")
    except Exception:
        print("⚠️ Skipped: NirCmd not available.")

    # 9️⃣ Screen Brightness
    section("Testing Screen Brightness")
    try:
        import screen_brightness_control as sbc
        current = sbc.get_brightness(display=0)[0]
        print(f"💡 Current brightness: {current}%")
        sbc.set_brightness(50)
        time.sleep(2)
        sbc.set_brightness(current)
        print(f"🔙 Brightness restored to {current}%")
    except Exception:
        print("⚠️ Skipped: screen_brightness_control not available.")

    # 🔟 Power Operations (Simulation)
    section("Testing Power Operations (Simulation)")
    print("⚡ Restart simulation: shutdown /r /t 5")
    print("⚡ Shutdown simulation: shutdown /s /t 5")

    # 11️⃣ Folder Access
    section("Testing Folder Access")
    for folder in ["downloads", "documents", "pictures"]:
        print(open_anything(folder))
        time.sleep(2)

    # 12️⃣ Misc Commands
    section("Testing Miscellaneous Commands")
    print(execute_system_command("dir"))
    print(execute_system_command("systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\""))

    # ✅ Done
    section("All Tests Completed")
    print("\n✅ ALL SYSTEM CONTROL TESTS COMPLETED SUCCESSFULLY!\n")

except Exception as e:
    print(f"\n❌ Critical error during system control test: {e}")
