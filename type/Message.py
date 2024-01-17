from .Channel import Channel
from .Guild import Guild
from .User import User


class PartialMessage:
    content: str
    pinned: bool
    mention_everyone: bool

class MessageParams(PartialMessage):
    author: User
    channel: Channel
    guild: Guild
    
class Message(MessageParams):
    def delete(self):
        ...
    
    def replay(self):
        ...