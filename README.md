# J.A.R.V.I.S - AI Voice Assistant

**Just A Rather Very Intelligent System**

A comprehensive AI-powered voice assistant built with Python that provides system automation, web control, and smart communication capabilities.

## 🚀 Features

### 🎤 Voice Control
- **Wake Word Detection**: Say "Jarvis" to activate
- **Natural Language Processing**: Powered by OpenAI GPT for intent recognition
- **Text-to-Speech**: Responds with voice feedback
- **Continuous Listening**: Always ready for commands

### 💻 System Automation
- **Application Control**: Open/close any Windows application
- **File Management**: Open files, folders, and system locations
- **System Information**: CPU usage, battery status, time queries
- **Screenshots**: Capture screen on command
- **System Commands**: Execute any Windows command

### 🌐 Web Automation
- **Google Search**: Intelligent web searches
- **YouTube Control**: Search and play videos automatically
- **WhatsApp Messaging**: Send messages via WhatsApp Web
- **Gmail Integration**: Compose and send emails using Gmail API
- **Browser Control**: Uses your Chrome profile with saved logins

### 🤖 AI Integration
- **OpenAI GPT**: Advanced natural language understanding
- **Intent Recognition**: Understands complex voice commands
- **Context Awareness**: Extracts entities from speech
- **Fallback Processing**: Multiple layers of command interpretation

### 📱 Communication
- **WhatsApp Web**: Automated message sending
- **Gmail API**: Professional email composition
- **Contact Management**: Dynamic contact recognition

## 🛠️ Installation

### Prerequisites
```bash
Python 3.8+
Google Chrome Browser
Microphone and Speakers
```

### Setup
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
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration
EMAIL=your_email@gmail.com
PASSWORD=your_app_password

# Weather API
WEATHER_API_KEY=your_weather_api_key

# News API
NEWS_API_KEY=your_news_api_key
```

4. **Gmail API Setup**
- Place `credentials.json` in project root
- First run will authenticate and create `token.pickle`

## 🎯 Usage

### Starting JARVIS
```bash
python jarvis.py
```

Choose activation method:
1. **Wake Word Only**: Say "Jarvis" to activate
2. **Face Recognition + Wake Word**: Camera-based authentication

### Voice Commands

#### System Control
```
"open notepad"
"close chrome"
"take screenshot"
"what is the time"
"cpu usage"
"shutdown system"
```

#### Web Automation
```
"search python tutorials"
"youtube search machine learning"
"open google"
"search for AI news"
```

#### Communication
```
"send whatsapp message to John saying hello"
"email to manager about meeting"
"compose email"
```

#### Information
```
"tell me a joke"
"what's the weather"
"latest news"
"wikipedia artificial intelligence"
```

## 📁 Project Structure

```
J.A.R.V.I.S/
├── jarvis.py                 # Main application
├── helpers.py                # Utility functions
├── system_control.py         # System automation
├── web_automation.py         # Browser automation
├── ai_intent_recognition.py  # OpenAI integration
├── intent_recognition.py     # Rule-based intents
├── wake_word.py             # Voice activation
├── gmail_service.py         # Gmail API integration
├── news.py                  # News fetching
├── youtube.py               # YouTube automation
├── OCR.py                   # Optical character recognition
├── diction.py               # Dictionary functions
├── Face-Recognition/        # Face recognition module
├── Test/                    # Test files
├── credentials.json         # Gmail API credentials
├── requirements.txt         # Dependencies
└── .env                     # Environment variables
```

## 🔧 Configuration

### Chrome Profile
JARVIS uses your Chrome profile for seamless web automation:
- **Profile Path**: `C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Default`
- **Executable**: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Voice Settings
- **Language**: English (India)
- **Wake Word**: "Jarvis"
- **Voice**: Configurable male/female

## 🧪 Testing

Run comprehensive tests:
```bash
# Test all functions
python test_all_jarvis_functions.py

# Test system control
python test_system_control.py

# Test web automation
python test_web_automation.py

# Test OpenAI integration
python test_openai_key.py
```

## 📋 Dependencies

### Core Libraries
```
speech_recognition==3.10.4
pyttsx3==2.91
openai==0.28.1
selenium==4.15.2
webdriver-manager==4.0.1
```

### System Libraries
```
pyautogui==0.9.54
psutil==6.0.0
opencv-python
face_recognition
```

### Web & API
```
requests==2.32.3
beautifulsoup4==4.12.3
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
```

## 🔐 Security Features

- **Face Recognition**: Optional biometric authentication
- **Profile Isolation**: Separate Chrome profile for automation
- **API Key Management**: Secure environment variable storage
- **Safe App Control**: Whitelist-based application management

## 🚨 Troubleshooting

### Common Issues

**Chrome Profile Conflicts**
```bash
# Close all Chrome instances before running JARVIS
taskkill /f /im chrome.exe
```

**Voice Recognition Issues**
```python
# Adjust microphone settings in helpers.py
r.energy_threshold = 400  # Increase for noisy environments
r.pause_threshold = 0.8   # Decrease for faster response
```

**API Authentication**
```bash
# Delete token files and re-authenticate
rm token.pickle
python jarvis.py
```

## 🔮 Future Enhancements

### Planned Features
- [ ] Smart Home Integration (IoT devices)
- [ ] Calendar Management
- [ ] Advanced Scheduling
- [ ] Multi-language Support
- [ ] Mobile App Integration
- [ ] Cloud Synchronization
- [ ] Plugin System
- [ ] Voice Training
- [ ] Contextual Memory
- [ ] Advanced Security

### Technical Improvements
- [ ] Async Processing
- [ ] Database Integration
- [ ] REST API Interface
- [ ] Docker Containerization
- [ ] CI/CD Pipeline
- [ ] Performance Monitoring

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- OpenAI for GPT integration
- Google for Gmail API and Speech Recognition
- Selenium WebDriver community
- Python speech recognition libraries
- Face recognition algorithms


---

**Made with ❤️ by the JARVIS Team**