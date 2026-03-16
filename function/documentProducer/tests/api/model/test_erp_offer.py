from api.model import erp_offer


def get_row() -> list:
    return [
        'AD7864ASZ-1              ', 'AD        ', '200', None, '10+       ',
        '14.4', '83690', 'Winking Semiconductor LTD               ', '2019-06-03T00:00:00.000Z',
        'SWU                           ', None
    ]


def get_row_no_mfr() -> list:
    return [
        'AD7864ASZ-1              ', None, '200', None, '10+       ',
        '14.4', '83690', 'Winking Semiconductor LTD               ', '2019-06-03T00:00:00.000Z',
        'SWU                           ', None
    ]


def get_row_no_mpn() -> list:
    return [
        None, 'AD        ', '200', None, '10+       ',
        '14.4', '83690', 'Winking Semiconductor LTD               ', '2019-06-03T00:00:00.000Z',
        'SWU                           ', None
    ]


def expected_model() -> dict:
    return {
        'mpn': 'AD7864ASZ-1',
        'manufacturerName': 'AD',
        'quantity': '200',
        'condition': None,
        'dateCode': '10+',
        'price': '14.4',
        'vendorNumber': '83690',
        'vendor': 'Winking Semiconductor LTD',
        'uploadedAt': '2019-06-03T00:00:00.000Z',
        'owner': 'SWU',
        'notes': None
    }


def test_get_model_success():
    model = erp_offer.get_model(get_row())

    assert model == expected_model()


def test_get_model_no_mpn():
    model = erp_offer.get_model(get_row_no_mpn())

    assert model is None


def test_get_model_no_mfr():
    model = erp_offer.get_model(get_row_no_mfr())

    assert model is None