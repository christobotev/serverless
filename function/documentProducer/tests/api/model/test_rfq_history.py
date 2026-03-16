from api.model import rfq_history


def get_row() -> list:
    return [
        'NA', '2019-06-07T00:00:00.000Z', '100043', 'Zollner Electronics Costa Rica Ltda.    ',
        '1182263', '1', 'MLZ2012E100M             ', 'TDK   ', '22000', '0', '0', None, '5714820-11', '0'
    ]


def get_row_no_mpn() -> list:
    return [
        'NA', '2019-06-07T00:00:00.000Z', '100043', 'Zollner Electronics Costa Rica Ltda.    ',
        '1182263', '1', None, 'TDK   ', '22000', '0', '0', None, '5714820-11', '0'
    ]


def get_row_no_ipn() -> list:
    return [
        'NA', '2019-06-07T00:00:00.000Z', '100043', 'Zollner Electronics Costa Rica Ltda.    ',
        '1182263', '1', 'MLZ2012E100M             ', 'TDK   ', '22000', '0', '0', None, None, '0'
    ]


def get_row_no_mfr() -> list:
    return [
        'NA', '2019-06-07T00:00:00.000Z', '100043', 'Zollner Electronics Costa Rica Ltda.    ',
        '1182263', '1', 'MLZ2012E100M             ', None, '22000', '0', '0', None, '5714820-11', '0'
    ]


def expected_model() -> dict:
    return {
        'mpn': 'MLZ2012E100M',
        'manufacturerName': 'TDK',
        'ipn': '5714820-11'
    }


def test_get_model_success():
    model = rfq_history.get_model(get_row())

    assert model == expected_model()


def test_get_model_no_mpn():
    model = rfq_history.get_model(get_row_no_mpn())

    assert model is None


def test_get_model_no_ipn():
    model = rfq_history.get_model(get_row_no_ipn())

    assert model is None


def test_get_model_no_mfr():
    model = rfq_history.get_model(get_row_no_mfr())

    assert model is None