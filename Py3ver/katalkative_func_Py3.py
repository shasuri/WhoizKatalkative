#-*- coding: utf-8 -*-
import datetime

class chatRoom:
	def __init__(self, title, memberNum):
		self.title = title
		self.memberNum = memberNum
		self.memberList = []
		self.preChatMember = ''
	
	def setLogSaveDate(self, date):
		self.logSaveDate = date

	def appendMember(self, memberInstance):
		self.memberList.append(memberInstance)

	def setPreChatMember(self, preChatMember):
		self.preChatMember = preChatMember

class chatMember:
	def __init__(self, name, invitedDate=''):
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
		self.voiceCount = 0
	

	def chatCounter(self):
		self.chatCount += 1
	
	def talkCounter(self, talkLength):
		self.talkCount += 1
		self.talkSize += talkLength

	def imageCounter(self):
		self.imageCount += 1

	def linkCounter(self):
		self.linkCount += 1

	def shareAddressCounter(self):
		self.shareAddressCount += 1

	def videoCounter(self):
		self.videoCount += 1

	def hashtagCounter(self):
		self.hashtagCount += 1

	def fileCounter(self):
		self.fileCount += 1

	def emoticonCounter(self):
		self.emoticonCount += 1

	def voiceCounter(self):
		self.voiceCount += 1

def printChatInfo(chatRoomInfo):
	decodeType = 'utf-8'
	
	print("Chatting Title : " + (chatRoomInfo.title).decode(decodeType))
	print("Chatting Member Number : %d" % chatRoomInfo.memberNum)
	print("Log is saved at " + str(chatRoomInfo.logSaveDate))
	
	for memberInfo in chatRoomInfo.memberList:
		print((memberInfo.name).decode(decodeType) + "'s Information : ")
		print("\tInvited date : " + str(memberInfo.invitedDate))
		print("\tchatted %d times" % memberInfo.chatCount)
		print("\ttalked %d times" % memberInfo.talkCount)
		print("\ttalked %d letters" % memberInfo.talkSize)
		print("\tlinked %d pages" % memberInfo.linkCount)
		print("\tused %d emoticons" % memberInfo.emoticonCount)
		print("\tuploaded %d images" % memberInfo.imageCount)
		print("\ttaged %d hashtags" % memberInfo.hashtagCount)
		print("\tuploded %d videos" % memberInfo.videoCount)
		print("\tuploded %d voice records" % memberInfo.voiceCount)
		print("\tuploded %d etc files" % memberInfo.fileCount)

def chatFileOpener(fileName):
	file = open(fileName, 'r', encoding = 'utf-8')
	return file

def chatRoomInfoChecker(fileLine):
    slicedLine = fileLine[3:]
    splitedLine = slicedLine.split()
    
    title = " ".join(splitedLine[:-3])
    
    memberNum = int(splitedLine[-3])
    
    chatRoomInfo = chatRoom(title, memberNum)

    return chatRoomInfo

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

def lineTypeChecker(chatSingleLine, chatRoom):
	
	if(mainLineChecker(chatSingleLine)):
		dividerPos = chatSingleLine.find(', ')

		dateLine = chatDateChecker(chatSingleLine[:dividerPos])

		chatContentLine = chatSingleLine[dividerPos+2:]

		if(chatContentLine.find(' : ') > -1):
			lineType = 'chat'
			chatLineChecker(chatContentLine, chatRoom)
			

		elif(chatContentLine.find('초대했습니다.') > -1):
			lineType = 'invite'
			inviteLineChecker(chatContentLine, chatRoom, dateLine)
			
		else:
			lineType = 'date'

	elif(chatSingleLine != '\n'):
		lineType = 'extra'
		talkLineChecker(chatSingleLine, chatRoom.preChatMember)
		
	else:
		lineType = 'blank'

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

def inviteLineChecker(inviteLine, inviteChatRoom, inviteDate):
	#ex)이재욱님이 012님, 조민정님, 윤승희님, 이우진님과 이창율님을 초대했습니다.
	inviteMemberData = inviteLine
	inviteMemberData = inviteMemberData.split('님')
	inviteMemberData.pop()
	
	preMemberList = inviteChatRoom.memberList

	for dataIndex in range(len(inviteMemberData)):
		if(dataIndex != 0):
			spacePos = inviteMemberData[dataIndex].find(' ')
			inviteMemberData[dataIndex] = (inviteMemberData[dataIndex])[spacePos+1:]
		
		if not(dataIndex == 0 and preMemberList):
			if not chatterSearcher(preMemberList, inviteMemberData[dataIndex]):
				chatterInfo = chatMember(inviteMemberData[dataIndex], inviteDate)
				inviteChatRoom.appendMember(chatterInfo)

def chatterSearcher(memberList, targetMemberName):
	for searchMember in memberList:
		if searchMember.name == targetMemberName:
			return searchMember

	return False

def linkLineChecker(linkLine, linkUploader):
	linkPos = linkPosFinder(linkLine)
	
	if linkPos > -1 :
		linkUploader.linkCounter()
		linkSlicedLine = linkLine[linkPos:]
		
		spacePos = linkSlicedLine.find(' ')

		if(spacePos == -1):
			fixedLine = linkLine[:linkPos]
		else:
			fixedLine = linkLine[:linkPos]+linkLine[spacePos+linkPos:]
		
		link = linkSlicedLine[:spacePos]

		return linkLineChecker(fixedLine, linkUploader)
	
	else:
		return linkLine

def linkPosFinder(linkLine):
	httpPos = linkLine.find('http://')
	httpsPos = linkLine.find('https://')
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
	
	elif(talkLine.find('(emoticon)') == 0):
		talker.emoticonCounter()
		talkLine = talkLine[10:]

	elif (talkLine.find('[사진]') == 0):
		talker.imageCounter()
		talkLine = talkLine[8:]

	talkLine = linkLineChecker(talkLine, talker)
	
	if(talkLine != '\n'):
		try:
			talkLength = len(talkLine.decode(decodeType))-1
		except:
			talkLength = len(list(talkLine.decode(decodeType)))-1
		
		talker.talkCounter(talkLength)
	
def fileUploadChecker(fileUploadLine):
	
	fileExist = False	
	revDotPos = fileUploadLine.rfind('.')
	
	if revDotPos > -1:
		fileLength = len(fileUploadLine)
		
		if fileLength > 6 and ((revDotPos == fileLength - 4) or (revDotPos == fileLength - 5) or (revDotPos == fileLength - 6)):

			supportFileList = ['mp3', 'wav', 'flac', 'tta', 'tak', 'aac', 'wma', 'ogg', 'm4a','doc', 'docx', 'hwp', 'txt', 'rtf', 'xml', 'pdf', 'wks', 'wps', 'xps', 'md', 'odf', 'odt', 'ods', 'odp', 'csv', 'tsv', 'xls', 'xlsx', 'ppt', 'pptx', 'pages', 'key', 'numbers', 'show', 'ce', 'zip', 'gz', 'bz2', 'rar', '7z', 'lzh', 'alz']
	
			fileExtension = fileUploadLine[revDotPos+1:-1]
						
			if fileExtension in supportFileList:
				fileExist = True

	return fileExist

def chatLineChecker(chatLine, chatRoom):

	chattingDividerPos = chatLine.find(' : ')
	
	chatterName = chatLine[:chattingDividerPos]

	chatting = chatLine[chattingDividerPos+3:]

	chatterInstance = chatterSearcher(chatRoom.memberList, chatterName)
	if not chatterInstance :
		chatterInstance = chatMember(chatterName)
		chatRoom.appendMember(chatterInstance)

	chatRoom.setPreChatMember(chatterInstance)

	chatterInstance.chatCounter()

	if(chatting == '<사진>\n'):
		chatterInstance.imageCounter()
	
	elif(chatting == '<동영상>\n'):
		chatterInstance.videoCounter()
	
	elif(chatting.find('#') == 0):
		chatterInstance.hashtagCounter()
	
	elif(chatting.find('<연락처') == 0):
		chatterInstance.shareAddressCounter()
	
	elif(chatting == ('<음성메시지>\n')):
		chatterInstance.voiceCounter()
	
	elif(fileUploadChecker(chatting)):
		chatterInstance.fileCounter()
		
	else:		
		talkLineChecker(chatting, chatterInstance)
	