# -*- coding: utf-8 -*-
from katalkative_func_Py3 import *

logFile = log_file_opener()
"""file : Open the Kakaotalk log file with 'log_file_opener' function.
"""

logFilePresentLine = next(logFile)
"""str : Load first line of log file with next().
"""

chatRoomInstance = chat_room_info_checker(logFilePresentLine)
"""katalkative_func_Py3.ChatMember : Set information of chatting room on 'ChatRoom' class, parsing first line.
"""

logFilePresentLine = next(logFile)

chatRoomInstance.set_log_saved_date(date_checker(logFilePresentLine[9:]))
"""Slice the useless part of second line and parsing the date part with 'date_checker' function, then set on instance.
"""

blank_line_passer(logFile, 2)
"""Pass the blank lines.
"""

for logFilePresentLine in logFile:
    line_type_checker(logFilePresentLine, chatRoomInstance)
"""Parse every single chatting line using 'line_type_checker' function.
"""

print_chat_info(chatRoomInstance)
"""Print information of chatting members.
"""

logFile.close()
"""Print information of chatting members.
"""
