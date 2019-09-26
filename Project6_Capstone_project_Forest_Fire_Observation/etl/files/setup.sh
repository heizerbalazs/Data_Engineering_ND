#!/bin/bash

# Non-standard and non-Amazon Machine Image Python modules:
sudo pip-3.6 install -U reverse-geocode
# sudo sed -i -e '$a\export PYSPARK_PYTHON=/usr/bin/python3' /etc/spark/conf/spark-env.sh

# Parse arguments
s3_bucket="$1"
s3_bucket_script="$s3_bucket/script.tar.gz"

# Download compressed script tar file from S3
aws s3 cp $s3_bucket_script /home/hadoop/script.tar.gz

# Untar file
tar zxvf "/home/hadoop/script.tar.gz" -C /home/hadoop/