def log_file_opener():
    """Open the chatting log file.
    Log file name and encoding type can be inputted. Default name and type are "KakaoTalkChats.txt" and "utf-8".
    
    Returns:
        log_file (file): Opened file.

    """
    print("Input name of log file : ", end="")
    log_file_name = input()

    if not log_file_name:
        log_file_name = "KakaoTalkChats.txt"

    print("Input encoding type of log file : ", end="")
    log_file_encoding = input()

    if not log_file_encoding:
        log_file_encoding = "utf-8"

    log_file = open(log_file_name, 'r', encoding=log_file_encoding)
    return log_file
