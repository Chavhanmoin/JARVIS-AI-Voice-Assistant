import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from news import speak_news

print("\n=== 📰 TESTING NEWS MODULE ===")
speak_news()
print("✅ News module test completed.")
