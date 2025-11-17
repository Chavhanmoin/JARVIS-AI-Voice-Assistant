import requests
import json
import random
import os
import webbrowser
from helpers import speak
from dotenv import load_dotenv

# ===========================================
# 🔑 Load Environment Variables
# ===========================================
load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

CACHE_FILE = "news_cache.json"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GNEWS_FALLBACK_URL = "https://gnews.io/api/v4/top-headlines?lang=en&country=in&max=5&apikey=1d2e7d7a4510c0a63e7a4fda"
GOOGLE_NEWS_URL = "https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en"

# ===========================================
# 📰 Fetch News (with multiple fallbacks)
# ===========================================
def fetch_news(category=None):
    """Fetch live news headlines using NewsAPI, fallback to GNews, then cache."""
    if not NEWS_API_KEY:
        speak("News API key is missing.")
        return []

    try:
        categories = ["technology", "science", "business", "entertainment", "health", "sports"]
        category = category or random.choice(categories)

        print(f"🌍 Fetching {category} news from NewsAPI...")
        url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=8)
        data = response.json()
        articles = [a["title"] for a in data.get("articles", []) if a.get("title")]

        # If empty, try broader search
        if not articles:
            alt_url = (
                f"https://newsapi.org/v2/everything?"
                f"q={category}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
            )
            alt_data = requests.get(alt_url, timeout=8).json()
            articles = [a["title"] for a in alt_data.get("articles", []) if a.get("title")]

        # Fallback to GNews if still no results
        if not articles:
            print("📰 Falling back to GNews API...")
            gnews_data = requests.get(GNEWS_FALLBACK_URL, timeout=8).json()
            articles = [a["title"] for a in gnews_data.get("articles", []) if a.get("title")]

        # Cache successful results
        if articles:
            with open(CACHE_FILE, "w", encoding="utf-8") as cache:
                json.dump({"category": category, "articles": articles}, cache, indent=2)
            print(f"✅ Cached {len(articles)} headlines.")
            return articles

        # Use cached data if all APIs fail
        return read_cached_news()

    except Exception as e:
        print(f"📰 News Fetch Error: {e}")
        return read_cached_news()

# ===========================================
# 💾 Read Cached News
# ===========================================
def read_cached_news():
    """Return cached headlines if available."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as cache:
            cached = json.load(cache)
            return cached.get("articles", [])
    return []

# ===========================================
# 🗣️ Speak News or Open Visual Fallback
# ===========================================
def speak_news():
    """Speak the latest news headlines; if none found, open Google News visually."""
    try:
        headlines = fetch_news()

        if not headlines:
            speak("Sorry, I couldn’t find fresh headlines right now. Opening Google News for you.")
            print("📰 Opening Google News in Chrome...")
            try:
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(CHROME_PATH))
                webbrowser.get('chrome').open(GOOGLE_NEWS_URL)
            except:
                webbrowser.open(GOOGLE_NEWS_URL)
            return

        # Speak and show news
        speak("Here are the latest news headlines for you.")
        for i, title in enumerate(headlines[:5], start=1):
            speak(f"Headline {i}: {title}")
        speak("That’s all for now, sir.")

        print("\n🗞️ Latest Headlines:")
        for i, h in enumerate(headlines[:5], 1):
            print(f"{i}. {h}")

    except Exception as e:
        print(f"🗞️ Error in speak_news: {e}")
        speak("Sorry, I couldn’t fetch the news right now. Opening Google News.")
        try:
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(CHROME_PATH))
            webbrowser.get('chrome').open(GOOGLE_NEWS_URL)
        except:
            webbrowser.open(GOOGLE_NEWS_URL)

# ===========================================
# 🌐 Fallback URL
# ===========================================
def getNewsUrl():
    """Return fallback Google News India page."""
    return GOOGLE_NEWS_URL

# ===========================================
# 🧪 Test Mode
# ===========================================
if __name__ == "__main__":
    print("\n=== 📰 TESTING NEWS MODULE ===")
    speak_news()
    print("✅ News module test completed.")
