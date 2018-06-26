from MemberInfo import MemberInfo


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
