import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diction import translate, get_word_meaning

def test_word_definitions():
    """Test OpenAI dictionary functionality."""
    print("=== 📖 TESTING OPENAI DICTIONARY ===\n")
    
    test_words = [
        "artificial",
        "intelligence", 
        "serendipity",
        "ephemeral",
        "python"
    ]
    
    for word in test_words:
        print(f"Testing word: {word}")
        result = translate(word)
        print(f"Result: {result}\n")
        print("-" * 50)
    
    print("✅ Dictionary test completed.")

def test_edge_cases():
    """Test edge cases."""
    print("\n=== 🧪 TESTING EDGE CASES ===\n")
    
    # Empty word
    print("Testing empty word:")
    result = translate("")
    print(f"Result: {result}\n")
    
    # Non-existent word
    print("Testing made-up word:")
    result = translate("xyzabc123")
    print(f"Result: {result}\n")
    
    print("✅ Edge case tests completed.")

if __name__ == "__main__":
    test_word_definitions()
    test_edge_cases()