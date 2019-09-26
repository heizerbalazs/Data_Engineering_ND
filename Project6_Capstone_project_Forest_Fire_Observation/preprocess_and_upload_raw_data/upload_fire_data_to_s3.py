import boto3
from boto3.s3.transfer import TransferConfig
import pandas as pd
import configparser
import threading
import os
import sys

config = configparser.ConfigParser()
config.read_file(open('s3_upload.cfg'))

KEY = config.get('AWS','KEY')
SECRET = config.get('AWS', 'SECRET')
IAM_ROLE_ARN = config.get('IAM_ROLE','IAM_ROLE_ARN')
BUCKET_NAME =config.get('S3','BUCKET_NAME')
FOLDER = config.get('S3','FOLDER')


session = boto3.session.Session(aws_access_key_id=KEY,
                                aws_secret_access_key=SECRET)
s3 = session.client('s3')
# s3.create_bucket(Bucket=BUCKET_NAME,
#                  CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})

def multi_part_upload_with_s3(file_path,folder,year,month):
    config = TransferConfig(
        # The transfer size threshold for which multi-part uploads, downloads, and copies will automatically be triggered
        multipart_threshold=1024*25,
        # The maximum number of threads that will be making requests to perform a transfer.
        max_concurrency=10,
        # The partition size of each part for a multi-part transfer.
        multipart_chunksize=1024*25,
        # If True, threads will be used when performing S3 transfers. 
        use_threads=True
                            )
    
    key_path = f'{folder}/{year}/{month}/firedata_{year}_{month}.json'
    # file_path = './data/WorldData/world_bank_development_indicators_2000_2019.csv'
    # key_path = f'{FOLDER}/world_bank_data_2000_2019.csv'

    
    s3.upload_file(file_path, BUCKET_NAME, key_path,
                   ExtraArgs={'ContentType': 'text/plain'},
                   Config=config,
                   Callback=ProgressPercentage(file_path))
    
class ProgressPercentage(object):
    
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

if __name__ == "__main__":

    path = '../data/nasa_fire_data'

    for r,d,f in os.walk(path):
        if len(d) == 0:
            for file_name in f:
                file_path = os.path.join(r, file_name)
                year = file_path[22:26]
                month = file_path[27:29]
                multi_part_upload_with_s3(file_path,FOLDER,year,month)