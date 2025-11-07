import os
from jarvis import Jarvis
from file_manager import *

def test_all_jarvis_functions():
    """Test all JARVIS functions"""
    
    print("🤖 TESTING ALL JARVIS FUNCTIONS")
    print("=" * 50)
    
    bot = Jarvis()
    
    # Test categories with commands
    test_categories = {
        "🌐 Web & Search": [
            "open google",
            "search python programming",
            "youtube search music",
            "python wikipedia"
        ],
        "💻 System Control": [
            "open notepad",
            "close notepad", 
            "take screenshot",
            "cpu usage",
            "what is the time"
        ],
        "📧 Communication": [
            "open gmail",
            "compose email about meeting"
        ],
        "🎯 Information": [
            "tell me a joke",
            "weather report",
            "latest news"
        ],
        "🔧 System": [
            "open calculator",
            "close calculator",
            "open settings"
        ],
        "🎤 Voice & AI": [
            "jarvis are you there",
            "who made you",
            "what does jarvis stand for"
        ]
    }
    
    total_tests = 0
    passed_tests = 0
    
    for category, commands in test_categories.items():
        print(f"\n{category}")
        print("-" * 30)
        
        for command in commands:
            total_tests += 1
            print(f"Testing: '{command}'")
            
            try:
                bot.execute_query(command)
                print("✅ PASSED")
                passed_tests += 1
            except Exception as e:
                print(f"❌ FAILED: {e}")
            
            print()
    
    # Results summary
    print("=" * 50)
    print(f"📊 JARVIS TEST RESULTS")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print("=" * 50)

def test_file_manager():
    """Test all file manager functions"""
    
    print("\n🗂️ TESTING FILE MANAGER FUNCTIONS")
    print("=" * 50)
    
    # Test paths
    test_folder = "C:\\temp\\jarvis_test"
    test_file = "C:\\temp\\jarvis_test\\test.txt"
    
    # Ensure the base directory exists for testing
    if not os.path.exists("C:\\temp"):
        os.makedirs("C:\\temp")
    
    print("1. Testing create_folder()")
    result = create_folder(test_folder)
    print(f"Result: {result}")
    
    print("\n2. Testing create_file()")
    result = create_file(test_file, "Hello from JARVIS!")
    print(f"Result: {result}")
    
    print("\n3. Testing list_files()")
    result = list_files(test_folder)
    print(f"Result: {result}")
    
    print("\n4. Testing open_folder()")
    result = open_folder(test_folder)
    print(f"Result: {result}")
    
    print("\n5. Testing copy_file()")
    copy_dest = "C:\\temp\\jarvis_test\\test_copy.txt"
    result = copy_file(test_file, copy_dest)
    print(f"Result: {result}")
    
    print("\n6. Testing move_file()")
    move_dest = "C:\\temp\\jarvis_test\\test_moved.txt"
    result = move_file(copy_dest, move_dest)
    print(f"Result: {result}")
    
    print("\n7. Testing delete_file()")
    result = delete_file(move_dest)
    print(f"Result: {result}")
    
    # Clean up the original test file before deleting the folder
    if os.path.exists(test_file):
        delete_file(test_file)
    
    print("\n8. Testing delete_folder()")
    result = delete_folder(test_folder)
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ File Manager Tests Completed")

if __name__ == "__main__":
    # Run the Jarvis function tests
    test_all_jarvis_functions()
    
    # Run the File Manager function tests
    test_file_manager()