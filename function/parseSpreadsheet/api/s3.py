import boto3
import os


def get_binary_file(bucket: str, key: str) -> bytes:
    """
    :param bucket: str
    :param key: str
    :return: binary
    """
    s3 = get_s3()

    s3_response = s3.get_object(Bucket=bucket, Key=key)

    return s3_response['Body'].read()


def get_s3():
    if os.environ["STAGE"] == 'dev':
        return boto3.client(
            service_name='s3',
            aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
            aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
            endpoint_url=os.getenv("MINIO_ENDPOINT", "http://s3:9000")
        )
    else:
        return boto3.client('s3')
