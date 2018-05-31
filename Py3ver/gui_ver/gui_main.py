from sys import path
path.insert(0, "../console_ver")
from katalkative_main_Py3 import *
from log_file_opener import gui_log_opener
from chat_room_info_checker import chat_room_info_checker
from blank_line_passer import blank_line_passer
from line_type_checker import line_type_checker
from print_chat_info import print_chat_info
from date_checker import date_checker

def result_loader(file_path, encoding_type):
	logFile = gui_log_opener(file_path, encoding_type)

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

	logFile.close()
	"""Print information of chatting members.
	"""

	return chatRoomInstance
