"""
===============================
🧠 JARVIS SYSTEM INTEGRATION TEST
Author: Moin Raju Chavhan
Version: 3.0 (No OCR Edition)
===============================
This script tests all modules of J.A.R.V.I.S sequentially.
Make sure your .env file and credentials.json are configured correctly.
"""

import os
import sys
import time

# ✅ Add project root to Python path (important for imports)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import speak, cpu, joke, weather, translate
from system_control import open_anything, close_anything, execute_system_command
from web_automation import search_google, search_youtube, compose_gmail, close_web_automation
from wikipedia_search import search_and_open_wikipedia
from news import speak_news
from diction import translate as dict_translate
from file_manager import (
    create_file, create_folder, delete_file, delete_folder,
    move_file, copy_file, list_files
)
from ai_intent_recognition import get_ai_intent
from intent_recognition import process_user_intent
from gmail_service import send_gmail_api
from youtube import youtube


def line(title):
    """Pretty section separator"""
    print("\n" + "=" * 60)
    print(f"🔹 {title}")
    print("=" * 60)


def pause(seconds=2):
    """Pause between tests"""
    time.sleep(seconds)


# ============================
# ✅ MODULE TESTS
# ============================

def test_helpers():
    line("HELPERS MODULE TEST")
    speak("Testing my speaking ability.")
    cpu()
    joke()
    weather()
    translate("computer")
    pause()


def test_system_control():
    line("SYSTEM CONTROL TEST")
    result1 = open_anything("notepad")
    print(result1)
    pause(3)
    result2 = close_anything("notepad")
    print(result2)
    result3 = execute_system_command("echo Jarvis System Command Test")
    print(result3)
    pause()


def test_web_automation():
    line("WEB AUTOMATION TEST")
    print(search_google("latest AI news"))
    pause(3)
    print(search_youtube("AI robots"))
    pause(3)
    print(compose_gmail("", "Test Email", "This is a test draft from Jarvis."))
    pause()
    close_web_automation()


def test_wikipedia():
    line("WIKIPEDIA SEARCH TEST")
    print(search_and_open_wikipedia("Artificial Intelligence"))
    pause()


def test_news():
    line("NEWS FETCH TEST")
    speak_news()
    pause()


def test_dictionary():
    line("DICTIONARY TEST")
    dict_translate("computer")
    pause()


def test_file_manager():
    line("FILE MANAGER TEST")
    base_path = os.path.join(os.getcwd(), "test_folder")
    test_file = os.path.join(base_path, "test.txt")
    dest_file = os.path.join(base_path, "moved_test.txt")

    print(create_folder(base_path))
    print(create_file(test_file, "Jarvis file management test successful."))
    print(list_files(base_path))
    print(copy_file(test_file, dest_file))
    print(move_file(dest_file, os.path.join(base_path, "renamed_test.txt")))
    print(delete_file(test_file))
    print(delete_folder(base_path))
    pause()


def test_intent_recognition():
    line("RULE-BASED INTENT TEST")
    queries = [
        "open chrome",
        "close notepad",
        "search google for AI",
        "search youtube for car songs",
        "tell me a joke",
        "what's the weather",
        "what's the time"
    ]
    for q in queries:
        print(f"User: {q}")
        print(process_user_intent(q))
        pause(1)


def test_ai_intent():
    line("AI INTENT TEST")
    queries = [
        "send message to John saying hello",
        "compose an email about the project deadline",
        "open youtube and search for relaxing songs"
    ]
    for q in queries:
        print(f"🧠 AI Understanding: {q}")
        print(get_ai_intent(q))
        pause(2)


def test_gmail_service():
    line("GMAIL SERVICE TEST")
    print(send_gmail_api("", "Jarvis Automated Test", "This is a draft test email from Jarvis AI."))
    pause()


def test_youtube():
    line("YOUTUBE SEARCH TEST")
    youtube("AI short film")
    pause()


# ============================
# ✅ FULL TEST RUNNER
# ============================

def full_test():
    """Runs all module tests sequentially."""
    line("STARTING FULL JARVIS SYSTEM TEST")
    speak("Starting full system diagnostics test, sir.")

    test_helpers()
    test_system_control()
    test_web_automation()
    test_wikipedia()
    test_news()
    test_dictionary()
    test_file_manager()
    test_intent_recognition()
    test_ai_intent()
    test_gmail_service()
    test_youtube()

    speak("All modules have been tested successfully.")
    print("\n✅ JARVIS SYSTEM TEST COMPLETED SUCCESSFULLY ✅")


if __name__ == "__main__":
    try:
        full_test()
    except KeyboardInterrupt:
        speak("Test interrupted by user.")
        print("\n❌ Test manually stopped.")
    except Exception as e:
        speak("Critical error encountered.")
        print(f"\n❌ Unexpected Error: {e}")
