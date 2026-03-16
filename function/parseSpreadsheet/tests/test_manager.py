from main import start_function
from api import s3
from file import xlsx
import manager
import pytest
from botocore.stub import Stubber
import boto3
from db import dynamo
from unittest.mock import MagicMock, PropertyMock
import os
from manager import batch_insert
from botocore.exceptions import ClientError


def get_all_sheet_rows():
    return [
        ['NUMBER', 'NUMBER', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT',
         'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'NUMBER', 'DATE', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER',
         'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'TEXT', 'TEXT', 'TEXT', 'NUMBER', 'NUMBER',
         'NUMBER', 'NUMBER', 'NUMBER', 'TEXT', 'TEXT', 'TEXT', 'NUMBER', 'NUMBER', 'NUMBER', 'TEXT', 'DATE', 'TEXT',
         'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'NUMBER'
         ],
        ['1', '1', '001 DE Zandt EZ1', 'PPR 101859', 'Medical', '', 'DDP', '30d 3% 90d net', 'Customer', '',
         'Integrated circuit', '1234554-00', '234234-ADFA', 'v2', 'IC-1234pq34', 'Infineon', '234099-09', '', 42948.0,
         '', '', '', '', '', '', '', '', '', '', '', 'pcs', '795863', 'Example S.E.', '', '', '', '', '', 'EUR', 'yes',
         'yes', 6.0, 1000.0, 1000.0, 'Tray', 42500.0, 'S', 4.0, '', '', '', '', '', 'yes', '', '', '', '', 1.0
         ]
    ]


def get_mocked_sheet_row_value(row):
    return get_all_sheet_rows()[row]


def get_mock_sheet():
    sheet = MagicMock()
    sheet.ncols = 59
    sheet.nrows = 2
    sheet.row_values = MagicMock(side_effect=get_mocked_sheet_row_value) # side effect makes it callable with args like sheet.row_values(1)

    return sheet


def test_success_start_function():
    sheet = get_mock_sheet()
    table = MagicMock()

    batch_insert(sheet, 'dummy_file', table)

    assert table.batch_writer().__enter__().put_item.call_count == len(get_all_sheet_rows())
    table.batch_writer().__enter__().put_item.assert_called()


def test_exception_start_function():
    sheet = get_mock_sheet()

    table = MagicMock()
    table.batch_writer = MagicMock()
    table.batch_writer().__enter__().put_item = MagicMock()
    table.batch_writer().__enter__().put_item.side_effect = ClientError({'Error': {'Code': '403', 'Message': 'Unauthorized'}}, 'PutItem')

    with pytest.raises(ClientError):
        batch_insert(sheet, 'dummy_file', table)

    assert table.batch_writer().__enter__().put_item.call_count != len(get_all_sheet_rows())
    table.batch_writer().__enter__().put_item.assert_called_once()