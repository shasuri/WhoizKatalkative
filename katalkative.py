#-*- coding: utf-8 -*-
import datetime

def chatFileOpener(fileName):
	file = open(fileName, 'r')
	return file

def chatTitleMemberNumChecker(fileFirstLine):
        slicedFirstLine = fileFirstLine[3:]
        splitedFirstLine = slicedFirstLine.split()
        
        title = " ".join(splitedFirstLine[:-3])
        
        memberNum = int(splitedFirstLine[-3])
        
        return title, memberNum

def chatDateChecker(dateLine):
	splitedDateData = dateLine.split()
	
	year = int(splitedDateData[0][:-3])	
	month = int(splitedDateData[1][:-3])
	day = int(splitedDateData[2][:-3])

	if (splitedDateData[3] == '오전'):
		meridem = 'AM'
	elif (splitedDateData[3] == '오후'):
		meridem = 'PM'
	else:
		meridem = 'Error'
	
	dividerPos = splitedDateData[4].find(":")
	
	hour = int(splitedDateData[4][:dividerPos])
	if(meridem == 'PM'):
		hour += 12

	minute = int(splitedDateData[4][dividerPos+1:])

	return datetime.datetime(year,month,day,hour,minute)

def blankLinePasser(passFile,lineNum):
	for passNum in range(lineNum):
		next(passFile)

def lineTypeChecker(chatSingleLine):
	yearPos = chatSingleLine.find('년')
	monthPos = chatSingleLine.find('월')
	dayPos = chatSingleLine.find('일')
	meridemPos = chatSingleLine.find('오')
	timeDividerPos = chatSingleLine.find(':')

	extraLineCheck = ((yearPos == 4) and
	((monthPos > 8) or (monthPos < 11)) and 
	((dayPos>13) and (dayPos<17)) and
	((meridemPos > 17) and (meridemPos < 21)) and
	((timeDividerPos > 25) and (timeDividerPos < 30)))
	
	if(extraLineCheck):
		if(chatSingleLine.find(' : ') > 0):
			lineType = 'chat'
		elif(chatSingleLine.find('초대했습니다.') > 0):
			lineType = 'invite'
		else:
			lineType = 'date'

	elif(chatSingleLine != '\n'):
		lineType = 'extra'
	else:
		lineType = 'blank'

	return lineType


decodeType = 'utf8'
logFileName = "../test.txt"
logFile = chatFileOpener(logFileName)

logFilePresentLine = next(logFile)
chatTitle, chatMemberNum = chatTitleMemberNumChecker(logFilePresentLine)
chatTitle = chatTitle.decode(decodeType)

logFilePresentLine = next(logFile)
slicedDateLine = logFilePresentLine[19:]

logSavedDate = chatDateChecker(slicedDateLine)

print "Chatting Title : " + chatTitle
print "Chatting Member Number : %d" % chatMemberNum
print "Log is saved at " + str(logSavedDate)

blankLinePasser(logFile, 2)

#print logFile.readline()
#i = 5
for singleLine in logFile:
	lineType = lineTypeChecker(singleLine)
	#print i, lineType
	#i = i + 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
logFile.close()