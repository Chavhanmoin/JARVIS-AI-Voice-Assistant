import re
from difflib import get_close_matches


class IntentRecognizer:
    def __init__(self):
        # 🧩 Defined intent dictionary with pattern keywords
        self.intents = {
            'open_app': {
                'patterns': ['open', 'launch', 'start', 'run'],
                'entities': ['notepad', 'chrome', 'calculator', 'paint', 'code', 'spotify', 'vs code']
            },
            'close_app': {
                'patterns': ['close', 'exit', 'quit', 'stop', 'end'],
                'entities': ['notepad', 'chrome', 'calculator', 'paint', 'code', 'spotify']
            },
            'search_google': {
                'patterns': ['search', 'google', 'find', 'look up', 'on google'],
                'keywords': ['search', 'google', 'find']
            },
            'search_youtube': {
                'patterns': ['youtube', 'video', 'watch', 'play'],
                'keywords': ['youtube', 'video', 'play']
            },
            'send_message': {
                'patterns': ['send', 'message', 'whatsapp', 'text'],
                'keywords': ['whatsapp', 'message', 'send']
            },
            'send_email': {
                'patterns': ['email', 'mail', 'compose', 'write'],
                'keywords': ['email', 'mail', 'gmail']
            },
            'system_info': {
                'patterns': ['cpu', 'battery', 'system', 'performance'],
                'keywords': ['cpu', 'battery', 'system']
            },
            'time_query': {
                'patterns': ['time', 'clock', 'current time', 'what time'],
                'keywords': ['time', 'clock']
            },
            'weather_query': {
                'patterns': ['weather', 'temperature', 'forecast', 'climate'],
                'keywords': ['weather', 'temperature']
            },
            'joke': {
                'patterns': ['joke', 'funny', 'laugh', 'humor'],
                'keywords': ['joke', 'funny']
            }
        }

    # ==========================================
    # 🔹 Entity Extraction
    # ==========================================
    def extract_entities(self, text, intent):
        """Extract relevant entities (apps, search terms, etc.)"""
        entities = {}
        text_lower = text.lower()

        if intent in ['open_app', 'close_app']:
            for word in text_lower.split():
                match = get_close_matches(word, self.intents[intent]['entities'], n=1, cutoff=0.7)
                if match:
                    entities['app'] = match[0]
                    break

        elif intent in ['search_google', 'search_youtube']:
            # Extract the query term (words after “search for” etc.)
            match = re.search(r"(search|find|look up|watch|play|youtube)\s+(.*)", text_lower)
            if match:
                query = match.group(2).strip()
                query = re.sub(r"\b(on|in|for|about)\b", "", query).strip()
                if query:
                    entities['query'] = query

        return entities

    # ==========================================
    # 🔹 Intent Recognition
    # ==========================================
    def recognize_intent(self, text):
        """Recognize user intent from a given text query."""
        text_lower = text.lower().strip()
        best_intent = None
        best_score = 0

        for intent, data in self.intents.items():
            score = 0

            # Pattern match → strong signal (+2 per match)
            for pattern in data['patterns']:
                if pattern in text_lower:
                    score += 2

            # Keyword match → weaker signal (+1 per match)
            if 'keywords' in data:
                for keyword in data['keywords']:
                    if keyword in text_lower:
                        score += 1

            if score > best_score:
                best_score = score
                best_intent = intent

        # Normalize confidence
        confidence = round(min(best_score / 5, 1), 2)

        # Extract entities if we found an intent
        entities = {}
        if best_intent:
            entities = self.extract_entities(text, best_intent)

        return {
            'intent': best_intent or 'unknown',
            'confidence': confidence,
            'entities': entities,
            'original_text': text
        }


# ==========================================
# 🔹 Helper Function for Jarvis
# ==========================================
def process_user_intent(query: str):
    """Return structured intent data for Jarvis."""
    recognizer = IntentRecognizer()
    result = recognizer.recognize_intent(query)

    # Log result for debugging
    print(f"🧭 Intent recognized: {result['intent']} (confidence: {result['confidence']})")
    if result['entities']:
        print(f"   Entities: {result['entities']}")

    return result


# ==========================================
# 🧪 Standalone Test Mode
# ==========================================
if __name__ == "__main__":
    while True:
        q = input("You: ")
        if q.lower() in ['exit', 'quit', 'bye']:
            break
        print(process_user_intent(q))
