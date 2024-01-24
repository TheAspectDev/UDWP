from UDWP.core import Client
from UDWP.type import Message
import asyncio

client = Client(
    token="your_token_here"
)
@client.on_start
async def Start():
    print("Client has connected successfully!")
    
@client.on_message
async def onMessage(e: Message):
    print(e.content)
    
    
client.run()