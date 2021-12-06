# -*- coding: utf-8 -*-
from log_parser import *


def log_file_opener():
    """Open the chatting log file.
    Log file name and encoding type can be inputted. Default name and type are "KakaoTalkChats.txt" and "utf-8".
    
    Returns:
        log_file (file): Opened file.

    """

    print("Input name of log file : ", end="")
    log_file_name = input()

    if not log_file_name:
        log_file_name = "KakaoTalkChats.txt"

    print("Input encoding type of log file : ", end="")
    log_file_encoding = input()

    if not log_file_encoding:
        log_file_encoding = "utf-8"

    log_file = open(log_file_name, 'r', encoding=log_file_encoding)
    return log_file
    

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

if __name__ == "__main__":
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
