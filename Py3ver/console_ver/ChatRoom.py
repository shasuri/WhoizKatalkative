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
