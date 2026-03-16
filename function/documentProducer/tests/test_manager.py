import asyncio
import pytest
from manager import process
from api import sqs
from unittest.mock import MagicMock


def erp_offers_msg():
    return [
        [
            {
                'customer': {
                    'name': 'Zollner Electronic Taicang Co Ltd', 'number': '\ufeff100006'
                },
                'order': {
                    'orderNumber': 3013853, 'transactionDate': '2/27/19',
                    'transactionQuantity': 10000,
                    'unitPrice': 0.01993,
                    'unitCost': 0.0188,
                    'additionalCost': 0.0,
                    'lineNumber': 1,
                    'customerPurchaseOrder': '4502937213-734-041',
                    'warehouseCode': 'H2',
                    'salesman': '804',
                    'lotNumber': 3015725,
                    'shipmentNumber': 4016616,
                    'shipmentVia': 39,
                    'shipmentTrackingNumber': 'DHL#1738502581',
                    'shipmentMethod': "DHL INT'L",
                    'invoiceNumber': 5015430,
                    'country': 'CN',
                    'ipn': {
                        'ipn': '1770387-00'
                    }
                },
                'item': {
                    'description': 'SINGLE COLOR LED',
                    'mpn': {
                        'mpn': 'LTST-C191KGKT',
                        'manufacturerName': 'LTO'
                    }
                }
            },
            {
                'customer': {
                    'name': 'Zollner Electronic Taicang Co Ltd',
                    'number': '100006'
                },
                'order': {
                    'orderNumber': 3013793,
                    'transactionDate': '2/27/19',
                    'transactionQuantity': 4000,
                    'unitPrice': 0.02173,
                    'unitCost': 0.0205,
                    'additionalCost': 0.0,
                    'lineNumber': 2,
                    'customerPurchaseOrder': '4502930267-734-041',
                    'warehouseCode': 'H2',
                    'salesman': '804',
                    'lotNumber': 3016416,
                    'shipmentNumber': 4016640,
                    'shipmentVia': 39,
                    'shipmentTrackingNumber': 'DHL#1738502581',
                    'shipmentMethod': "DHL INT'L",
                    'invoiceNumber': 5015437,
                    'country': 'CN',
                    'ipn': {
                        'ipn': '1768401-00'
                    }
                },
                'item': {
                    'description': 'SINGLE COLOR LED, RED, 1.2mm',
                    'mpn': {
                        'mpn': 'LTST-S270KRKT', 'manufacturerName': 'LTO'
                    }
                }
            }
        ]
    ]


def mock_sqs_client(loop):
    sqs_client = MagicMock()

    execute_stub = MagicMock(return_value='Success!')

    # Wrap the stub in a coroutine (so it can be awaited)
    execute_coro = asyncio.coroutine(execute_stub)

    sqs_client.send_message = execute_coro
    sqs_client.close = execute_coro

    return sqs_client


@pytest.mark.asyncio
async def test_success(monkeypatch, capsys):
    # The loop is not mandatory here, the mark tells pytest to run
    # the test inside an event loop rather than calling it directly.

    monkeypatch.setattr(sqs, 'get_aiobotocore_client', mock_sqs_client)

    # if any of the sqs client methods were not called an exception will be raised
    await process(erp_offers_msg(), 'erp_offer', None)

    captured = capsys.readouterr()
    assert captured.out == "Time to completion:                           0.00s\n"


def mock_sqs_client_fail(loop):
    """ When send_message fails, sqs_client.close will never be called"""
    sqs_client = MagicMock()

    execute_stub = MagicMock(return_value='Success!')

    # Wrap the stub in a coroutine (so it can be awaited)
    execute_coro = asyncio.coroutine(execute_stub)

    sqs_client.send_message = execute_coro

    return sqs_client


@pytest.mark.asyncio
async def test_fail(monkeypatch, capsys):
    # The loop is not mandatory here, the mark tells pytest to run
    # the test inside an event loop rather than calling it directly.

    monkeypatch.setattr(sqs, 'get_aiobotocore_client', mock_sqs_client_fail)

    # if any of the sqs client methods were not called an exception will be raised
    with pytest.raises(TypeError):
        await process(erp_offers_msg(), 'erp_offer', None)

    captured = capsys.readouterr()
    assert captured.out != "Time to completion:                           0.00s\n"