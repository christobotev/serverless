from main import start_function
import pytest
from requests.exceptions import HTTPError


def order_history_message() -> dict:
    return {
        'transactions': [
            {
                'customer': {
                    'name': 'Zollner Electronics Costa Rica Ltda.',
                    'number': '\ufeff200001'
                },
                'order': {
                    'orderNumber': 3013528,
                    'transactionDate': '2/19/19',
                    'transactionQuantity': 15000,
                    'unitPrice': 0.00343,
                    'unitCost': 0.0024,
                    'additionalCost': 0.0,
                    'lineNumber': 6,
                    'customerPurchaseOrder': '4502903453-649-040',
                    'warehouseCode': 'H2',
                    'salesman': '804',
                    'lotNumber': 3015989,
                    'shipmentNumber': 4016543,
                    'shipmentVia': 30,
                    'shipmentTrackingNumber': '1Z3XV8438604542809',
                    'shipmentMethod': 'WILL ADVISE',
                    'invoiceNumber': 5015356,
                    'country': 'CR',
                    'ipn': {
                        'ipn': '1578450-00'
                    }
                },
                'item': {
                    'description': 'RES CHIP 1206 130R 1% TK100',
                    'mpn': {
                        'mpn': 'RMC1/8K1300FTP',
                        'manufacturerName': 'KAM'
                    }
                }
            }
        ]
    }


def rfq_history_message() -> dict:
    return {
        'transactions': [
            {
                'mpn': '',
                'manufacturerName': '',
                'ipn': ''
            }
        ]
    }


def erp_offer_message() -> dict:
    return {
        'transactions': [
            {
                'mpn': 'BAS7002VH6327',
                'manufacturerName': 'INFINE    ',
                'quantity': '1671000',
                'condition': None,
                'dateCode': None,
                'price': '0.027',
                'vendorNumber': '200263',
                'vendor': 'WEIKENG INDUSTRIAL CO. LTD              ',
                'uploadedAt': '2019-06-03T00:00:00.000Z',
                'owner': 'KARMUNL                       ',
                'notes': 'SPQ 3K, moq 15k, 8 weeks '
            },
        ]
    }


def test_success_order_history(requests_mock):
    requests_mock.post("http://webserver/api/quote_history/orders", json={'response': 'success'}, status_code=200)

    try:
        start_function(order_history_message(), 'order_history')
    except Exception as e:
        # just being explicit that there should be no exceptions triggered
        pytest.fail("Force fail the test. " + str(e))


def test_success_erp_offer(requests_mock):
    requests_mock.post("http://webserver/api/quote_unverified_offers", json={'response': 'success'}, status_code=200)

    try:
        start_function(order_history_message(), 'erp_offer')
    except Exception as e:
        # just being explicit that there should be no exceptions triggered
        pytest.fail("Force fail the test. " + str(e))


def test_success_rfq_history(requests_mock):
    requests_mock.post("http://webserver/api/rfq_history/items", json={'response': 'success'}, status_code=200)

    try:
        start_function(order_history_message(), 'rfq_history')
    except Exception as e:
        # just being explicit that there should be no exceptions triggered
        pytest.fail("Force fail the test. " + str(e))


def test_fail_start_function(requests_mock):
    requests_mock.post(
        "http://webserver/api/rfq_history/items",
        json={'response': 'Internal server error'},
        status_code=500
    )

    with pytest.raises(HTTPError):
        start_function(order_history_message(), 'rfq_history')

