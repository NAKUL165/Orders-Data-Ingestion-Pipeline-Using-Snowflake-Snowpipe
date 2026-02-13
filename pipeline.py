-- =========================================
-- 🔹 USE ACCOUNTADMIN ROLE
-- =========================================
USE ROLE ACCOUNTADMIN;

-- =========================================
-- 🔹 CREATE DATABASE
-- =========================================
CREATE OR REPLACE DATABASE snowpipe_dev_aws;
USE DATABASE snowpipe_dev_aws;

-- =========================================
-- 🔹 CREATE TARGET TABLE
-- =========================================
CREATE OR REPLACE TABLE seller_data (
    seller_id TEXT,
    seller_zip_code_prefix INTEGER,
    seller_city TEXT,
    seller_state TEXT
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

-- Run this to get EXTERNAL ID
DESC INTEGRATION s3_integration;

-- =========================================
-- 🔹 CREATE EXTERNAL STAGE
-- =========================================
CREATE OR REPLACE STAGE s3_stage
URL = 's3://<YOUR_BUCKET_NAME>/<FOLDER_PATH>/'
STORAGE_INTEGRATION = s3_integration
FILE_FORMAT = csv_format;

-- Verify files
LIST @s3_stage;

-- =========================================
-- 🔹 CREATE NOTIFICATION INTEGRATION (SQS)
-- =========================================
CREATE OR REPLACE NOTIFICATION INTEGRATION aws_sqs_notification_int
TYPE = QUEUE
ENABLED = TRUE
AWS_SQS_QUEUE_ARN = 'arn:aws:sqs:<REGION>:<ACCOUNT_ID>:<SQS_QUEUE_NAME>'
AWS_IAM_ROLE_ARN = 'arn:aws:iam::<ACCOUNT_ID>:role/<SNOWPIPE_ROLE>';

-- Run this to get EXTERNAL ID
DESC INTEGRATION aws_sqs_notification_int;

-- =========================================
-- 🔹 CREATE SNOWPIPE
-- =========================================
CREATE OR REPLACE PIPE s3_to_snowflake_pipe
AUTO_INGEST = TRUE
INTEGRATION = aws_sqs_notification_int
AS
COPY INTO seller_data
FROM @s3_stage;

-- =========================================
-- 🔹 CHECK PIPE STATUS
-- =========================================
SELECT SYSTEM$PIPE_STATUS('s3_to_snowflake_pipe');

-- =========================================
-- 🔹 MANUAL REFRESH (Optional)
-- =========================================
ALTER PIPE s3_to_snowflake_pipe REFRESH;

-- =========================================
-- 🔹 CHECK DATA
-- =========================================
SELECT * FROM seller_data;

-- =========================================
-- 🔹 LOAD HISTORY
-- =========================================
SELECT *
FROM TABLE(
  INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'SELLER_DATA',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
  )
);
