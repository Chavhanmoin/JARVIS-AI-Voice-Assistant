import pyautogui
import psutil
import subprocess
import time
from helpers import speak

def open_app(app_name):
    """Universal app opener using Windows Start menu"""
    try:
        print(f"Attempting to open {app_name}...")
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(0.5)
        speak(f"{app_name} opened.")
        return True
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        return False

def close_app(app_name):
    """Universal app closer with multiple methods"""
    killed = []
    
    # Method 1: Kill by process name
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = proc.info['name'].lower()
            if app_name.lower() in proc_name or proc_name.startswith(app_name.lower()):
                proc.terminate()
                killed.append(proc.info['name'])
        except:
            continue
    
    # Method 2: Kill by window title if no process found
    if not killed:
        try:
            pyautogui.getWindowsWithTitle(app_name)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(0.5)
            killed.append(app_name)
        except:
            pass
    
    if killed:
        speak(f"{app_name} closed.")
        return True
    else:
        speak(f"{app_name} is not running.")
        return False