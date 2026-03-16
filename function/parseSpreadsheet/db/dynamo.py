import os
import boto3
from botocore.exceptions import ClientError


def connect():
    """
    :return: <class 'boto3.resources.factory.dynamodb.ServiceResource'> | None
    """
    if os.environ["STAGE"] == 'dev':
        return boto3.resource('dynamodb', region_name=os.environ["AWS_REGION"], endpoint_url='http://dynamo:8000')

    return boto3.resource('dynamodb', region_name=os.environ["AWS_REGION"])


def get_spreadsheet_table():
    """
    :return: <class 'boto3.resources.factory.dynamodb.Table'>
    """
    dynamo = connect()

    try:
        table = dynamo.Table(os.environ["SPREADSHEETS_ROWS_TABLE"])
        table.reload()

        return table
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Table " + os.environ["SPREADSHEETS_ROWS_TABLE"]
                  + " does not exist. Create the table first and try again.")
        else:
            print("Unknown exception occurred while querying for the "
                  + os.environ["SPREADSHEETS_ROWS_TABLE"] + " table. Printing full error:")

