# youtube.py — optimized
import urllib.parse
import webbrowser
import os
import shutil
import sys
from typing import Optional

def _find_chrome_executable() -> Optional[str]:
    """
    Attempt to locate a Chrome executable in a cross-platform manner.
    Returns the path to the executable or None if not found.
    """
    # Try common names on PATH first
    for name in ("google-chrome", "chrome", "chrome.exe", "Google Chrome"):
        path = shutil.which(name)
        if path:
            return path

    # Platform-specific common install locations
    if sys.platform.startswith("win"):
        candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
    elif sys.platform.startswith("darwin"):
        mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(mac_path):
            return mac_path
    else:  # linux
        # common Chrome/Chromium binary names
        for c in ("/usr/bin/google-chrome-stable", "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"):
            if os.path.exists(c):
                return c

    return None

# Register Chrome once (if available)
_CHROME_PATH = _find_chrome_executable()
if _CHROME_PATH:
    try:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(_CHROME_PATH))
        print(f"Chrome registered: {_CHROME_PATH}")
    except Exception as e:
        print(f"Failed to register Chrome ({_CHROME_PATH}): {e}")
else:
    print("Chrome not found — will use system default browser.")

def youtube(textToSearch: str) -> str:
    """
    Open a YouTube search for the given query.
    Returns a short status message.
    """
    if not textToSearch or not str(textToSearch).strip():
        msg = "Empty or invalid search query."
        print(msg)
        return msg

    query = urllib.parse.quote_plus(str(textToSearch).strip())
    url = f"https://www.youtube.com/results?search_query={query}"
    print(f"Opening YouTube search: {url}")

    # Prefer registered Chrome; fall back to default browser
    try:
        if _CHROME_PATH:
            webbrowser.get('chrome').open_new_tab(url)
            msg = f"YouTube search opened in Chrome for: {textToSearch}"
            print(msg)
            return msg
    except Exception as e:
        print(f"Warning: failed to open Chrome ({e}). Falling back to default browser.")

    # Default fallback
    try:
        webbrowser.open_new_tab(url)
        msg = f"YouTube search opened in default browser for: {textToSearch}"
        print(msg)
        return msg
    except Exception as e:
        msg = f"Failed to open YouTube search: {e}"
        print(msg)
        return msg

# Short alias to keep backwards compatibility
open_youtube_search = youtube

if __name__ == "__main__":
    youtube("lofi hip hop radio")
