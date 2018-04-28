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
		self.hashtagCount = 0
		self.fileCount = 0
	

	def chatCounter(self):
		self.chatCount += 1
	
	def talkCounter(self, talkLength):
		self.talkCount += 1
		self.talkSize += talkLength
		self.chatCounter()

	def imageCounter(self):
		self.imageCount += 1
		self.chatCounter()

	def linkCounter(self):
		self.linkCount += 1
		self.chatCounter()

	def shareAddressCounter(self):
		self.shareAddressCount += 1
		self.chatCounter()

	def videoCounter(self):
		self.videoCount += 1
		self.chatCounter()

	def hashtagCounter(self):
		self.hashtagCount += 1
		self.chatCounter()

	def fileCounter(self):
		self.fileCount += 1
		self.chatCounter()

	def emoticonCounter(self):
		self.emoticonCount += 1
		self.chatCounter()

def printMemberInfo(memberList):
	decodeType = 'utf-8'
	
	for singleInstance in memberList:
		print (singleInstance.name).decode(decodeType) + "'s Information : "
		print "\tInvited date : " + str(singleInstance.invitedDate)
		print "\tchatted %d times" % singleInstance.chatCount
		print "\ttalked %d times" % singleInstance.talkCount
		print "\ttalked %d letters" % singleInstance.talkSize
		print "\tlinked %d pages" % singleInstance.linkCount
		print "\tused %d emoticons" % singleInstance.emoticonCount
		print "\tuploaded %d images" % singleInstance.imageCount
		print "\ttaged %d hashtags" % singleInstance.hashtagCount
		print "\tuploded %d videos" % singleInstance.videoCount
		print "\tuploded %d files(except image and video)" % singleInstance.fileCount

def chatFileOpener(fileName):
	file = open(fileName, 'r')
	return file

def chatRoomInfoChecker(fileLine):
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
	if(hour == 12):
		if(meridem == 'AM'):
			hour -= 12
		elif(meridem == 'PM'):
			pass
	elif(meridem == 'PM'):
		hour += 12

	minute = int(splitedDateData[4][dividerPos+1:])

	return datetime.datetime(year,month,day,hour,minute)

def blankLinePasser(passFile,lineNum):
	for passNum in range(lineNum):
		next(passFile)

def lineTypeChecker(chatSingleLine, memberList, recentChatter):
	
	if(mainLineChecker(chatSingleLine)):
		dividerPos = chatSingleLine.find(', ')

		dateLine = chatDateChecker(chatSingleLine[:dividerPos])

		chatContentLine = chatSingleLine[dividerPos+2:]

		if(chatContentLine.find(' : ') > -1):
			lineType = 'chat'
			presentChatter = chatLineChecker(chatContentLine, memberList)
			return presentChatter

		elif(chatContentLine.find('초대했습니다.') > -1):
			lineType = 'invite'
			inviteLineChecker(chatContentLine, memberList, dateLine)
			
		else:
			lineType = 'date'

	elif(chatSingleLine != '\n'):
		lineType = 'extra'
		presentChatter = talkLineChecker(chatSingleLine, recentChatter)
		return presentChatter
	else:
		lineType = 'blank'
		return recentChatter

def mainLineChecker(chatSingleLine):
	yearPos = chatSingleLine.find('년')
	monthPos = chatSingleLine.find('월')
	dayPos = chatSingleLine.find('일')
	meridemPos = chatSingleLine.find('오')
	timeDividerPos = chatSingleLine.find(':')

	mainLineCheck = ((yearPos == 4) and
	((monthPos > 8) and (monthPos < 11)) and 
	((dayPos>13) and (dayPos<17)) and
	((meridemPos > 17) and (meridemPos < 21)) and
	((timeDividerPos > 25) and (timeDividerPos < 30)))

	return mainLineCheck

def inviteLineChecker(inviteLine, memberList, inviteDate):
	inviteMemberData = inviteLine
	inviteMemberData = inviteMemberData.split('님')
	inviteMemberData.pop()
	
	for dataIndex in range(len(inviteMemberData)):
		if(dataIndex != 0):
			spacePos = inviteMemberData[dataIndex].find(' ')
			inviteMemberData[dataIndex] = inviteMemberData[dataIndex][spacePos+1:]
		
		if not(dataIndex == 0 and memberList):
			if chatterSearcher(memberList, inviteMemberData[dataIndex]).name == 'UnknownName':
				chatterInfo = chatMember(inviteMemberData[dataIndex], inviteDate)
				memberList.append(chatterInfo)

def chatterSearcher(memberList, searchMemberName):
	targetInstance = chatMember('UnknownName', 'UnknownDate')

	for searchInstance in memberList:
		if searchInstance.name == searchMemberName:
			targetInstance = searchInstance
			break

	return targetInstance

def linkChecker(linkChat, linkUploader, linkPos):
	linkUploader.linkCounter()

	linkLine = linkChat[linkPos:]
	linkEnd = linkLine.find(' ')
	
	afterLink = ''

	if(linkEnd > -1):
		linkLine = linkChat[linkPos:linkEnd]
		afterLink = linkChat[linkEnd:]
	
	beforeLink = linkChat[:linkPos]
	
	afterLinkPos = linkPosFinder(afterLink)
	
	if(afterLinkPos > -1):
		afterLink = linkChecker(afterLink, linkUploader, afterLinkPos)
	
	exceptChat = beforeLink + afterLink
	
	return exceptChat

def linkPosFinder(assumptLinkChat):
	httpPos = assumptLinkChat.find('http://')
	httpsPos = assumptLinkChat.find('https://')
	linkPos = -1
	
	if(httpPos > -1):
		linkPos = httpPos
	elif(httpsPos > -1):
		linkPos = httpsPos

	return linkPos

def talkLineChecker(talkLine, talker):
	decodeType = 'utf-8'

	if(talkLine.find('(이모티콘)') == 0):
		talker.emoticonCounter()
		talkLine = talkLine[14:]

	linkPos = linkPosFinder(talkLine)
	
	if linkPos > -1:
		talkLine = linkChecker(talkLine, talker, linkPos)

	if(talkLine != '\n'):
		try:
			talkLength = len(talkLine.decode(decodeType))-1
		except:
			talkLength = len(talkLine)/3
		talker.talkCounter(talkLength)
	return talker
	
def fileChecker(fileLine, fileUploader, dotPos):
	supportFileList = ['mp4', 'm4v', 'avi', 'asf', 'wmv', 'mkv', 'ts', 'mpg', 'mpeg', 'mov', 'flv', 'ogv', 'doc', 'docx', 'hwp', 'txt', 'rtf', 'xml', 'pdf', 'wks', 'wps', 'xps', 'md', 'odf', 'odt', 'ods', 'odp', 'csv', 'tsv', 'xls', 'xlsx', 'ppt', 'pptx', 'pages', 'key', 'numbers', 'show', 'ce', 'zip', 'gz', 'bz2', 'rar', '7z', 'lzh', 'alz']
	
	assumptExtension = fileLine[dotPos+1:-1]

	fileExist = False
	
	for fileExtension in supportFileList:
		if (assumptExtension == fileExtension):
			fileUploader.fileCounter()
			fileExist = True
			break

	return fileExist

def chatLineChecker(chatLine, memberList):

	chattingDividerPos = chatLine.find(' : ')
	
	chatter = chatLine[:chattingDividerPos]

	chatting = chatLine[chattingDividerPos+3:]
	
	chatterInstance = chatterSearcher(memberList, chatter)	
	
	if(chatterInstance.name == 'UnknownName'):
		newChatter = chatMember(chatter, 'UnknownDate')
		memberList.append(newChatter)
		chatterInstance = newChatter
	
	if(chatting == '<사진>\n'):
		chatterInstance.imageCounter()
	elif(chatting == '<동영상>\n'):
		chatterInstance.videoCounter()
	elif(chatting.find('#') == 0):
		chatterInstance.hashtagCounter()
	elif(chatting.find('<연락처') == 0):
		chatterInstance.shareAddressCounter()
	else:
		dotPos = chatting.find('.')
		chattingSize = len(chatting)
		fileExist = False
		#print chatting.decode('utf-8')
		#print chatting[dotPos:].decode('utf-8')
		#print chattingSize - dotPos

		if chattingSize > 6 and ((dotPos == chattingSize - 4) or (dotPos == chattingSize - 5) or (dotPos == chattingSize - 6)):
			#print 'Assumpt file',
			
			fileExist = fileChecker(chatting, chatterInstance, dotPos)
		
		if not fileExist:
			talkLineChecker(chatting, chatterInstance)
	return chatterInstance
	