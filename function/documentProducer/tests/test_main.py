from main import start_function
from api import s3
from file import csv
from botocore.stub import Stubber
import manager
import boto3
import asyncio


def mock_s3_get_file(bucket: str, key: str) -> list:
    return ["\ufeff100006,Zollner Electronic Taicang Co Ltd       ,4502937213-734-041  ,2/27/19,SINGLE COLOR LED              ,3013853,1,10000,0.01993,0.0188,0,H2,804,LTST-C191KGKT            ,LTO   ,1770387-00               ,4016616,3015725,39,DHL INT'L      ,DHL#1738502581           ,5015430,CN \r\n",
            '100006,Zollner Electronic Taicang Co Ltd       ,4502930267-734-041  ,2/27/19,"SINGLE COLOR LED, RED, 1.2mm  ",3013793,2,4000,0.02173,0.0205,0,H2,804,LTST-S270KRKT            ,LTO   ,1768401-00               ,4016640,3016416,39,DHL INT\'L      ,DHL#1738502581           ,5015437,CN \r\n',
            '100006,Zollner Electronic Taicang Co Ltd       ,4502992302-708-041  ,2/27/19,FAN MB WITH CABLE             ,3014465,1,0,0,0,0,H2,804,XF-65654                 ,SAY   ,2017367-00               ,0,3016254,,,,5015312, \r\n',
            '91609,ZOLLNER ELEKTRONIK AG                   ,4502911101-784-011  ,2/27/19,3.3V SINGLE POWER SUPPLY 10/10,3013590,1,0,0,0,0,HK,804,KSZ8721BLI-TR            ,MCP   ,1684199-00               ,0,3016243,,,,5015323,']


def mock_csv_parse(lines: list) -> list:
    """ Data just to get you familiar with what's expected (what the data looks like) """
    return [
        ['\ufeff100006', 'Zollner Electronic Taicang Co Ltd       ', '4502937213-734-041  ', '2/27/19',
         'SINGLE COLOR LED              ', '3013853', '1', '10000', '0.01993', '0.0188', '0', 'H2', '804',
         'LTST-C191KGKT            ', 'LTO   ', '1770387-00               ', '4016616', '3015725', '39',
         "DHL INT'L      ", 'DHL#1738502581           ', '5015430', 'CN '],
        ['100006', 'Zollner Electronic Taicang Co Ltd       ', '4502930267-734-041  ', '2/27/19',
         'SINGLE COLOR LED, RED, 1.2mm  ', '3013793', '2', '4000', '0.02173', '0.0205', '0', 'H2', '804',
         'LTST-S270KRKT            ', 'LTO   ', '1768401-00               ', '4016640', '3016416', '39',
         "DHL INT'L      ", 'DHL#1738502581           ', '5015437', 'CN '],
        ['100006', 'Zollner Electronic Taicang Co Ltd       ', '4502992302-708-041  ', '2/27/19',
         'FAN MB WITH CABLE             ', '3014465', '1', '0', '0', '0', '0', 'H2', '804', 'XF-65654                 ',
         'SAY   ', '2017367-00               ', '0', '3016254', None, None, None, '5015312', None],
        ['91609', 'ZOLLNER ELEKTRONIK AG                   ', '4502911101-784-011  ', '2/27/19',
         '3.3V SINGLE POWER SUPPLY 10/10', '3013590', '1', '0', '0', '0', '0', 'HK', '804', 'KSZ8721BLI-TR            ',
         'MCP   ', '1684199-00               ', '0', '3016243', None, None, None, '5015323', None]
    ]


def mock_import_manager_return(messages: list, queue_name: str, loop) -> bool:
    yield from asyncio.sleep(1)
    return True


def raise_client_exception(bucket: str, key: str) -> None:
    client = boto3.client('s3')
    stubber = Stubber(client)
    stubber.add_client_error('get_object', 300, 'Access Denied. (File not found)')
    stubber.activate()
    client.get_object(Bucket=bucket, Key=key)


def test_success_start_function(monkeypatch, capsys):
    monkeypatch.setattr(s3, 'get_file', mock_s3_get_file)
    monkeypatch.setattr(csv, 'parse', mock_csv_parse)
    monkeypatch.setattr(manager, 'process', mock_import_manager_return)
    bucket = 'testBucket'
    key = 'order_history/testKey'

    start_function(bucket, key)

    captured = capsys.readouterr()

    assert captured.out == "Lambda finished successfully!\n"


def test_fail_start_function(monkeypatch, capsys):
    bucket = 'testBucket'
    key = 'order_history/testKey'
    monkeypatch.setattr(s3, 'get_file', raise_client_exception)

    start_function(bucket, key)

    captured = capsys.readouterr()
    assert captured.out == "There was an issue while working with file : order_history/testKey\n"


def test_missing_model(monkeypatch, capsys):
    bucket = 'testBucket'
    key = 'made_up_model/testKey'
    monkeypatch.setattr(s3, 'get_file', mock_s3_get_file)
    monkeypatch.setattr(csv, 'parse', mock_csv_parse)

    start_function(bucket, key)

    captured = capsys.readouterr()
    assert captured.out == "There was an issue while working with file : made_up_model/testKey\n"
