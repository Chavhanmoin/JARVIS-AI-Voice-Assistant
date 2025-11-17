import os
import time
import subprocess
import pyautogui
from helpers import speak

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

class WhatsAppDesktop:
    def __init__(self):
        self.app_path = self._find_whatsapp_path()
    
    def _find_whatsapp_path(self):
        """Find WhatsApp desktop app path"""
        import glob
        import os
        
        # Get current user
        username = os.getenv('USERNAME', 'Admin')
        
        possible_paths = [
            f"C:\\Users\\{username}\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
            f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\WindowsApps\\WhatsApp.exe",
            r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_*\WhatsApp.exe",
            r"C:\Program Files\WindowsApps\*WhatsApp*\WhatsApp.exe"
        ]
        
        for path in possible_paths:
            if "*" in path:
                matches = glob.glob(path)
                if matches:
                    return matches[0]
            elif os.path.exists(path):
                return path
        return None
    
    def open_whatsapp(self):
        """Open WhatsApp desktop app"""
        try:
            if self.app_path:
                subprocess.Popen(f'"{self.app_path}"', shell=True)
                time.sleep(4)
                return True
            else:
                # Try Microsoft Store app launch
                try:
                    subprocess.run(["powershell", "-Command", "Start-Process 'ms-windows-store://pdp/?productid=9NKSQGP7F2NH'"], check=True)
                    time.sleep(2)
                except:
                    pass
                
                # Try direct launch via explorer
                subprocess.Popen("explorer.exe shell:appsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!WhatsAppDesktop", shell=True)
                time.sleep(4)
                return True
        except Exception as e:
            print(f"Failed to open WhatsApp: {e}")
            return False
    
    def send_message(self, contact_name, message):
        """Send message via WhatsApp desktop"""
        try:
            # Open WhatsApp if not already open using the working method
            if not self._is_whatsapp_open():
                from system_control import open_application
                open_application("whatsapp")
                time.sleep(4)  # Wait for WhatsApp to load
            
            # Wait for WhatsApp to be ready
            time.sleep(1)
            
            # Focus WhatsApp window
            import win32gui
            def focus_whatsapp():
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_text = win32gui.GetWindowText(hwnd).lower()
                        if 'whatsapp' in window_text:
                            win32gui.SetForegroundWindow(hwnd)
                            return False
                    return True
                win32gui.EnumWindows(enum_windows_callback, [])
            
            focus_whatsapp()
            time.sleep(1)
            
            # Click on search box at top
            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width // 4, 100)  # Search area at top
            time.sleep(1)
            
            # Clear search and type contact name
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.5)
            pyautogui.typewrite(contact_name)
            time.sleep(2)
            
            # Click on first contact result
            pyautogui.click(screen_width // 4, 200)  # First contact in list
            time.sleep(2)
            
            # Click on message input area at bottom
            pyautogui.click(screen_width // 2, screen_height - 50)
            time.sleep(1)
            
            # Clear any text in message field and type message
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.5)
            pyautogui.typewrite(message)
            time.sleep(1)
            
            # Send message
            pyautogui.press('enter')
            
            speak(f"Message sent to {contact_name}")
            return True
            
        except Exception as e:
            speak("Failed to send WhatsApp message")
            print(f"WhatsApp message error: {e}")
            return False
    
    def _is_whatsapp_open(self):
        """Check if WhatsApp is already running"""
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if 'whatsapp' in proc.info['name'].lower():
                    return True
            return False
        except:
            return False

# Global instance
_whatsapp_instance = None

def get_whatsapp():
    """Get WhatsApp instance"""
    global _whatsapp_instance
    if not _whatsapp_instance:
        _whatsapp_instance = WhatsAppDesktop()
    return _whatsapp_instance

def send_whatsapp_message(contact, message):
    """Send WhatsApp message via desktop app"""
    whatsapp = get_whatsapp()
    return whatsapp.send_message(contact, message)

def send_whatsapp_message_direct(contact, message):
    """Send message assuming WhatsApp is already open"""
    import pyautogui
    import time
    
    try:
        # Ensure we're not in start menu - press Escape first
        pyautogui.press('escape')
        time.sleep(1)
        
        # Wait and ensure WhatsApp window is focused
        time.sleep(2)
        
        # Click on WhatsApp window center to focus it
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(1)
        
        # Click on the search box at the top (contact search)
        pyautogui.click(300, 100)
        time.sleep(1)
        
        # Clear and type contact name
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.typewrite(contact)
        time.sleep(3)
        
        # Click on first contact result instead of pressing Enter
        pyautogui.click(300, 180)  # Click on first contact in results
        time.sleep(3)
        
        # Click on message input area at bottom of chat
        pyautogui.click(screen_width // 2, screen_height - 100)
        time.sleep(1)
        
        # Type and send message
        pyautogui.typewrite(message)
        time.sleep(1)
        pyautogui.press('enter')
        
        return True
        
    except Exception as e:
        print(f"WhatsApp message error: {e}")
        return False

if __name__ == "__main__":
    # Test the WhatsApp functionality
    whatsapp = WhatsAppDesktop()
    print(f"WhatsApp path: {whatsapp.app_path}")
    # whatsapp.send_message("Test Contact", "Hello from JARVIS!")