from chat_member_searcher import chat_member_searcher
from file_checker import file_checker
from talk_line_checker import talk_line_checker
from MemberInfo import MemberInfo
from head_element_checker import head_element_checker
from ChatMember import ChatMember


def chat_line_checker(chat_line, chat_room):
    """Parse the chatter and chatting contents and check there is a solo content which can not contains other contents.
    
    Args:
        chat_line (str): The line to be parsed and checked.
        chat_room (ChatMember): ChatMember instance of who chat the link_line.

    Examples:
        `Jack : #Simple is better than complex.`
        
    """
    content_divider_pos = chat_line.find(' : ')

    chatter_name = chat_line[:content_divider_pos]

    chatting = chat_line[content_divider_pos + 3:]

    chatter = chat_member_searcher(chat_room.memberList, chatter_name)
    if not chatter:
        chatter = ChatMember(chatter_name)
        chat_room.append_member(chatter)

    chat_room.set_chatted_member(chatter)

    chatter.info_counter(MemberInfo.chat)

    if chatting == '<사진>\n':
        chatter.info_counter(MemberInfo.image)

    elif chatting == '<동영상>\n':
        chatter.info_counter(MemberInfo.video)

    elif chatting.find('#') == 0:
        chatter.info_counter(MemberInfo.hashtag)

    elif chatting.find('<연락처') == 0:
        chatter.info_counter(MemberInfo.address)

    elif chatting == '<음성메시지>\n':
        chatter.info_counter(MemberInfo.voice)

    elif file_checker(chatting):
        chatter.info_counter(MemberInfo.file)

    else:
        chatting = head_element_checker(chatting, chatter)

        if chatting != '\n':
            chatter.info_counter(MemberInfo.talk)
            talk_line_checker(chatting, chatter)
