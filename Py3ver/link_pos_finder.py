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
