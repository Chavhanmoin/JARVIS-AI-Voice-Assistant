# test_jarvis_all.py

import datetime
import traceback
from helpers import speak, screenshot, cpu, joke, weather, translate
from system_control import open_anything, close_anything, execute_system_command
from web_automation import search_google, search_youtube
from intent_recognition import process_user_intent
from ai_intent_recognition import get_ai_intent

import time

# Separator line for visual clarity
SEPARATOR = "-" * 70

# Collect test results
test_results = []

def log_test(name, func, *args, **kwargs):
    """Runs a test, logs result, and catches errors"""
    print(f"\n{SEPARATOR}")
    print(f"🧪 TESTING: {name}")
    print(SEPARATOR)
    try:
        result = func(*args, **kwargs)
        print(f"✅ OUTPUT:\n{result if result is not None else '[NO RETURN VALUE]'}")
        test_results.append((name, "PASS", ""))
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"❌ ERROR:\n{error_msg}")
        test_results.append((name, "FAIL", error_msg))


def test_all_functions():
    # Voice
    log_test("Voice Output", speak, "This is a test of JARVIS speaking system.")

    # Screenshot
    log_test("Screenshot Capture", screenshot)

    # CPU Info
    log_test("System CPU & Battery Info", cpu)

    # Joke Telling
    log_test("Joke Function", joke)

    # Weather
    log_test("Weather Info", weather)

    # Translation / Dictionary
    log_test("Translate Word", translate, "artificial")

    # App Opening
    log_test("Open Application (Notepad)", open_anything, "notepad")
    time.sleep(2)

    # App Closing
    log_test("Close Application (Notepad)", close_anything, "notepad")
    time.sleep(1)

    # Execute System Command
    log_test("Execute System Command", execute_system_command, "echo Hello from JARVIS")

    # Google Search
    log_test("Google Search", search_google, "Elon Musk")

    # YouTube Search
    log_test("YouTube Search", search_youtube, "Avengers Trailer")

    # Rule-based Intent Recognition
    log_test("Rule-based Intent Recognition", process_user_intent, "Open Chrome browser")

    # AI-based Intent Recognition
    log_test("AI-based Intent Recognition", get_ai_intent, "Search YouTube for Iron Man trailer")

    # Time Query
    log_test("Get Current Time", lambda: speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}"))


def display_summary():
    print(f"\n\n{SEPARATOR}")
    print("📝 JARVIS FUNCTIONALITY TEST REPORT")
    print(SEPARATOR)

    for idx, (name, status, error) in enumerate(test_results, 1):
        print(f"{idx:02d}. {name}: {'✅ PASS' if status == 'PASS' else '❌ FAIL'}")
        if status == "FAIL":
            print("    → Error Summary:")
            print("    " + error.strip().splitlines()[-1])  # Show last error line

    print(f"\nTotal Tests: {len(test_results)}")
    passed = sum(1 for _, s, _ in test_results if s == "PASS")
    failed = len(test_results) - passed
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(SEPARATOR)


if __name__ == "__main__":
    print(f"\n🔧 Starting full diagnostic test of J.A.R.V.I.S system...\n")
    test_all_functions()
    display_summary()
    speak("JARVIS testing complete.")
