import websocket, json, threading
from time import sleep

def send_json_request(ws, request):
    ws.send(json.dumps(request))
    
def recieve_json_response(ws):
    response = ws.recv()
    if response: 
        return json.loads(response)
    
def heartbeat(interval, ws):
    while True:
        sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        
        
ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
event = recieve_json_response(ws)

heartbeat_interval = event["d"]["heartbeat_interval"] / 20000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))
token =                                                                                                                                                             "dQw4w9WgXcQ:djEwzQ6CjL9AxIfOaQz3XGs2FbOx+AF5oZUgXCoYI7h+o8ct9MN4YIF88V8rUFUe/m6u7DunxtNwpCOIkB0hp2NXwY9l9t0uR0OxjqNr7jnFOYDlTXsYHH3JYZhSD0wi+ciGlyE="

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


send_json_request(ws, str(payload))

while True:
    event = recieve_json_response(ws)
    
    print(event)
    
    try:
        print(f"{event['d']['author']['username']}: {event['d']['content']}")
        op_code = event['op']
        if op_code == 11:
            print("heartbeat recieved")
    except: pass