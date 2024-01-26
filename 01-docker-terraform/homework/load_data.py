import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from contextlib import closing


def convert_to_datetime(df):
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    return df


# Helper function to fetch and process CSV
def fetch_csv(csv_name, url):
    if not os.path.exists(csv_name):
        try:
            os.system(f"wget {url} -O {csv_name}")
        except Exception as e:
            print(f"Error fetching CSV: {e}")
            return None, None

    try:
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip', low_memory=False)
        df = next(df_iter)
        df = convert_to_datetime(df)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None, None

    return df, df_iter


# Function to initialize db
def initialize_db(user, password, host, port, db):
    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    except Exception as e:
        print(f"Error initializing database: {e}")
        return None

    return engine


def main(params):
    csv_name = 'output.csv.gz' if params.url.endswith('.csv.gz') else 'output.csv'
    engine = initialize_db(params.user, params.password, params.host, params.port, params.db)

    if engine is None:
        print("Error initializing database")
        return

    df, df_iter = fetch_csv(csv_name, params.url)
    if df is None or df_iter is None:
        print("Error fetching CSV")
        return

    with closing(engine.connect()):

        df.head(n=0).to_sql(name=params.table_name, con=engine, if_exists='replace')
        df.to_sql(name=params.table_name, con=engine, if_exists='append')

        for df in df_iter:
            df = convert_to_datetime(df)
            df.to_sql(name=params.table_name, con=engine, if_exists='append')
            print('Inserted another chunk')

        print("Finished ingesting data into the PostgreSQL database")


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
