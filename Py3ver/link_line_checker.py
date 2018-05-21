from link_pos_finder import link_pos_finder
from MemberInfo import MemberInfo


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
