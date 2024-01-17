from websocket import WebSocketApp
from json import loads as jsonLoad, dumps as jsonDumps

def send_json_request(ws: WebSocketApp, request: any):
    ws.send(jsonDumps(request))
    
def recieve_json_response(ws: WebSocketApp):
    response = ws.recv()
    if response: 
        return jsonLoad(response)