import websocket, threading, json, time
from .type.Generator import *

MODULE_NAME = "UDWP"
WS_URL = "wss://gateway.discord.gg/?v=6&encoding=json"
OS = "windows"
BROWSER = "chrome"
DEVICE = "pc"
DEFAULT_OP = 2
HB_INTERVAL = 40 
MESSAGE_LISTENERS = []

def on_event(ws, event):
    event = json.loads(event)
    t = event.get('t')
    d = event.get('d')
    
    if t == "MESSAGE_CREATE" and d:
        for func in MESSAGE_LISTENERS:
            func(getMessage(d))
        
def keepalive(interval, ws):
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": None
        }
        ws.send(json.dumps(heartbeatJSON))
    
def on_message(func):
    MESSAGE_LISTENERS.append(func)
    return func

class Client:
    def __init__(self, token: str):
        self.ws = websocket.WebSocketApp(WS_URL, on_message=on_event)
        self.token = token
        self.ws.on_open = self.__on_open
    def __on_open(self, ws):
        payload = {
            "op": DEFAULT_OP,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": OS,
                    "$browser": BROWSER,
                    "$device": DEVICE,
                }
            },
        }
        ws.send(json.dumps(payload))
        threading.Thread(target=keepalive, args=(HB_INTERVAL, ws)).start()    
    
    def run(self):   
        self.ws.run_forever()