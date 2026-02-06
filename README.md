# Orders-Data-Ingestion-Pipeline-Using-Snowflake-Snowpipe

## Tech Stack: Snowflake, Snowpipe, Google Cloud Storage (GCS), Google Pub/Sub, SQL

# Project Overview

This project demonstrates a cloud-based, event-driven ETL pipeline using Snowflake Snowpipe to automate the ingestion of order data from Google Cloud Storage (GCS) into Snowflake. It ensures real-time data availability, schema validation, and historical tracking, enabling efficient analytics and reporting on order transactions.

The pipeline integrates Pub/Sub notifications to trigger automated ingestion whenever new files arrive, eliminating manual intervention and ensuring data freshness.

# Features

Event-driven ingestion of multi-source order data into Snowflake using Snowpipe.

Automated schema validation and error handling for reliable data processing.

Historical tracking and monitoring of data loads for analytics readiness.

Integration with GCS and Pub/Sub for secure, real-time data ingestion.

SQL-based monitoring to check pipe status, ingestion history, and loaded records.

# Architecture

Source: Raw order data files uploaded to a GCS bucket (gcs://snowpipe-raw-data-gds/).

Notification: GCS bucket triggers a Pub/Sub notification whenever a new file is uploaded.

Snowpipe: Snowflake Snowpipe automatically ingests new files into the orders_data_lz table.

Data Validation & Monitoring: SQL queries track ingestion history, pipe status, and validate schema.
