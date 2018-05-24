import datetime


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
