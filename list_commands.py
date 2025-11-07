#!/usr/bin/env python3
"""List All JARVIS Commands"""

def list_jarvis_commands():
    """Extract commands from jarvis.py"""
    print("JARVIS.PY COMMANDS")
    print("=" * 50)
    
    jarvis_commands = [
        "wikipedia Taj Mahal",
        "youtube downloader", 
        "voice female/male",
        "jarvis are you there",
        "jarvis who made you",
        "open youtube",
        "open amazon",
        "open Downloads",
        "cpu", 
        "screenshot",
        "open google",
        "open stackoverflow",
        "play music",
        "youtube search Wardha",
        "the time",
        "search Bajaj Institute of Technology",
        "location Nagpur",
        "your master",
        "your name", 
        "who made you",
        "stands for",
        "open Paints",
        "close Paints",
        "your friend",
        "github",
        "sleep/exit/quit"
    ]
    
    for i, cmd in enumerate(jarvis_commands, 1):
        print(f"{i:2d}. {cmd}")

def list_helper_functions():
    """Extract functions from helpers.py"""
    print("\nHELPERS.PY FUNCTIONS")
    print("=" * 50)
    
    helper_functions = [
        "speak(text) - Text to speech",
        "screenshot() - Take screenshot", 
        "cpu() - CPU and battery info",
        "joke() - Tell jokes",
        "takeCommand() - Voice recognition",
        "weather() - Weather info for Wardha",
        "translate(word) - Dictionary lookup",
        "open_app(name) - Open application",
        "close_app(name) - Close application"
    ]
    
    for i, func in enumerate(helper_functions, 1):
        print(f"{i:2d}. {func}")

def list_ai_intents():
    """List AI intents supported"""
    print("\nAI INTENTS SUPPORTED")
    print("=" * 50)
    
    ai_intents = [
        "open_app - Open applications",
        "close_app - Close applications", 
        "search_google - Google search",
        "search_youtube - YouTube search",
        "send_whatsapp - WhatsApp messages",
        "time_query - Current time",
        "system_info - CPU/battery info",
        "joke - Tell jokes",
        "weather_query/get_weather - Weather info",
        "screenshot - Take screenshot",
        "email/mail/gmail - Email composition",
        "shutdown - System shutdown",
        "news - Latest news",
        "translate/dictionary - Word lookup"
    ]
    
    for i, intent in enumerate(ai_intents, 1):
        print(f"{i:2d}. {intent}")

def list_voice_commands():
    """List example voice commands"""
    print("\nEXAMPLE VOICE COMMANDS")
    print("=" * 50)
    
    examples = [
        "Jarvis, open notepad",
        "Jarvis, what is the time",
        "Jarvis, weather today", 
        "Jarvis, search python tutorials",
        "Jarvis, youtube search music",
        "Jarvis, take screenshot",
        "Jarvis, tell me a joke",
        "Jarvis, cpu usage",
        "Jarvis, latest news",
        "Jarvis, close calculator",
        "Jarvis, write email about meeting",
        "Jarvis, send whatsapp to John saying hello",
        "Jarvis, translate artificial intelligence",
        "Jarvis, shutdown system"
    ]
    
    for i, cmd in enumerate(examples, 1):
        print(f"{i:2d}. {cmd}")

if __name__ == "__main__":
    list_jarvis_commands()
    list_helper_functions() 
    list_ai_intents()
    list_voice_commands()
    
    print("\nUSAGE:")
    print("1. Run: python jarvis.py")
    print("2. Say 'Jarvis' + command")
    print("3. Or press Ctrl+K + type command")