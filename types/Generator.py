from .Channel import Channel
from .Guild import Guild
from .User import User
from .Message import Message


def getAuthor(data) -> User:
    username = data['author']['username']
    id = data['author']['id']
    global_name = data['author']['global_name']
    avatar = data['author']['avatar']
    
    user = User()
    user.username = username
    user.id = id
    user.global_name = global_name
    user.avatar = avatar
    
    return user

def getGuild(data) -> Guild:
    guide_id = data['guide_id']
    
    guild = Guild()
    guild.guild_id = guide_id
    
    return guild

def getChannel(data) -> Channel:
    channel_id = data['channel_id']
    guide = getGuild(data)
    
    channel = Channel()
    channel.channel_id = channel_id
    channel.guild = guide
    
    return guide

def getMessage(data) -> Message:
    channel = getChannel(data)
    guild = getGuild(data)
    author = getAuthor(data)
    content = data['content']
    mention_everyone = data['mention_everyone']
    pinned = data['pinned']
    
    message = Message()
    message.channel = channel
    message.author = author
    message.guild = guild
    message.content = content
    message.mention_everyone = mention_everyone
    message.pinned = pinned
    

    return message