import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from gmail_service import send_gmail_api

print("\n=== 📧 TESTING GMAIL SERVICE MODULE ===")
print(send_gmail_api("", "Jarvis API Test", "This is a test draft email from Jarvis AI."))
print("✅ Gmail service test completed.")
