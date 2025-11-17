# Software Requirements Specification (SRS)
# J.A.R.V.I.S - AI Voice Assistant System

**Version**: 3.0  
**Date**: November 2024  
**Authors**: JARVIS Development Team  
**Document Type**: Software Requirements Specification

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [System Architecture](#5-system-architecture)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Technical Specifications](#7-technical-specifications)
8. [Data Flow Diagrams](#8-data-flow-diagrams)
9. [Use Case Diagrams](#9-use-case-diagrams)
10. [Database Design](#10-database-design)
11. [Security Requirements](#11-security-requirements)
12. [Testing Requirements](#12-testing-requirements)

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for J.A.R.V.I.S (Just A Rather Very Intelligent System), an AI-powered voice assistant designed to provide comprehensive system automation, web control, communication management, and IoT device control capabilities.

### 1.2 Scope
J.A.R.V.I.S is a desktop-based voice assistant that integrates multiple technologies to provide:
- Voice-controlled system automation
- Web browser automation
- Email and calendar management
- WhatsApp messaging
- IoT device control
- Information retrieval services

### 1.3 Definitions and Acronyms
- **AI**: Artificial Intelligence
- **API**: Application Programming Interface
- **IoT**: Internet of Things
- **NLP**: Natural Language Processing
- **TTS**: Text-to-Speech
- **STT**: Speech-to-Text
- **REST**: Representational State Transfer
- **OAuth**: Open Authorization
- **GUI**: Graphical User Interface

### 1.4 References
- OpenAI GPT API Documentation
- Google APIs Documentation
- Sinric Pro API Documentation
- Python Speech Recognition Library
- Selenium WebDriver Documentation

---

## 2. Overall Description

### 2.1 Product Perspective
J.A.R.V.I.S is a standalone desktop application that acts as a central hub for various automation tasks. It integrates with multiple external services and APIs to provide comprehensive voice-controlled functionality.

### 2.2 Product Functions
- **Voice Recognition**: Convert speech to text commands
- **Natural Language Processing**: Understand user intent
- **System Control**: Manage Windows applications and settings
- **Web Automation**: Control web browsers and perform searches
- **Communication**: Send emails and WhatsApp messages
- **Calendar Management**: Schedule meetings and appointments
- **IoT Control**: Manage smart home devices
- **Information Services**: Provide weather, news, and definitions

### 2.3 User Classes
- **Primary Users**: Individual users seeking voice-controlled automation
- **Technical Users**: Developers and system administrators
- **End Users**: Non-technical users requiring simple voice commands

### 2.4 Operating Environment
- **Operating System**: Windows 10/11
- **Python Version**: 3.8+
- **Browser**: Google Chrome
- **Hardware**: Microphone, speakers, internet connection
- **Memory**: Minimum 4GB RAM
- **Storage**: 500MB free space

---

## 3. System Features

### 3.1 Voice Recognition and Processing

#### 3.1.1 Description
The system shall recognize voice commands and convert them to actionable instructions.

#### 3.1.2 Functional Requirements
- **FR-001**: System shall detect wake word "Jarvis"
- **FR-002**: System shall convert speech to text using Google Speech Recognition
- **FR-003**: System shall process natural language using OpenAI GPT
- **FR-004**: System shall provide voice feedback using TTS
- **FR-005**: System shall handle multiple accents and speech patterns

### 3.2 System Automation

#### 3.2.1 Description
The system shall control Windows applications and system settings.

#### 3.2.2 Functional Requirements
- **FR-006**: System shall open any Windows application by name
- **FR-007**: System shall close running applications
- **FR-008**: System shall adjust system volume and brightness
- **FR-009**: System shall capture screenshots
- **FR-010**: System shall provide system information (CPU, battery)
- **FR-011**: System shall create and manage files/folders

### 3.3 Web Automation

#### 3.3.1 Description
The system shall automate web browser operations.

#### 3.3.2 Functional Requirements
- **FR-012**: System shall perform Google searches
- **FR-013**: System shall search and play YouTube videos
- **FR-014**: System shall open specific websites
- **FR-015**: System shall maintain browser sessions
- **FR-016**: System shall handle browser authentication

### 3.4 Communication Management

#### 3.4.1 Description
The system shall manage email and messaging communications.

#### 3.4.2 Functional Requirements
- **FR-017**: System shall compose and send emails via Gmail API
- **FR-018**: System shall send WhatsApp messages via desktop app
- **FR-019**: System shall extract recipient and message from voice commands
- **FR-020**: System shall handle contact recognition
- **FR-021**: System shall provide delivery confirmation

### 3.5 Calendar Integration

#### 3.5.1 Description
The system shall manage calendar events and scheduling.

#### 3.5.2 Functional Requirements
- **FR-022**: System shall create calendar events
- **FR-023**: System shall parse date and time from natural language
- **FR-024**: System shall integrate with Google Calendar API
- **FR-025**: System shall handle recurring events
- **FR-026**: System shall provide event reminders

### 3.6 IoT Device Control

#### 3.6.1 Description
The system shall control IoT devices through Sinric Pro platform.

#### 3.6.2 Functional Requirements
- **FR-027**: System shall control individual devices (fan, light, LED)
- **FR-028**: System shall control all devices simultaneously
- **FR-029**: System shall authenticate with Sinric Pro API
- **FR-030**: System shall provide device status feedback
- **FR-031**: System shall handle device connection failures

### 3.7 Information Services

#### 3.7.1 Description
The system shall provide information retrieval services.

#### 3.7.2 Functional Requirements
- **FR-032**: System shall provide weather information
- **FR-033**: System shall fetch latest news headlines
- **FR-034**: System shall provide word definitions
- **FR-035**: System shall search Wikipedia
- **FR-036**: System shall tell jokes and entertainment content

### 3.8 Memory and Learning

#### 3.8.1 Description
The system shall remember and learn from user interactions.

#### 3.8.2 Functional Requirements
- **FR-037**: System shall remember last executed commands
- **FR-038**: System shall repeat previous commands on request
- **FR-039**: System shall store user preferences
- **FR-040**: System shall maintain session history

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- **Voice Interface**: Primary interaction method
- **Console Interface**: System status and debugging
- **GUI Overlays**: Volume/brightness indicators

### 4.2 Hardware Interfaces
- **Microphone**: Audio input for voice commands
- **Speakers**: Audio output for responses
- **Display**: Visual feedback and overlays

### 4.3 Software Interfaces
- **OpenAI API**: Natural language processing
- **Google APIs**: Gmail, Calendar, Speech Recognition
- **Sinric Pro API**: IoT device control
- **Weather API**: Weather information
- **News API**: News headlines

### 4.4 Communication Interfaces
- **HTTP/HTTPS**: API communications
- **WebSocket**: Real-time IoT communication
- **OAuth2**: Secure authentication
- **REST**: API data exchange

---

## 5. System Architecture

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    J.A.R.V.I.S System                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ Voice   │   │   AI    │   │ System  │
   │ Layer   │   │ Engine  │   │ Control │
   └────┬────┘   └────┬────┘   └────┬────┘
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ Speech  │   │ OpenAI  │   │ Windows │
   │ Recog   │   │   GPT   │   │   API   │
   └─────────┘   └─────────┘   └─────────┘
```

### 5.2 Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Controller                         │
│                      (jarvis.py)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐        ┌────▼────┐       ┌────▼────┐
│ Voice │        │   AI    │       │ System  │
│Module │        │ Module  │       │ Module  │
└───┬───┘        └────┬────┘       └────┬────┘
    │                 │                 │
┌───▼───┐        ┌────▼────┐       ┌────▼────┐
│helpers│        │ai_intent│       │ system_ │
│  .py  │        │recog.py │       │control  │
└───────┘        └─────────┘       └─────────┘
```

### 5.3 Data Flow Architecture

```
Voice Input → Speech Recognition → NLP Processing → Intent Classification
     ↓                                                        ↓
Command Execution ← Action Selection ← Entity Extraction ← Response
     ↓
Voice/Visual Feedback
```

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements
- **Response Time**: Voice commands processed within 2-3 seconds
- **Throughput**: Handle 100+ commands per session
- **Memory Usage**: Maximum 500MB RAM usage
- **CPU Usage**: Maximum 20% CPU utilization during idle

### 6.2 Reliability Requirements
- **Availability**: 99% uptime during active sessions
- **Error Recovery**: Graceful handling of API failures
- **Fault Tolerance**: Continue operation with partial service failures
- **Data Integrity**: Maintain command history and preferences

### 6.3 Usability Requirements
- **Learning Curve**: New users productive within 10 minutes
- **Voice Recognition**: 95% accuracy for clear speech
- **Response Clarity**: Clear, natural voice responses
- **Error Messages**: Helpful error feedback

### 6.4 Security Requirements
- **Authentication**: Secure OAuth2 implementation
- **Data Protection**: Encrypted credential storage
- **API Security**: Secure API key management
- **Privacy**: No sensitive data logging

### 6.5 Compatibility Requirements
- **Operating System**: Windows 10/11 compatibility
- **Browser**: Chrome 90+ support
- **Python**: Python 3.8+ compatibility
- **Hardware**: Standard PC hardware support

---

## 7. Technical Specifications

### 7.1 Technology Stack

#### 7.1.1 Core Technologies
```
Language: Python 3.8+
Speech Recognition: Google Speech Recognition API
Text-to-Speech: pyttsx3
Natural Language Processing: OpenAI GPT-3.5/4
```

#### 7.1.2 Web Technologies
```
Browser Automation: Selenium WebDriver
HTTP Client: Requests library
Web Scraping: BeautifulSoup4
Chrome Driver: WebDriver Manager
```

#### 7.1.3 APIs and Services
```
OpenAI API: Natural language processing
Google Gmail API: Email functionality
Google Calendar API: Calendar management
Sinric Pro API: IoT device control
Weather API: Weather information
News API: News headlines
```

#### 7.1.4 System Integration
```
GUI Automation: PyAutoGUI
System Information: psutil
Windows APIs: win32api, win32gui
File Operations: os, pathlib
```

### 7.2 Dependencies

#### 7.2.1 Core Dependencies
```python
speech_recognition==3.10.4
pyttsx3==2.91
openai==1.13.3
requests==2.32.3
selenium==4.25.0
```

#### 7.2.2 System Dependencies
```python
pyautogui==0.9.54
psutil==6.0.0
pyaudio==0.2.14
```

#### 7.2.3 API Dependencies
```python
google-auth==2.34.0
google-auth-oauthlib==1.2.1
google-api-python-client==2.143.0
```

---

## 8. Data Flow Diagrams

### 8.1 Level 0 DFD (Context Diagram)

```
                    ┌─────────────┐
                    │    User     │
                    └──────┬──────┘
                           │ Voice Commands
                           ▼
    ┌──────────────────────────────────────────┐
    │                                          │
    │            J.A.R.V.I.S                  │
    │         Voice Assistant                  │
    │                                          │
    └─────┬────────────────────────────────┬───┘
          │                                │
          ▼                                ▼
    ┌──────────┐                    ┌──────────┐
    │ External │                    │ System   │
    │ Services │                    │Resources │
    └──────────┘                    └──────────┘
```

### 8.2 Level 1 DFD (System Overview)

```
Voice Input → [Voice Recognition] → [NLP Processing] → [Command Router]
                                                            │
                    ┌───────────────────────────────────────┼───────────────┐
                    │                                       │               │
                    ▼                                       ▼               ▼
            [System Control] ← → [Web Automation] ← → [Communication] ← → [IoT Control]
                    │                                       │               │
                    ▼                                       ▼               ▼
            Windows System                              Gmail/WhatsApp   Smart Devices
```

### 8.3 Level 2 DFD (Detailed Process Flow)

```
[Voice Input] → [Speech-to-Text] → [Intent Recognition] → [Entity Extraction]
                                                               │
                    ┌──────────────────────────────────────────┼──────────────┐
                    │                                          │              │
                    ▼                                          ▼              ▼
            [App Control] ← → [File Management] ← → [Email Service] ← → [IoT Service]
                    │                                          │              │
                    ▼                                          ▼              ▼
            [Response Gen] ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
                    │
                    ▼
            [Voice Output]
```

---

## 9. Use Case Diagrams

### 9.1 Primary Use Cases

```
                    ┌─────────────┐
                    │    User     │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│Voice Control│    │System Auto  │    │Communication│
│             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│Web Control  │    │IoT Control  │    │Information  │
│             │    │             │    │Services     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 9.2 System Control Use Cases

```
User → Open Application
User → Close Application
User → Adjust Volume
User → Change Brightness
User → Take Screenshot
User → Get System Info
User → File Management
```

### 9.3 Communication Use Cases

```
User → Send Email
User → Send WhatsApp Message
User → Schedule Meeting
User → Create Calendar Event
User → Contact Management
```

---

## 10. Database Design

### 10.1 Data Storage Structure

#### 10.1.1 Memory Storage (memory.json)
```json
{
  "last_command": {
    "intent": "string",
    "details": "object",
    "timestamp": "datetime"
  },
  "user_preferences": {
    "voice_speed": "integer",
    "default_browser": "string",
    "preferred_news_source": "string"
  }
}
```

#### 10.1.2 Dictionary Data (data.json)
```json
{
  "word": ["definition1", "definition2"],
  "term": ["meaning1", "meaning2"]
}
```

#### 10.1.3 Configuration Data (.env)
```
OPENAI_API_KEY=string
EMAIL=string
PASSWORD=string
WEATHER_API_KEY=string
NEWS_API_KEY=string
```

### 10.2 Token Management

#### 10.2.1 Gmail Token (token.json)
```json
{
  "token": "string",
  "refresh_token": "string",
  "token_uri": "string",
  "client_id": "string",
  "client_secret": "string",
  "scopes": ["array"]
}
```

#### 10.2.2 Calendar Token (calendar_token.pickle)
- Binary pickle file containing OAuth2 credentials
- Automatically refreshed when expired

---

## 11. Security Requirements

### 11.1 Authentication and Authorization
- **OAuth2 Implementation**: Secure Google API authentication
- **Token Management**: Encrypted token storage
- **API Key Protection**: Environment variable storage
- **Session Management**: Secure session handling

### 11.2 Data Protection
- **Credential Encryption**: Secure credential storage
- **API Communication**: HTTPS for all API calls
- **Local Data Security**: Protected local file access
- **Privacy Compliance**: No sensitive data logging

### 11.3 Access Control
- **Application Whitelisting**: Safe application execution
- **Command Validation**: Input sanitization
- **File System Protection**: Restricted file operations
- **Network Security**: Secure API communications

### 11.4 Error Handling
- **Graceful Failures**: No sensitive data in error messages
- **Logging Security**: Sanitized log outputs
- **Exception Handling**: Secure error recovery
- **Audit Trail**: Command execution logging

---

## 12. Testing Requirements

### 12.1 Unit Testing
- **Module Testing**: Individual component testing
- **Function Testing**: Core function validation
- **API Testing**: External service integration testing
- **Error Testing**: Exception handling validation

### 12.2 Integration Testing
- **System Integration**: Component interaction testing
- **API Integration**: External service integration
- **Hardware Integration**: Microphone/speaker testing
- **Browser Integration**: Web automation testing

### 12.3 System Testing
- **End-to-End Testing**: Complete workflow testing
- **Performance Testing**: Response time validation
- **Load Testing**: Multiple command handling
- **Stress Testing**: Resource usage validation

### 12.4 User Acceptance Testing
- **Voice Recognition Testing**: Accuracy validation
- **Command Processing**: Intent recognition testing
- **Response Quality**: Output validation
- **Usability Testing**: User experience validation

### 12.5 Test Cases

#### 12.5.1 Voice Recognition Tests
```
TC-001: Wake word detection accuracy
TC-002: Command recognition in noisy environment
TC-003: Multiple accent handling
TC-004: Long command processing
TC-005: Interrupted command handling
```

#### 12.5.2 System Control Tests
```
TC-006: Application opening/closing
TC-007: Volume/brightness control
TC-008: File management operations
TC-009: System information retrieval
TC-010: Screenshot functionality
```

#### 12.5.3 Communication Tests
```
TC-011: Email composition and sending
TC-012: WhatsApp message sending
TC-013: Calendar event creation
TC-014: Contact recognition
TC-015: Message delivery confirmation
```

#### 12.5.4 IoT Control Tests
```
TC-016: Individual device control
TC-017: Multiple device control
TC-018: Device status feedback
TC-019: Connection failure handling
TC-020: Authentication validation
```

---

## Appendices

### Appendix A: API Documentation References
- OpenAI API: https://platform.openai.com/docs
- Google APIs: https://developers.google.com/apis-explorer
- Sinric Pro API: https://sinric.pro/api-documentation

### Appendix B: Installation Guides
- Python Installation: https://python.org/downloads
- Chrome WebDriver: https://chromedriver.chromium.org
- Google API Setup: https://console.developers.google.com

### Appendix C: Configuration Examples
- Environment variables setup
- Google API credentials configuration
- Sinric Pro device setup

### Appendix D: Troubleshooting Guide
- Common installation issues
- API authentication problems
- Voice recognition troubleshooting
- Performance optimization tips

---

**Document Version**: 3.0  
**Last Updated**: November 2024  
**Review Date**: December 2024  
**Approved By**: JARVIS Development Team