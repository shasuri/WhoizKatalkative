#-*- coding: utf-8 -*-
from katalkative_func import *

decodeType = 'utf8'
logFileName = "../KakaoTalkChats.txt"
logFile = chatFileOpener(logFileName)

logFilePresentLine = next(logFile)
chatTitle, chatMemberNum = chatRoomInfoChecker(logFilePresentLine)
chatTitle = chatTitle.decode(decodeType)

logFilePresentLine = next(logFile)
slicedDateLine = logFilePresentLine[19:]

logSavedDate = chatDateChecker(slicedDateLine)

blankLinePasser(logFile, 2)

#i = 5

chatMemberList = []
previousChatter = 'Blank'
for logFilePresentLine in logFile:
		previousChatter = lineTypeChecker(logFilePresentLine, chatMemberList, previousChatter)
'''
	try:
		lineType = lineTypeChecker(logFilePresentLine, chatMemberList)

	except:
		print 'errored line',
		print logFilePresentLine.decode(decodeType)
'''
'''
	print i, 
	print logFilePresentLine.decode(decodeType)
	i += 1
'''
print "Chatting Title : " + chatTitle
print "Chatting Member Number : %d" % chatMemberNum
print "Log is saved at " + str(logSavedDate)
printMemberInfo(chatMemberList)                                                                                                                                                              
logFile.close()