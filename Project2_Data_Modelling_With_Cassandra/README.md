# Sparkify database and ETL pipeline presentation (Cassandra)
[![Project Passed](https://img.shields.io/badge/project-passed-success.svg)](https://img.shields.io/badge/project-passed-success.svg)

### Description
This database is organizing the data collected by Sparkify on songs and user activity. The collected event logs are stored in the *./event_data folder* as csv files. The aim of the database is to answer the following 3 quiestion:
1. List the songs and related information (e.g.: artist, length of the song, ...) listend in a given session.[*](#session_table:)
2. List the  songs, song related informaton and the user who listend it in a given session.[*](#session_playlist_table:)
3. List the users whose listend a specific song.[*](song_table:)
Using the *query first* data modeling approach, three table were created (for more information please check the [Data Tables](#data-tables) section). The original csv data is consumed by the **etl.py** script (for more information on the script see the [ETL process](#etl-process) section).

### Data Tables:
1. **session_table:**

    **Columns:**
    - *artist:* text
    - *song_title:* text
    - *song_length:* float
    - *session_id:* int
    - *item_in_session:* int
    - *PRIMARY KEY (session_id, item_in_session)*
    
    **Corresponding test query:**
    SELECT * FROM session_table WHERE session_id = 338 and item_in_session = 4
      
2. **session_playlist_table:** 

     **Columns:**
     - *artist_name:* text
     - *song_title:* text
     - *user_first_name:* text
     - *user_last_name:* text
     - *user_id:* int
     - *session_id:* int
     - *item_in_session:* int, ascendingly orderd by this column
     - *PRIMARY KEY ((user_id, session_id), item_in_session)*
                                                  
    **Corresponding test query:**
    SELECT * FROM session_playlist_table WHERE user_id = 10 AND session_id = 182

3. **song_table:**

     **Columns:**
     - *user_first_name:* text
     - *user_last_name:* text
     - *song_title:* text
     - *user_id:* int
     - *PRIMARY KEY (song_title, user_id)*
    
    **Corresponding test query:**
    SELECT * FROM song_table WHERE song_title = 'All Hands Against His Own'

    
### ETL process

The ETL process is implemented in three python files:
1. **cql_queries.py:** This file contains the queries creating and dropping the tables.
2. **create_tables.py:** This script executes the DROP TBALE and CREATE TABLE queries.
3. **etl.py:** This script reads the files in the *./event_data* folder and write it into a *event_datafile_new.csv*. Then insert the data from this newly created file to the tables created by the *create_tables.py* script.

### Testing
In the **Query_test.ipynb** the *test queries* are executed for each table.