import sys
from api import s3
from file import csv
import manager
import asyncio
import importlib
from typing import Generator
import logging

ITEMS_PER_REQUEST = 100
LOGGER = logging.getLogger()


def _has_rows(rows: list) -> bool:
    if not rows:
        print('Rows are empty, nothing to import!')
        return False

    return True


def _break_down_rows(rows: list, document_type: str) -> list:
    formatted_rows = []
    model = importlib.import_module('api.model.' + document_type)

    for index, row in enumerate(rows):
        transaction = model.get_model(row)
        if transaction is not None:
            formatted_rows.append(transaction)

    return list(_divide_chunks(formatted_rows, ITEMS_PER_REQUEST))


def _divide_chunks(l: list, n: int) -> Generator:
    for i in range(0, len(l), n):
        yield l[i:i + n]


def start_function(bucket: str, key: str) -> None:
    """ document_type === document/api model === queue name """
    try:
        document_type = key.partition('/')[0]
        rows_list = s3.get_file(bucket, key)

        rows = csv.parse(rows_list)

        if _has_rows(rows):
            rows_structured_by_message = _break_down_rows(rows, document_type)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(manager.process(rows_structured_by_message, document_type, loop))

            print('Lambda finished successfully!')
    except Exception as e:
        # If we get an exception, don't retry automatically
        # We can use step function if we need better control over this process
        print('There was an issue while working with file : ' + key)
        LOGGER.error(str(e))


# This is used when the lambda function is triggered locally though main.py vs lambda_function which is for aws


if __name__ == '__main__':
    bucket = str(sys.argv[1])
    key = str(sys.argv[2])
    start_function(bucket, key)

