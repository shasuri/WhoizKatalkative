from enum import Enum


class MemberInfo(Enum):
    """Enumeration class to make easy to manage ChatMember attributes.
    """
    chat = 0
    talk = 1
    emoticon = 2
    image = 3
    link = 4
    video = 5
    hashtag = 6
    file = 7
    address = 8
    voice = 9
    talkSize = 10
