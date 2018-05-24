from MemberInfo import MemberInfo
from set_user_name import set_user_name


def print_chat_info(chat_room):
    """Print the information of the chatting room and members listed in chat_room.memberList.
    
    Args:
        chat_room (ChatRoom): ChatRoom instance of the chatting room.

    """
    set_user_name(chat_room)

    print("Chatting Title : " + chat_room.title)
    print("Chatting Member Number : %d" % chat_room.memberNum)
    print("Log is saved at " + str(chat_room.logSaveDate))

    for single_member in chat_room.memberList:
        print("\n" + single_member.name + "'s Information : ")
        print("\tInvited date : " + str(single_member.invitedDate))
        print("\tchatted %d times" % single_member.infoList[MemberInfo.chat.value])
        print("\ttalked %d times" % single_member.infoList[MemberInfo.talk.value])
        print("\ttalked %d letters" % single_member.infoList[MemberInfo.talkSize.value])
        print("\tlinked %d pages" % single_member.infoList[MemberInfo.link.value])
        print("\tused %d emoticons" % single_member.infoList[MemberInfo.emoticon.value])
        print("\tuploaded %d images" % single_member.infoList[MemberInfo.image.value])
        print("\ttaged %d hashtags" % single_member.infoList[MemberInfo.hashtag.value])
        print("\tuploded %d etc files" % single_member.infoList[MemberInfo.file.value])
