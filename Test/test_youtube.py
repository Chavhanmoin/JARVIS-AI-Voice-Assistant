import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from youtube import youtube

print("\n=== 🎥 TESTING YOUTUBE MODULE ===")
youtube("AI short film")
print("✅ YouTube module test completed.")
