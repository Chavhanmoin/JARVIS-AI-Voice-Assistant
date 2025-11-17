import os
import json
from dotenv import load_dotenv
import openai
import re

# ===============================
# 🔹 Load Environment & API Key
# ===============================
load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("⚠️ Warning: OPENAI_API_KEY missing in .env file")


# ===============================
# 🔹 AI Intent Recognizer Class
# ===============================
class AIIntentRecognizer:
    def __init__(self):
        self.system_prompt = (
            """You are JARVIS — an intelligent personal assistant.
You receive natural language commands and must return a valid JSON in this format:
{
  "intent": "detected_intent",
  "entities": {"key": "value"},
  "confidence": 0.9,
  "action": "specific_action"
}

✅ Rules:
- Always output valid JSON (no text outside JSON).
- intent = short snake_case name (e.g. "open_app", "search_youtube", "send_email", "schedule_meeting").
- entities = key-value pairs (e.g. {"app": "notepad"}, {"query": "AI news"}).
- confidence = number between 0.0 and 1.0.
- Be flexible with user wording.
- For emails, extract subject and generate professional body (3-4 sentences).
- For dates: Extract EXACT date mentioned. "15 nov" = "15 November", "nov 15" = "15 November". Do NOT change the date.
- For meetings: Extract subject, date, and time separately.

Examples:
- "open youtube and search car songs" → {"intent": "search_youtube", "entities": {"query": "car songs"}, "confidence": 0.95, "action": "youtube_search"}
- "schedule meeting with hod on 15 nov 2pm" → {"intent": "schedule_meeting", "entities": {"subject": "Meeting with HOD", "date": "15 November", "time": "2:00 PM"}, "confidence": 0.9, "action": "create_meeting"}
- "meeting with team tomorrow 3pm" → {"intent": "schedule_meeting", "entities": {"subject": "Meeting with team", "date": "tomorrow", "time": "3:00 PM"}, "confidence": 0.9, "action": "create_meeting"}
- "write a mail to head of department for sick leave" → {"intent": "send_email", "entities": {"subject": "Sick Leave Request", "body": "Dear Head of Department,\n\nI am writing to request sick leave due to health issues. I would like to take leave from [date] and will provide medical certificate if required.\n\nPlease approve my leave application.\n\nThank you.\nBest regards"}, "confidence": 0.9, "action": "compose_email"}"""
        )

    def recognize_intent(self, user_input: str) -> dict:
        """Use OpenAI to recognize user intent and return structured JSON"""
        try:
            if not user_input or len(user_input.strip()) < 2:
                return self._fallback_intent(user_input, reason="Empty input")

            # Select best available model
            model = "gpt-4-turbo" if self._model_available("gpt-4-turbo") else "gpt-3.5-turbo"

            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze this: {user_input}"}
                ],
                max_tokens=250,
                temperature=0.3
            )

            result_text = response.choices[0].message.content.strip()

            # Attempt to extract JSON from possibly mixed response
            result_json = self._extract_json(result_text)

            if not result_json:
                print(f"AI returned non-JSON response: {result_text}")
                return self._fallback_intent(user_input, reason="Invalid JSON")

            # Ensure required fields
            return self._validate_result(result_json, user_input)

        except Exception as e:
            print(f"AI Intent Recognition Error: {e}")
            return self._fallback_intent(user_input, reason=str(e))

    # ==============================================================
    # 🔸 Utility Helpers
    # ==============================================================

    def _extract_json(self, text: str) -> dict:
        """Try to extract and parse JSON object from the model response."""
        try:
            # Extract JSON block (if model adds extra text)
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                text = match.group(0)
            return json.loads(text)
        except Exception:
            return None

    def _validate_result(self, data: dict, user_input: str) -> dict:
        """Ensure the result has all required fields."""
        return {
            "intent": data.get("intent", "other"),
            "entities": data.get("entities", {}),
            "confidence": float(data.get("confidence", 0.7)),
            "action": data.get("action", data.get("intent", "other")),
            "original_text": user_input
        }

    def _fallback_intent(self, text: str, reason: str = "fallback") -> dict:
        """Fallback rule-based intent extraction for common patterns."""
        t = (text or "").lower()
        entities = {}

        # Simple heuristic rules
        if "youtube" in t and ("search" in t or "play" in t):
            query = re.sub(r".*(youtube|search|play)", "", t).strip()
            entities["query"] = query
            return {
                "intent": "search_youtube",
                "entities": entities,
                "confidence": 0.8,
                "action": "youtube_search",
                "original_text": text
            }

        if "open" in t:
            app = re.sub(r"(open|launch|start)", "", t).strip()
            entities["app"] = app
            return {
                "intent": "open_app",
                "entities": entities,
                "confidence": 0.75,
                "action": "open_application",
                "original_text": text
            }

        if "close" in t:
            app = re.sub(r"(close|exit|stop)", "", t).strip()
            entities["app"] = app
            return {
                "intent": "close_app",
                "entities": entities,
                "confidence": 0.75,
                "action": "close_application",
                "original_text": text
            }

        return {
            "intent": "other",
            "entities": {},
            "confidence": 0.2,
            "action": "fallback",
            "original_text": text
        }

    def _model_available(self, model_name: str) -> bool:
        """Quick heuristic — tries to switch model if gpt-4 unavailable."""
        try:
            _ = openai.Model.retrieve(model_name)
            return True
        except Exception:
            return False


# ==============================================================
# 🔸 Public Helper
# ==============================================================
def get_ai_intent(query: str) -> dict:
    """Get AI-powered intent recognition output."""
    recognizer = AIIntentRecognizer()
    result = recognizer.recognize_intent(query)
    print(f"AI Intent: {result['intent']} (confidence: {result['confidence']})")
    if result.get("entities"):
        print(f"   Entities: {result['entities']}")
    return result


# ==============================================================
# 🔸 Standalone Testing
# ==============================================================
if __name__ == "__main__":
    print("JARVIS AI Intent Recognizer (type 'exit' to quit)\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "bye"]:
            break
        output = get_ai_intent(query)
        print(json.dumps(output, indent=2))
