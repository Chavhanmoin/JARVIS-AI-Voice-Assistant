import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from web_automation import search_google, search_youtube, send_whatsapp_message, close_web_automation

print("\n=== 🌐 TESTING WEB AUTOMATION MODULE ===\n")

# ---------------------------------------------------
# Google Search Test
# ---------------------------------------------------
print("🔹 Testing Google Search...")
result = search_google("Latest AI tools 2025")
print(result)
time.sleep(5)

# ---------------------------------------------------
# YouTube Search Test
# ---------------------------------------------------
print("\n🔹 Testing YouTube Search...")
result = search_youtube("AI music videos")
print(result)
time.sleep(10)

# ---------------------------------------------------
# WhatsApp Test
# ---------------------------------------------------
print("\n🔹 Testing WhatsApp Message Sending...")
print("⚠️ Make sure WhatsApp Web is logged in before running this test!")
result = send_whatsapp_message("Test Contact", "Hello from Jarvis Automation!")
print(result)

# ---------------------------------------------------
# Close Browser
# ---------------------------------------------------
print("\n🔹 Closing Browser...")
close_web_automation()

print("\n✅ WEB AUTOMATION MODULE TEST COMPLETED SUCCESSFULLY!\n")
