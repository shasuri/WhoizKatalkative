# -*- coding: utf-8 -*-
from katalkative_func_Py3 import *

# Open the Kakaotalk log file with 'log_file_opener' function.
logFile = log_file_opener()

# Load first line of log file with next().
logFilePresentLine = next(logFile)

# Set information of chatting room on 'ChatRoom' class, parsing first line.
chatRoomInstance = chat_room_info_checker(logFilePresentLine)

logFilePresentLine = next(logFile)

# Slice the useless part of second line and parsing the date part with 'date_checker' function, then set on instance.
chatRoomInstance.set_log_saved_date(date_checker(logFilePresentLine[9:]))

# Pass the blank lines.
blank_line_passer(logFile, 2)

# Parse every single chatting line using 'line_type_checker' function.
for logFilePresentLine in logFile:
    line_type_checker(logFilePresentLine, chatRoomInstance)

# Print information of chatting members.
print_chat_info(chatRoomInstance)

# Close the log file.
logFile.close()
