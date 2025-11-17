import os
import pickle
import webbrowser
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from helpers import speak
from dateutil import parser

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'calendar_token.pickle'
CHROME_EXECUTABLE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def get_calendar_service():
    """Get authenticated Google Calendar service"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                speak("Calendar credentials not found. Please add credentials.json file.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def create_calendar_event(title, date_str, time_str="", description=""):
    """Create Google Calendar event directly"""
    try:
        service = get_calendar_service()
        if not service:
            return False
        
        # Parse date dynamically
        import re
        from dateutil import parser
        
        try:
            # Try to parse the date string directly
            event_date = parser.parse(date_str, fuzzy=True)
            
            # If parsed date is in the past, move to next year
            if event_date.date() < datetime.now().date():
                event_date = event_date.replace(year=event_date.year + 1)
                
        except:
            # Fallback manual parsing
            year = datetime.now().year
            current_date = datetime.now()
            
            day_match = re.search(r'(\d+)', date_str)
            day = int(day_match.group(1)) if day_match else current_date.day
            
            months = {
                'jan': 1, 'january': 1, 'feb': 2, 'february': 2,
                'mar': 3, 'march': 3, 'apr': 4, 'april': 4,
                'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
                'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
                'oct': 10, 'october': 10, 'nov': 11, 'november': 11,
                'dec': 12, 'december': 12
            }
            
            month = current_date.month
            for month_name, month_num in months.items():
                if month_name in date_str.lower():
                    month = month_num
                    break
            
            # Create date and check if it's in the past
            event_date = datetime(year, month, day)
            if event_date.date() < current_date.date():
                event_date = event_date.replace(year=year + 1)
        
        # Parse time
        if time_str:
            import re
            time_match = re.search(r'(\d+):(\d+)', time_str)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
            else:
                hour_match = re.search(r'(\d+)', time_str)
                hour = int(hour_match.group(1)) if hour_match else 14
                minute = 0
            
            # Convert to 24-hour format
            if "p.m" in time_str.lower() or "pm" in time_str.lower():
                if hour != 12:
                    hour += 12
            elif "a.m" in time_str.lower() or "am" in time_str.lower():
                if hour == 12:
                    hour = 0
            
            event_date = event_date.replace(hour=hour, minute=minute)
        else:
            event_date = event_date.replace(hour=14, minute=0)
        
        # Create event
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': event_date.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': (event_date + timedelta(hours=1)).isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
        }
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        
        # Open Google Calendar with Chrome profile
        import subprocess
        subprocess.Popen([CHROME_EXECUTABLE, '--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data', '--profile-directory=Default', 'https://calendar.google.com'])
        
        formatted_date = event_date.strftime("%B %d, %Y")
        speak(f"Meeting scheduled successfully for {formatted_date} at {time_str}" if time_str else f"Meeting scheduled successfully for {formatted_date}")
        return True
        
    except Exception as e:
        speak("Failed to create calendar event")
        print(f"Calendar error: {e}")
        return False