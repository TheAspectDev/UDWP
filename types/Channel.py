from .Guide import Guide

class PartialChannel:
    channel_id: int

class ChannelParams(PartialChannel):
    guild: Guide
    
class Channel(ChannelParams):
    def delete(self):
        ...