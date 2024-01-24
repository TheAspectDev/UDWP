import json
import asyncio
from typing import Literal
import websockets
from .type.Generator import *
import requests
from time import sleep as tsleep
import threading

MODULE_NAME = "UDWP"
WS_URL = "wss://gateway.discord.gg/?v=6&encoding=json"
DISCORD_ENDPOINT = "https://discord.com/api/v9/"
OS = "windows"
BROWSER = "chrome"
DEVICE = "pc"
DEFAULT_OP = 2
MESSAGE_LISTENERS = []
MESSAGE_LISTENERS_FUNCTIONS = []
TASK_LISTENERS = []
HB_INTERVAL = 40
HB_SETTINGS = {
    "op": 1,
    "d": None
}
req_session = requests.Session()

def on_event(event: dict):
    t = event.get('t')
    d = event.get('d')
    op = event.get('op')
    
    if t == "MESSAGE_CREATE" and d:
        for func in MESSAGE_LISTENERS:
            if func[1] == "MESSAGE_CREATE":
                task = asyncio.create_task(func[0](getMessage(d)))
                MESSAGE_LISTENERS_FUNCTIONS.append([task, "MESSAGE_CREATE"])
    
    if op == 10:
        for func in MESSAGE_LISTENERS:
            if func[1] == "CONNECTION_CREATE":
                task = asyncio.create_task(func[0]())
                MESSAGE_LISTENERS_FUNCTIONS.append([task, "CONNECTION_CREATE"])
        for task in TASK_LISTENERS:
            task()
        

def make_request(method: Literal["get",
                                "post",
                                "patch",
                                "delete"],
                 link: str,
                 payload=None):
    
    full_url = DISCORD_ENDPOINT + link
    if 'Authorization' not in req_session.headers:
        raise Exception("Authorization header is missing.")

    if method == 'get':
        return req_session.get(full_url)
    elif method == 'post':
        return req_session.post(full_url, json=payload)
    elif method == 'patch':
        return req_session.patch(full_url, json=payload)
    elif method == 'delete':
        return req_session.delete(full_url)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

async def keepalive(interval: int, ws: websockets):
    while True:
        await ws.send(json.dumps(HB_SETTINGS))
        await asyncio.sleep(interval)

class Client:
    def __init__(self, token: str):
        self.token = token

    async def __on_open(self, ws: websockets):
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
        await ws.send(json.dumps(payload))
        asyncio.create_task(keepalive(HB_INTERVAL, ws))
        
    def on_start(self, func: callable):
        MESSAGE_LISTENERS.append([func, "CONNECTION_CREATE"])
        return func
    def on_message(self, func: callable):
        MESSAGE_LISTENERS.append([func, "MESSAGE_CREATE"])
        return func

    async def create_task(self, func):
        task = asyncio.create_task(func)
        return task

    async def __run(self):
        req_session.headers = {
            "Authorization": self.token
        }
        async with websockets.connect(WS_URL, max_size=None) as ws:
            await self.__on_open(ws)
            while True:
                on_event(json.loads(await ws.recv()))
                
        
    def run(self):
        asyncio.run(self.__run())    