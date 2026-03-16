import boto3
import os


def get_file(bucket: str, key: str) -> list:
    response = _pull(bucket, key)

    return response['Body'].read().decode('utf-8').splitlines(True)


def _pull(bucket: str, key: str) -> dict:
    """ Private function. Pulls file from aws s3 | Throws ValueError """
    s3 = _get_s3()

    return s3.get_object(Bucket=bucket, Key=key)


def _get_s3():
    if os.environ["STAGE"] == 'dev':
        return boto3.client(
            service_name='s3',
            aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
            aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
            endpoint_url=os.getenv("MINIO_ENDPOINT", "http://s3:9000")
        )
    else:
        return boto3.client('s3')
