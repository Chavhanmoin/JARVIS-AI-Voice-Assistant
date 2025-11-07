import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from diction import translate

print("\n=== 📖 TESTING DICTIONARY MODULE ===")
translate("technology")
print("✅ Dictionary module test completed.")
