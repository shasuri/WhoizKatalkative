#-*- coding: utf-8 -*-
import datetime

class chatMember:
	def __init__(self, name, invitedDate):
		self.name = name
		self.invitedDate = invitedDate		
		self.chatCount = 0
		
		self.talkSize = 0
		self.talkCount = 0
		
		self.emoticonCount = 0
		self.imageCount = 0
		self.linkCount = 0
		self.videoCount = 0
		self.shareAddressCounter = 0
		self.hashtagCounter = 0
	
	def talkSizeAdder(self, chattingLength):
		self.talkSize += chattingLength
	
	def chatCounter(self):
		self.chatCount += 1

	def talkCounter(self):
		self.talkCount += 1
		chatCounter()
	
	def imageCounter(self):
		self.imageCount += 1
		chatCounter()
	def shareAddressCounter(self):
		self.shareAddressCount += 1
		chatCounter()
	def videoCounter(self):
		self.videoCount += 1
		chatCounter()
	def hashtagCounter(self):
		self.hashtagCount += 1
		chatCounter()

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

def lineTypeChecker(chatSingleLine, memberList):
	
	dividerPos = chatSingleLine.find(', ')
	dateLine = chatDateChecker(chatSingleLine[:dividerPos])
	chatterContentLine = chatSingleLine[dividerPos+2:]

	if(extraLineChecker(chatSingleLine)):
		if(chatterContentLine.find(' : ') > -1):
			lineType = 'chat'

		elif(chatterContentLine.find('초대했습니다.') > -1):
			lineType = 'invite'
			inviteLineChecker(chatSingleLine, memberList, dateLine)
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

def inviteLineChecker(inviteLine, memberList, inviteDate):
	
	#dividerPos = inviteLine.find(', ')

	#inviteDateLine = inviteLine[:dividerPos]
	#inviteDate = chatDateChecker(inviteDateLine)
	
	#inviteMemberData = inviteLine[dividerPos+2:]
	inviteMemberData = inviteLine
	inviteMemberData = inviteMemberData.split('님')
	inviteMemberData.pop()
	
	for dataIndex in range(len(inviteMemberData)):
		if(dataIndex != 0):
			spacePos = inviteMemberData[dataIndex].find(' ')
			inviteMemberData[dataIndex] = inviteMemberData[dataIndex][spacePos+1:]
		
		if not(dataIndex == 0 and memberList):
			if not chatterSearcher(memberList, inviteMemberData[dataIndex]):
				chatterInfo = chatMember(inviteMemberData[dataIndex], inviteDate)
				memberList.append(chatterInfo)

def chatterSearcher(memberList, searchMemberName):
	targetInstance = False

	for searchInstance in memberList:
		if searchInstance.name == searchMemberName:
			targetInstance = searchInstance
			break

	return targetInstance

def talkLineChecker(talkLine, talker):
	'''
	emoticonCheck = chatLine.find('(이모티콘)')
	imageCheck = chatLine.find('<사진>')
	if emoticonCheck > 0:
		if chatLine[emoticonCheck:] != '\n':
			talkLineChecker
	'''
	#(이모티콘)
	#<사진>
	#http:// or https://
	#<동영상>


def chatLineChecker(chatLine, memberList):
	#decodeType = 'utf8'
	#dateDividerPos = talkLine.find(', ')
	#chatLine = chatLine[dateDividerPos+2:]

	chattingDividerPos = chatLine.find(' : ')
	
	chatter = chatLine[:chattingDividerPos]
	chatting = chatLine[chattingDividerPos+3:]
	
	emoticonCheck = chatting.find('(이모티콘)')
	'''
	if(emoticonCheck > -1):
		chatter.emoticonCounter()
		talkWithEmoticon = chatLine[emoticonCheck+14:]
		
		if talkWithEmoticon != '\n':
			talkLineChecker(talkWithEmoticon, chatter)
	'''
	if(chatting == '<사진>\n'):
		chatter.imageCounter()
	
	elif(chatting == '<동영상>\n'):
		chatter.videoCounter()
	elif(chatting.find('#') == 0)
		chatter.hashtagCounter()
	elif(chatting.find('<연락처') == 0):
		chatter.shareAddressCounter()
	else:
		talkLineChecker(chatting, chatter)
	#elif(chatting.find('http://') > -1 or chatting.find('https://') > -1):
	#	chatter.linkCounter

	
	'''
	chatterInstance = chatterSearcher(memberList, chatter)
	chattingLength = len(chatting.decode(decodeType)) - 1

	chatterInstance.chattingSizeAdder(chattingLength)
	chatterInstance.chatCounter()
	'''