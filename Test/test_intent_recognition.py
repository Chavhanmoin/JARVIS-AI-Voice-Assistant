import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from intent_recognition import process_user_intent

print("\n=== ⚙️ TESTING RULE-BASED INTENT RECOGNITION MODULE ===")

queries = [
    "open notepad",
    "close chrome",
    "search youtube for AI songs",
    "what's the weather",
    "tell me a joke"
]

for q in queries:
    print(f"\nUser: {q}")
    print(process_user_intent(q))
    time.sleep(1)

print("✅ Rule-based intent recognition test completed.")
