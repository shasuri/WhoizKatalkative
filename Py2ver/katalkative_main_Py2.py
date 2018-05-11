#-*- coding: utf-8 -*-
from katalkative_func_Py2 import *

decodeType = 'utf-8'
logFileName = ""#input path
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
