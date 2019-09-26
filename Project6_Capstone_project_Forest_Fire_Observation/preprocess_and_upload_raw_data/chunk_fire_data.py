import pandas as pd
import os
import logging

get_a_month = lambda x, year, month: f'{year}-{month}-' in x

def get_file_paths(directory):
    files = os.listdir(directory)
    for i, file in enumerate(files):
        files[i] = directory+file
    return files

def get_file_chunk(df,year,months):
    file_chunk = df[df['acq_date'].apply(get_a_month,year=str(year),month=str(month))]
    df = df.drop(df[df['acq_date'].apply(get_a_month,year=str(year),month=str(month))].index)
    return df, file_chunk


if __name__ == "__main__":

    # raw data
    file_paths = get_file_paths('../data/Forestfires/')
    df = pd.DataFrame()
    # folder structure
    folder = 'nasa_fire_data'
    first_year, last_year = 2000, 2019
    years = [i for i in range(first_year, last_year+1)]
    months = [i for i in range(1,13)]
    # set up logging
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt='%H:%M:%S')

    logging.info('application setup done')

    for i, year in enumerate(years):
        logging.info(f'Processing the data from {year}...')
        for month in months:

            # 1 Load new dataframe if it is the tenth month
            # and concat it with the dataframe
            if month == 11:
                df = pd.concat([df, pd.read_json(file_paths[i])])
                logging.info(f'The {i}th file {file_paths[i]} readed...')
                logging.info(f'The df now has {df.shape[0]} rows...')

            if not df.empty:

                # 1 Create a new folder if not exists
                if month < 10:
                    month = f'0{month}'
                
                path = f'../data/'+folder+f'/{year}/{month}'
                if not os.path.exists(path):
                    os.makedirs(path)
                    logging.info(f'{path} folder created...')
                    
                # 3 Get the proper chunk of the dataframe
                df, file_chunk = get_file_chunk(df,year,months)
                logging.info(f'{year} {month} chunk of data is returned with {file_chunk.shape[0]} records...')
                logging.info(f'The df now has {df.shape[0]} rows...')

                #  4 Save the chunk of the dataframe
                file_chunk.to_json(path+f'/fires{year}{month}.json', orient='records')
                logging.info(f'{year} {month} chunk of data is written to {path}...')
