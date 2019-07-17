# DROP TABLES

session_table_drop = "DROP TABLE IF EXISTS session_table"
session_playlist_table_drop = "DROP TABLE IF EXISTS session_playlist_table_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"


# CREATE TABLES

session_table_create = ("CREATE TABLE IF NOT EXISTS session_table (artist text, \
                                                                song_title text, \
                                                                song_length float, \
                                                                session_id int, \
                                                                item_in_session int, \
                                                                PRIMARY KEY (session_id, item_in_session))")

session_playlist_table_create = ("CREATE TABLE IF NOT EXISTS session_playlist_table (artist_name text, \
                                                                                     song_title text, \
                                                                                     user_first_name text, \
                                                                                     user_last_name text, \
                                                                                     user_id int, \
                                                                                     session_id int, \
                                                                                     item_in_session int, \
                                                                                     PRIMARY KEY ((user_id, session_id), item_in_session)\
                                                                                     ) WITH CLUSTERING ORDER BY (item_in_session ASC)")

song_table_create = ("CREATE TABLE  IF NOT EXISTS song_table (user_first_name text, \
                                                             user_last_name text, \
                                                             song_title text, \
                                                             user_id int, \
                                                             PRIMARY KEY (song_title, user_id))")


# INSERT RECORDS

session_table_insert = ("INSERT INTO session_table (artist, song_title, song_length, session_id, item_in_session) \
                         VALUES (%s, %s, %s, %s, %s)")

session_playlist_table_insert = ("INSERT INTO session_playlist_table (artist_name, song_title, user_first_name, user_last_name, user_id, session_id, item_in_session) \
                                  VALUES (%s, %s, %s, %s, %s, %s, %s)")

song_table_insert = ("INSERT INTO song_table (user_first_name, user_last_name, song_title, user_id) \
                      VALUES (%s, %s, %s, %s)")


# QUERY LISTS

create_table_queries = [session_table_create, session_playlist_table_create, song_table_create]
drop_table_queries = [session_table_drop, session_playlist_table_drop, song_table_drop]