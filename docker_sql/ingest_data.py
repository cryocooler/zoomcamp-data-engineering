#!/usr/bin/env python
# coding: utf-8
import os
import argparse
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    parquet_name = "output.parquet"

    os.system(f"wget {url} -O {parquet_name}")

    ## download the parquet
    df = pd.read_parquet("output.parquet")

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    engine.connect()

    df.head(n=0).to_sql(name="green_taxi_data", con=engine, if_exists="replace")

    print(pd.io.sql.get_schema(df, name=table_name, con=engine))

    df.to_sql(name=table_name, con=engine, if_exists="replace")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="I")
    parser.add_argument("--user", help="user for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="hostname for postgres")
    parser.add_argument("--port", help="port")
    parser.add_argument("--db", help="database name")
    parser.add_argument("--table_name", help="table name for data storage")
    parser.add_argument("--url", help="url of the parquet file")

    args = parser.parse_args()

    main(args)
