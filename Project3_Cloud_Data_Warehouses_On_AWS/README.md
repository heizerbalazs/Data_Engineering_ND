# Sparkify database and ETL pipeline presentation (Redshift)
[![Project Passed](https://img.shields.io/badge/project-passed-success.svg)](https://img.shields.io/badge/project-passed-success.svg)

### Description

This database is organizing the data collected by Sparkify on songs and user activity. The data about songs and the collected user logs are stored in **S3** and loaded into **Redshift** (for more information about the infrastructure check the [AWS ifrastructure](#aws-infrastructure) section). The aim of the database is to make easy queries for the data, therefore star schema was choosen (for more detail about the tables see the [Database Schema](#database-schema) section). The dataset from **S3** was first loaded into two staging table then inserted into the [Fact](#fact-table) and [Dimension](#dimension-tables) tables. The data in **S3** is consumed by the **etl.py** script (for more information on the script see the [ETL process](#etl-process) section).

### Database Schema

**Fact Table:**
- **songplays:**  log data about users song plays
    - *songplay_id:* INT IDENTITY(1,1)
    - *start_time:* TIMESTAMP sortkey
    - *user_id:* INT
    - *level:* VARCHAR
    - *song_id:* VARCHAR distkey
    - *artist_id:* VARCHAR
    - *session_id:* INT
    - *location:* VARCHAR
    - *user_agent:* VARCHAR
    
**Dimension Tables:**
- **users:** app users
    - *user_id:* INT sortkey
    - *first_name:* VARCHAR
    - *last_name:* VARCHAR
    - *gender:* VARCHAR
    - *level:* VARCHAR

- **songs:** songs avialable in the app
    - *song_id:* VARCHAR sortkey distkey
    - *title:* VARCHAR
    - *artist_id:* VARCHAR
    - *year:* INT
    - *duration:* FLOAT8

- **artists:** artists, whose music is avialble in the app
    - *artist_id:* VARCHAR sortkey
    - *name:* VARCHAR
    - *locaton:* VARCHAR
    - *lattitude:* FLOAT8
    - *longitude:* FLOAT8

- **time:**  timestamps of records in **songplays** broken down into specific units
    - *start_time:* TIMESTAMP sortkey
    - *hour:* INT
    - *day:* INT
    - *week:* INT
    - *month:* INT
    - *year:* INT
    - *weekday:* INT

### ETL process

The ETL process is implemented in three python files:
1. **cql_queries.py:** This file contains the queries creating and dropping the tables.
2. **create_tables.py:** This script executes the DROP TBALE and CREATE TABLE queries.
3. **etl.py:** This script reads the files in the *./event_data* folder and write it into a *event_datafile_new.csv*. Then insert the data from this newly created file to the tables created by the *create_tables.py* script.

### AWS infrastructure

**Runbook.ipynb** - configure, create and delete aws resources like *iam role*, *redshift cluster*, *s3*

### Test

Analytics queries, intend to test the database, can be find in **QueryBook.ipynb** note book.
    