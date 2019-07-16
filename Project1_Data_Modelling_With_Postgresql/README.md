# Sparkify database and ETL process presentation
[![Project Passed](https://img.shields.io/badge/project-passed-success.svg)](https://img.shields.io/badge/project-passed-success.svg)

### Description
This database is organizing the data collected by Sparkify on songs and user activity. The data about songs and the collected user logs are stored in several directories in JSON format. The aim of the database is to make easy queries for the databse, therefore star schema was choosen (for more detail about the tables see the [Database Schema](#databsa-schema) subsection). The original JSON data is consumed by the **etl.py** script (for more information on the script see the [ETL process](#etl-process)subsection). [Dimension tables](#dimension-tables:) were created first, then the [Fact table](#fact-table).

### Database Schema
**Fact Table:**
- **songplays:**  log data about users song plays
    - *songplay_id:* SERIAL PRIMARY KEY
    - *start_time:* TIMESTAMP
    - *user_id:* INT
    - *level:* VARCHAR
    - *song_id:* VARCHAR
    - *artist_id:* VARCHAR
    - *session_id:* INT
    - *location:* VARCHAR
    - *user_agent:* VARCHAR
    
**Dimension Tables:**
- **users:** app users
    - *user_id:* INT PRIMARY KEY
    - *first_name:* VARCHAR
    - *last_name:* VARCHAR
    - *gender:* VARCHAR
    - *level:* VARCHAR

- **songs:** songs avialable in the app
    - *song_id:* VARCHAR PRIMARY KEY
    - *title:* VARCHAR
    - *artist_id:* VARCHAR
    - *year:* INT
    - *duration:* FLOAT8

- **artists:** artists, hows musice is avialble in the app
    - *artist_id:* VARCHAR PRIMARY KEY
    - *name:* VARCHAR
    - *locaton:* VARCHAR
    - *lattitude:* FLOAT8
    - *longitude:* FLOAT8

- **time:**  timestamps of records in **songplays** broken down into specific units
    - *start_time:* TIMESTAMP PRIMARY KEY
    - *hour:* INT
    - *day:* INT
    - *week:* INT
    - *month:* INT
    - *year:* INT
    - *weekday:* INT
    
### ETL process

To consume the different data sources (log files and songs metadata) two functions were implemented:
- **process_log_file:**
    - *inputs:* psycopg2 cursor, filepath
    - *action:* read and transform json files than run SQL INSRET command
- **process_song_file:**
    - *inputs:* psycopg2 cursor, filepath
    - *action:* read and transform json files than run SQL INSRET command