from api.model import order_history


def get_row() -> list:
    return [
        '\ufeff100006', 'Zollner Electronic Taicang Co Ltd       ',
        '4502937213-734-041  ', '2/27/19', 'SINGLE COLOR LED              ', '3013853', '1', '10000',
        '0.01993', '0.0188', '0', 'H2', '804', 'LTST-C191KGKT            ', 'LTO   ', '1770387-00               ',
        '4016616', '3015725', '39', "DHL INT'L      ", 'DHL#1738502581           ', '5015430', 'CN '
    ]


def get_row_no_ipn() -> list:
    return [
        '\ufeff100006', 'Zollner Electronic Taicang Co Ltd       ',
        '4502937213-734-041  ', '2/27/19', 'SINGLE COLOR LED              ', '3013853', '1', '10000',
        '0.01993', '0.0188', '0', 'H2', '804', 'LTST-C191KGKT            ', 'LTO   ', None,
        '4016616', '3015725', '39', "DHL INT'L      ", 'DHL#1738502581           ', '5015430', 'CN '
    ]


def expected_model() -> dict:
    return {
        'customer': {
            'name': 'Zollner Electronic Taicang Co Ltd',
            'number': '\ufeff100006'
        },
        'order': {
            'orderNumber': 3013853,
            'transactionDate': '2/27/19',
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
    }


def test_get_model_success():
    model = order_history.get_model(get_row())

    assert model == expected_model()


def test_get_model_none():
    model = order_history.get_model(get_row_no_ipn())

    assert model is None
