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
    def delete(self):
        ...
    
    def replay(self, content: str):
        from ..core import sendPost
        sendPost(f"channels/{self.channel.channel_id}/messages", {
            "content": content,
            "message_reference": {
                "channel_id": self.channel.channel_id,
                "guild_id": self.guild if self.guild == None else self.guild.guild_id,
                "message_id": self.message_id,
            }
        })