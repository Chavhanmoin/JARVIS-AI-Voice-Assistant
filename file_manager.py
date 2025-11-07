import os
import shutil
import subprocess
from pathlib import Path
from helpers import speak


# ===============================
# 🔹 File & Folder Management
# ===============================

def create_file(file_path: str, content: str = "") -> str:
    """Create a new file, including parent folders if needed."""
    try:
        path = Path(file_path).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        speak(f"File created successfully: {path.name}")
        return f"✅ File created: {path}"
    except Exception as e:
        speak("Sorry, I failed to create the file.")
        return f"❌ File creation error: {e}"


def create_folder(folder_path: str) -> str:
    """Create a new folder, even nested ones."""
    try:
        path = Path(folder_path).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        speak(f"Folder created successfully: {path.name}")
        return f"✅ Folder created: {path}"
    except Exception as e:
        speak("Sorry, I couldn't create the folder.")
        return f"❌ Folder creation error: {e}"


def open_file(file_path: str) -> str:
    """Open a file using the default application."""
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            speak("File not found.")
            return f"⚠️ File not found: {path}"

        os.startfile(path)
        speak(f"Opening file: {path.name}")
        return f"✅ File opened: {path}"
    except Exception as e:
        speak("Sorry, I failed to open that file.")
        return f"❌ File open error: {e}"


def open_folder(folder_path: str) -> str:
    """Open a folder in File Explorer."""
    try:
        path = Path(folder_path).expanduser().resolve()
        if not path.exists():
            speak("Folder not found.")
            return f"⚠️ Folder not found: {path}"

        subprocess.run(["explorer", str(path)])
        speak(f"Opening folder: {path.name}")
        return f"✅ Folder opened: {path}"
    except Exception as e:
        speak("Sorry, I couldn't open the folder.")
        return f"❌ Folder open error: {e}"


def delete_file(file_path: str) -> str:
    """Delete a file safely."""
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            speak("File not found.")
            return f"⚠️ File not found: {path}"

        os.remove(path)
        speak(f"File deleted: {path.name}")
        return f"🗑️ File deleted: {path}"
    except Exception as e:
        speak("Sorry, I failed to delete the file.")
        return f"❌ File delete error: {e}"


def delete_folder(folder_path: str) -> str:
    """Delete a folder and all its contents."""
    try:
        path = Path(folder_path).expanduser().resolve()
        if not path.exists():
            speak("Folder not found.")
            return f"⚠️ Folder not found: {path}"

        shutil.rmtree(path)
        speak(f"Folder deleted: {path.name}")
        return f"🗑️ Folder deleted: {path}"
    except Exception as e:
        speak("Sorry, I failed to delete the folder.")
        return f"❌ Folder delete error: {e}"


def copy_file(source: str, destination: str) -> str:
    """Copy a file to a destination."""
    try:
        src = Path(source).expanduser().resolve()
        dst = Path(destination).expanduser().resolve()

        if not src.exists():
            speak("Source file not found.")
            return f"⚠️ Source not found: {src}"

        shutil.copy2(src, dst)
        speak(f"File copied successfully to {dst.name}")
        return f"✅ File copied: {src} ➜ {dst}"
    except Exception as e:
        speak("Sorry, I failed to copy the file.")
        return f"❌ Copy error: {e}"


def move_file(source: str, destination: str) -> str:
    """Move a file to a new destination."""
    try:
        src = Path(source).expanduser().resolve()
        dst = Path(destination).expanduser().resolve()

        if not src.exists():
            speak("Source file not found.")
            return f"⚠️ Source not found: {src}"

        shutil.move(src, dst)
        speak(f"File moved to {dst.name}")
        return f"✅ File moved: {src} ➜ {dst}"
    except Exception as e:
        speak("Sorry, I failed to move the file.")
        return f"❌ Move error: {e}"


def list_files(folder_path: str) -> str:
    """List files and folders in a given directory."""
    try:
        path = Path(folder_path).expanduser().resolve()
        if not path.exists():
            speak("Folder not found.")
            return f"⚠️ Folder not found: {path}"

        files = os.listdir(path)
        speak(f"Found {len(files)} items in this folder.")
        return f"📁 Files in {path}:\n" + "\n".join(files)
    except Exception as e:
        speak("Sorry, I couldn't list the files.")
        return f"❌ List error: {e}"
