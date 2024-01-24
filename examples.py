from UDWP.core import Client
from UDWP.type import Message
import asyncio

client = Client(
    token="ODUxODg0OTA0NzU3MzI5OTcx.GPwbKt.oBakpZDB-aFzJyoIK-bvlJ9eK6WEEd52Ffjyao"
)
@client.on_start
async def Start():
    print("Client has connected successfully!")
    
@client.on_message
async def onMessage(e: Message):
    print(e.content)
    
    
client.run()