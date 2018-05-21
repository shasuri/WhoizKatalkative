from MemberInfo import MemberInfo


def head_element_checker(chat_line, talker):
    """Check the chat_line contains the elements which can be located ahead of the talk or not.
    For example, emoticon or images of the chatting room board.
    
    Args:
        chat_line (str): The line to be checked contains the head elements or not.
        talker (ChatMember): ChatMember instance of who chat the chat_line.

    Returns:
        chat_line (str): The line which is excepted the head elements.

    Examples:
        `(emoticon)Explicit is better than implicit.`

    """
    if chat_line.find('(이모티콘)') == 0:
        talker.info_counter(MemberInfo.emoticon)
        chat_line = chat_line[6:]

    elif chat_line.find('(emoticon)') == 0:
        talker.info_counter(MemberInfo.emoticon)
        chat_line = chat_line[10:]

    elif chat_line.find('[사진]') == 0:
        talker.info_counter(MemberInfo.image)
        chat_line = chat_line[4:]

    return chat_line
