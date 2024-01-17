import websocket, threading, json, time
token =                                                                                                                                                          "ODUxODg0OTA0NzU3MzI5OTcx.GXm39c.zjLCmIVR7YrymW4sRtRoxjXOQ9uZYkyBvcGHc0"
payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc",
        }
    },
}
def on_message(ws, event):
    event = json.loads(event)
    t = event.get('t')
    d = event.get('d')
    
    if t == "MESSAGE_CREATE" and d:
        print(d)
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
    ws.send(json.dumps(payload))
    heartbeat_interval = 40  # Set an initial value
    threading.Thread(target=keepalive, args=(heartbeat_interval, ws)).start()
    
ws_url = "wss://gateway.discord.gg/?v=6&encoding=json"
ws_app = websocket.WebSocketApp(ws_url, on_message=on_message)
ws_app.on_open = on_open
ws_app.run_forever()