import pandas as pd
from sqlalchemy import create_engine, text

print("Pandas version: ", pd.__version__)

def main():
    print('Starting chunkwise insertion into postgres database')
    
    #os.system(f"wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz -O green_tripdata_2019-10.csv.gz")
    #os.system(f"wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O taxi_zone_lookup.csv")

    
    # Create the database engine
    engine = create_engine('postgresql://postgres:postgres@localhost:5433/postgres')
    
    # Create the database, first delete if exists
    connection = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
    connection.execute(text('DROP DATABASE IF EXISTS ny_taxi'))
    connection.execute(text('CREATE DATABASE ny_taxi'))
    engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')
    
    # Load the data in chunks
    df_iter = pd.read_csv('green_tripdata_2019-10.csv.gz', compression='gzip', iterator=True, chunksize=100000, low_memory=False)
    df = next(df_iter)

    # Convert to datetime 
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

    df.head(0).to_sql('green_taxi_data', index=False, con=engine, if_exists='replace')

    df_iter = pd.read_csv('green_tripdata_2019-10.csv.gz', compression='gzip', iterator=True, chunksize=100000, low_memory=False)
    while True:
        try:
            df = next(df_iter)
            df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
            df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
            df.to_sql('green_taxi_data', index=False, con=engine, if_exists='append')
            print(f'Sucessfullly saved {len(df)} rows')
        except StopIteration:
            print('All Chunks of data ingested into postgres database.')
            break

    df2 = pd.read_csv('taxi_zone_lookup.csv')
    df2.to_sql('taxi_zone_lookup', index=False, con=engine, if_exists='replace')

    # Close connection
    connection.close()
    print('Connection closed')

if __name__=='__main__':
    main()