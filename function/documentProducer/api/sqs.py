import aiobotocore
import os


def get_aiobotocore_client(loop):
    """
    :param loop: <class 'asyncio.unix_events._UnixSelectorEventLoop'>
    :return: <class 'aiobotocore.client.SQS'>
    """
    session = aiobotocore.get_session(loop=loop)

    return session.create_client('sqs', region_name=os.environ['AWS_REGION'], endpoint_url=os.environ['SQS_ENDPOINT'])

