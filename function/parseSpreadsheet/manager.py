def batch_insert(sheet, filename: str, table):
    """
    :param sheet: <class 'xlrd.sheet.Sheet'>
    :param filename: The filename in s3
    :param table:
    :return:
    """
    # get the default column names for this file
    columns_list = _get_column_names_list(sheet.ncols)

    with table.batch_writer() as batch:
        rows_total = sheet.nrows
        current_row = 0

        while current_row < rows_total:
            row = _stringify_list(sheet.row_values(current_row))
            row_as_dictionary = _lists_to_dictionary(columns_list, row)

            base_dictionary = _get_main_fields(current_row, filename)

            # append the row to the base dict
            base_dictionary.update(row_as_dictionary)
            batch.put_item(Item=base_dictionary)
            current_row += 1


def _get_main_fields(row_num: int, filename: str) -> dict:
    return {'fileId': filename, 'rowNum': int(row_num)}


def _get_column_names_list(cols_total: int) -> list:
    names = []
    for i in range(cols_total):
        names.append(str(i))

    return names


def _lists_to_dictionary(list1: list, list2: list) -> dict:
    zipbObj = zip(list1, list2)

    return dict(zipbObj)


def _stringify_list(data: list) -> list:
    new_list = []
    for value in data:
        new_list.append(str(value))

    return new_list
