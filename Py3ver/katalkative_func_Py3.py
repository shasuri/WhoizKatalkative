# -*- coding: utf-8 -*-
import datetime
from enum import Enum


class ChatRoom:
    def __init__(self, title, member_number):
        self.title = title
        self.memberNum = member_number
        self.memberList = []
        self.preChatMember = ''
        self.logSaveDate = ''

    def set_log_saved_date(self, date):
        self.logSaveDate = date

    def append_member(self, member):
        self.memberList.append(member)

    def set_chatted_member(self, chatted_member):
        self.preChatMember = chatted_member


class MemberInfo(Enum):
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


class ChatMember:
    def __init__(self, name, invite_date=''):
        self.name = name
        self.invitedDate = invite_date

        self.infoList = [0 for infoIndex in range(11)]

    def info_counter(self, info):
        self.infoList[info.value] += 1

    def talk_counter(self, talk_length):
        self.infoList[MemberInfo.talkSize.value] += talk_length


def print_chat_info(chat_room):
    print("Chatting Title : " + chat_room.title)
    print("Chatting Member Number : %d" % chat_room.memberNum)
    print("Log is saved at " + str(chat_room.logSaveDate))

    for single_member in chat_room.memberList:
        print(single_member.name + "'s Information : ")
        print("\tInvited date : " + str(single_member.invitedDate))
        print("\tchatted %d times" % single_member.infoList[MemberInfo.chat.value])
        print("\ttalked %d times" % single_member.infoList[MemberInfo.talk.value])
        print("\ttalked %d letters" % single_member.infoList[MemberInfo.talkSize.value])
        print("\tlinked %d pages" % single_member.infoList[MemberInfo.link.value])
        print("\tused %d emoticons" % single_member.infoList[MemberInfo.emoticon.value])
        print("\tuploaded %d images" % single_member.infoList[MemberInfo.image.value])
        print("\ttaged %d hashtags" % single_member.infoList[MemberInfo.hashtag.value])
        print("\tuploded %d videos" % single_member.infoList[MemberInfo.video.value])
        print("\tuploded %d voice records" % single_member.infoList[MemberInfo.voice.value])
        print("\tuploded %d etc files" % single_member.infoList[MemberInfo.file.value])


def log_file_opener(log_file_encoding='utf-8'):
    log_file_name = input()
    log_file = open(log_file_name, 'r', encoding=log_file_encoding)
    return log_file


def chat_room_info_checker(info_line):
    sliced_line = info_line[1:]
    sliced_line = sliced_line.split()
    if '님과' in info_line:
        title = " ".join(sliced_line[:-4])
        member_number = int(sliced_line[-4])

    else:
        title = " ".join(sliced_line[:-3])
        member_number = int(sliced_line[-3])

    chat_room = ChatRoom(title, member_number)

    return chat_room


def date_checker(date_line):
    date_data = date_line.split()

    year = int(date_data[0][:-1])
    month = int(date_data[1][:-1])
    day = int(date_data[2][:-1])

    if date_data[3] == '오전':
        meridem = 'AM'
    elif date_data[3] == '오후':
        meridem = 'PM'
    else:
        meridem = 'Error'

    divider_pos = date_data[4].find(":")

    hour = int(date_data[4][:divider_pos])
    if hour == 12:
        if meridem == 'AM':
            hour -= 12
        elif meridem == 'PM':
            pass
    elif meridem == 'PM':
        hour += 12

    minute = int(date_data[4][divider_pos + 1:])

    return datetime.datetime(year, month, day, hour, minute)


def blank_line_passer(pass_file, pass_line_num):
    for passNum in range(pass_line_num):
        next(pass_file)


def line_type_checker(line, chat_room):
    if main_line_checker(line):
        divider_pos = line.find(', ')

        date_line = date_checker(line[:divider_pos])

        content_line = line[divider_pos + 2:]

        if ' : ' in content_line:
            line_type = 'chat'
            chat_line_checker(content_line, chat_room)

        elif '초대했습니다.' in content_line:
            line_type = 'invite'
            invite_line_checker(content_line, chat_room, date_line)

        else:
            line_type = 'date'

    elif line != '\n':
        line_type = 'extra'
        talk_line_checker(line, chat_room.preChatMember)

    else:
        line_type = 'blank'


def main_line_checker(line):
    year_pos = line.find('년')
    month_pos = line.find('월')
    day_pos = line.find('일')
    meridem_pos = line.find('오')
    time_divider_pos = line.find(':')

    main_line_check = ((year_pos == 4) and
                       ((month_pos > 6) and (month_pos < 9)) and
                       ((day_pos > 9) and (day_pos < 13)) and
                       ((meridem_pos > 11) and (meridem_pos < 15)) and
                       ((time_divider_pos > 15) and (time_divider_pos < 20)))

    return main_line_check


def invite_line_checker(invite_line, invite_chat_room, invite_date):
    # ex)이재욱님이 012님, 조민정님, 윤승희님, 이우진님과 이창율님을 초대했습니다.

    invite_line = invite_line.split('님')
    invite_line.pop()

    member_list = invite_chat_room.memberList

    for dataIndex in range(len(invite_line)):
        if dataIndex != 0:
            space_pos = invite_line[dataIndex].find(' ')
            invite_line[dataIndex] = (invite_line[dataIndex])[space_pos + 1:]

        if not (dataIndex == 0 and member_list):
            if not chat_member_searcher(member_list, invite_line[dataIndex]):
                chat_member = ChatMember(invite_line[dataIndex], invite_date)
                invite_chat_room.append_member(chat_member)


def chat_member_searcher(member_list, search_member_name):
    for searchMember in member_list:
        if searchMember.name == search_member_name:
            return searchMember

    return False


def link_line_checker(link_line, link_uploader):
    link_pos = link_pos_finder(link_line)

    if link_pos > -1:
        link_uploader.info_counter(MemberInfo.link)
        link_sliced_line = link_line[link_pos:]

        space_pos = link_sliced_line.find(' ')

        if space_pos == -1:
            fixed_line = link_line[:link_pos]
        else:
            fixed_line = link_line[:link_pos] + link_line[space_pos + link_pos:]

        link = link_sliced_line[:space_pos]

        return link_line_checker(fixed_line, link_uploader)

    else:
        return link_line


def link_pos_finder(link_line):
    link_pos = -1

    if 'http://' in link_line:
        link_pos = link_line.find('http://')
    elif 'https://' in link_line:
        link_pos = link_line.find('https://')

    return link_pos


def talk_line_checker(talk_line, talker):
    talk_line = link_line_checker(talk_line, talker)

    talk_length = len(talk_line) - 1
    talker.talk_counter(talk_length)


def head_element_checker(chat_line, talker):
    if chat_line.find('(이모티콘)') == 0:
        talker.info_counter(MemberInfo.emoticon)
        chat_line = chat_line[6:]

    elif chat_line.find('(emoticon)') == 0:
        talker.info_counter(MemberInfo.emoticon)
        chat_line = chat_line[10:]

    elif chat_line.find('[사진]') == 0:
        talker.info_counter(MemberInfo.image)
        chat_line = chat_line[4:]

    return chat_line


def file_checker(file_upload_line):
    file_exist = False
    extension_dot_pos = file_upload_line.rfind('.')

    if extension_dot_pos > -1:
        line_length = len(file_upload_line)

        if line_length > 6 and ((extension_dot_pos == line_length - 4) or (extension_dot_pos == line_length - 5) or (
                extension_dot_pos == line_length - 6)):

            support_file_list = ['mp3', 'wav', 'flac', 'tta', 'tak', 'aac', 'wma', 'ogg', 'm4a', 'doc', 'docx', 'hwp',
                                 'txt', 'rtf', 'xml', 'pdf', 'wks', 'wps', 'xps', 'md', 'odf', 'odt', 'ods', 'odp',
                                 'csv', 'tsv', 'xls', 'xlsx', 'ppt', 'pptx', 'pages', 'key', 'numbers', 'show', 'ce',
                                 'zip', 'gz', 'bz2', 'rar', '7z', 'lzh', 'alz']

            file_extension = file_upload_line[extension_dot_pos + 1:-1]

            if file_extension in support_file_list:
                file_exist = True

    return file_exist


def chat_line_checker(chat_line, chat_room):
    content_divider_pos = chat_line.find(' : ')

    chatter_name = chat_line[:content_divider_pos]

    chatting = chat_line[content_divider_pos + 3:]

    chatter = chat_member_searcher(chat_room.memberList, chatter_name)
    if not chatter:
        chatter = ChatMember(chatter_name)
        chat_room.append_member(chatter)

    chat_room.set_chatted_member(chatter)

    chatter.info_counter(MemberInfo.chat)

    if chatting == '<사진>\n':
        chatter.info_counter(MemberInfo.image)

    elif chatting == '<동영상>\n':
        chatter.info_counter(MemberInfo.video)

    elif chatting.find('#') == 0:
        chatter.info_counter(MemberInfo.hashtag)

    elif chatting.find('<연락처') == 0:
        chatter.info_counter(MemberInfo.address)

    elif chatting == '<음성메시지>\n':
        chatter.info_counter(MemberInfo.voice)

    elif file_checker(chatting):
        chatter.info_counter(MemberInfo.file)

    else:
        chatting = head_element_checker(chatting, chatter)

        if chatting != '\n':
            chatter.info_counter(MemberInfo.talk)
            talk_line_checker(chatting, chatter)
