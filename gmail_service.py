import os
import base64
import urllib.parse
import subprocess
import webbrowser
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from helpers import speak

# ==========================================
# 🔹 Gmail API Setup
# ==========================================
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly"
]

# ==========================================
# 📁 Root Path Detection
# ==========================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = CURRENT_DIR
while ROOT_DIR != os.path.dirname(ROOT_DIR):
    if os.path.exists(os.path.join(ROOT_DIR, "credentials.json")) or os.path.exists(os.path.join(ROOT_DIR, ".env")):
        break
    ROOT_DIR = os.path.dirname(ROOT_DIR)

CREDENTIALS_FILE = os.path.join(ROOT_DIR, "credentials.json")
TOKEN_FILE = os.path.join(ROOT_DIR, "token.json")

print(f"[INFO] Credentials path: {CREDENTIALS_FILE}")
print(f"[INFO] Token path: {TOKEN_FILE}")

CHROME_EXECUTABLE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ==========================================
# 🔹 Gmail Service Initialization
# ==========================================
def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None
    try:
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                print("🔄 Gmail token refreshed successfully.")
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError("⚠️ credentials.json missing!")

                print("🌐 Launching Chrome for Gmail authentication...")
                subprocess.Popen([
                    CHROME_EXECUTABLE,
                    "--profile-directory=Default",
                    "--new-window",
                    "https://accounts.google.com/"
                ])

                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
                print(f"💾 Token saved at: {TOKEN_FILE}")

        service = build("gmail", "v1", credentials=creds)
        print("✅ Gmail API service initialized successfully.")
        return service

    except Exception as e:
        print(f"❌ Gmail service initialization failed: {e}")
        speak("I couldn't connect to Gmail. Please reauthenticate.")
        return None

# ==========================================
# ✉️ Gmail Compose (Opens Chrome)
# ==========================================
def send_gmail_api(to_email: str, subject: str, body: str, send_now: bool = True) -> str:
    """
    Opens Gmail in Chrome with subject, body, and salutation pre-filled.
    Leaves recipient blank for manual review.
    """
    try:
        # Ensure service is connected
        service = get_gmail_service()
        if not service:
            return "❌ Gmail service not available."

        # Add professional format to email
        email_body = f"Dear Sir/Madam,\n\n{body}\n\nBest regards,\nMoin Raju Chavhan"

        encoded_subject = urllib.parse.quote(subject)
        encoded_body = urllib.parse.quote(email_body)

        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_body}"

        # Open Gmail Compose window in Chrome
        webbrowser.register(
            "chrome",
            None,
            webbrowser.BackgroundBrowser(CHROME_EXECUTABLE)
        )
        webbrowser.get("chrome").open_new_tab(gmail_url)

        speak("Opening Gmail compose window for you to review and send.")
        print(f"📧 Gmail compose window opened with subject: '{subject}'")

        return f"📝 Gmail compose window opened with subject '{subject}' and body pre-filled."

    except Exception as e:
        speak("Sorry, I couldn't open Gmail compose window.")
        return f"❌ Gmail compose error: {e}"

# ==========================================
# 🔍 Check Gmail Connection
# ==========================================
def check_gmail_connection() -> str:
    try:
        service = get_gmail_service()
        if not service:
            return "❌ Gmail not connected."
        profile = service.users().getProfile(userId="me").execute()
        email = profile.get("emailAddress", "Unknown")
        speak("Gmail is connected successfully.")
        return f"✅ Gmail connected for: {email}"
    except Exception as e:
        return f"⚠️ Gmail connection failed: {e}"

# ==========================================
# 🧪 Test Run
# ==========================================
if __name__ == "__main__":
    print("\n=== 📧 TESTING GMAIL SERVICE MODULE ===")
    connection = check_gmail_connection()
    print(connection)

    if "✅" in connection:
        response = send_gmail_api("", "Jarvis Test Email", "This is a test message generated by Jarvis AI.")
        print(response)
    print("✅ Gmail service test completed.")
