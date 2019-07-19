import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, TimestampType
from pyspark.sql.functions import udf, col, monotonically_increasing_id, from_unixtime
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, dayofweek, date_format

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:2.7.0') \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data + 'song-data/A/A/*/*.json'

    # define schema for input_data
    song_schema = StructType([
        StructField('song_id', StringType(), True),
        StructField('title', StringType(), True),
        StructField('year', LongType(), True),
        StructField('duration', DoubleType(), True),
        StructField('artist_id', StringType(), True),
        StructField('artist_name', StringType(), True),
        StructField('artist_location', StringType(), True),
        StructField('artist_latitude', DoubleType(), True),
        StructField('artist_longitude', DoubleType(), True),
    ])
    
    # read song data file
    df = spark.read.json(path=song_data, schema=song_schema)

    # extract columns to create songs table
    songs_table = df.select(col('song_id'),
                      col('title'),
                      col('artist_id'),
                      col('year'),
                      col('duration'))
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year','artist_id') \
                         .format('parquet') \
                         .save(output_data+'songs/songs.parquet')

    # extract columns to create artists table
    artists_table = df.select(col('artist_id'),
                        col('artist_name').alias('name'),
                        col('artist_location').alias('loaction'),
                        col('artist_latitude').alias('latitude'),
                        col('artist_longitude').alias('longitude')) \
                        .dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.format('parquet') \
                       .save(output_data+'artists/artists.parquet')


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = input_data + 'log_data'

    # define schema for input_data
    log_schema = StructType([
        StructField('artist', StringType(), True),
        StructField('auth', StringType(), True),
        StructField('firstName', StringType(), True),
        StructField('gender', StringType(), True),
        StructField('itemInSession', LongType(), True),
        StructField('lastName', StringType(), True),
        StructField('length', DoubleType(), True),
        StructField('level', StringType(), True),
        StructField('location', StringType(), True),
        StructField('method', StringType(), True),
        StructField('page', StringType(), True),
        StructField('registration', DoubleType(), True),
        StructField('sessionId', LongType(), True),
        StructField('song', StringType(), True),
        StructField('status', LongType(), True),
        StructField('ts', LongType(), True),
        StructField('userAgent', StringType(), True),
        StructField('userId', StringType(), True)
    ])

    # read log data file
    df = spark.read.json(path=log_data, schema=log_schema)
    
    # filter by actions for song plays
    df = df.filter(col('page') == 'NextSong')

    # extract columns for users table    
    users_table = df.select(col('userId').cast(LongType()).alias('user_id'),
                     col('firstName').alias('first_name'),
                     col('lastName').alias('last_name'),
                     col('gender'),
                     col('level')) \
             .dropna() \
             .dropDuplicates()

    # find users who has poth free and paid account and keep only the paied
    upgradedUser = users_table.groupBy('user_id') \
                        .count() \
                        .filter(col('count')==2) \
                        .select('user_id').rdd.flatMap(lambda x: x).collect()

    users_table = users_table.filter(
        (col('user_id').isin(upgradedUser) & col('level') == 'paid')
        | ~col('user_id').isin(upgradedUser))

    # write users table to parquet files
    users_table.write.format('parquet') \
                     .save(output_data+'users/users.parquet')
    
    # extract columns to create time table
    time_table = df.withColumn('date',from_unixtime(col('ts')/1000, 'yyyy-MM-dd HH:mm:ss')) \
                    .select(col('date').alias('start_time'),
                            hour(col('date')).alias('hour'),
                            dayofmonth(col('date')).alias('day'),
                            weekofyear(col('date')).alias('week'),
                            month(col('date')).alias('month'),
                            year(col('date')).alias('year'),
                            dayofweek(col('date')).alias('weekday')
                            )\
                    .dropDuplicates()
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year','month') \
                         .format('parquet') \
                         .save(output_data+'time/time.parquet')

    # get filepath to song data file
    song_data = input_data + 'song-data/A/A/*/*.json'

    # define schema for input_data
    song_schema = StructType([
        StructField('song_id', StringType(), True),
        StructField('title', StringType(), True),
        StructField('year', LongType(), True),
        StructField('duration', DoubleType(), True),
        StructField('artist_id', StringType(), True),
        StructField('artist_name', StringType(), True),
        StructField('artist_location', StringType(), True),
        StructField('artist_latitude', DoubleType(), True),
        StructField('artist_longitude', DoubleType(), True),
    ])

    # read in song data to use for songplays table
    song_df = spark.read.json(path=song_data, schema=song_schema)

    # extract columns from joined song and log datasets to create songplays table 
    cond = [
        df.song == song_df.title,
        df.artist == song_df.artist_name,
        df.length == song_df.duration
    ]

    songplays_table = df.join(song_df, cond, 'left_outer') \
                        .withColumn('songplay_id', monotonically_increasing_id()) \
                        .select(col('songplay_id'),
                                from_unixtime(col('ts')/1000, 'yyyy-MM-dd HH:mm:ss').alias('start_time'),
                                col('userId').alias('user_id'),
                                col('level'),
                                col('song_id'),
                                col('artist_id'),
                                col('sessionId').alias('session_id'),
                                col('location'),
                                col('userAgent').alias('user_agent'),
                                year(col('start_time')).alias('year'),
                                month(col('start_time')).alias('month'))

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy('year','month') \
                         .format('parquet') \
                         .save(output_data+'songpalys/songplays.parquet')


def main():
    spark = create_spark_session()
    input_data = 's3a://udacity-dend/'
    output_data = 's3a://dend-dl/'
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == '__main__':
    main()