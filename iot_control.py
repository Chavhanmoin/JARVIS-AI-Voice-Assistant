import websocket
import json
import hmac
import hashlib
import time
import uuid
import threading
import ssl

# --- 🛑 CRITICAL: USE YOUR NEW, SECONDARY JARVIS CREDENTIALS HERE 🛑 ---
# Replace these with the NEW App Key and App Secret generated in Step 1
APP_KEY = "fb2c1853-925d-4807-9b78-9d9466512f25" 
APP_SECRET = "c0eb60f4-e4ba-412f-a18e-90f7cb165b42-f6f4af53-ebe5-437e-b3e3-ac91f48f63c9"

# --- Device IDs (UNCHANGED) ---
DEVICES = {
    "light": "67e2f69a947cbabd20e48169", 
    "fan": "67e2f6d2947cbabd20e481b4",
    "led": "67e2f6bb8ed485694cffde46"
}

# --- WebSocket URL (PROVEN TO WORK) ---
SINRIC_WS_URL = "wss://ws.sinric.pro" 
ws = None

# --- HMAC Signature Calculation Function ---
def get_signature(payload_json_string, app_secret):
    # Function remains the same
    return hmac.new(app_secret.encode('utf-8'), payload_json_string.encode('utf-8'), hashlib.sha256).hexdigest()

# --- Command Sending Function (Final Working WS Payload) ---
def send_command(device_name, state):
    global ws
    if ws is None or not hasattr(ws, 'sock') or ws.sock is None: 
        print("❌ Error: WebSocket not connected. Command not sent.")
        return

    device_id = DEVICES.get(device_name.lower())

    command_payload = {
        "deviceId": device_id,
        "action": "setPowerState",
        "value": {"state": state},
        "createdAt": f"{time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}",
        "replyToken": str(uuid.uuid4()),
        "type": "request",
        "clientId": "python-assistant-jarvis",
        "scope": "device"
    }

    payload_str = json.dumps(command_payload, separators=(',', ':'))
    signature = get_signature(payload_str, APP_SECRET)
    
    full_message = {
        "header": {"payloadVersion": 2, "signature": signature},
        "payload": command_payload
    }

    try:
        ws.send(json.dumps(full_message))
        print(f"✅ WS Command sent: {device_name} set to {state}")
    except Exception as e:
        print(f"❌ Failed to send WS command: {e}")
    time.sleep(0.5)

# --- WebSocket Handlers (UNCHANGED) ---
def on_message(ws_local, message):
    try:
        data = json.loads(message)
        if "payload" in data and "clientId" in data["payload"]:
            print(f"📩 From Sinric (Device Event): {data['payload']}")
        else:
            print(f"📩 {data}")
    except Exception as e:
        print(f"⚠️ Invalid message: {e} - Raw: {message}")

def on_error(ws_local, error):
    print(f"⚠️ Error: {error}")

def on_close(ws_local, close_status_code, close_msg):
    global ws
    ws = None
    print(f"🛑 Disconnected from Sinric Pro WebSocket. Code: {close_status_code}")

def on_open(ws_local):
    global ws
    ws = ws_local
    print("✅ Connected to Sinric Pro WebSocket")

# ---------- Connect to Sinric (PROVEN METHOD) ----------
def connect():
    global ws
    
    # CRITICAL: Using the LIST format for headers with the NEW credentials
    sinric_headers = [
        f"appkey:{APP_KEY}",
        f"deviceids:{','.join(DEVICES.values())}",
        f"apikey:{APP_KEY}",
        f"signature:{APP_SECRET}" 
    ]
    
    ws_app = websocket.WebSocketApp(
        SINRIC_WS_URL,
        header=sinric_headers,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error
    )
    
    wst = threading.Thread(
        target=ws_app.run_forever, 
        kwargs={'sslopt': {"cert_reqs": ssl.CERT_NONE}}
    )
    wst.daemon = True
    wst.start()
    
    print("Waiting for connection to stabilize...")
    start_time = time.time()
    while ws is None or not hasattr(ws, 'sock') or ws.sock is None:
        time.sleep(0.5) 
        if time.time() - start_time > 10: 
            print("❌ Connection failed after timeout.")
            return None
    
    print("Connection stabilized. Ready to send commands.")
    return ws_app

# --- Main Execution (UNCHANGED) ---
if __name__ == "__main__":
    
    ws_app = connect()
    
    if ws_app is None:
        print("Fatal error during connection. Cannot proceed.")
        exit()
    
    time.sleep(1) 
    
    print("\n--- Sending Test Commands via WebSocket ---")
    send_command("light", "On")
    time.sleep(3) 
    send_command("fan", "On")
    time.sleep(3)
    send_command("light", "Off")
    time.sleep(3)
    send_command("led", "On")
    time.sleep(3)
    
    print("\n--- Control Complete. Script is now listening for incoming events. Press Ctrl+C to exit. ---")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        if ws_app:
            ws_app.close()