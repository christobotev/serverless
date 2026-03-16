import main
import json


def lambda_handler(event: dict, context):
    """
    :param event: the event consumed from SQS
    :param context: the context of the event trigger
    :return: None
    """

    source = event['Records'][0]['eventSourceARN']
    msg_body = json.loads(event['Records'][0]['body'])

    queue_name = source.rsplit(':', 1)[-1].strip()
    main.start_function(msg_body, queue_name)

    print('Consumer Finished!')
