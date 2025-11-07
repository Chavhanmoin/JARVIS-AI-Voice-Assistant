import os
import json
import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import requests
import geocoder
import subprocess
from difflib import get_close_matches
from dotenv import load_dotenv

# Load environment variables (especially the weather API key)
# Adjust the path to your .env location if needed
load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Initialize enhanced TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# Optimize TTS settings
engine.setProperty('rate', 180)  # Slightly faster speech
engine.setProperty('volume', 0.9)  # High volume

# Geolocation for weather
g = geocoder.ip('me')

# Dictionary (for translate) data
try:
    data = json.load(open('data.json'))
except Exception as e:
    data = {}
    print("Could not load data.json:", e)

# App aliases (for Windows .exe names)
app_aliases = {
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

def speak(audio) -> None:
    """Speak out the given text via TTS."""
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")
        print(f"Speaking: {audio}")

def screenshot() -> None:
    """Take a screenshot and save to a predefined folder."""
    try:
        img = pyautogui.screenshot()
        save_path = r'C:\Users\Admin\Pictures\Screenshots\screenshot.png'  # Change path as needed
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img.save(save_path)
        speak("Screenshot taken and saved.")
    except Exception as e:
        print("Error saving screenshot:", e)
        speak("Sorry, I could not take screenshot.")

def cpu() -> None:
    """Report CPU usage and battery status."""
    try:
        usage = psutil.cpu_percent()
        speak("CPU is at " + str(usage) + " percent.")
    except Exception as e:
        print("CPU error:", e)

    try:
        battery = psutil.sensors_battery()
        if battery:
            speak("Battery is at " + str(battery.percent) + " percent.")
        else:
            speak("Battery information is not available.")
    except Exception as e:
        print("Battery error:", e)

def joke() -> None:
    """Tell a few jokes (limited)."""
    try:
        jokes = pyjokes.get_jokes()
        for i in range(min(5, len(jokes))):
            speak(jokes[i])
    except Exception as e:
        print("Joke error:", e)

def takeCommand() -> str:
    """Adaptive speech recognition"""
    r = sr.Recognizer()
    r.energy_threshold = 3000
    r.pause_threshold = 1.5  # Wait 1.5 seconds of silence
    
    with sr.Microphone( ) as source:
        print('🎤 Listening...')
        r.adjust_for_ambient_noise(source, duration=0.3)
        
        try:
            # Listen with adaptive timeout - extends if user keeps speaking
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return 'None'
    
    try:
        query = r.recognize_google(audio, language='en-in')
        if query and query.strip():
            print(f'✅ User said: {query}')
            return query.strip().lower()
        else:
            return 'None'
    except Exception as e:
        print(f'❌ Recognition failed: {e}')
        return 'None'

def weather():
    """Fetch weather data using the World Weather Online API and speak it."""
    if not WEATHER_API_KEY:
        speak("Weather API key is not set.")
        return

    try:
        # Use Wardha as default location (your actual location)
        location = "Wardha"
        api_url = (
            f"http://api.worldweatheronline.com/premium/v1/weather.ashx"
            f"?key={WEATHER_API_KEY}&q={location}&format=json&num_of_days=1"
        )
        res = requests.get(api_url)
        data = res.json()

        current = data['data']['current_condition'][0]
        temp_c = current['temp_C']
        wind = current['windspeedKmph']
        humidity = current['humidity']
        description = current['weatherDesc'][0]['value']

        speak(f"Current weather in {location}")
        speak(f"Condition: {description}")
        speak(f"Temperature: {temp_c} degrees Celsius")
        speak(f"Wind Speed: {wind} kilometers per hour")
        speak(f"Humidity: {humidity} percent")
    except Exception as e:
        print("Weather fetch error:", e)
        speak("Sorry, I couldn't fetch weather information right now.")

def translate(word: str):
    """Translate or define the word (using a loaded dictionary)."""
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x + ' instead? Respond Yes or No.')
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please check your spelling.")
        else:
            speak("I didn't understand your response.")
    else:
        speak("Word doesn't exist in the dictionary.")

def resolve_app_name(name: str) -> str:
    """Convert a voice-given name to the real executable name."""
    return app_aliases.get(name.lower(), name + ".exe")

def open_app(app_name: str):
    """Open an application by name."""
    try:
        resolved = resolve_app_name(app_name)
        subprocess.Popen(resolved)
        speak(f"Opening {app_name}")
    except Exception as e:
        print("Error opening app:", e)
        speak(f"Sorry, I couldn't open {app_name}")

def close_app(app_name: str):
    """Close a running application by killing its process."""
    resolved = resolve_app_name(app_name)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if resolved.lower() in proc.info['name'].lower():
                proc.kill()
                speak(f"{app_name} has been closed.")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    speak(f"{app_name} is not running.")
