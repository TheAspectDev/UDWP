# UDWP	
This library is under development and shouldn't be used in production.	
- User Discord Wrapper written in Python.	

## Getting Started
Download the library using:
```shell
pip install git+https://github.com/TheAspectDev/UDWP.git
```
Code your own self-bot :
```py	
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
```	