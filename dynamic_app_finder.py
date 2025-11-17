import os
import subprocess
import winreg
from helpers import speak

def find_and_open_app(app_name):
    """Enhanced application finder for all types of installed apps"""
    app_name = app_name.lower().strip()
    
    # Try Microsoft Store apps first
    if _try_store_app(app_name):
        return True
    
    # Try Windows built-in apps
    if _try_builtin_app(app_name):
        return True
    
    # Try registry-based apps
    if _try_registry_app(app_name):
        return True
    
    # Try file system search
    return _try_filesystem_search(app_name)

def _try_store_app(app_name):
    """Try start menu search for any application"""
    try:
        import pyautogui
        import time
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        speak(f"{app_name} opened.")
        return True
    except:
        return False

def _try_builtin_app(app_name):
    """Try Windows built-in applications"""
    builtin_apps = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "wordpad": "wordpad.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "registry editor": "regedit.exe",
        "system information": "msinfo32.exe",
        "device manager": "devmgmt.msc",
        "disk management": "diskmgmt.msc",
        "event viewer": "eventvwr.msc",
        "services": "services.msc",
        "computer management": "compmgmt.msc"
    }
    
    if app_name in builtin_apps:
        try:
            subprocess.Popen(builtin_apps[app_name], shell=True)
            speak(f"{app_name} opened.")
            return True
        except:
            pass
    
    return False

def _try_registry_app(app_name):
    """Search Windows registry for installed applications"""
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for reg_path in registry_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0].lower()
                    if app_name in display_name or any(word in display_name for word in app_name.split()):
                        try:
                            install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                            if install_location and os.path.exists(install_location):
                                exe_path = _find_exe_in_path(install_location, app_name)
                                if exe_path:
                                    subprocess.Popen(f'"{exe_path}"', shell=True)
                                    speak(f"{app_name} opened.")
                                    return True
                        except:
                            pass
                        
                        try:
                            display_icon = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                            if display_icon.endswith('.exe') and os.path.exists(display_icon):
                                subprocess.Popen(f'"{display_icon}"', shell=True)
                                speak(f"{app_name} opened.")
                                return True
                        except:
                            pass
                    
                    winreg.CloseKey(subkey)
                except:
                    continue
            winreg.CloseKey(key)
        except:
            continue
    
    return False

def _try_filesystem_search(app_name):
    """Search common installation directories"""
    search_paths = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"C:\Users\Admin\AppData\Local",
        r"C:\Users\Admin\AppData\Roaming",
        r"C:\ProgramData",
        r"C:\Users\Admin\Desktop",
        r"C:\Users\Admin\Downloads",
        os.path.expanduser("~/AppData/Local"),
        os.path.expanduser("~/AppData/Roaming")
    ]
    
    for base_path in search_paths:
        if os.path.exists(base_path):
            try:
                for item in os.listdir(base_path):
                    if app_name in item.lower() or any(word in item.lower() for word in app_name.split()):
                        item_path = os.path.join(base_path, item)
                        
                        if item.lower().endswith('.exe'):
                            try:
                                subprocess.Popen(f'"{item_path}"', shell=True)
                                speak(f"{app_name} opened.")
                                return True
                            except:
                                continue
                        
                        if os.path.isdir(item_path):
                            exe_path = _find_exe_in_path(item_path, app_name)
                            if exe_path:
                                subprocess.Popen(f'"{exe_path}"', shell=True)
                                speak(f"{app_name} opened.")
                                return True
            except:
                continue
    
    return False

def _find_exe_in_path(directory, app_name):
    """Find executable file in directory"""
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.exe'):
                    if app_name in file.lower() or any(word in file.lower() for word in app_name.split()):
                        return os.path.join(root, file)
            
            if root != directory:
                break
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.exe'):
                    return os.path.join(root, file)
            
            if root != directory:
                break
    except:
        pass
    
    return None
