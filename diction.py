import os
import re
import openai
from dotenv import load_dotenv
from helpers import speak

# Load environment variables
load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_word_meaning(word):
    """Get word meaning using OpenAI API."""
    if not openai.api_key:
        return "OpenAI API key not found."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a dictionary assistant. Provide only one line definition. Maximum 15 words. No examples."},
                {"role": "user", "content": f"Define '{word}' in one line"}
            ],
            max_tokens=30,
            temperature=0.1
        )
        
        definition = response.choices[0].message.content.strip()
        return definition
        
    except Exception as e:
        return f"Error getting definition: {str(e)}"

def extract_word_from_query(query):
    """Extract word to define from natural language query."""
    query = query.lower().strip()
    
    # Common patterns for asking definitions
    patterns = [
        r'meaning of (.+)',
        r'define (.+)',
        r'what is (.+)',
        r'what does (.+) mean',
        r'explain (.+)',
        r'tell me about (.+)',
        r'(.+) meaning',
        r'(.+) definition'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            word = match.group(1).strip()
            # Clean up common words
            word = re.sub(r'\b(the|a|an|is|does|means?)\b', '', word).strip()
            return word
    
    # If no pattern matches, return the query as is
    return query

def translate(query):
    """Main function to get and speak word definition from natural language."""
    word = extract_word_from_query(query)
    
    if not word:
        speak("Please provide a word to define.")
        return "No word provided."
    
    print(f"🔍 Looking up definition for: {word}")
    speak(f"Looking up the meaning of {word}")
    
    definition = get_word_meaning(word)
    
    if definition.startswith("Error"):
        speak("Sorry, I couldn't find the definition.")
        print(f"❌ {definition}")
        return definition
    
    speak(f"The meaning of {word} is {definition}")
    print(f"📖 {word}: {definition}")
    return definition

if __name__ == "__main__":
    # Test natural language queries
    test_queries = [
        "what is artificial intelligence",
        "meaning of serendipity", 
        "define python",
        "what does ephemeral mean",
        "intelligence"
    ]
    
    for query in test_queries:
        print(f"\nTesting: {query}")
        translate(query)
        print("-" * 40)