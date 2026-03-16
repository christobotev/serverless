from main import start_function
from api import s3
from file import xlsx
import manager
import pytest
from botocore.stub import Stubber
import boto3
from db import dynamo


def raise_s3_client_exception(bucket: str, key: str) -> None:
    client = boto3.client('s3')
    stubber = Stubber(client)
    stubber.add_client_error('get_object', 300, 'Access Denied. (File not found)')
    stubber.activate()
    client.get_object(Bucket=bucket, Key=key)


def mock_s3_get_binary_file(bucket: str, key: str):
    return str.encode('class type=bytes')


def mock_xlsx_get_sheet_from_binary(content: bytes):
    return 'class xlrd.sheet.Sheet'


def mock_batch_insert(sheet, filename, table):
    pass


def mock_dynamo_table():
    return "resource dynamodb.Table(name='dev-spreadsheets')"


def test_success_start_function(monkeypatch):
    # These services are not injected so the only way to mock them is with monkeypatch
    monkeypatch.setattr(s3, 'get_binary_file', mock_s3_get_binary_file)
    monkeypatch.setattr(xlsx, 'get_sheet_from_binary', mock_xlsx_get_sheet_from_binary)
    monkeypatch.setattr(manager, 'batch_insert', mock_batch_insert)
    monkeypatch.setattr(dynamo, 'get_spreadsheet_table', mock_dynamo_table)

    bucket = 'testBucket'
    key = 'order_history/testKey'

    start_function(bucket, key)


def test_fail_start_function(monkeypatch, capsys):
    bucket = 'testBucket'
    key = 'order_history/testKey'
    monkeypatch.setattr(s3, 'get_binary_file', raise_s3_client_exception)

    start_function(bucket, key)

    captured = capsys.readouterr()

    assert captured.out == "There was an issue while working with file : order_history/testKey\n"
