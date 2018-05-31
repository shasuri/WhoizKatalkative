from chat_member_searcher import chat_member_searcher


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

def gui_set_user(chat_room,user_name):
    member_list = chat_room.memberList

    user_exist = chat_member_searcher(member_list, user_name)

    user_info = chat_member_searcher(member_list, '회원님')

    if not user_exist:
        pass
    else:
        user_info.name = user_exist.name
        user_info.invitedDate = user_exist.invitedDate

        member_list.remove(user_exist)

