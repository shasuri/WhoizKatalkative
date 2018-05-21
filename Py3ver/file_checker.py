def file_checker(file_upload_line):
    """Check the file_upload_line is the file uploaded log or not.

    Args:
        file_upload_line (str): The line to be checked that is the file uploaded log or not.

    Returns:
        file_exist (bool): True means file_upload_line is the file uploaded log, False means not.

    Examples:
        `python-3.6.5-docs-pdf-letter.zip`

    """
    file_exist = False
    extension_dot_pos = file_upload_line.rfind('.')  # Find position of the extension dot by reverse find.

    if extension_dot_pos > -1:
        line_length = len(file_upload_line)

        if line_length > 6 and ((extension_dot_pos == line_length - 4) or (extension_dot_pos == line_length - 5) or (
                extension_dot_pos == line_length - 6)):  # Check position of the extension dot is on right position.

            support_file_list = ['mp3', 'wav', 'flac', 'tta', 'tak', 'aac', 'wma', 'ogg', 'm4a', 'doc', 'docx', 'hwp',
                                 'txt', 'rtf', 'xml', 'pdf', 'wks', 'wps', 'xps', 'md', 'odf', 'odt', 'ods', 'odp',
                                 'csv', 'tsv', 'xls', 'xlsx', 'ppt', 'pptx', 'pages', 'key', 'numbers', 'show', 'ce',
                                 'zip', 'gz', 'bz2', 'rar', '7z', 'lzh', 'alz']  # File extensions which are supported by Kakaotalk.

            file_extension = file_upload_line[extension_dot_pos + 1:-1]

            if file_extension in support_file_list:
                file_exist = True

    return file_exist
