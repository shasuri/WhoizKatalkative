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
