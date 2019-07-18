# Sparkify database and ETL pipeline presentation

This database is organizing the data collected by Sparkify on songs and user activity. The data about songs and the collected user logs are stored in **S3** on aws. The aim of the database is to make easy queries for the data, therefore star schema was choosen (for more detail about the tables see the **Database Schema** subsection). The dataset from **S3** was first loaded into two staging table then inserted into the **Fact** and **Dimension** tables.

The resources on aws are created and deleted in the **Runbook.ipynb** notebook.
After the resources are avialable **create_tables.py** creates the tables on **Redshift**, then **etl.py** loads the data into the tables.
Analytics queries, intend to test the database, can be fing in **QueryBook.ipynb** note book.

## Database Schema
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

- **artists:** artists, hows musice is avialble in the app
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
    