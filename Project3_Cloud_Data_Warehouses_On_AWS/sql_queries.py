import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

DWH_IAM_ROLE=config.get('CLUSTER','DWH_IAM_ROLE')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events_table (artist VARCHAR,
                                                     auth VARCHAR,
                                                     firstName VARCHAR,
                                                     gender VARCHAR,
                                                     iteminSession INT,
                                                     lastName VARCHAR,
                                                     length REAL,
                                                     level VARCHAR,
                                                     location VARCHAR,
                                                     method VARCHAR,
                                                     page VARCHAR,
                                                     registration BIGINT,
                                                     sessionId INT,
                                                     song VARCHAR distkey,
                                                     status INT,
                                                     ts TIMESTAMP,
                                                     userAgent VARCHAR,
                                                     userId INT)
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs_table (num_songs INT,
                                                    artist_id VARCHAR,
                                                    artist_latitude VARCHAR,
                                                    artist_longitude VARCHAR,
                                                    artist_location VARCHAR,
                                                    artist_name VARCHAR,
                                                    song_id VARCHAR,
                                                    title VARCHAR distkey,
                                                    duration REAL,
                                                    year INT)
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay_table (songplay_id INT IDENTITY(1, 1),
                                               start_time TIMESTAMP NOT NULL sortkey,
                                               user_id INT NOT NULL,
                                               level VARCHAR,
                                               song_id VARCHAR distkey,
                                               artist_id VARCHAR,
                                               session_id INT,
                                               location VARCHAR,
                                               user_agent VARCHAR)
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS user_table (user_id INT NOT NULL sortkey,
                                           first_name VARCHAR,
                                           last_name VARCHAR,
                                           gender VARCHAR,
                                           level VARCHAR);
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_table (song_id VARCHAR sortkey distkey,
                                           title VARCHAR,
                                           artist_id VARCHAR,
                                           year INT,
                                           duration REAL);
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist_table (artist_id VARCHAR sortkey,
                                             name VARCHAR,
                                             location VARCHAR,
                                             latitude VARCHAR,
                                             longitude VARCHAR)
    DISTSTYLE ALL;
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time_table (start_time TIMESTAMP sortkey,
                                           hour INT,
                                           day INT,
                                           week INT,
                                           month INT,
                                           year INT,
                                           weekday INT);
""")

# STAGING TABLES

staging_events_copy = """
    COPY staging_events_table
    FROM {}
    CREDENTIALS 'aws_iam_role={}'
    FORMAT AS JSON {}
    TIMEFORMAT AS 'epochmillisecs'
    REGION 'us-west-2';
""".format(config['S3']['LOG_DATA'],DWH_IAM_ROLE,config['S3']['LOG_JSONPATH'])

staging_songs_copy = """
    COPY staging_songs_table 
    FROM {}
    CREDENTIALS 'aws_iam_role={}'
    FORMAT AS JSON 'auto'
    REGION 'us-west-2';
""".format(config['S3']['SONG_DATA'],DWH_IAM_ROLE)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay_table (start_time, user_id, level, song_id,
                                artist_id, session_id, location, user_agent)
    SELECT ts, userId, level, song_id, artist_id, sessionId, location, userAgent
    FROM staging_events_table
    JOIN staging_songs_table ON (staging_events_table.artist = staging_songs_table.artist_name);
""")

user_table_insert = ("""
    INSERT INTO user_table (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT userId, firstName, lastName, gender, level
    FROM staging_events_table
    WHERE userId IS NOT NULL;
""")

song_table_insert = ("""
    INSERT INTO song_table (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id, title, artist_id, year, duration
    FROM staging_songs_table;
""")

artist_table_insert = ("""
    INSERT INTO artist_table (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs_table;
""")

time_table_insert = ("""
    INSERT INTO time_table (start_time, hour, day, week, month, year, weekday)
    SELECT ts, date_part(h, ts), date_part(d, ts), date_part(w, ts),
           date_part(mon, ts), date_part(y, ts), date_part(dow, ts)   
    FROM staging_events_table
    WHERE song IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]