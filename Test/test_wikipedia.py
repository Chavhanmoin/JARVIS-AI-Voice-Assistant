import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from wikipedia_search import search_and_open_wikipedia

print("\n=== 📚 TESTING WIKIPEDIA SEARCH MODULE ===")
print(search_and_open_wikipedia("Artificial Intelligence"))
print("✅ Wikipedia search test completed.")
