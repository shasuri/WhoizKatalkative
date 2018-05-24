from ChatMember import ChatMember
from chat_member_searcher import chat_member_searcher


def invite_line_checker(invite_line, invite_chat_room, invite_date):
    """Check the inviting line and append the ChatMember instance who is in the inviting line on the member list.
    
    Args:
        invite_line (str): Inviting line which is checked by line_type_checker function.
        invite_chat_room (ChatRoom): ChatRoom instance of the chatting room.
        invite_date (datetime.datetime): datetime.datetime instance of the inviting date.
    
    Examples:
        `Jack님이 Mary님, Jill님과 Cindy님을 초대했습니다.`

    """

    invite_line = invite_line.split('님')
    invite_line.pop()  # Delete the useless part.

    member_list = invite_chat_room.memberList

    for dataIndex in range(len(invite_line)):
        if dataIndex != 0:
            space_pos = invite_line[dataIndex].find(' ')
            invite_line[dataIndex] = (invite_line[dataIndex])[space_pos + 1:]

        if not (dataIndex == 0 and member_list):
            if not chat_member_searcher(member_list, invite_line[dataIndex]):
                chat_member = ChatMember(invite_line[dataIndex], invite_date)
                invite_chat_room.append_member(chat_member)
