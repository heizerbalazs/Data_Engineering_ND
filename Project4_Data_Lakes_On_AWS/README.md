# Sparkify datalake and ETL pipeline presentation
![Project Passed](https://img.shields.io/badge/project-passed-success.svg)

### Description
This data lake is organizing the data collected by Sparkify on songs and user activity. The data about songs and the collected user logs are stored in S3. The **etl.py** scripts contains the spark process which extracts the data from the json files, and loads it into four dimension and one fact table. The extracted data tables were written back to S3 in parquet format.

### Database Schema
**Fact Table:**
- **songplays:**  log data about users song plays
    - *songplay_id:* long
    - *start_time:* timestamp
    - *user_id:* long
    - *level:* string
    - *song_id:* string
    - *artist_id:* string
    - *session_id:* long
    - *location:* string
    - *user_agent:* string
    - *year* long partition column
    - *month* long partition column
    
**Dimension Tables:**
- **users:** app users
    - *user_id:* long
    - *first_name:* string
    - *last_name:* string
    - *gender:* string
    - *level:* string

- **songs:** songs avialable in the app
    - *song_id:* string
    - *title:* string
    - *artist_id:* string
    - *year:* long partition column
    - *duration:* double

- **artists:** artists, hows musice is avialble in the app
    - *artist_id:* string
    - *name:* string
    - *locaton:* string
    - *lattitude:* double
    - *longitude:* double

- **time:**  timestamps of records in **songplays** broken down into specific units
    - *start_time:* timestamp
    - *hour:* long
    - *day:* long
    - *week:* long
    - *month:* long partition column
    - *year:* long partition column
    - *weekday:* long