import os
import datetime
import speech_recognition as sr
from helpers import (
    speak, cpu, weather, joke, screenshot, takeCommand,
    remember_command, recall_last_command
)
from diction import translate
from news import speak_news
from system_control import open_anything as open_app_func, close_anything, execute_system_command
from file_manager import create_file, create_folder, open_file, open_folder
from web_automation import search_google, search_youtube
from gmail_service import send_gmail_api
from iot_control import control_iot_device, initialize_iot


class Jarvis:
    def __init__(self):
        speak("Jarvis system ready with memory enabled.")
        self.microphone_index = None  # Use Windows default microphone
        self.current_location = os.path.expanduser("~")  # Start at home directory
        self.get_default_microphone()

    # ==================================================
    # 🎙️ MICROPHONE SETUP
    # ==================================================
    def get_default_microphone(self):
        """Display and use Windows default microphone."""
        try:
            # Get default microphone info
            mic_list = sr.Microphone.list_microphone_names()
            default_mic = mic_list[0] if mic_list else "Unknown"
            
            # Test default microphone
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print(f"Using Windows default microphone: {default_mic}")
            speak(f"Using Windows default microphone: {default_mic}")
            return None  # None means use default
        except Exception as e:
            print(f"Microphone setup error: {e}")
            speak("Microphone setup failed. Please check your Windows audio settings.")
            return None

    # ==================================================
    # 👋 GREETING
    # ==================================================
    def wishMe(self):
        hour = datetime.datetime.now().hour
        greet = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
        speak(f"{greet}, sir. I am online and ready.")
        cpu()
        weather()

    # ==================================================
    # 🔁 REPEAT LAST COMMAND
    # ==================================================
    def repeat_last(self):
        """Repeats the last executed command."""
        last = recall_last_command()
        if not last:
            speak("I don’t remember any recent command.")
            return

        intent = last["intent"]
        details = last["details"]
        speak(f"Repeating your last command: {intent}.")
        self.route_command(intent, recall_mode=True, recall_data=details)

    # ==================================================
    # 🧭 COMMAND ROUTER
    # ==================================================
    def route_command(self, query, recall_mode=False, recall_data=None):
        """Intent-based routing with memory integration."""
        query = query.lower().strip()

        # ===== RECALL FEATURE =====
        if not recall_mode and any(word in query for word in ["repeat", "again", "do that again", "previous"]):
            self.repeat_last()
            return

        # ===== GOOGLE SEARCH =====
        elif "search" in query and "google" in query:
            search_term = query.replace("search", "").replace("google", "").replace("on", "").strip()
            speak(f"Searching Google for {search_term}")
            search_google(search_term)
            remember_command("google search", {"term": search_term})
            return

        elif "search" in query:
            search_term = query.replace("search", "").strip()
            speak(f"Searching Google for {search_term}")
            search_google(search_term)
            remember_command("google search", {"term": search_term})
            return

        # ===== GMAIL =====
        if any(word in query for word in ["email", "mail", "send mail", "send email"]):
            if not recall_mode:
                # Use AI to extract email details from the command
                from ai_intent_recognition import get_ai_intent
                ai_result = get_ai_intent(query)
                
                # Try to extract subject and body from AI
                entities = ai_result.get("entities", {})
                subject = entities.get("subject", "")
                body = entities.get("body", "")
                
                # If AI didn't extract details, ask user
                if not subject:
                    speak("What should be the subject?")
                    subject = takeCommand()
                if not body:
                    speak("What should I write in the body?")
                    body = takeCommand()
                
                remember_command("send email", {"subject": subject, "body": body})
            else:
                subject, body = recall_data["subject"], recall_data["body"]
            send_gmail_api("", subject, body, send_now=False)
            return

        # ===== YOUTUBE =====
        elif "youtube" in query or (any(word in query for word in ["play", "song", "music"]) and "open" not in query):
            topic = recall_data["topic"] if recall_mode else query.replace("youtube", "").replace("play", "").strip()
            speak(f"Playing {topic} on YouTube.")
            remember_command("youtube", {"topic": topic})
            search_youtube(topic)
            return

        # ===== NEWS =====
        elif "news" in query:
            speak_news()
            remember_command("news", {})
            return

        # ===== WEATHER =====
        elif "weather" in query:
            weather()
            remember_command("weather", {})
            return

        # ===== WIKIPEDIA =====
        elif "wikipedia" in query:
            topic = query.replace("wikipedia", "").replace("search", "").strip()
            speak(f"Searching Wikipedia for {topic}")
            import webbrowser
            webbrowser.open(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}")
            remember_command("wikipedia", {"topic": topic})
            return

        # ===== SYSTEM CONTROL =====
        elif "open" in query:
            app = query.replace("open", "").strip()
            print(f"DEBUG: Trying to open app: '{app}'")
            # Check if it's a folder location
            if app in ["downloads", "documents", "desktop", "pictures", "music", "videos"]:
                folder_path = os.path.expanduser(f"~/{app.title()}")
                self.current_location = folder_path
                open_folder(folder_path)
                speak(f"{app} folder opened.")
            else:
                print(f"DEBUG: Calling open_anything with: '{app}'")
                try:
                    result = open_app_func(app)
                    print(f"DEBUG: open_app_func returned: {result}")
                    if result and "✅" in result:
                        speak(f"{app} opened successfully.")
                    else:
                        speak(f"Could not open {app}.")
                except Exception as e:
                    print(f"ERROR calling open_app_func: {e}")
                    speak(f"Error opening {app}.")
                    import traceback
                    traceback.print_exc()
            remember_command("open", {"app": app})
            return

        elif "close" in query:
            app = query.replace("close", "").strip()
            result = close_anything(app)
            if result and "🛑" in result:
                speak(f"{app} closed successfully.")
            else:
                speak(f"{app} is not running or could not be closed.")
            remember_command("close", {"app": app})
            return

        elif "volume" in query:
            from system_control import change_volume
            if "up" in query:
                change_volume("up", 10)
            elif "down" in query:
                change_volume("down", 10)
            elif "full" in query or "max" in query:
                change_volume("set", 100)
            elif "mute" in query:
                change_volume("mute")
            elif "set" in query:
                import re
                match = re.search(r'\d+', query)
                if match:
                    volume = int(match.group())
                    change_volume("set", volume)
                else:
                    speak("Please specify a volume level.")
            remember_command("volume", {"query": query})
            return

        elif "brightness" in query:
            from system_control import change_brightness
            if "up" in query:
                change_brightness("up", 10)
            elif "down" in query:
                change_brightness("down", 10)
            elif "full" in query or "max" in query:
                change_brightness("set", 100)
            elif "set" in query:
                import re
                match = re.search(r'\d+', query)
                if match:
                    brightness = int(match.group())
                    change_brightness("set", brightness)
                else:
                    speak("Please specify a brightness level.")
            remember_command("brightness", {"query": query})
            return

        # ===== SYSTEM INFO =====
        elif "cpu" in query:
            try:
                import psutil
                usage = psutil.cpu_percent(interval=1)
                speak(f"CPU is at {usage} percent.")
            except Exception:
                speak("Unable to get CPU status.")
            remember_command("cpu", {})
            return

        elif "battery" in query:
            try:
                import psutil
                battery = psutil.sensors_battery()
                if battery:
                    plugged = "charging" if battery.power_plugged else "not charging"
                    speak(f"Battery is at {battery.percent} percent and {plugged}.")
                else:
                    speak("Battery information not available.")
            except Exception:
                speak("Unable to get battery status.")
            remember_command("battery", {})
            return

        # ===== JOKE / SCREENSHOT =====
        elif "joke" in query:
            joke()
            remember_command("joke", {})
            return

        elif "screenshot" in query:
            screenshot()
            remember_command("screenshot", {})
            return

        elif any(phrase in query for phrase in ["meaning of", "define", "what is", "what does", "explain", "tell me about", "meaning"]):
            # Extract the word/term to define
            word = ""
            if "meaning of" in query:
                word = query.split("meaning of", 1)[1].strip()
            elif "define" in query:
                word = query.replace("define", "").strip()
            elif "what is" in query:
                word = query.replace("what is", "").replace("the", "").strip()
            elif "what does" in query:
                word = query.replace("what does", "").replace("mean", "").strip()
            elif "explain" in query:
                word = query.replace("explain", "").strip()
            elif "tell me about" in query:
                word = query.replace("tell me about", "").strip()
            elif query.endswith(" meaning"):
                word = query.replace(" meaning", "").strip()
            
            if word:
                translate(word)
                remember_command("translate", {"word": word})
            else:
                speak("What would you like me to define?")
            return

        # ===== FILE MANAGEMENT =====
        elif "create" in query and "folder" in query:
            folder_name = query.replace("create", "").replace("folder", "").replace("a", "").strip()
            if not folder_name:
                speak("What should I name the folder?")
                folder_name = takeCommand()
            folder_path = os.path.join(self.current_location, folder_name)
            create_folder(folder_path)
            remember_command("create folder", {"name": folder_name, "location": self.current_location})
            return

        elif "create" in query and ("file" in query or "text" in query):
            file_name = query.replace("create", "").replace("file", "").replace("text", "").replace("a", "").strip()
            if not file_name:
                speak("What should I name the file?")
                file_name = takeCommand()
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            file_path = os.path.join(self.current_location, file_name)
            create_file(file_path)
            remember_command("create file", {"name": file_name, "location": self.current_location})
            return

        elif "delete" in query and "folder" in query:
            folder_name = query.replace("delete", "").replace("folder", "").strip()
            if not folder_name:
                speak("Which folder should I delete?")
                folder_name = takeCommand()
            folder_path = os.path.join(self.current_location, folder_name)
            from file_manager import delete_folder
            delete_folder(folder_path)
            remember_command("delete folder", {"name": folder_name})
            return

        elif "delete" in query and "file" in query:
            file_name = query.replace("delete", "").replace("file", "").strip()
            if not file_name:
                speak("Which file should I delete?")
                file_name = takeCommand()
            file_path = os.path.join(self.current_location, file_name)
            from file_manager import delete_file
            delete_file(file_path)
            remember_command("delete file", {"name": file_name})
            return

        # ===== WHATSAPP =====
        elif "whatsapp" in query and any(word in query for word in ["send", "message"]):
            try:
                print("Processing WhatsApp command...")
                from ai_intent_recognition import get_ai_intent
                from system_control import open_anything
                
                ai_result = get_ai_intent(query)
                print(f"AI result: {ai_result}")
                entities = ai_result.get("entities", {})
                
                # Extract contact and message from AI entities
                contact = entities.get("contact", entities.get("recipient", ""))
                message = entities.get("message", "")
                
                # If AI extracted details, use them directly
                if contact and message:
                    print(f"AI extracted - Contact: {contact}, Message: {message}")
                else:
                    print("AI extraction failed, using manual parsing...")
                    # Parse manually as fallback
                    import re
                    patterns = [
                        r'to\s+([^\s]+).*say\s+(.+)',
                        r'to\s+([^\s]+).*saying\s+(.+)',
                        r'message\s+to\s+([^\s]+)\s+(.+)'
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, query)
                        if match:
                            contact = match.group(1)
                            message = match.group(2)
                            print(f"Manual extracted - Contact: {contact}, Message: {message}")
                            break
                    
                    if not contact or not message:
                        speak("Who should I send the message to?")
                        contact = takeCommand()
                        speak("What message should I send?")
                        message = takeCommand()
                
                if contact and message:
                    print(f"Opening WhatsApp and sending message to {contact}: {message}")
                    speak(f"Sending message to {contact}.")
                    # Step 1: Open WhatsApp using the working command
                    import time
                    open_anything("whatsapp")
                    time.sleep(4)
                    
                    # Step 2-5: Search, click contact, type message, send
                    from whatsapp_desktop import send_whatsapp_message_direct
                    if send_whatsapp_message_direct(contact, message):
                        speak(f"Message sent to {contact} successfully.")
                    else:
                        speak(f"Failed to send message to {contact}.")
                    remember_command("whatsapp", {"contact": contact, "message": message})
                else:
                    speak("I need both contact name and message to send WhatsApp.")
            except Exception as e:
                print(f"WhatsApp command error: {e}")
                speak("Sorry, there was an error processing the WhatsApp command.")
            return

        # ===== IOT CONTROL =====
        elif (any(word in query for word in ["turn", "switch"]) or any(phrase in query for phrase in ["fan on", "fan off", "light on", "light off", "led on", "led off", "all on", "all off"])) and (any(device in query for device in ["fan", "light", "led", "all", "device"]) or any(action in query for action in ["on", "off", "of"])):
            # Parse action - handle "turn of" typo and "turn fan on" patterns
            action = None
            if any(phrase in query for phrase in ["turn on", "switch on", " on ", "on all", "on fan", "on light", "on led", "fan on", "light on", "led on", "all on"]):
                action = "on"
            elif any(phrase in query for phrase in ["turn off", "turn of", "switch off", " off ", "of all", "of fan", "of light", "of led", "fan off", "light off", "led off", "all off"]):
                action = "off"
            
            # Check for all devices
            if any(word in query for word in ["all", "everything", "all device", "all devices"]) and action:
                devices = ["fan", "light", "led"]
                for device in devices:
                    control_iot_device(device, action)
                speak(f"All devices turned {action}")
                remember_command("iot all control", {"action": action})
                return
            
            # Individual device control
            device = None
            for d in ["fan", "light", "led"]:
                if d in query:
                    device = d
                    break
            
            if device and action:
                control_iot_device(device, action)
                remember_command("iot control", {"device": device, "action": action})
            return
        
        # Fallback for simple device commands
        elif any(device in query for device in ["fan", "light", "led"]) and any(action in query for action in ["on", "off"]):
            device = None
            action = None
            
            for d in ["fan", "light", "led"]:
                if d in query:
                    device = d
                    break
            
            for a in ["on", "off"]:
                if a in query:
                    action = a
                    break
            
            if device and action:
                control_iot_device(device, action)
                remember_command("iot control", {"device": device, "action": action})
            return
        
        elif "all" in query and any(action in query for action in ["on", "off"]):
            action = "on" if "on" in query else "off"
            devices = ["fan", "light", "led"]
            
            for device in devices:
                control_iot_device(device, action)
            
            speak(f"All devices turned {action}")
            remember_command("iot all control", {"action": action})
            return

        # ===== SCHEDULE/MEETING =====
        elif any(word in query for word in ["schedule", "meeting", "appointment"]):
            from ai_intent_recognition import get_ai_intent
            from calendar_service import create_calendar_event
            
            ai_result = get_ai_intent(query)
            entities = ai_result.get("entities", {})
            
            # Extract meeting details
            title = entities.get("subject", "Meeting")
            date_str = entities.get("date", "")
            time_str = entities.get("time", "")
            
            # Create calendar event only
            if create_calendar_event(title, date_str, time_str, query):
                speak(f"Meeting '{title}' scheduled successfully.")
            else:
                speak("Failed to schedule the meeting.")
            
            remember_command("schedule meeting", {"query": query})
            return

        # ===== EXIT =====
        elif any(word in query for word in ["exit", "quit", "sleep", "goodbye"]):
            speak("Goodbye sir. Session memory saved.")
            os._exit(0)

        else:
            speak("Sorry, I didn’t understand that command.")


# ==================================================
# 🧠 MAIN LOOP
# ==================================================
if __name__ == "__main__":
    jarvis = Jarvis()
    
    # Initialize IoT system
    print("Initializing IoT system...")
    if initialize_iot():
        print("IoT system ready")
    else:
        print("IoT system initialization failed")
    
    # Skip initialization if Enter is pressed
    import threading
    import sys
    
    def check_skip():
        input("Press Enter to skip initialization...")
        return True
    
    skip_thread = threading.Thread(target=check_skip, daemon=True)
    skip_thread.start()
    
    # Wait 3 seconds for user input
    skip_thread.join(timeout=3)
    
    if not skip_thread.is_alive():
        print("Initialization skipped.")
    else:
        jarvis.wishMe()

    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Ready - Say 'Jarvis' to activate")
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=5)

            wake = recognizer.recognize_google(audio, language="en-in").lower()
            if "jarvis" in wake:
                print("Wake word detected - Listening for command...")
                command = takeCommand()
                if command:
                    jarvis.route_command(command)

        except KeyboardInterrupt:
            speak("Exiting system. Goodbye sir.")
            break
        except Exception:
            continue
