from .Channel import Channel
from .Guild import Guild
from .User import User


class PartialMessage:
    message_id: int
    content: str
    pinned: bool
    mention_everyone: bool

class MessageParams(PartialMessage):
    author: User
    channel: Channel
    guild: Guild | None
    
    
class Message(MessageParams):
    def edit(self, content: str):
        from ..core import make_request
        data = make_request("patch",f"channels/{self.channel.channel_id}/messages/{self.message_id}", {
            "content": content,
        })
        if (data.status_code != 200):
            raise Exception("Request Error")
        
        return data
    
    def replay(self, content: str):
        from ..core import make_request
        data = make_request("post" ,f"channels/{self.channel.channel_id}/messages", {
            "content": content,
            "message_reference": {
                "channel_id": self.channel.channel_id,
                "guild_id": self.guild if self.guild == None else self.guild.guild_id,
                "message_id": self.message_id,
            }
        })
        
        if (data.status_code != 200):
            raise Exception("Request Error")
        
        return data
        
    def delete(self):
        from ..core import make_request
        data = make_request("delete", f"channels/{self.channel.channel_id}/messages/{self.message_id}")
        
        if (data.status_code not in [200, 204]):
            raise Exception(data.json()['message'])
        
        return data
