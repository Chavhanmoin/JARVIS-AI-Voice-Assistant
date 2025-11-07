from jarvis import Jarvis
from helpers import takeCommand, speak
import sys

def simple_jarvis():
    """Simple JARVIS without wake word - just continuous listening"""
    
    print("🤖 JARVIS Simple Mode")
    print("Type 'exit' to quit")
    print("=" * 30)
    
    bot = Jarvis()
    bot.wishMe()
    
    while True:
        try:
            # Get command via keyboard input
            command = input("\n💬 Enter command (or 'exit'): ").strip()
            
            if command.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                speak("Goodbye Sir, shutting down JARVIS")
                break
            
            if command:
                print(f"🎯 Executing: {command}")
                bot.execute_query(command.lower())
            
        except KeyboardInterrupt:
            speak("Goodbye Sir, shutting down JARVIS")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_jarvis()