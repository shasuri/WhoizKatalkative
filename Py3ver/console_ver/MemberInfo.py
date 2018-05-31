from enum import Enum


class MemberInfo(Enum):
    """Enumeration class to make easy to manage ChatMember attributes.
    """
    chat = 0
    talk = 1
    talkSize = 2
    emoticon = 3
    image = 4
    link = 5
    video = 6
    hashtag = 7
    file = 8
    address = 9
    voice = 10
    
