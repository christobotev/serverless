import sys
from api import s3
from file import xlsx
import manager
import ntpath
import logging
from db import dynamo

LOGGER = logging.getLogger()


def start_function(bucket: str, key: str):
    try:
        binary_file = s3.get_binary_file(bucket, key)

        sheet = xlsx.get_sheet_from_binary(binary_file)

        table = dynamo.get_spreadsheet_table()

        manager.batch_insert(sheet, ntpath.basename(key), table)
    except Exception as e:
        # Don't retry automatically (for now at least)
        print('There was an issue while working with file : ' + key)
        LOGGER.error(str(e))

# This is used when the lambda function is triggered locally though main.py vs lambda_function which is for aws


if __name__ == '__main__':
    bucket = str(sys.argv[1])
    key = str(sys.argv[2])
    start_function(bucket, key)
