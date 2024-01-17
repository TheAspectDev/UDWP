from .types.Generator import getUser
from .types.User import User
from .types.Message import Message
from utils import send_json_request
import websocket, threading, json, time


MODULE_NAME = "UDWP"
TOKEN = "token"
OS = "windows"
BROWSER = "chrome"
DEVICE = "pc"
DEFAULT_OP = 2
MESSAGE_LISTENERS: list[callable] = []
PAYLOAD = {
    "op": DEFAULT_OP,
    "d": {
        "token": TOKEN,
        "properties": {
            "$os": OS,
            "$browser": BROWSER,
            "$device": DEVICE,
        }
    },
}


def on_message(func: function):
    def inner():
        MESSAGE_LISTENERS.append(func)
    inner()
    return f"{MODULE_NAME} Command - {func.__name__}"


def on_event(ws, event):
    event = json.loads(event)
    t = event.get('t')
    d = event.get('d')
    
    if t == "MESSAGE_CREATE" and d:
        for func in MESSAGE_LISTENERS:
            message = Message()
            author = getAuthor()
            
            func(Message)
        
def keepalive(interval, ws):
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": None
        }
        ws.send(json.dumps(heartbeatJSON))
def on_open(ws):
    print("Connection opened.")
    ws.send(json.dumps(PAYLOAD))
    heartbeat_interval = 40  # Set an initial value
    threading.Thread(target=keepalive, args=(heartbeat_interval, ws)).start()
    
ws_url = "wss://gateway.discord.gg/?v=6&encoding=json"
ws_app = websocket.WebSocketApp(ws_url, on_message=on_event)
ws_app.on_open = on_open
ws_app.run_forever()


