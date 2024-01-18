import argparse
import os
from time import time
import pandas as pd
from sqlalchemy import create_engine


# Helper function to fetch and process CSV
def fetch_csv(csv_name, url):
    os.system(f"wget {url} -O {csv_name}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip', low_memory=False)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    return df, df_iter


# Function to initialize db
def initialize_db(user, password, host, port, db):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    return engine


def main(params):
    csv_name = 'output.csv.gz' if params.url.endswith('.csv.gz') else 'output.csv'
    engine = initialize_db(params.user, params.password, params.host, params.port, params.db)

    df, df_iter = fetch_csv(csv_name, params.url)
    df.head(n=0).to_sql(name=params.table_name, con=engine, if_exists='replace')
    df.to_sql(name=params.table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=params.table_name, con=engine, if_exists='append')
            t_end = time()
            print(f'Inserted another chunk, took {t_end - t_start:.3f} seconds')
        except StopIteration:
            print("Finished ingesting data into the PostgreSQL database")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', required=True, help='User name for Postgres')
    parser.add_argument('--password', required=True, help='Password for Postgres')
    parser.add_argument('--host', required=True, help='Host for Postgres')
    parser.add_argument('--port', required=True, help='Port for Postgres')
    parser.add_argument('--db', required=True, help='Database name for Postgres')
    parser.add_argument('--table_name', required=True, help='Name of table where we will write results to')
    parser.add_argument('--url', required=True, help='URL of the csv file')
    args = parser.parse_args()
    main(args)
