import pandas as pd
from cassandra.cluster import Cluster
import re
import os
import glob
import numpy as np
import json
import csv
from cql_queries import *

def process_app_history_files():
    """
    This function reads all csv files from the event_data folder,
    and writes the following columns into event_datafile_new.csv file.
    
    Inputs:
    -------
    This function does not have any input.
    
    Output:
    -------
    This function does not return anything.
    """
    
    # Get your current folder and subfolder event data
    filepath = os.getcwd() + '/event_data'

    # Create a for loop to create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):
    
        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root,'*'))
        
    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = [] 
    
    # for every filepath in the file path list 
    for f in file_path_list:

    # reading csv file 
        with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)
        
             # extracting each data row one by one and append it        
            for line in csvreader:
                #print(line)
                full_data_rows_list.append(line) 

    # creating a smaller event data csv file called event_datafile_full csv that will be used to   insert data into the \
    # Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                            'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))

def load_data(session, filepath):
    """
    This function reads a file and load it into the Apache Cassandra tables.
    
    Inputs:
    -------
    session - object represents connection to an Apache Cassandra cluster
    filepath - access point of the csv file loaded into Apache Cassandra tables
    
    Output:
    -------
    This function does not return anything.
    """
    
    with open(filepath, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            # load session data
            session.execute(session_table_insert, (line[0], line[9], float(line[5]), int(line[8]), int(line[3])))
            # load session playlist data
            session.execute(session_playlist_table_insert, (line[0], line[9], line[1], line[4], int(line[10]), int(line[8]), int(line[3])))
            # load song data
            session.execute(song_table_insert, (line[1], line[4], line[9], int(line[10])))

def main():
    print("Connect...\n")
    cluster = Cluster()
    session = cluster.connect()
    session.set_keyspace("sparkifydb")
    
    print("Extract...\n\nTransform...\n")
    process_app_history_files()
    
    print("Load...\n")
    load_data(session, filepath="./event_datafile_new.csv")
    
    print("Disconnect...")
    session.shutdown()
    cluster.shutdown()
    
if __name__ == "__main__":
    main()