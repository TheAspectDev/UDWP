import json
import asyncio
import websockets
from .mtypes.Generator import *
import requests

MODULE_NAME = "UDWP"
WS_URL = "wss://gateway.discord.gg/?v=6&encoding=json"
DISCORD_ENDPOINT = "https://discord.com/api/v9/"
OS = "windows"
BROWSER = "chrome"
DEVICE = "pc"
DEFAULT_OP = 2
MESSAGE_LISTENERS = []
MESSAGE_LISTENERS_FUNCTIONS = []
HB_INTERVAL = 40
HB_SETTINGS = {
    "op": 1,
    "d": None
}

req_session = requests.Session()

def on_event(event: dict):
    t = event.get('t')
    d = event.get('d')

    if t == "MESSAGE_CREATE" and d:
        for func in MESSAGE_LISTENERS:
             task = asyncio.create_task(func(getMessage(d)))
             MESSAGE_LISTENERS_FUNCTIONS.append(task)

def sendPost(link: str, payload: dict):
    FULL_URL = DISCORD_ENDPOINT + link
    if 'Authorization' in req_session.headers:
        return req_session.post(
            FULL_URL,
            json=payload,
        )
    else:
        raise "Authorization Error"

async def keepalive(interval: int, ws: websockets):
    while True:
        await ws.send(json.dumps(HB_SETTINGS))
        await asyncio.sleep(interval)

def on_message(func: callable):
    MESSAGE_LISTENERS.append(func)
    return func

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

    async def run(self):
        req_session.headers = {
            "Authorization": self.token
        }
        async with websockets.connect(WS_URL, max_size=None) as ws:
            await self.__on_open(ws)
            while True:
                on_event(json.loads(await ws.recv()))