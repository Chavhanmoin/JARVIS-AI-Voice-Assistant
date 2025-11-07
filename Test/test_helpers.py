import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from helpers import speak, cpu, joke, weather, translate

print("\n=== 🧠 TESTING HELPERS MODULE ===")
speak("Testing my speaking ability.")
cpu()
joke()
weather()
translate("computer")
time.sleep(1)
print("✅ Helpers module test completed.")
