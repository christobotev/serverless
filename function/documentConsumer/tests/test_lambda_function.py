from lambda_function import lambda_handler
import main
import pytest
from requests.exceptions import HTTPError


def get_sqs_event() -> dict:
    return {
        'Records': [
            {
                'messageId': 'b1af3a3b-7f27-42ee-841f-3b09966ae29e',
                'receiptHandle': 'LongHash==',
                'body': '{"transactions": "arrayOfObjects"}',
                'attributes': {
                    'ApproximateReceiveCount': '1',
                    'SentTimestamp': '1562954813657',
                    'SenderId': 'AROARRUIXCY4WBFJTLQP7:python-functions-dev-document-producer-small',
                    'ApproximateFirstReceiveTimestamp': '1562954813668'
                },
                'messageAttributes': {},
                'md5OfBody': '249db876563c46ea56deee7391cf1fa3',
                'eventSource': 'aws:sqs',
                'eventSourceARN': 'arn:aws:sqs:us-west-2:106587166265:order_history',
                'awsRegion': 'us-west-2'
            }
        ]
    }


def mock_start_function_success(msg_body: dict, queue_name: str):
    # Void
    pass


def mock_start_function_exception(msg_body: dict, queue_name: str):
    # Void
    raise HTTPError("500 Internal Server Error")


def test_success(monkeypatch, capsys):
    monkeypatch.setattr(main, 'start_function', mock_start_function_success)

    lambda_handler(get_sqs_event(), 'Not used')

    # Should be able to see stdout on success
    captured = capsys.readouterr()
    assert captured.out == "Consumer Finished!\n"


def test_fail(monkeypatch, capsys):
    monkeypatch.setattr(main, 'start_function', mock_start_function_exception)

    with pytest.raises(HTTPError):
        lambda_handler(get_sqs_event(), 'Not used')

    captured = capsys.readouterr()
    assert captured.out != "Consumer Finished!\n"
