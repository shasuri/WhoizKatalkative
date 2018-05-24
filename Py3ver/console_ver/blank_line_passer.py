def blank_line_passer(pass_file, pass_line_num):
    """Pass blank lines of the log file.
    
    Args:
        pass_file (file): Log file.
        pass_line_num (int): The number of line to be passed.
    
    """
    for passNum in range(pass_line_num):
        next(pass_file)
