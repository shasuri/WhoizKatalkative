#-*- coding: utf-8 -*-
from katalkative_func import *

decodeType = 'utf8'
logFileName = "../test.txt"
logFile = chatFileOpener(logFileName)

logFilePresentLine = next(logFile)
chatTitle, chatMemberNum = chatTitleMemberNumChecker(logFilePresentLine)
chatTitle = chatTitle.decode(decodeType)

logFilePresentLine = next(logFile)
slicedDateLine = logFilePresentLine[19:]

logSavedDate = chatDateChecker(slicedDateLine)
'''
print "Chatting Title : " + chatTitle
print "Chatting Member Number : %d" % chatMemberNum
print "Log is saved at " + str(logSavedDate)
'''
blankLinePasser(logFile, 2)

#print logFile.readline()
#i = 5

chatMemberList = []

for logFilePresentLine in logFile:
	lineType = lineTypeChecker(logFilePresentLine)
	'''
	if(lineType == 'invite'):
		inviteLineChecker(logFilePresentLine, chatMemberList)
		for i in chatMemberList:
			print (i.name).decode(decodeType)
	'''
	#print i, lineType
	#i = i + 1                                                                                                                                                                   
logFile.close()