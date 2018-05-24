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
