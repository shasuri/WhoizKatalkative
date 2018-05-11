#-*- coding: utf-8 -*-
import datetime

from enum import Enum


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


class memberInfo(Enum):
	chat = 0
	talk = 1
	emoticon = 2
	image = 3
	link = 4
	video = 5
	hashtag = 6
	file = 7
	address = 8
	voice = 9
	talkSize = 10


class chatMember:
	def __init__(self, name, invitedDate=''):

		self.name = name
		self.invitedDate = invitedDate

		self.infoList = [0 for infoIndex in range(11)]

	def infoCounter(self, info):
		self.infoList[info.value] += 1

	def talkAdder(self, talkLength):
		self.infoList[memberInfo.talkSize.value] += talkLength


def printChatInfo(chatRoomInfo):

	print("Chatting Title : " + (chatRoomInfo.title))
	print("Chatting Member Number : %d" % chatRoomInfo.memberNum)
	print("Log is saved at " + str(chatRoomInfo.logSaveDate))
	
	for singleMember in chatRoomInfo.memberList:
		print((singleMember.name)+ "'s Information : ")
		print("\tInvited date : " + str(singleMember.invitedDate))
		print("\tchatted %d times" % singleMember.infoList[memberInfo.chat.value])
		print("\ttalked %d times" % singleMember.infoList[memberInfo.talk.value])
		print("\ttalked %d letters" % singleMember.infoList[memberInfo.talkSize.value])
		print("\tlinked %d pages" % singleMember.infoList[memberInfo.link.value])
		print("\tused %d emoticons" % singleMember.infoList[memberInfo.emoticon.value])
		print("\tuploaded %d images" % singleMember.infoList[memberInfo.image.value])
		print("\ttaged %d hashtags" % singleMember.infoList[memberInfo.hashtag.value])
		print("\tuploded %d videos" % singleMember.infoList[memberInfo.video.value])
		print("\tuploded %d voice records" % singleMember.infoList[memberInfo.voice.value])
		print("\tuploded %d etc files" % singleMember.infoList[memberInfo.file.value])

def chatFileOpener(fileName, fileEncode):
	file = open(fileName, 'r', encoding = fileEncode)
	return file

def chatRoomInfoChecker(fileLine):
    slicedLine = fileLine[1:]
    slicedLine = slicedLine.split()
    
    title = " ".join(slicedLine[:-3])
    
    memberNum = int(slicedLine[-3])
    
    chatRoomInfo = chatRoom(title, memberNum)

    return chatRoomInfo

def chatDateChecker(dateLine):

	splitedDateData = dateLine.split()

	year = int(splitedDateData[0][:-1])	
	month = int(splitedDateData[1][:-1])
	day = int(splitedDateData[2][:-1])

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
	((monthPos > 6) and (monthPos < 9)) and 
	((dayPos>9) and (dayPos<13)) and
	((meridemPos > 11) and (meridemPos < 15)) and
	((timeDividerPos > 15) and (timeDividerPos < 20)))

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
		linkUploader.infoCounter(memberInfo.link)
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
	talkLine = linkLineChecker(talkLine, talker)
	
	talkLength = len(talkLine)-1
	talker.talkAdder(talkLength)

def headLineChecker(headLine, talker):
	if(headLine.find('(이모티콘)') == 0):
		talker.infoCounter(memberInfo.emoticon)
		headLine = headLine[6:]
	
	elif(headLine.find('(emoticon)') == 0):
		talker.infoCounter(memberInfo.emoticon)
		headLine = headLine[10:]

	elif (headLine.find('[사진]') == 0):
		talker.infoCounter(memberInfo.image)
		headLine = headLine[4:]

	return headLine

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

	chatterInstance.infoCounter(memberInfo.chat)

	if(chatting == '<사진>\n'):
		chatterInstance.infoCounter(memberInfo.image)
	
	elif(chatting == '<동영상>\n'):
		chatterInstance.infoCounter(memberInfo.video)
	
	elif(chatting.find('#') == 0):
		chatterInstance.infoCounter(memberInfo.hashtag)
	
	elif(chatting.find('<연락처') == 0):
		chatterInstance.infoCounter(memberInfo.address)
	
	elif(chatting == ('<음성메시지>\n')):
		chatterInstance.infoCounter(memberInfo.voice)
	
	elif(fileUploadChecker(chatting)):
		chatterInstance.infoCounter(memberInfo.file)
		
	else:
		chatting = headLineChecker(chatting, chatterInstance)
		
		if(chatting != '\n'):
			chatterInstance.infoCounter(memberInfo.talk)
			talkLineChecker(chatting, chatterInstance)
