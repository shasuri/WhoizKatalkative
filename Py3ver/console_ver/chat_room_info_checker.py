from ChatRoom import ChatRoom


def chat_room_info_checker(info_line):
    """Check first line of the log file and make ChatRoom instance
    
    Args:
        info_line (str): First line of the log file which contains chatting title and member number.

    Returns:
        chat_room (ChatRoom): ChatRoom instance of the chatting room.

    """
    sliced_line = info_line[1:]  # Slice the crashed byte on first line.
    sliced_line = sliced_line.split()

    if '님과' in sliced_line:
        divider_pos = sliced_line.index('님과')

        if divider_pos == 1:  # Personal chat room case.
            chat_room_type = 'personal'
            title = sliced_line[0]
            member_number = 2

        elif divider_pos == 2:  # Non specified group chat room name case.
            chat_room_type = 'nspecifed'
            title = " ".join(sliced_line[:-4])
            member_number = int(sliced_line[-4])

    else:  # Specified group chat room name case.
        chat_room_type = 'specifed'
        title = " ".join(sliced_line[:-3])
        member_number = int(sliced_line[-3])

    chat_room = ChatRoom(title, member_number, chat_room_type)

    return chat_room
