#-*- coding: utf-8 -*-
import datetime

class chatMember:
	def __init__(self, name, invitedDate):
		self.name = name
		self.invitedDate = invitedDate
	def printName(self):
		print self.name

def chatFileOpener(fileName):
	file = open(fileName, 'r')
	return file

def chatTitleMemberNumChecker(fileLine):
        slicedLine = fileLine[3:]
        splitedLine = slicedLine.split()
        
        title = " ".join(splitedLine[:-3])
        
        memberNum = int(splitedLine[-3])
        
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
	extraLineCheck = extraLineChecker(chatSingleLine)
	
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

def extraLineChecker(chatSingleLine):
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

	return extraLineCheck

def inviteLineChecker(inviteLine, memberList):
	
	dividerPos = inviteLine.find(', ')

	inviteDateLine = inviteLine[:dividerPos]
	inviteDate = chatDateChecker(inviteDateLine)
	
	inviteMemberData = inviteLine[dividerPos+2:]
	inviteMemberData = inviteMemberData.split('님')
	inviteMemberData.pop()
	
	for dataIndex in range(len(inviteMemberData)):
		if(dataIndex != 0):
			spacePos = inviteMemberData[dataIndex].find(' ')
			inviteMemberData[dataIndex] = inviteMemberData[dataIndex][spacePos+1:]
		
		if not(dataIndex == 0 and memberList):
			nameOverlap = findOverlapMember(memberList, inviteMemberData[dataIndex])
			if not nameOverlap:
				chatterInfo = chatMember(inviteMemberData[dataIndex], inviteDate)
				memberList.append(chatterInfo)

def findOverlapMember(memberList, inviteMember):
	overlapped = 0
	for findIndex in range(len(memberList)):
		if  memberList[findIndex].name == inviteMember:
			overlapped = 1 
	return overlapped