#-*- coding: utf-8 -*-
from katalkative_func import *

decodeType = 'utf-8'
logFileName = "../Katalkative_texts/KakaoTalkChats_bigfile.txt"
logFile = chatFileOpener(logFileName)

logFilePresentLine = next(logFile)
chatRoomInstance = chatRoomInfoChecker(logFilePresentLine)

logFilePresentLine = next(logFile)
chatRoomInstance.setLogSaveDate(chatDateChecker(logFilePresentLine[19:]))

blankLinePasser(logFile, 2)

for logFilePresentLine in logFile:
	lineTypeChecker(logFilePresentLine, chatRoomInstance)

printChatInfo(chatRoomInstance)
logFile.close()