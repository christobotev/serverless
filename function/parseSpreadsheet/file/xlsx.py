import xlrd


def get_sheet_from_binary(content: bytes):
    """
    :param content: <class 'bytes'>
    :return: <class 'xlrd.sheet.Sheet'>
    """
    wb = xlrd.open_workbook(file_contents=content)
    return wb.sheet_by_index(0)
