# Project description
In the last few months Amazon forest fires attracted the atention of the online media. The Amazon rainforest is an important part of Earth's ecosystem, it produces the 20 procent of the oxygen in the atmosphere, it slows doen the global warming. The fires in Amazon mainly caused by human activity. Therefore, I have built a Data Lake on S3, using satelite data published by NASA and World Bank data about several social and economic metrics of countries. The Data Lake can be used to look for economic and social origins of wildfires.

[Amazon rainforest fire: How did the Amazon fire start? How long has it been on fire?](https://www.express.co.uk/news/world/1168299/amazon-rainforest-fire-how-did-amazon-fires-start-cause-deforestation-how-long-fire)

[The Amazon in Brazil is on fire - how bad is it?](https://www.bbc.com/news/world-latin-america-49433767)

### Example query
- Can we find correlation between change in agricultural landarea and number of fires in a given year?

# Data sources
- [NASA Active Fire Data](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data): NASA distributes Near Real-Time (NRT) active fire data within 3 hours of satellite overpass from NASA's Moderate Resolution Imaging Spectroradiometer (MODIS) and NASA's Visible Infrared Imaging Radiometer Suite (VIIRS). In this project I used the MODIS data source.
- [World Bank Open Data](https://data.worldbank.org/): World Bank provide data about economy, society and development indicators of countries. I downloaded this data in csv format, uploaded to S3 and processed with EMR cluster. 7 table were extracted from the raw data. 

# Data lake desing and data pipeline
The picture below depicts the schema of the data lake.
[![DB schema](./FireEvents_db_scheam.png)](https://dbdiagram.io/d/5d6d66e8ced98361d6de20d0)

### Tables
1. __Countries  table:__ Stores country names and codes.
2. __Fire  table:__ Stores data about fires. Partitioned by countryId and month.
3. __SocialIndicators  table:__ Stores indicators like birth rate, death rate, GDP.
4. __LandUsage  table:__ Stores information about land usage in countries.
5. __AgriculturarAndNaturalResources  table:__ Stores information about agricultural import/export and rents.
6. __BiodiversityIndicators  table:__ Stores information about endangerd species and protected land area.
7. __EmissionIndicators  table:__ Stores data about emissions by industry.
8. __EnergyProductionIndicators  table:__ Stores data about energy production.

For more detailed description please check the Data_dictionary.xlsx file. Because not all indicator were available for all countries in all years, I left *null* for missing values. In the Fire and Countries table there is no missing value.

# AWS infrastructure
- Because my raw doat was quiet unstructured (especially the World Bank data) I choosed EMR for ETL.
- The raw and transformed data is stored in S3.
- The AWS infrastructure is set up according to this [tutorial](https://www.themarketingtechnologist.co/upload-your-local-spark-script-to-an-aws-emr-cluster-using-a-simply-python-script/?fbclid=IwAR2fvjMwc4_z_AOmtyfOPma1LB4x4FSB6XhTeMn7LVUou--bMM1GvYmvymE).
- My python code (*run.py*) first creates an EMR cluster, uploads *setup.sh* file which installs the required python modules when the cluster is bootstraping and set the default python version to python 3. Then run the pyspark job, and terminates the cluster, when the job is done or failed.
- The pyspark job can be find in the *etl.py* script. It reads the raw data from S3 and writes it back after the transformation.

# Project extension for different scenarios
- __If the data was increased by 100x__:
In this case we need more storage and memory to process the data. With scaling the EMR cluster we can solve the problem. Computing the storage which we will need is easy (consider data size and repliaction factor). To consider the memory configuration the following [blog post](https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/) can be a good starting point.
- __If the pipelines were run on a daily basis by 7am__:
To automatically update the database with the most recent data, we can use an ETL tool like Apache Airflow and build a DAG.
- __If the database needed to be accessed by 100+ people__:
To make the data accesible for more people, the transformed data can be loaded into a Redshift cluster.