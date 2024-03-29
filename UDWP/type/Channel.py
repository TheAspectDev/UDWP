from .Guild import Guild

class PartialChannel:
    channel_id: int

class ChannelParams(PartialChannel):
    guild: Guild | None
    
class Channel(ChannelParams):
    def delete(self):
        ...
        
    def send(self, content: str):
        from ..core import make_request
        make_request("post", f"channels/{self.channel_id}/messages", {
            "content": content,
        })