from jarvis import Jarvis
from helpers import speak
import sys

def main():
    """Simple JARVIS without voice recognition issues"""
    
    print("🤖 JARVIS - Simple Mode")
    print("Type commands directly")
    print("Type 'voice' to try voice mode")
    print("Type 'exit' to quit")
    print("=" * 30)
    
    bot = Jarvis()
    bot.wishMe()
    
    while True:
        try:
            choice = input("\n💬 Command or 'voice': ").strip().lower()
            
            if choice in ['exit', 'quit', 'bye']:
                speak("Goodbye Sir")
                break
            
            elif choice == 'voice':
                try_voice_mode(bot)
            
            elif choice:
                print(f"🎯 Executing: {choice}")
                bot.execute_query(choice)
            
        except KeyboardInterrupt:
            speak("Goodbye Sir")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def try_voice_mode(bot):
    """Try voice mode with timeout"""
    import speech_recognition as sr
    
    print("\n🎤 Voice Mode - Say something (10 second timeout)")
    
    try:
        r = sr.Recognizer()
        r.energy_threshold = 1000
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("👂 Listening...")
            
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
            command = r.recognize_google(audio, language='en-US')
            
            print(f"🗣️ You said: {command}")
            bot.execute_query(command.lower())
            
    except sr.WaitTimeoutError:
        print("⏰ Timeout - no speech detected")
    except sr.UnknownValueError:
        print("❓ Could not understand speech")
    except Exception as e:
        print(f"🎤 Voice error: {e}")
    
    print("🔙 Back to text mode")

if __name__ == "__main__":
    main()