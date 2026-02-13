/*
=====================================================
AWS Snowpipe Auto-Ingest Project
Architecture:
S3 → SNS → SQS → Snowflake Notification Integration → Snowpipe → Table

Before running:
1. Replace <ACCOUNT_ID>
2. Replace <SNOWPIPE_ROLE>
3. Replace <YOUR_BUCKET_NAME>
4. Replace <FOLDER_PATH>
5. Replace <REGION>
6. Replace <SQS_QUEUE_NAME>
7. Add External ID from DESC INTEGRATION into IAM Trust Policy
=====================================================
*/

-- =========================================
-- 🔹 USE ROLE
-- =========================================
USE ROLE ACCOUNTADMIN;

-- =========================================
-- 🔹 CREATE DATABASE
-- =========================================
CREATE OR REPLACE DATABASE snowpipe_dev_aws;
USE DATABASE snowpipe_dev_aws;

-- =========================================
-- 🔹 CREATE TABLE
-- =========================================
CREATE OR REPLACE TABLE orders_Datalz (
    order_id INT,
    product VARCHAR(20),
    quantity INT,
    order_status VARCHAR(30),
    order_date DATE
);

-- =========================================
-- 🔹 CREATE FILE FORMAT
-- =========================================
CREATE OR REPLACE FILE FORMAT csv_format
TYPE = CSV
FIELD_DELIMITER = ','
SKIP_HEADER = 1
EMPTY_FIELD_AS_NULL = TRUE;

-- =========================================
-- 🔹 CREATE STORAGE INTEGRATION (S3)
-- =========================================
CREATE OR REPLACE STORAGE INTEGRATION s3_integration
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 's3'
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<ACCOUNT_ID>:role/<SNOWPIPE_ROLE>'
STORAGE_ALLOWED_LOCATIONS = ('s3://<YOUR_BUCKET_NAME>/<FOLDER_PATH>/');

-- Get External ID for IAM Trust Policy
DESC INTEGRATION s3_integration;

-- =========================================
-- 🔹 CREATE STAGE
-- =========================================
CREATE OR REPLACE STAGE s3_stage
URL = 's3://<YOUR_BUCKET_NAME>/<FOLDER_PATH>/'
STORAGE_INTEGRATION = s3_integration
FILE_FORMAT = csv_format;

-- Check files in stage
LIST @s3_stage;

-- =========================================
-- 🔹 CREATE NOTIFICATION INTEGRATION (SQS)
-- =========================================
CREATE OR REPLACE NOTIFICATION INTEGRATION aws_sqs_notification_int
TYPE = QUEUE
ENABLED = TRUE
AWS_SQS_QUEUE_ARN = 'arn:aws:sqs:<REGION>:<ACCOUNT_ID>:<SQS_QUEUE_NAME>'
AWS_IAM_ROLE_ARN = 'arn:aws:iam::<ACCOUNT_ID>:role/<SNOWPIPE_ROLE>';

-- Get External ID for IAM Trust Policy
DESC INTEGRATION aws_sqs_notification_int;

-- =========================================
-- 🔹 CREATE SNOWPIPE
-- =========================================
CREATE OR REPLACE PIPE s3_to_snowflake_pipe
AUTO_INGEST = TRUE
INTEGRATION = aws_sqs_notification_int
AS
COPY INTO orders_Datalz
FROM @s3_stage
FILE_FORMAT = (FORMAT_NAME = csv_format);

-- =========================================
-- 🔹 CHECK PIPE STATUS
-- =========================================
SELECT SYSTEM$PIPE_STATUS('s3_to_snowflake_pipe');

-- =========================================
-- 🔹 MANUAL REFRESH (Optional)
-- =========================================
ALTER PIPE s3_to_snowflake_pipe REFRESH;

-- =========================================
-- 🔹 VERIFY DATA
-- =========================================
SELECT * FROM orders_Datalz;

-- =========================================
-- 🔹 CHECK LOAD HISTORY
-- =========================================
SELECT *
FROM TABLE(
  INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'ORDERS_DATALZ',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
  )
);
