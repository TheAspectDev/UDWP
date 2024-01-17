from .Channel import Channel
from .User import User


class PartialGuild:
    guild_id: int
    # name: str
    # channels = list[Channel]

class GuildParams(PartialGuild):
    ...
    
class Guild(GuildParams):
    def delete(self):
        ...
    
    def replay(self):
        ...