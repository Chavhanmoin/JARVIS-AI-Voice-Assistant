import os
import sys
import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser
import smtplib
from sys import platform
from dotenv import load_dotenv

# === Local Modules ===
from helpers import cpu, weather, joke, screenshot
from youtube import youtube
from news import speak_news, getNewsUrl
from diction import translate
from system_control import open_anything, close_anything, execute_system_command
from web_automation import (
    search_google, search_youtube,
    send_whatsapp_message, compose_gmail, close_web_automation
)
from wikipedia_search import search_and_open_wikipedia
from file_manager import (
    create_file, create_folder, open_file, open_folder,
    delete_file, delete_folder, copy_file, move_file, list_files
)
from ai_intent_recognition import get_ai_intent

# === Load .env file ===
load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# === Initialize TTS engine ===
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text: str):
    """Speaks the given text using pyttsx3."""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()


def takeCommand() -> str:
    """Listens to user's command and returns recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        audio = recognizer.listen(source, phrase_time_limit=7)

    try:
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"🗣️ User: {query}")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        print("Speech recognition service error.")
        return ""
    except Exception as e:
        print(f"Recognition Error: {e}")
        return ""


class Jarvis:
    def __init__(self):
        # Setup Chrome path based on OS
        if platform == "win32":
            self.chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        elif platform == "darwin":
            self.chrome_path = "open -a /Applications/Google\\ Chrome.app"
        elif "linux" in platform:
            self.chrome_path = "/usr/bin/google-chrome"
        else:
            print("❌ Unsupported OS")
            sys.exit(1)

        try:
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))
        except:
            pass  # fallback to default browser

    def wishMe(self):
        """Greets the user and gives system status."""
        hour = datetime.datetime.now().hour
        greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
        speak(f"{greeting} Sir. I am JARVIS, ready for your commands.")
        cpu()
        weather()

    def sendEmail(self, to: str, content: str):
        """Sends an email using SMTP."""
        if not EMAIL or not PASSWORD:
            speak("Email credentials missing in .env file.")
            return

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.sendmail(EMAIL, to, content)
            speak("Email sent successfully!")
        except Exception as e:
            print("Email error:", e)
            speak("Sorry sir, I couldn't send the email.")

    def handle_simple_commands(self, query: str):
        """Handles common direct commands."""
        query = query.lower()

        if "wikipedia" in query:
            search_and_open_wikipedia(query)

        elif "youtube" in query and "search" in query:
            term = query.replace("youtube", "").replace("search", "").strip()
            if term:
                youtube(term)
                speak(f"Searching YouTube for {term}")
            else:
                speak("What should I search on YouTube?")
                youtube(takeCommand())

        elif "open" in query:
            site = query.replace("open", "").strip()
            urls = {
                "youtube": "https://youtube.com",
                "google": "https://google.com",
                "amazon": "https://amazon.in",
                "stackoverflow": "https://stackoverflow.com",
                "github": "https://github.com"
            }
            if site in urls:
                webbrowser.get("chrome").open(urls[site])
                speak(f"Opening {site}")
            else:
                open_anything(site)

        elif "close" in query:
            item = query.replace("close", "").strip()
            result = close_anything(item)
            speak(result)

        elif "time" in query:
            speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")

        elif "joke" in query:
            joke()

        elif "screenshot" in query:
            speak("Taking screenshot")
            screenshot()

        elif "shutdown" in query:
            speak("Shutting down your system")
            os.system("shutdown /p /f" if platform == "win32" else "poweroff")

        elif any(word in query for word in ["exit", "sleep", "quit", "goodbye"]):
            try:
                close_web_automation()
            except:
                pass
            speak("Goodbye Sir, powering down JARVIS.")
            os._exit(0)

    def execute_query(self, query: str):
        """Routes command to appropriate handler (AI or direct)."""
        if not query:
            return

        # Try AI-based intent recognition first
        try:
            ai_intent = get_ai_intent(query)
            if ai_intent and ai_intent.get("confidence", 0) > 0.5:
                self.handle_ai_intent(ai_intent)
                return
        except Exception as e:
            print(f"AI intent error: {e}")

        # If not recognized by AI, fallback to direct commands
        self.handle_simple_commands(query)

    def handle_ai_intent(self, ai_intent):
        """Executes commands identified by AI model."""
        intent = ai_intent.get("intent", "")
        entities = ai_intent.get("entities", {})

        if intent == "search_google":
            query = entities.get("query", "")
            if query:
                search_google(query)
                speak(f"Searching Google for {query}")
        elif intent == "search_youtube":
            query = entities.get("query", "")
            if query:
                youtube(query)
                speak(f"Opening YouTube for {query}")
        elif intent in ["open_app", "open"]:
            app = entities.get("app", "")
            open_anything(app)
        elif intent in ["close_app", "close"]:
            app = entities.get("app", "")
            close_anything(app)
        elif intent in ["system_info", "cpu"]:
            cpu()
        elif intent in ["weather", "get_weather"]:
            weather()
        elif intent in ["joke"]:
            joke()
        else:
            speak("Sorry, I couldn't understand that intent.")


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.wishMe()

    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("🎧 Listening for wake word 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = recognizer.listen(source, phrase_time_limit=5)

            wake = recognizer.recognize_google(audio, language="en-in").lower()
            if "jarvis" in wake:
                speak("Yes Sir?")
                command = takeCommand().lower()
                jarvis.execute_query(command)

        except sr.UnknownValueError:
            continue
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
