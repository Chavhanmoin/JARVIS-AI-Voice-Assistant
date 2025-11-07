import os
import json
import pyttsx3
import pyautogui
import psutil
import requests
import geocoder
import pyjokes
import subprocess
import random
import re
import speech_recognition as sr
from difflib import get_close_matches
from dotenv import load_dotenv

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
# 📚 Local Dictionary Data (✅ Fixed Path)
# ===========================================
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")

try:
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    data = {}
    print(f"⚠️ Could not load dictionary data.json from {DATA_PATH}: {e}")

# ===========================================
# 💻 App Aliases (Windows)
# ===========================================
APP_ALIASES = {
    "chrome": "chrome.exe",
    "spotify": "spotify.exe",
    "notepad": "notepad.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "vs code": "Code.exe",
    "vlc": "vlc.exe",
    "telegram": "Telegram.exe",
    "zoom": "Zoom.exe",
    "cmd": "cmd.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe"
}

# ===========================================
# 🗣️ Voice Output
# ===========================================
def speak(text: str):
    """Speak text aloud using the TTS engine."""
    if not text:
        return
    print(f"🗣️ JARVIS: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ TTS Error: {e}")

# ===========================================
# 📸 Screenshot
# ===========================================
def screenshot():
    """Take a screenshot and save to user's Pictures folder."""
    try:
        save_path = os.path.expanduser("~/Pictures/Screenshots/screenshot.png")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        pyautogui.screenshot().save(save_path)
        speak("Screenshot taken and saved successfully.")
    except Exception as e:
        print(f"📸 Screenshot Error: {e}")
        speak("Sorry, I couldn't take a screenshot.")

# ===========================================
# 💻 System Information
# ===========================================
def cpu():
    """Announce CPU and battery status."""
    try:
        usage = psutil.cpu_percent(interval=1)
        speak(f"CPU is at {usage} percent.")
    except Exception as e:
        print(f"⚙️ CPU Info Error: {e}")

    try:
        battery = psutil.sensors_battery()
        if battery:
            speak(f"Battery is at {battery.percent} percent.")
        else:
            speak("Battery information is not available.")
    except Exception as e:
        print(f"🔋 Battery Info Error: {e}")

# ===========================================
# 😂 SAFE JOKE SYSTEM (Filtered & Random)
# ===========================================
last_joke = None

# Blacklist patterns for filtering bad jokes
BLACKLIST_PATTERNS = [
    r"\bkill\b", r"\bshoot\b", r"\bgun\b", r"\bmurder\b", r"\bterror\b",
    r"\brape\b", r"\bsex\b", r"\bsexual\b", r"\bmolest\b", r"\bminor\b",
    r"\bchildren\b", r"\bpedophile\b", r"\bbaby\b", r"\bviolence\b",
    r"\bweapon\b", r"\bsuicide\b", r"\bterrorist\b"
]
COMPILED_BLACKLIST = [re.compile(p, re.IGNORECASE) for p in BLACKLIST_PATTERNS]

SAFE_FALLBACK_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why do Java developers wear glasses? Because they don't C sharp.",
    "A SQL query walks into a bar and says, 'Can I join you?'",
    "Debugging is like being the detective in a crime movie where you're also the murderer.",
    "Why do programmers hate nature? It has too many bugs.",
    "What's a programmer's favorite hangout place? The Foo Bar."
]

def is_safe_joke(text: str) -> bool:
    """Check if joke is safe to say."""
    if not text or len(text) < 10:
        return False
    for pat in COMPILED_BLACKLIST:
        if pat.search(text):
            print(f"[FILTERED JOKE] Blocked joke: {text[:50]}...")
            return False
    return True

def joke():
    """Tell a safe, filtered random joke each time."""
    global last_joke
    try:
        # Try online joke API first
        for _ in range(3):
            res = requests.get("https://v2.jokeapi.dev/joke/Any?type=single", timeout=5)
            if res.status_code == 200:
                new_joke = res.json().get("joke", "")
                if new_joke and is_safe_joke(new_joke) and new_joke != last_joke:
                    last_joke = new_joke
                    speak(new_joke)
                    return

        # Fallback to pyjokes
        new_joke = pyjokes.get_joke(language="en", category="neutral")
        if not is_safe_joke(new_joke) or new_joke == last_joke:
            new_joke = random.choice(SAFE_FALLBACK_JOKES)
        last_joke = new_joke
        speak(new_joke)

    except Exception as e:
        print(f"😂 Joke Error: {e}")
        # Offline safe fallback
        safe = random.choice([j for j in SAFE_FALLBACK_JOKES if j != last_joke])
        last_joke = safe
        speak(safe)

# ===========================================
# 🎧 Voice Recognition
# ===========================================
def takeCommand() -> str:
    """Capture and recognize voice commands."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 400
    recognizer.pause_threshold = 1.2

    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""

    try:
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"✅ You said: {query}")
        return query.lower().strip()
    except sr.UnknownValueError:
        print("🤔 Could not understand speech.")
        return ""
    except sr.RequestError:
        print("🌐 Speech service unavailable.")
        return ""
    except Exception as e:
        print(f"🎧 Recognition Error: {e}")
        return ""

# ===========================================
# 🌦️ Dynamic Weather (Auto-location, Fixed)
# ===========================================
def weather():
    """Fetch and speak live weather using WorldWeatherOnline API (safe fallback)."""
    if not WEATHER_API_KEY:
        speak("Weather API key is missing.")
        return

    try:
        g = geocoder.ip("me")
        location = g.city or "Wardha"

        url = (
            f"http://api.worldweatheronline.com/premium/v1/weather.ashx"
            f"?key={WEATHER_API_KEY}&q={location}&format=json&num_of_days=1"
        )
        res = requests.get(url, timeout=5)
        data = res.json()

        current = data.get("data", {}).get("current_condition", [{}])[0]
        if not current:
            current = data.get("data", {}).get("weather", [{}])[0]

        temp_c = current.get("temp_C", "N/A")
        desc = current.get("weatherDesc", [{"value": "Unavailable"}])[0]["value"]
        wind = current.get("windspeedKmph", "N/A")
        humidity = current.get("humidity", "N/A")

        weather_text = (
            f"Currently in {location}, it is {desc.lower()}, "
            f"temperature is {temp_c} degrees Celsius, "
            f"humidity around {humidity} percent, "
            f"and wind speed is {wind} kilometers per hour."
        )

        speak(weather_text)
        print(f"🌤️ {weather_text}")

    except Exception as e:
        print(f"🌦️ Weather Error: {e}")
        speak("Sorry, I couldn't fetch the weather details right now.")

# ===========================================
# 📖 Dictionary / Translation
# ===========================================
def translate(word: str):
    """Translate or define a word from local data.json."""
    if not word:
        speak("Please say a word to search.")
        return
    if not data:
        speak("Dictionary data is missing.")
        return

    word = word.lower()
    if word in data:
        speak(data[word])
    elif matches := get_close_matches(word, data.keys()):
        suggestion = matches[0]
        speak(f"Did you mean {suggestion}? Please say Yes or No.")
        response = takeCommand()
        if "yes" in response:
            speak(data[suggestion])
        else:
            speak("Okay, word not found.")
    else:
        speak("Sorry, that word is not in my dictionary.")

# ===========================================
# 💾 Application Management
# ===========================================
def resolve_app_name(name: str) -> str:
    """Map spoken app name to its .exe equivalent."""
    return APP_ALIASES.get(name.lower(), name + ".exe")

def open_app(app_name: str):
    """Open any installed application."""
    try:
        resolved = resolve_app_name(app_name)
        subprocess.Popen(resolved, shell=True)
        speak(f"Opening {app_name}")
    except Exception as e:
        print(f"🚫 Open App Error: {e}")
        speak(f"Sorry, I couldn't open {app_name}.")

def close_app(app_name: str):
    """Close any running application."""
    resolved = resolve_app_name(app_name)
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if resolved.lower() in proc.info["name"].lower():
                proc.kill()
                speak(f"{app_name} has been closed.")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    speak(f"{app_name} is not running.")
