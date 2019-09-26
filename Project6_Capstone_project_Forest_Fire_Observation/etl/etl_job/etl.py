from functools import partial
import logging
from world_data_schema import ColumnDefinitions
import reverse_geocode

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, TimestampType
from pyspark.sql.functions import udf, col, to_timestamp, monotonically_increasing_id, expr
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, dayofweek, date_format, from_unixtime

def setup_logging(default_level=logging.WARNING):
    """
    Setup logging configuration
    """
    logging.basicConfig(level=default_level)
    return logging.getLogger('DeployPySparkScriptOnAws')

# Heleper function
def flatten_table(column_names, column_values):
    row = iter(zip(column_names, column_values))
    _, column_name = next(row)  # Special casing retrieving the first column
    _, country_name = next(row)
    _, country_code = next(row)
    return [
        Row(ColumnName=column_name, CountryName=country_name, CountryCode=country_code, Year=column, ColumnValue=value)
        for column, value in row
    ]

def coords_to_country(lat,lon):
    try:
        return reverse_geocode.search([(lat,lon)])[0]['country']
    except IndexError as e:
        logging.warning(e)
        return 'unknown'

def create_spark_session():
    spark = SparkSession \
        .builder \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:2.8.5') \
        .getOrCreate()
    return spark

def process_world_bank_data(spark, input_data, output_data):
    
    df = spark.read.csv(path=input_data, header=True)

    # Drop unnecessary columns and list the remainings
    df = df.drop('Series Code')
    column_names = df.columns
    # Flatten the data frame
    df = df.rdd.flatMap(partial(flatten_table, column_names)).toDF()
    # Formatting Year column
    df = df.withColumn('Year',expr("substring(Year, 0, 4)"))
    # Drop row where CountryName is null
    df = df.na.drop(subset=['CountryName'])
    # Set proper dataTypes
    df = df.select(col('ColumnName'),
                    col('ColumnValue').cast(DoubleType()),
                    col('CountryName'),
                    col('CountryCode'),
                    col('Year').cast(LongType()))

    df = df.groupby(['Year','CountryName', 'CountryCode']).pivot('ColumnName').max('ColumnValue')

    countries_table = df.select(col('CountryName').alias('country'),
                                       col('CountryCode').alias('countryCode')) \
                                    .distinct() \
                                    .sort(col('Country')) \
                                    .withColumn('id',monotonically_increasing_id())
    
    countries_table.write.format('parquet') \
                    .save(output_data+'/countries/countries.parquet')
    logging.info('/countries/countries.parquet is written to S3')

    condition = [
        df['CountryCode'] == countries_table['countryCode'],
        df['CountryName'] == countries_table['country']
        ]

    df = df.join(countries_table, condition, 'left').withColumnRenamed('id','country_id')


    for oldColumns, newColumns, destinationFolder in ColumnDefinitions:
        output_table = df.select(col('country_id').alias('countryId'),
                                col('Year').alias('year'),
                                 *[col(oldColumnName).alias(newColumnName) \
                                 for oldColumnName, newColumnName in zip(oldColumns,newColumns)])
        output_table.write.format('parquet') \
                            .save(output_data+destinationFolder)
        logging.info(f'{destinationFolder} is written to S3')


def process_nasa_fire_data(spark, input_data, output_data):

    coords_to_country_udf = udf(coords_to_country,StringType())

    df = spark.read.json(path=input_data)
    logging.info("Converting geolocation to country...")
    df = df.withColumn('df_country',coords_to_country_udf(df.latitude, df.longitude))
    df = df.select('*',dayofmonth(col('acq_date')).alias('day'),
                    weekofyear(col('acq_date')).alias('week'),
                    month(col('acq_date')).alias('month'),
                    year(col('acq_date')).alias('year'))

    countries_table = spark.read.parquet("s3n://balazs-heizer-udacity-dend-capstone-project/db/countries/countries.parquet")

    condition = [
        df['df_country'] == countries_table['country']
    ]

    df = df.join(countries_table, condition, 'left').withColumnRenamed('id','country_id')

    # Keep only the rows where the country is known
    df = df.where(col('df_country') != 'unknown')
    df = df.drop('acq_date', 'acq_time','df_country', 'country', 'countryCode')
    
    df.write.partitionBy('country_id','month') \
                         .format('parquet') \
                         .save(output_data)
    
    logging.info(f'results are written to S3 {output_data}')

logger = setup_logging(default_level=logging.INFO)

if __name__ == "__main__":

    spark = create_spark_session()
    output_data = "s3n://balazs-heizer-udacity-dend-capstone-project/db"

    # process world bank data
    input_data = "s3n://balazs-heizer-udacity-dend-capstone-project/world_data/world_bank_data_2000_2019.csv"
    process_world_bank_data(spark, input_data, output_data)

    # process fire data
    years = [i for i in range(2000,2020)]

    for i in years:
        input_data = "s3n://balazs-heizer-udacity-dend-capstone-project/nasa_fire_data/{}/*/*.json".format(i)
        output_data = "s3n://balazs-heizer-udacity-dend-capstone-project/db/fires/{}/fire_{}.parquet".format(i,i)
        process_nasa_fire_data(spark, input_data, output_data)


    spark.stop()
