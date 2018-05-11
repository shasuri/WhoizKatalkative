#-*- coding: utf-8 -*-
from katalkative_func_Py3 import *

encodeType = 'utf-8'
logFileName = "../../Katalkative_texts/KakaoTalkChats_bigfile.txt"
logFile = chatFileOpener(logFileName, encodeType)

logFilePresentLine = next(logFile)
chatRoomInstance = chatRoomInfoChecker(logFilePresentLine)

logFilePresentLine = next(logFile)

chatRoomInstance.setLogSaveDate(chatDateChecker(logFilePresentLine[9:]))

blankLinePasser(logFile, 2)

for logFilePresentLine in logFile:
	lineTypeChecker(logFilePresentLine, chatRoomInstance)

printChatInfo(chatRoomInstance)
logFile.close()
