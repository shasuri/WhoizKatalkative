import datetime
from enum import Enum


class ChatRoom:
    """The class which construct chatting room instance with information.
    
    Attributes:
        title (str): Title of chatting room.
        memberNum (int): The number of member when log was saved.
        memberList (list): List of members constructed with ChatMember instance.
        preChatMember (ChatMember): ChatMember instance who chatted on a previous line.
        logSaveDate (datetime.datetime): datetime.datetime instance which is chatting log saved time.
    """

    def __init__(self, title, member_number, room_type='specified'):
        self.title = title
        self.memberNum = member_number
        self.roomType = room_type
        self.memberList = []
        self.preChatMember = ''
        self.logSaveDate = ''

    def set_log_saved_date(self, date):
        """Set the time when log was saved on logSaveDate.

        Args:
            date (datetime.datetime): Second line of log file parsed by date_checker function. 
        """
        self.logSaveDate = date

    def append_member(self, member):
        """Append the ChatMember instance in memberList.

        Args:
            member (ChatMember): ChatMember instance.
        """
        self.memberList.append(member)

    def set_chatted_member(self, chatted_member):
        """Save the ChatMember instance who chatted on a previous line.

        Args:
            chatted_member (ChatMember): ChatMember instance who chatted on a previous line.
        """
        self.preChatMember = chatted_member


class MemberInfo(Enum):
    """Enumeration class to make easy to manage ChatMember attributes.
    """
    chat = 0
    talk = 1
    talkSize = 2
    emoticon = 3
    image = 4
    link = 5
    video = 6
    hashtag = 7
    file = 8
    address = 9
    voice = 10


class ChatMember:
    """The Class which save members' information.

    Attributes:
        name (str): Name of the member.
        invitedDate (datetime.datetime): The time when the member was invited.
        infoList (list): List of member's various information.
    """

    def __init__(self, name, invite_date=''):
        self.name = name
        self.invitedDate = invite_date
        self.infoList = [0 for infoIndex in range(11)]

    def info_counter(self, info):
        """Count the information using MemberInfo enumeration value.

        Args:
            info (MemberInfo): Using value and load the sequence number which is right to the information.
        """
        self.infoList[info.value] += 1

    def talk_counter(self, talk_length):
        """Count the talk length on 11th element in infoList.

        Args:
            talk_length (int): Talk length of the chatting.
        """
        self.infoList[MemberInfo.talkSize.value] += talk_length


def chat_room_info_checker(info_line):
    """Check first line of the log file and make ChatRoom instance
    
    Args:
        info_line (str): First line of the log file which contains chatting title and member number.

    Returns:
        chat_room (ChatRoom): ChatRoom instance of the chatting room.

    """
    sliced_line = info_line[1:]  # Slice the crashed byte on first line.
    sliced_line = sliced_line.split()

    if '님과' in sliced_line:
        divider_pos = sliced_line.index('님과')

        if divider_pos == 1:  # Personal chat room case.
            chat_room_type = 'personal'
            title = sliced_line[0]
            member_number = 2

        elif divider_pos == 2:  # Non specified group chat room name case.
            chat_room_type = 'nspecifed'
            title = " ".join(sliced_line[:-4])
            member_number = int(sliced_line[-4])

    else:  # Specified group chat room name case.
        chat_room_type = 'specifed'
        title = " ".join(sliced_line[:-3])
        member_number = int(sliced_line[-3])

    chat_room = ChatRoom(title, member_number, chat_room_type)

    return chat_room


def date_checker(date_line):
    """Parse the date string which formatted by Kakaotalk.
    
    Args:
        date_line (str): The date string.

    Returns:
        datetime.datetime: datetime.datetime instance.

    """
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
    """Pass blank lines of the log file.
    
    Args:
        pass_file (file): Log file.
        pass_line_num (int): The number of line to be passed.
    
    """
    for passNum in range(pass_line_num):
        next(pass_file)


def line_type_checker(line, chat_room):
    """Check the type of content line by patterns.
    
    Args:
        line (str): Content line of the log file.
        chat_room (ChatRoom): ChatRoom instance of the chatting room.
    
    Examples:
        `2018년 3월 23일 오후 11:16, Jack : Life is short, You need Python.`

    """
    if main_line_checker(line):  # Check the line is a main line or an extra line.
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
    """Check the line is a main line or an extra line by the position of the date part string.
    
    Args:
        line (str): Content line to be checked.

    Returns:
        main_line_check (bool): True means the line is a main line, False means the line is an extra line.

    """
    year_pos = line.find('년')
    month_pos = line.find('월')
    day_pos = line.find('일')
    meridem_pos = line.find('오')
    time_divider_pos = line.find(':')

    main_line_check = ((year_pos == 4) and
                       ((month_pos > 6) and (month_pos < 9)) and
                       ((day_pos > 9) and (day_pos < 13)) and
                       ((meridem_pos > 11) and (meridem_pos < 15)) and
                       ((time_divider_pos > 15) and (time_divider_pos < 20)))  # Range of position of the normal date part string.

    return main_line_check


def invite_line_checker(invite_line, invite_chat_room, invite_date):
    """Check the inviting line and append the ChatMember instance who is in the inviting line on the member list.
    
    Args:
        invite_line (str): Inviting line which is checked by line_type_checker function.
        invite_chat_room (ChatRoom): ChatRoom instance of the chatting room.
        invite_date (datetime.datetime): datetime.datetime instance of the inviting date.
    
    Examples:
        `Jack님이 Mary님, Jill님과 Cindy님을 초대했습니다.`

    """

    invite_line = invite_line.split('님')
    invite_line.pop()  # Delete the useless part.

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
    """Search the ChatMember instance by member's name.

    Args:
        member_list (list): memberList of the ChatRoom instance.
        search_member_name (str): Searching name.

    Returns:
        searchMember (ChatMember): The member who has the search_member_name and exists in member_list.
        bool: False means the member does not exist in member_list.

    """
    for searchMember in member_list:
        if searchMember.name == search_member_name:
            return searchMember

    return False


def link_line_checker(link_line, link_uploader):
    """Recursive function which check the link_line contains the internet link or not by checking existence of 'http://' or 'https://'

    Args:
        link_line (str): Line to be checked contains the internet link.
        link_uploader (ChatMember): ChatMember instance of who chatted the link_line.
    
    Returns:
        link_line_checker (function): Do recursive process with the line which excepts single link string.
        link_line (str): If there is no more link string, return the line which excepts all link strings.

    Examples:
        `https://www.python.org`
    
    """
    link_pos = link_pos_finder(link_line)  # Find the link stirng.

    if link_pos > -1:  # Link string founded.
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
    """Find the string which contains 'http://' or 'https://'.
    
    Args:
        link_line (str): The line may contains 'http://' or 'https://'.

    Return:
        link_pos (int): The position of http part. If http part does not exist in link_line, return -1.

    """
    link_pos = -1

    if 'http://' in link_line:
        link_pos = link_line.find('http://')
    elif 'https://' in link_line:
        link_pos = link_line.find('https://')

    return link_pos


def talk_line_checker(talk_line, talker):
    """Check the talk_line except link part and count the number of talk and talking length on talker's information.
    
    Args:
        talk_line (str): The line to be excepted link part and then gives talking length.
        talker (ChatMember): ChatMember instance of who chatted the talk_line.

    Examples:
        talk_line (str): `https://www.python.org/dev/peps/pep-0020/ Beautiful is better than ugly.`

    """
    talk_line = link_line_checker(talk_line, talker)

    talk_length = len(talk_line) - 1
    talker.talk_counter(talk_length)


def head_element_checker(chat_line, talker):
    """Check the chat_line contains the elements which can be located ahead of the talk or not.
    For example, emoticon or images of the chatting room board.
    
    Args:
        chat_line (str): The line to be checked contains the head elements or not.
        talker (ChatMember): ChatMember instance of who chat the chat_line.

    Returns:
        chat_line (str): The line which is excepted the head elements.

    Examples:
        `(emoticon)Explicit is better than implicit.`

    """
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
    """Check the file_upload_line is the file uploaded log or not.

    Args:
        file_upload_line (str): The line to be checked that is the file uploaded log or not.

    Returns:
        file_exist (bool): True means file_upload_line is the file uploaded log, False means not.

    Examples:
        `python-3.6.5-docs-pdf-letter.zip`

    """
    file_exist = False
    extension_dot_pos = file_upload_line.rfind('.')  # Find position of the extension dot by reverse find.

    if extension_dot_pos > -1:
        line_length = len(file_upload_line)

        if line_length > 6 and ((extension_dot_pos == line_length - 4) or (extension_dot_pos == line_length - 5) or (
                extension_dot_pos == line_length - 6)):  # Check position of the extension dot is on right position.

            support_file_list = {'mp3', 'wav', 'flac', 'tta', 'tak', 'aac', 'wma', 'ogg', 'm4a', 'doc', 'docx', 'hwp',
                                 'txt', 'rtf', 'xml', 'pdf', 'wks', 'wps', 'xps', 'md', 'odf', 'odt', 'ods', 'odp',
                                 'csv', 'tsv', 'xls', 'xlsx', 'ppt', 'pptx', 'pages', 'key', 'numbers', 'show', 'ce',
                                 'zip', 'gz', 'bz2', 'rar', '7z', 'lzh', 'alz'}  # File extensions which are supported by Kakaotalk.

            file_extension = file_upload_line[extension_dot_pos + 1:-1]

            if file_extension in support_file_list:
                file_exist = True

    return file_exist


def chat_line_checker(chat_line, chat_room):
    """Parse the chatter and chatting contents and check there is a solo content which can not contains other contents.
    
    Args:
        chat_line (str): The line to be parsed and checked.
        chat_room (ChatMember): ChatMember instance of who chat the link_line.

    Examples:
        `Jack : #Simple is better than complex.`
        
    """
    content_divider_pos = chat_line.find(' : ')

    chatter_name = chat_line[:content_divider_pos]

    chatting = chat_line[content_divider_pos + 3:]

    chatter = chat_member_searcher(chat_room.memberList, chatter_name)
    if not chatter:
        chatter = ChatMember(chatter_name)
        chat_room.append_member(chatter)

    chat_room.set_chatted_member(chatter)

    chatter.info_counter(MemberInfo.chat)

    if chatting == '\n':
        chatter.info_counter(MemberInfo.emoticon)

    elif chatting == '<사진>\n':
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

def set_user_name(chat_room):
    """Set the user's name to '회원님' which is default user name in log file, and delete the member instance in member list.
    Args:
        chat_room (ChatRoom): ChatRoom instance of the chatting room.
    """
    print("What is your name? : ", end="")
    user_name = input()

    member_list = chat_room.memberList

    user_exist = chat_member_searcher(member_list, user_name)

    user_info = chat_member_searcher(member_list, '회원님')

    if not user_exist:
        pass
    else:
        user_info.name = user_exist.name
        user_info.invitedDate = user_exist.invitedDate

        member_list.remove(user_exist)