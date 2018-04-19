#-*- coding: utf-8 -*-
import datetime

def chatFileOpener(fileName):
	file = open(fileName, 'r')
	return file

def chatTitleMemberNumChecker(fileFirstLine):
        #print list(fileFirstLine)
        '''titleMemberNumPos = fileFirstLine.find("카카오톡 대화") - 1
        titleMemberNumString = fileFirstLine[3:titleMemberNumPos]'''
        #print list(titleMemberNumString)
        
        slicedFirstLine = fileFirstLine[3:]
        splitedFirstLine = slicedFirstLine.split()
        
        title = " ".join(splitedFirstLine[:-3])
        
        memberNum = int(splitedFirstLine[-3])
        
        #print title
        '''
        while(titleMemberNumString[memberNumPos] != ' '):
        	memberNumPos -= 1
        memberNum = int(titleMemberNumString[memberNumPos+1:])
        '''
        ''' 
        for stringIndex in range(titleMemberNumStringLen):
        	stringLastIndex = titleMemberNumStringLen - stringIndex
        	if(titleMemberNumString[stringLastIndex] == ' '):
        		memberNumPos = stringLastIndex
        		break
		'''
        return title, memberNum

def chatDateChecker(dateLine):
	splitDateData = dateLine.split()
	
	year = int(splitDateData[0][:-3])
	
	month = int(splitDateData[1][:-3])
	
	day = int(splitDateData[2][:-3])

	if (splitDateData[3] == '오전'):
		meridem = 'AM'
	elif (splitDateData[3] == '오후'):
		meridem = 'PM'
	else:
		meridem = 'Error'
	
	dividerPos = splitDateData[4].find(":")
	
	hour = int(splitDateData[4][:dividerPos])
	if(meridem == 'PM'):
		hour += 12

	minute = int(splitDateData[4][dividerPos+1:])

	return datetime.datetime(year,month,day,hour,minute)

logFileName = "../test.txt"
logFile = chatFileOpener(logFileName)

logFilePresentLine = next(logFile)
chatTitle, chatMemberNum = chatTitleMemberNumChecker(logFilePresentLine)
#print chatTitle
#print chatMemberNum

logFilePresentLine = next(logFile)
slicedDateLine = logFilePresentLine[19:]
'''print list(slicedDateLine)
print slicedDateLine'''
logSavedDate = chatDateChecker(slicedDateLine)

print "Chatting Title : " + chatTitle
print "Chatting Member Number : %d" % chatMemberNum
print "Log is saved at " + str(logSavedDate)
logFile.close()








