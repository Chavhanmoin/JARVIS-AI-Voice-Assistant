import wikipedia
import webbrowser
from helpers import speak, takeCommand

def search_and_open_wikipedia(query: str):
    """Search Wikipedia for a topic, summarize it, and open in browser."""
    try:
        # Clean and extract search term
        search_term = query.lower().replace("wikipedia", "").strip()

        if not search_term:
            speak("What should I search on Wikipedia?")
            return "⚠️ No search term provided."

        speak(f"Searching Wikipedia for {search_term}...")

        # Get summary first to validate existence
        summary = wikipedia.summary(search_term, sentences=2, auto_suggest=True)
        page = wikipedia.page(search_term, auto_suggest=True)

        # Open the article
        webbrowser.open(page.url)
        speak(f"✅ Found {page.title} on Wikipedia.")
        speak(summary)

        return f"Wikipedia article opened for: {page.title}"

    except wikipedia.exceptions.DisambiguationError as e:
        # Handle ambiguous terms (multiple possible pages)
        try:
            option = e.options[0]
            page = wikipedia.page(option)
            webbrowser.open(page.url)
            speak(f"⚠️ Multiple results found. Opening the first one: {option}.")
            return f"Wikipedia article opened for: {option}"
        except Exception:
            speak("Too many results. Please specify more clearly.")
            return "Disambiguation error."

    except wikipedia.exceptions.PageError:
        speak(f"Sorry, no article found for {search_term}.")
        return f"❌ No Wikipedia article found for: {search_term}"

    except Exception as e:
        speak("Sorry, Wikipedia search failed due to a technical issue.")
        print(f"❌ Wikipedia Error: {e}")
        return f"Error during Wikipedia search: {str(e)}"


def wikipedia_voice_search():
    """Interactive voice-based Wikipedia search."""
    speak("What do you want to search on Wikipedia?")
    query = takeCommand()

    if query and query.lower() != "none":
        return search_and_open_wikipedia(query)
    else:
        speak("No search term received.")
        return "⚠️ No input received."
