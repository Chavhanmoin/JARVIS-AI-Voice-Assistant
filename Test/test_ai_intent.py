import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ai_intent_recognition import get_ai_intent

print("\n=== 🧠 TESTING AI INTENT MODULE ===")

queries = [
    "open youtube and search relaxing music",
    "compose email to manager about project deadline",
    "close chrome",
]

for q in queries:
    print(f"\nUser: {q}")
    print(get_ai_intent(q))
    time.sleep(2)

print("✅ AI intent recognition test completed.")
