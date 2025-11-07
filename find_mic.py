import speech_recognition as sr

# Get a list of all available microphone names and their indices
mic_list = sr.Microphone.list_microphone_names()

print("Available microphones:")
# Enumerate through the list to print each microphone with its index
for index, name in enumerate(mic_list):
    print(f"  Index {index}: {name}")