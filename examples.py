from UDWP.core import Client
from UDWP.type import Message

client = Client(
    token="your_token_here"
)
@client.on_start
async def start():
    print("Client has connected successfully!")
    
@client.on_message
async def msgHandler(e: Message):
    print(e.content)    
    
client.run()