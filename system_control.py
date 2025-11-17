import os
import subprocess
import psutil
import winreg
import time
import ctypes
import threading
import tkinter as tk
from helpers import speak
try:
    from universal_app_control import open_app, close_app
    print("DEBUG: Successfully imported universal_app_control")
except Exception as e:
    print(f"ERROR: Failed to import universal_app_control: {e}")
    def open_app(name):
        print(f"FALLBACK: Using pyautogui directly for {name}")
        import pyautogui
        import time
        try:
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(name)
            time.sleep(1)
            pyautogui.press('enter')
            speak(f"{name} opened.")
            return True
        except:
            return False
    def close_app(name):
        return False

# ===================================================
# 🧠 JARVIS SYSTEM CONTROL — FULL EDITION
# ===================================================

SendInput = ctypes.windll.user32.keybd_event

# Volume & Brightness Keys
VOLUME_UP, VOLUME_DOWN, VOLUME_MUTE = 0xAF, 0xAE, 0xAD
BRIGHTNESS_UP, BRIGHTNESS_DOWN = 0xB9, 0xB8


# ===================================================
# 🌞 JARVIS CUSTOM OVERLAY (Brightness + Volume)
# ===================================================
def show_overlay(level, mode="brightness"):
    """Display a smooth overlay popup with Jarvis theme."""
    def _overlay():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.9)
        root.configure(bg='#1c1c1c')

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        width, height = 320, 90
        x = (screen_w // 2) - (width // 2)
        y = screen_h - 180
        root.geometry(f"{width}x{height}+{x}+{y}")

        frame = tk.Frame(root, bg="#2b2b2b", bd=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        title = "Brightness" if mode == "brightness" else "Volume"
        label = tk.Label(frame, text=f"{title}: {level}%", fg="#ff3333", bg="#2b2b2b", font=("Segoe UI", 15, "bold"))
        label.pack(pady=(5, 4))

        canvas = tk.Canvas(frame, bg="gray25", height=20, bd=0, highlightthickness=0)
        canvas.pack(padx=10, pady=5, fill="x")

        fill_len = int((level / 100) * 300)
        canvas.create_rectangle(0, 0, fill_len, 20, fill="#ff3333", width=0)

        root.after(1300, root.destroy)
        root.mainloop()

    threading.Thread(target=_overlay, daemon=True).start()


# ===================================================
# 🖥️ MAIN SYSTEM CONTROLLER CLASS
# ===================================================
class SystemController:
    """Handles app management, file control, volume, brightness, and system commands."""

    def __init__(self):
        self.installed_apps = self._get_installed_apps()

    # ---------------------------------------------------
    # 🔍 Fetch Installed Apps (Registry)
    # ---------------------------------------------------
    def _get_installed_apps(self):
        apps = {}
        try:
            paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            ]
            for path in paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            install_path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                            if name and install_path:
                                apps[name.lower()] = install_path
                        except:
                            continue
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Registry read error: {e}")
        return apps

    # ---------------------------------------------------
    # 🚀 OPEN APPLICATION / FILE / FOLDER
    # ---------------------------------------------------
    def open_application(self, app_name):
        app_name = app_name.lower().strip()
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "chrome": r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "vscode": r'"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"',
            "word": "winword.exe",
            "excel": "excel.exe",
            "spotify": "spotify.exe",
            "settings": "start ms-settings:",
            "obs studio": "obs64.exe",
            "obs": "obs64.exe",
            "notion": "notion.exe",
            "whatsapp": "start whatsapp:"
        }

        folders = {
            "documents": os.path.expanduser("~/Documents"),
            "desktop": os.path.expanduser("~/Desktop"),
            "downloads": os.path.expanduser("~/Downloads"),
            "download": os.path.expanduser("~/Downloads"),
            "pictures": os.path.expanduser("~/Pictures"),
            "music": os.path.expanduser("~/Music"),
            "file explorer": "explorer.exe",
            "explorer": "explorer.exe",
            "file": "explorer.exe"
        }

        # Folder and explorer handling
        if app_name in folders:
            path = folders[app_name]
            if path.endswith(".exe"):
                subprocess.Popen(path, shell=True)
                speak(f"{app_name} opened.")
            else:
                os.startfile(path)
                speak(f"{app_name} folder opened.")
            return f"✅ Opened {app_name}."

        # App mapping
        if app_name in app_map:
            try:
                subprocess.Popen(app_map[app_name], shell=True)
                speak(f"{app_name} opened.")
                return f"✅ Opened {app_name}."
            except Exception as e:
                speak(f"Failed to open {app_name}.")
                return f"⚠️ Failed to open {app_name}: {e}"

        # Registry apps
        if app_name in self.installed_apps:
            path = self.installed_apps[app_name]
            if os.path.exists(path):
                # If it's a directory, look for executable
                if os.path.isdir(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.lower().endswith('.exe') and app_name in file.lower():
                                exe_path = os.path.join(root, file)
                                subprocess.Popen(f'"{exe_path}"', shell=True)
                                speak(f"{app_name} opened.")
                                return f"✅ Opened {app_name}."
                        break  # Only check first level
                    # If no specific exe found, just open the folder
                    os.startfile(path)
                else:
                    # If it's already an exe file
                    subprocess.Popen(f'"{path}"', shell=True)
                speak(f"{app_name} opened.")
                return f"✅ Opened {app_name}."

        # .exe fallback
        try:
            subprocess.Popen(f"{app_name}.exe", shell=True)
            speak(f"{app_name} opened.")
            return f"✅ Opened {app_name}."
        except:
            speak(f"I couldn’t find {app_name}.")
            return f"❌ Could not open {app_name}."

    # ---------------------------------------------------
    # 🛑 CLOSE APPLICATION
    # ---------------------------------------------------
    def close_application(self, app_name):
        app_name = app_name.lower().strip()
        process_map = {
            "notepad": "notepad.exe",
            "calculator": "CalculatorApp.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "spotify": "spotify.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "vscode": "Code.exe",
            "settings": "SystemSettings.exe",
            "obs studio": "obs64.exe",
            "obs": "obs64.exe",
            "notion": "Notion.exe"
        }

        target = process_map.get(app_name, f"{app_name}.exe")
        killed = []

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                proc_name = proc.info["name"].lower()
                # Check exact match or partial match
                if target.lower() == proc_name or target.lower() in proc_name or app_name in proc_name:
                    proc.kill()
                    killed.append(proc.info["name"])
            except:
                continue

        if killed:
            speak(f"{app_name} closed.")
            return f"🛑 Closed: {', '.join(killed)}"
        else:
            speak(f"{app_name} is not currently running.")
            return f"⚠️ No process found for {app_name}."

    # ---------------------------------------------------
    # 💾 OPEN FILE OR PATH
    # ---------------------------------------------------
    def open_file_or_folder(self, path):
        try:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                os.startfile(expanded)
                speak(f"Opened {path}.")
                return f"✅ Opened {path}."
            else:
                speak(f"Path not found for {path}.")
                return f"❌ Path not found: {path}"
        except Exception as e:
            speak(f"Error opening {path}.")
            return f"⚠️ Error opening {path}: {e}"

    # ---------------------------------------------------
    # ⚙️ EXECUTE SYSTEM COMMAND
    # ---------------------------------------------------
    def system_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip() or result.stderr.strip() or "No output."
            speak("Command executed successfully.")
            return f"💻 {command}\nOutput:\n{output}"
        except Exception as e:
            speak("Error executing command.")
            return f"⚠️ System command error: {e}"

    # ---------------------------------------------------
    # 🔊 VOLUME CONTROL
    # ---------------------------------------------------
    def volume_control(self, action, value=None):
        try:
            value = int(value or 10)
            steps = value // 2

            if "up" in action:
                for _ in range(steps):
                    SendInput(VOLUME_UP, 0, 0, 0)
                    time.sleep(0.05)
                speak(f"Volume increased by {value} percent.")

            elif "down" in action:
                for _ in range(steps):
                    SendInput(VOLUME_DOWN, 0, 0, 0)
                    time.sleep(0.05)
                speak(f"Volume decreased by {value} percent.")

            elif "mute" in action:
                SendInput(VOLUME_MUTE, 0, 0, 0)
                speak("Volume muted.")

            elif "set" in action:
                for _ in range(60):
                    SendInput(VOLUME_DOWN, 0, 0, 0)
                    time.sleep(0.01)
                for _ in range(value // 2):
                    SendInput(VOLUME_UP, 0, 0, 0)
                    time.sleep(0.03)
                speak(f"Volume set to {value} percent.")
            else:
                speak("Please say volume up, down, set, or mute.")

            show_overlay(value, "volume")

        except Exception as e:
            speak("Volume control failed.")
            print(f"⚠️ Volume error: {e}")

    # ---------------------------------------------------
    # 🌞 BRIGHTNESS CONTROL
    # ---------------------------------------------------
    def brightness_control(self, action, value=None):
        try:
            value = int(value or 10)
            current = int(subprocess.getoutput(
                'powershell "(Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness).CurrentBrightness"'
            ) or 50)
            new_brightness = current

            if "up" in action:
                new_brightness = min(100, current + value)
                speak(f"Brightness increased to {new_brightness} percent.")
            elif "down" in action:
                new_brightness = max(0, current - value)
                speak(f"Brightness decreased to {new_brightness} percent.")
            elif "set" in action:
                new_brightness = max(0, min(100, value))
                speak(f"Brightness set to {new_brightness} percent.")
            else:
                speak("Please say brightness up, down, or set.")
                return

            subprocess.run(
                f'powershell "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_brightness})"',
                shell=True, capture_output=True
            )

            show_overlay(new_brightness, "brightness")

        except Exception as e:
            speak("Brightness control failed.")
            print(f"⚠️ Brightness error: {e}")


# ===================================================
# 🧩 WRAPPER FUNCTIONS
# ===================================================
_controller_instance = None

def get_controller():
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = SystemController()
    return _controller_instance

def open_anything(name):
    print(f"DEBUG: open_anything ENTRY with: '{name}'")
    import pyautogui
    import time
    try:
        print(f"DEBUG: Starting Windows Start menu process")
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(name)
        time.sleep(1)
        pyautogui.press('enter')
        speak(f"{name} opened.")
        print(f"DEBUG: Successfully opened {name}")
        return f"✅ Opened {name}."
    except Exception as e:
        print(f"ERROR in open_anything: {e}")
        speak(f"Error opening {name}.")
        return f"❌ Error opening {name}."

def close_anything(name):
    if close_app(name):
        return f"🛑 Closed {name}."
    else:
        return f"⚠️ {name} is not running."

def execute_system_command(command):
    controller = get_controller()
    return controller.system_command(command)

def change_volume(action, value=None):
    controller = get_controller()
    return controller.volume_control(action, value)

def change_brightness(action, value=None):
    controller = get_controller()
    return controller.brightness_control(action, value)
