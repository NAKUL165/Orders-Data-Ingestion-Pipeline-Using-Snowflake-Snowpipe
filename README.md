## Orders-Data-Ingestion-Pipeline-Using-Snowflake-Snowpipe
Tech Stack: Snowflake, Snowpipe, AWS S3, SNS, SQS, SQL
## Project Overview

This project demonstrates a cloud-based, event-driven ETL pipeline using Snowflake Snowpipe to automate the ingestion of order data from AWS S3 into Snowflake. It ensures real-time data availability, schema validation, and historical tracking, enabling efficient analytics and reporting on order transactions.

The pipeline integrates SNS and SQS notifications to trigger automated ingestion whenever new files arrive in S3, eliminating manual intervention and ensuring data freshness.

## Features

## Event-driven ingestion of multi-source order data into Snowflake using Snowpipe.

Automated schema validation and error handling for reliable data processing.

Historical tracking and monitoring of data loads for analytics readiness.

Integration with S3, SNS, and SQS for secure, real-time data ingestion.

SQL-based monitoring to check pipe status, ingestion history, and loaded records.

## Architecture

Source: Raw order data files uploaded to an S3 bucket (s3://<YOUR_BUCKET_NAME>/<FOLDER_PATH>/).

Notification: S3 bucket triggers an SNS notification whenever a new file is uploaded. The SNS notification is delivered to an SQS queue subscribed to the topic.

Snowpipe: Snowflake Snowpipe is configured with a notification integration that listens to the SQS queue. It automatically ingests new files into the orders_Datalz table.

Data Validation & Monitoring: SQL queries track ingestion history, pipe status, and validate schema, ensuring accurate and timely data ingestion.

Setup Steps

## AWS Setup:

Create an S3 bucket for raw order data.

Create an SNS topic.

Create an SQS queue and subscribe it to the SNS topic.

Configure S3 event notifications to publish object creation events to the SNS topic.

Create an IAM Role for Snowflake with:

s3:GetObject, s3:ListBucket

sqs:ReceiveMessage, sqs:DeleteMessage, sqs:GetQueueAttributes

Attach the External ID from Snowflake integration to the trust policy.

## Snowflake Setup:

Create a database and target table (orders_Datalz).

Create a file format (CSV) and storage integration for S3.

Create an external stage pointing to your S3 bucket.

Create a notification integration for the SQS queue.

Create a Snowpipe that auto-ingests files from the stage when notified via SQS.

## Monitoring & Validation:

Use SYSTEM$PIPE_STATUS to check pipe status.

Query INFORMATION_SCHEMA.COPY_HISTORY to validate data loads.

Run SELECT * FROM orders_Datalz; to verify ingested records.

snowpipe-aws-project/
│
├── snowpipe_aws_setup.sql       # Full Snowflake SQL script
├── iam_policy.json              # IAM policy template for Snowflake
├── trust_policy.json            # Trust policy template for IAM role
└── README.md                    # Project overview and instructions
