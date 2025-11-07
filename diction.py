import json
from difflib import get_close_matches
import pyttsx3
import speech_recognition as sr
import os

# ===============================
# Initialize Dictionary Data
# ===============================
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")

try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"⚠️ Failed to load dictionary data: {e}")
    data = {}

# ===============================
# Initialize Text-to-Speech Engine
# ===============================
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)


def speak(text: str):
    """Speak the given text aloud."""
    print(f"🗣️ {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")


def takeCommand(timeout=5, phrase_limit=7) -> str:
    """Capture voice input and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"✅ Heard: {query}")
            return query.lower().strip()
        except sr.WaitTimeoutError:
            print("⏳ Listening timed out.")
        except sr.UnknownValueError:
            print("🤔 Could not understand audio.")
        except Exception as e:
            print(f"🎧 Recognition error: {e}")
    return ""


def translate(word: str):
    """Find the meaning of a word or suggest similar words."""
    word = word.lower().strip()

    if not data:
        speak("Sorry, dictionary data is unavailable.")
        return "Dictionary not loaded."

    # Exact match
    if word in data:
        meaning = data[word]
        speak(meaning)
        return meaning

    # Suggest closest word
    matches = get_close_matches(word, data.keys(), n=3, cutoff=0.75)
    if matches:
        suggestion = matches[0]
        speak(f"Did you mean {suggestion}? Please say Yes or No.")
        answer = takeCommand()

        if "yes" in answer:
            meaning = data[suggestion]
            speak(meaning)
            return meaning
        elif "no" in answer:
            speak("Okay, the word doesn't exist.")
            return "No match found."
        else:
            speak("I didn’t understand your response.")
            return "Response unclear."
    else:
        speak("Sorry, I couldn’t find that word.")
        return "No word found."


# ===============================
# Standalone Test Mode
# ===============================
if __name__ == "__main__":
    speak("Please tell me a word to search in the dictionary.")
    user_word = takeCommand()
    if user_word:
        translate(user_word)
    else:
        speak("No input detected. Exiting dictionary mode.")
