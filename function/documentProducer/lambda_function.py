import main
import urllib.parse


print('Loading function...')


def lambda_handler(event: dict, context):
    """
   :param event: the event consumed from SQS
   :param context: the context of the event trigger
   :return: None
   """

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    main.start_function(bucket, key)
