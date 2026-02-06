-- Use role
use role accountadmin;

-- Create database
create or replace database snowpipe_dev;

-- Create table 
create or replace table orders_data_lz(
    order_id int,
    product varchar(20),
    quantity int,
    order_status varchar(30),
    order_date date
);

-- Create a Cloud Storage Integration in Snowflake
-- Integration means creating config based secure access
create or replace storage integration gcs_bucket_read_int
 type = external_stage
 storage_provider = gcs
 enabled = true
 storage_allowed_locations = ('gcs://snowpipe-raw-data-gds/');

-- Retrieve the Cloud Storage Service Account for your snowflake account
desc storage integration gcs_bucket_read_int;


-- Service account info for storage integration for linking

-- A stage in Snowflake refers to a location (internal or external) 
-- where data files are uploaded, stored, and prepared before being loaded into Snowflake tables.
create or replace stage snowpipe_stage
url = 'gcs://snowpipe-raw-data-gds/'
storage_integration = gcs_bucket_read_int;


-- Show stages
show stages;

list @snowpipe_stage;

-- Create PUB-SUB Topic named as gcs-to-pubsub-notification
-- Then run below mentioned command from Google Console Cloud Shell to setup create notification event
-- gsutil notification create -t gcs-to-pubsub-notification -f json gs://snowpipe-raw-data-gds/


-- create notification integration
create or replace notification integration notification_from_pubsub_int
 type = queue
 notification_provider = gcp_pubsub
 enabled = true
 gcp_pubsub_subscription_name = 'projects/dev-sunset-468907-e9/subscriptions/gcs-to-pubsub-notification-sub';

-- Describe integration
desc integration notification_from_pubsub_int;

-- Service account for PUB-SUB which needs to be whitelisted under Google Cloud IAM for linking

-- Create Snow Pipe
Create or replace pipe gcs_to_snowflake_pipe
auto_ingest = true
integration = notification_from_pubsub_int
as
copy into orders_data_lz
from @snowpipe_stage
file_format = (type = 'CSV');

-- Show pipes
show pipes;

-- Check the status of pipe
select system$pipe_status('gcs_to_snowflake_pipe');

select * from orders_data_lz;

-- Stop snowpipe
ALTER PIPE gcs_to_snowflake_pipe SET PIPE_EXECUTION_PAUSED = true;
