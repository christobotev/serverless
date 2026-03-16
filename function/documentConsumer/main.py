import sys
import requests
from requests.auth import HTTPBasicAuth
import os
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def _empty_message(message: dict) -> bool:
    """ Private method """
    if not message['transactions']:
        print('Rows are empty, nothing to import!')
        return False

    return True


def _get_url(queue_name) -> str:
    """
    Returns the API endpoint for the given queue, if exists
    Throws a Value Error Exception
    """

    if queue_name == 'order_history':
        return os.environ['BRIDGE_API'] + '/quote_history/orders'
    elif queue_name == 'rfq_history':
        return os.environ['BRIDGE_API'] + '/rfq_history/items'
    elif queue_name == 'erp_offer':
        return os.environ['BRIDGE_API'] + '/quote_unverified_offers'

    raise ValueError('Unknown Queue!')


def start_function(message: dict, queue_name: str) -> None:
    if _empty_message(message):
        url = _get_url(queue_name)
        auth = HTTPBasicAuth(os.environ['BRIDGE_USERNAME'], os.environ['BRIDGE_PASSWORD'])
        response = requests.post(url, json=message, auth=auth)

        LOGGER.info('Queue : ' + str(queue_name))
        LOGGER.info('API Call result: ' + str(response.json()))

        # will raise an HTTPError if the HTTP request returned an unsuccessful status code.
        response.raise_for_status()

# This is used when the lambda function is triggered locally though main.py vs lambda_function which is for aws


if __name__ == '__main__':
    message = str(sys.argv[1])
    start_function(message)
