from main_line_checker import main_line_checker
from date_checker import date_checker
from chat_line_checker import chat_line_checker
from invite_line_checker import invite_line_checker
from talk_line_checker import talk_line_checker


def line_type_checker(line, chat_room):
    """Check the type of content line by patterns.
    
    Args:
        line (str): Content line of the log file.
        chat_room (ChatRoom): ChatRoom instance of the chatting room.
    
    Examples:
        `2018년 3월 23일 오후 11:16, Jack : Life is short, You need Python.`

    """
    if main_line_checker(line):  # Check the line is a main line or an extra line.
        divider_pos = line.find(', ')

        date_line = date_checker(line[:divider_pos])

        content_line = line[divider_pos + 2:]

        if ' : ' in content_line:
            line_type = 'chat'
            chat_line_checker(content_line, chat_room)

        elif '초대했습니다.' in content_line:
            line_type = 'invite'
            invite_line_checker(content_line, chat_room, date_line)

        else:
            line_type = 'date'

    elif line != '\n':
        line_type = 'extra'
        talk_line_checker(line, chat_room.preChatMember)

    else:
        line_type = 'blank'
