from .Guild import Guild

class PartialChannel:
    channel_id: int

class ChannelParams(PartialChannel):
    guild: Guild
    
class Channel(ChannelParams):
    def delete(self):
        ...