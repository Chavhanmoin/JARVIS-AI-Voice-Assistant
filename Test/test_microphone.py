import sys
import os
import speech_recognition as sr

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_microphone():
    """Test microphone functionality"""
    print("MICROPHONE TEST")
    print("=" * 30)
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    # List available microphones
    print("Available microphones:")
    mic_list = sr.Microphone.list_microphone_names()
    for i, mic_name in enumerate(mic_list):
        print(f"  {i}: {mic_name}")
    
    # Test default microphone
    print(f"\nTesting default microphone...")
    
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=2)
            print("Listening... Say something!")
            
            # Listen for 5 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing...")
            
            # Try to recognize
            text = r.recognize_google(audio, language="en-in")
            print(f"You said: {text}")
            print("Microphone test PASSED!")
            
    except sr.WaitTimeoutError:
        print("No speech detected within timeout")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Recognition service error: {e}")
    except Exception as e:
        print(f"Microphone test FAILED: {e}")

if __name__ == "__main__":
    test_microphone()