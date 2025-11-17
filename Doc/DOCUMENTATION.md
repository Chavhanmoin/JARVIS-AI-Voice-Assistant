# J.A.R.V.I.S - AI Voice Assistant Documentation

**Just A Rather Very Intelligent System**

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Voice Commands](#voice-commands)
8. [System Components](#system-components)
9. [API Integrations](#api-integrations)
10. [Configuration](#configuration)
11. [Testing](#testing)
12. [Troubleshooting](#troubleshooting)

## Overview

J.A.R.V.I.S is a comprehensive AI-powered voice assistant built with Python that provides system automation, web control, smart communication, and IoT device management capabilities. The system uses advanced natural language processing, voice recognition, and multiple API integrations to deliver a seamless user experience.

## Features

### 🎤 Voice Control
- **Wake Word Detection**: Activated by saying "Jarvis"
- **Natural Language Processing**: Powered by OpenAI GPT for intent recognition
- **Text-to-Speech**: Responds with voice feedback using pyttsx3
- **Continuous Listening**: Always ready for commands
- **Memory System**: Remembers and can repeat last commands

### 💻 System Automation
- **Application Control**: Open/close any Windows application
- **File Management**: Create, delete files and folders
- **System Information**: CPU usage, battery status, time queries
- **Screenshots**: Capture screen on command
- **Volume/Brightness Control**: Adjust system settings with voice
- **Dynamic App Detection**: Find and launch applications from multiple directories

### 🌐 Web Automation
- **Google Search**: Intelligent web searches with Chrome automation
- **YouTube Control**: Search and play videos automatically
- **Wikipedia Integration**: Quick information lookup
- **Browser Control**: Uses Chrome profile with saved logins

### 📱 Communication
- **WhatsApp Desktop**: Automated message sending via desktop app
- **Gmail API**: Professional email composition and sending
- **Contact Management**: Dynamic contact recognition
- **AI-Powered Email Generation**: Extracts subject and body from voice commands

### 📅 Calendar Integration
- **Google Calendar API**: Direct meeting scheduling
- **Dynamic Date Parsing**: Handles various date/time formats
- **Chrome Profile Integration**: Seamless authentication

### 🏠 IoT Control
- **Sinric Pro Integration**: Control Arduino-based home devices
- **REST API Communication**: Reliable device control
- **Multi-Device Support**: Fan, LED, Light control
- **Group Control**: Turn all devices on/off with single command

### 🤖 AI Integration
- **OpenAI GPT**: Advanced natural language understanding
- **Intent Recognition**: Understands complex voice commands
- **Context Awareness**: Extracts entities from speech
- **Fallback Processing**: Multiple layers of command interpretation

### 📰 Information Services
- **Weather Updates**: Real-time weather information
- **News Headlines**: Latest news from multiple sources
- **Dictionary/Definitions**: Word meanings and explanations
- **Jokes**: Entertainment functionality

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        J.A.R.V.I.S                         │
│                     Main Controller                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐        ┌────▼────┐       ┌────▼────┐
│ Voice │        │   AI    │       │ System  │
│ I/O   │        │ Engine  │       │ Control │
└───┬───┘        └────┬────┘       └────┬────┘
    │                 │                 │
┌───▼───┐        ┌────▼────┐       ┌────▼────┐
│Speech │        │ OpenAI  │       │  File   │
│ Recog │        │   GPT   │       │ Manager │
└───────┘        └─────────┘       └─────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │   Web   │   │  Email  │   │   IoT   │
   │ Control │   │ Service │   │ Control │
   └─────────┘   └─────────┘   └─────────┘
```

## Tech Stack

### Core Technologies
- **Python 3.8+**: Main programming language
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: pyttsx3 engine
- **Natural Language Processing**: OpenAI GPT API

### Web Technologies
- **Selenium WebDriver**: Browser automation
- **Chrome WebDriver**: Web control and automation
- **Requests**: HTTP API communications
- **BeautifulSoup**: Web scraping

### APIs & Services
- **OpenAI API**: Natural language processing
- **Google APIs**: Gmail, Calendar, Speech Recognition
- **Sinric Pro API**: IoT device control
- **Weather API**: Weather information
- **News API**: News headlines

### System Integration
- **PyAutoGUI**: GUI automation
- **psutil**: System information
- **Windows APIs**: System control
- **OAuth2**: Secure authentication

### Data Storage
- **JSON**: Configuration and data storage
- **Pickle**: Token and session management
- **File System**: Local data persistence

## Installation

### Prerequisites
```bash
Python 3.8+
Google Chrome Browser
Microphone and Speakers
Windows 10/11
```

### Setup Steps
1. **Clone Repository**
```bash
git clone https://github.com/your-repo/J.A.R.V.I.S.git
cd J.A.R.V.I.S
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
EMAIL=your_email@gmail.com
PASSWORD=your_app_password
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key
```

4. **Setup Google APIs**
- Place `credentials.json` in project root
- First run will authenticate and create tokens

## Usage

### Starting JARVIS
```bash
python jarvis.py
```

### Activation
1. Say "Jarvis" to activate
2. Give voice command
3. System processes and responds

## Voice Commands

### System Control
```
"open notepad"
"close chrome"
"take screenshot"
"what is the time"
"cpu usage"
"volume up"
"brightness down"
```

### Web Automation
```
"search python tutorials"
"youtube search machine learning"
"open google"
"wikipedia artificial intelligence"
```

### Communication
```
"send whatsapp message to John saying hello"
"email about meeting tomorrow"
"schedule meeting with team on Friday"
```

### IoT Control
```
"turn on fan"
"light off"
"all devices on"
"turn off all lights"
```

### Information
```
"tell me a joke"
"what's the weather"
"latest news"
"define artificial intelligence"
```

## System Components

### Core Modules

#### `jarvis.py`
- Main system controller
- Command routing and processing
- Wake word detection
- Memory management

#### `helpers.py`
- Core utility functions
- Speech recognition and TTS
- Weather and system information
- Memory operations

#### `ai_intent_recognition.py`
- OpenAI GPT integration
- Natural language processing
- Entity extraction
- Intent classification

#### `system_control.py`
- Windows system automation
- Application control
- Volume/brightness management
- Dynamic app detection

#### `web_automation.py`
- Browser automation
- Google search functionality
- YouTube video control
- Selenium WebDriver management

#### `gmail_service.py`
- Gmail API integration
- Email composition and sending
- OAuth2 authentication
- Chrome profile integration

#### `calendar_service.py`
- Google Calendar API
- Meeting scheduling
- Date/time parsing
- Event management

#### `iot_control.py`
- Sinric Pro API integration
- IoT device control
- REST API communication
- Device state management

#### `whatsapp_desktop.py`
- WhatsApp desktop automation
- Message sending
- Contact search
- GUI automation

## API Integrations

### OpenAI GPT
- **Purpose**: Natural language understanding
- **Usage**: Intent recognition, entity extraction
- **Configuration**: API key in `.env`

### Google APIs
- **Gmail API**: Email functionality
- **Calendar API**: Meeting scheduling
- **Speech Recognition**: Voice processing

### Sinric Pro API
- **Purpose**: IoT device control
- **Method**: REST API calls
- **Devices**: Fan, LED, Light control

### Weather API
- **Service**: WeatherAPI.com
- **Purpose**: Weather information
- **Key**: Required in `.env`

### News API
- **Purpose**: Latest news headlines
- **Configuration**: API key required

## Configuration

### Environment Variables
```env
# AI Services
OPENAI_API_KEY=sk-...

# Email Configuration
EMAIL=your_email@gmail.com
PASSWORD=your_app_password

# Weather Service
WEATHER_API_KEY=your_weather_key

# News Service
NEWS_API_KEY=your_news_key
```

### Chrome Configuration
- **Profile Path**: Uses default Chrome profile
- **Extensions**: Supports Chrome extensions
- **Login State**: Maintains logged-in sessions

### Voice Settings
- **Language**: English (India)
- **Wake Word**: "Jarvis"
- **Microphone**: Windows default
- **TTS Voice**: Configurable

## Testing

### Test Files
- `test_iot.py`: IoT functionality testing
- `Test/`: Comprehensive test suite
- Individual module tests available

### Running Tests
```bash
# IoT Control Test
python test_iot.py

# System Tests
python Test/test_system_control.py

# Web Automation Tests
python Test/test_web_automation.py
```

## Troubleshooting

### Common Issues

#### Voice Recognition Problems
```python
# Adjust microphone settings in helpers.py
r.energy_threshold = 400  # Increase for noisy environments
r.pause_threshold = 0.8   # Decrease for faster response
```

#### Chrome Profile Conflicts
```bash
# Close all Chrome instances
taskkill /f /im chrome.exe
```

#### API Authentication
```bash
# Delete token files and re-authenticate
del token.json
del calendar_token.pickle
python jarvis.py
```

#### IoT Connection Issues
- Verify Sinric Pro credentials
- Check internet connection
- Ensure device IDs are correct

### Error Handling
- Graceful fallbacks for API failures
- Retry mechanisms for network issues
- User feedback for errors
- Logging for debugging

## Performance Optimization

### Memory Management
- Efficient command caching
- Selective module loading
- Resource cleanup

### Response Time
- Async processing where possible
- Cached API responses
- Optimized voice recognition

### Reliability
- Multiple fallback mechanisms
- Error recovery systems
- Robust exception handling

## Security Features

### Authentication
- OAuth2 for Google services
- Secure token storage
- API key protection

### Data Privacy
- Local data storage
- Encrypted credentials
- No sensitive data logging

### Access Control
- Application whitelisting
- Safe command execution
- User confirmation for critical actions

## Future Enhancements

### Planned Features
- [ ] Smart Home Integration (IoT expansion)
- [ ] Multi-language Support
- [ ] Mobile App Integration
- [ ] Cloud Synchronization
- [ ] Plugin System
- [ ] Advanced Scheduling
- [ ] Contextual Memory Enhancement

### Technical Improvements
- [ ] Async Processing
- [ ] Database Integration
- [ ] REST API Interface
- [ ] Docker Containerization
- [ ] Performance Monitoring

---

**Made with ❤️ by the JARVIS Development Team**