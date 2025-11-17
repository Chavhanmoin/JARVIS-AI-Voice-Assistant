import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ===================================================
# 🌐 Web Automation Core Class
# ===================================================
class WebAutomation:
    """Handles Google, YouTube, and WhatsApp automation."""

    def __init__(self):
        self.driver = None
        self.setup_driver()

    # ---------------------------------------------------
    # 🚀 Setup Chrome Driver
    # ---------------------------------------------------
    def setup_driver(self):
        """Set up Chrome WebDriver with optimized options."""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome WebDriver initialized successfully.")
        except Exception as e:
            print(f"❌ Failed to initialize ChromeDriver: {e}")
            self.driver = None

    # ---------------------------------------------------
    # 🔍 Google Search
    # ---------------------------------------------------
    def google_search(self, query):
        """Perform a Google search."""
        try:
            # Check if driver is valid
            if not self.driver:
                self.setup_driver()
            else:
                # Test if session is still valid
                try:
                    self.driver.current_url
                except:
                    self.setup_driver()
            
            print(f"🌐 Searching Google for: {query}")
            self.driver.get("https://www.google.com")
            box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "q")))
            box.clear()
            box.send_keys(query, Keys.RETURN)
            print(f"✅ Google search executed for '{query}'")
            return f"✅ Google search executed for '{query}'."
        except Exception as e:
            print(f"⚠️ Google search failed: {e}")
            # Try to recreate driver on failure
            self.setup_driver()
            return f"⚠️ Google search failed: {e}"

    # ---------------------------------------------------
    # 🎬 YouTube Search & Play
    # ---------------------------------------------------
    def youtube_search(self, query):
        """Search and play the top YouTube result."""
        if not self.driver:
            self.setup_driver()
        try:
            print(f"📺 Searching YouTube for: {query}")
            self.driver.get("https://www.youtube.com")
            box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "search_query")))
            box.clear()
            box.send_keys(query, Keys.RETURN)

            # Click the first video
            video = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title"))
            )
            video.click()
            print(f"🎬 Playing top YouTube result for '{query}'")
            return f"🎬 Playing top YouTube result for '{query}'."
        except Exception as e:
            print(f"⚠️ YouTube automation failed: {e}")
            return f"⚠️ YouTube automation failed: {e}"

    # ---------------------------------------------------
    # 💬 WhatsApp Automation
    # ---------------------------------------------------
    def whatsapp_send_message(self, contact, message):
        """Send a message via WhatsApp Web."""
        if not self.driver:
            self.setup_driver()

        try:
            print("💬 Opening WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            print("⏳ Waiting for QR login or existing session...")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']"))
            )
            print("✅ WhatsApp Web loaded.")

            # Wait for user login if needed
            time.sleep(10)

            # Search for contact
            search_box = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            search_box.click()
            search_box.send_keys(contact)
            time.sleep(3)

            # Click contact
            contact_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[@title='{contact}']"))
            )
            contact_element.click()
            time.sleep(2)

            # Send message
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
            )
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            print(f"💬 Message sent to {contact}: '{message}'")
            return f"💬 Message sent to {contact}: '{message}'"
        except Exception as e:
            print(f"❌ WhatsApp automation failed: {e}")
            return f"❌ WhatsApp automation failed: {e}"

    # ---------------------------------------------------
    # 🛑 Close Browser
    # ---------------------------------------------------
    def close_browser(self):
        """Close Chrome browser safely."""
        if self.driver:
            try:
                self.driver.quit()
                print("🛑 Browser closed successfully.")
            except:
                pass
            self.driver = None


# ===================================================
# Wrapper Functions for Jarvis Integration
# ===================================================
_web_bot = None

def init_web_automation():
    """Initialize or reuse the existing browser session."""
    global _web_bot
    if not _web_bot or not _web_bot.driver:
        _web_bot = WebAutomation()
    return _web_bot

def search_google(query):
    global _web_bot
    try:
        bot = init_web_automation()
        return bot.google_search(query)
    except Exception as e:
        # Reset the bot on any error
        _web_bot = None
        bot = init_web_automation()
        return bot.google_search(query)

def search_youtube(query):
    """Search YouTube and play first video using fresh Selenium session"""
    driver = None
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        
        print(f"📺 Searching YouTube for: {query}")
        
        # Create fresh Chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Go to YouTube
        driver.get("https://www.youtube.com")
        
        # Search for the query
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "search_query"))
        )
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait and click first video
        time.sleep(3)
        first_video = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title"))
        )
        first_video.click()
        
        print(f"🎬 Playing first YouTube result for: {query}")
        
        # Keep browser open for video playback
        time.sleep(2)
        
        return f"🎬 Playing first YouTube result for: {query}"
        
    except Exception as e:
        print(f"⚠️ YouTube automation failed: {e}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        return f"⚠️ YouTube automation failed: {e}"

def send_whatsapp_message(contact, message):
    bot = init_web_automation()
    return bot.whatsapp_send_message(contact, message)

def close_web_automation():
    global _web_bot
    if _web_bot:
        _web_bot.close_browser()
        _web_bot = None
