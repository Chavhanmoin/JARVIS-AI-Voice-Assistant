import os
import json
import pyttsx3
import pyautogui
import psutil
import requests
import geocoder
import pyjokes
import random
import re
import datetime
import speech_recognition as sr
from difflib import get_close_matches
from dotenv import load_dotenv
import webbrowser
import urllib.parse

# ===========================================
# 🌍 Environment Setup
# ===========================================
load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ===========================================
# 🗣️ Text-to-Speech Engine
# ===========================================
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 180)
engine.setProperty("volume", 0.9)

# ===========================================
# 🧠 JARVIS Memory Cache
# ===========================================
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def load_memory():
    """Load the recent command memory from file."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_memory(memory):
    """Save the memory back to file."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-5:], f, indent=2)  # keep only last 5 commands

def remember_command(intent, details):
    """Store command intent & parameters."""
    memory = load_memory()
    memory.append({"intent": intent, "details": details, "time": datetime.datetime.now().isoformat()})
    save_memory(memory)

def recall_last_command():
    """Get the most recent command from memory."""
    memory = load_memory()
    return memory[-1] if memory else None

# ===========================================
# 🗣️ Voice Output
# ===========================================
def speak(text: str):
    """Speak text aloud using the TTS engine."""
    global engine
    if not text:
        return
    print(f"JARVIS: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[0].id)
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 0.9)
            engine.say(text)
            engine.runAndWait()
        except Exception as e2:
            print(f"❌ TTS Reinit Error: {e2}")


# ===========================================
# 💻 System Information
# ===========================================
def cpu():
    """Announce CPU and battery status."""
    try:
        usage = psutil.cpu_percent(interval=1)
        speak(f"CPU is at {usage} percent.")
    except Exception:
        pass

    try:
        battery = psutil.sensors_battery()
        if battery:
            plugged = "charging" if battery.power_plugged else "not charging"
            speak(f"Battery is at {battery.percent} percent and {plugged}.")
    except Exception:
        pass


# ===========================================
# 📸 Screenshot
# ===========================================
def screenshot():
    """Take a screenshot and save to user's Pictures folder."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_path = os.path.expanduser(f"~/Pictures/Screenshots/screenshot_{timestamp}.png")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        pyautogui.screenshot().save(save_path)
        speak("Screenshot taken and saved successfully.")
    except Exception:
        speak("Sorry, I couldn't take a screenshot.")


# ===========================================
# 😂 Safe Jokes
# ===========================================
SAFE_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why do Java developers wear glasses? Because they don’t C sharp.",
    "A SQL query walks into a bar and asks — 'Can I join you?'",
    "Debugging is like being the detective in a crime movie where you’re also the murderer.",
    "Why do programmers hate nature? It has too many bugs."
]

def joke():
    """Tell a random safe joke."""
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any?type=single", timeout=5)
        if res.status_code == 200:
            j = res.json().get("joke", "")
            speak(j)
            return
        speak(random.choice(SAFE_JOKES))
    except:
        speak(random.choice(SAFE_JOKES))


# ===========================================
# 🌦️ Weather
# ===========================================
def weather():
    """Fetch and speak live weather."""
    location = "Wardha"
    try:
        if WEATHER_API_KEY:
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
            res = requests.get(url, timeout=5)
            
            if res.status_code == 200:
                data = res.json()
                temp = int(data["current"]["temp_c"])
                desc = data["current"]["condition"]["text"]
                speak(f"Currently in {location}, it's {desc} with a temperature of {temp} degrees celsius.")
                return
        
        speak(f"The weather in {location} is pleasant today.")
        
    except Exception:
        speak(f"The weather in {location} is pleasant today.")





# ===========================================
# 🎧 Voice Recognition
# ===========================================
def takeCommand() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:  # Always use Windows default microphone
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
    try:
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"Command: {query}")
        return query.lower()
    except:
        return ""
