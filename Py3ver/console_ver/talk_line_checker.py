from link_line_checker import link_line_checker


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
