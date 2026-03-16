from timeit import default_timer
import os
from api import sqs
import json


async def process(messages: list, queue_name: str, loop) -> None:
    sqs_client = sqs.get_aiobotocore_client(loop)

    start_timing = default_timer()
    for index, message in enumerate(messages):
        await sqs_client.send_message(
            QueueUrl=os.environ['SQS_QUEUE_URL'] + queue_name,
            MessageBody=str(json.dumps({"transactions": message}))
        )

    await sqs_client.close()

    _print_ttc(start_timing)


def _print_ttc(start_time: float) -> None:
    """Prints time to completion """
    elapsed = default_timer() - start_time
    time_completed_at = "{:5.2f}s".format(elapsed)

    print("{0:<30} {1:>20}".format('Time to completion: ', time_completed_at))
