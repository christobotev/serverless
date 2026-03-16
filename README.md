## Serverless Data Ingestion (AWS Lambda)

This project processes files uploaded to S3 and routes the data through SQS, external APIs, and DynamoDB.

## What it does

### 1. CSV producer pipeline
- Trigger: S3 object created for `.csv` files under:
  - `order_history/`
  - `rfq_history/`
  - `erp_offer/`
- Lambda: `document-producer-small` and `document-producer-large`
- Behavior:
  - Download CSV from S3
  - Parse and map rows to transaction models
  - Batch rows (100 per message)
  - Push batches to SQS

### 2. SQS consumer pipeline
- Trigger: SQS messages (`order_history` / `rfq_history` queues)
- Lambda: `document-consumer`
- Behavior:
  - Read one message at a time (`batchSize: 1`)
  - Route payload to Bridge API endpoint based on queue name
  - Send authenticated HTTP request to Bridge

### 3. Spreadsheet parser pipeline
- Trigger: S3 object created for `.xlsx` files under `spreadsheets/`
- Lambda: `parseSpreadsheet`
- Behavior:
  - Download xlsx file from S3
  - Parse rows
  - Store each row in DynamoDB (`fileId` + `rowNum`)

## Project structure

- `function/documentProducer` - CSV ingest and SQS producer
- `function/documentConsumer` - SQS consumer and Bridge API forwarder
- `function/parseSpreadsheet` - XLSX parser and DynamoDB writer
- `layer/` - Lambda layers
- `serverless.yml` - Lambda and event configuration
- `docker-compose.yaml` - local dev services

## Local development

1. Copy env template:
   - `cp .env.dist .env`
2. Fill required values in `.env` (AWS, SQS, Bridge, MinIO):
   - `MINIO_ACCESS_KEY`
   - `MINIO_SECRET_KEY`
   - `MINIO_ENDPOINT` (default `http://s3:9000`)
3. Install local dependencies:
   - `make init`

### Helpful container commands

- `make bash/node`
- `make bash/python`

### DynamoDB admin (local)

Inside the node container, run `dynamodb-admin`, then open:
- `http://localhost:7001`

Note: local DynamoDB is in-memory, so data is lost on restart.

## Deployment

- Deploy lambdas:
  - `make deploy/functions/python`
- Remove lambdas and S3 event wiring:
  - `make remove/functions/python`

Warning: `sls remove` can delete user data/resources.

## Testing

Run tests inside the python environment:
- `pipenv run pytest`

## Adding a new function

1. Add function code under `function/<name>/`.
2. Add/update `requirements.txt` for that function.
3. Register function in `serverless.yml`.
4. Add installation hook in `Makefile` if needed.
5. Deploy with `sls deploy` (or the existing make target).

## Adding a layer

### Layer as prebuilt artifact

1. Create a folder in `layer/`.
2. Add `requirements.txt`.
3. Copy `get_layer_packages.sh` into that folder.
4. Run `sh get_layer_packages.sh` (outside container).
5. Zip contents (example: `zip -r my-layer.zip .`).
6. Keep only the archive if desired.
7. Configure layer artifact in `serverless.yml`.
8. Deploy with `sls deploy`.

### Layer packaged at deploy time

1. Create a folder in `layer/`.
2. Add `requirements.txt`.
3. Copy `get_layer_packages.sh`.
4. Run `sh get_layer_packages.sh` (outside container).
5. Configure layer in `serverless.yml`.
6. Deploy with `sls deploy`.
