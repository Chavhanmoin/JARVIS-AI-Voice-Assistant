import pyautogui
import time
from helpers import speak

def open_app_via_start_menu(app_name):
    """Open application using Windows Start menu search"""
    try:
        # Press Windows key to open Start menu
        pyautogui.press('win')
        time.sleep(0.5)
        
        # Type the application name
        pyautogui.write(app_name)
        time.sleep(1)
        
        # Press Enter to open the first result
        pyautogui.press('enter')
        
        speak(f"{app_name} opened.")
        return True
    except Exception as e:
        print(f"Start menu search failed: {e}")
        return False