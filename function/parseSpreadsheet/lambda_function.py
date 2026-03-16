import urllib.parse
import main


def lambda_handler(event: dict, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    main.start_function(bucket, key)
