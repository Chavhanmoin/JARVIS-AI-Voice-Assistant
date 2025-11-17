import requests
import json
import time
import base64
from helpers import speak

# Sinric Pro credentials
EMAIL = "moin.chavhan64@gmail.com"
PASSWORD = "579B8mZ39@RL@s5"

# Device IDs
DEVICE_IDS = {
    "fan": "67e2f6d2947cbabd20e481b4",
    "led": "67e2f6bb8ed485694cffde46", 
    "light": "67e2f69a947cbabd20e48169"
}

class SinricIoTController:
    def __init__(self):
        self.access_token = None
        self.base_url = "https://api.sinric.pro/api/v1"
        
    def login(self):
        """Login to get access token"""
        credentials = f"{EMAIL}:{PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {'client_id': 'jarvis-app'}
        
        try:
            response = requests.post(f"{self.base_url}/auth", headers=headers, data=data)
            result = response.json()
            
            if result.get('success'):
                self.access_token = result.get('accessToken')
                return True
            return False
        except:
            return False
    
    def control_device(self, device_name, state):
        """Control device via REST API"""
        if not self.access_token and not self.login():
            return False
            
        if device_name not in DEVICE_IDS:
            return False
            
        device_id = DEVICE_IDS[device_name]
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        params = {
            'clientId': 'jarvis-app',
            'type': 'request',
            'createdAt': int(time.time() * 1000),
            'action': 'setPowerState',
            'value': json.dumps({"state": "On" if state else "Off"})
        }
        
        try:
            url = f"{self.base_url}/devices/{device_id}/action"
            response = requests.get(url, headers=headers, params=params)
            result = response.json()
            return result.get('success', False)
        except:
            return False

# Global instance
_iot_controller = None

def get_iot_controller():
    global _iot_controller
    if not _iot_controller:
        _iot_controller = SinricIoTController()
    return _iot_controller

def initialize_iot():
    """Initialize IoT connection"""
    controller = get_iot_controller()
    return controller.login()

def control_iot_device(device_name, action):
    """Control IoT device - main interface"""
    controller = get_iot_controller()
    
    # Parse action
    if action.lower() in ["on", "turn on", "switch on", "enable"]:
        state = True
    elif action.lower() in ["off", "turn off", "switch off", "disable"]:
        state = False
    else:
        speak("Please say on or off")
        return False
    
    if controller.control_device(device_name, state):
        action_word = "turned on" if state else "turned off"
        speak(f"{device_name} {action_word}")
        return True
    else:
        speak(f"Failed to control {device_name}")
        return False

def get_device_status():
    """Get status of IoT devices"""
    controller = get_iot_controller()
    if controller.access_token or controller.login():
        return "IoT system connected"
    else:
        return "IoT system disconnected"