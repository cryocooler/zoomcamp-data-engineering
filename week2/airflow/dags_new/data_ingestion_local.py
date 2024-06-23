from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
import pandas as pd


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
default_args = {"start_date": datetime(2021, 1, 1)}


local_workflow = DAG(
    "LocalIngestionDag",
    description="a simple DAG to download and ingest a parquet file",
    schedule_interval="30 6 2 * *",
    default_args=default_args,
)

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

# previous_year = datetime.now().year - 1

URL_PREFIX = "https://d37ci6vzurychx.cloudfront.net/trip-data"
URL_TEMPLATE = (
    URL_PREFIX
    + "/yellow_tripdata_{{ execution_date.add(years=-1).strftime('%Y-%m') }}.parquet"
)


OUTPUT_FILE_TEMPLATE = (
    AIRFLOW_HOME
    + "/output_{{ execution_date.add(years=-1).strftime('%Y-%m') }}.parquet"
)

with local_workflow:

    wget_task = BashOperator(
        task_id="curl_file",
        bash_command=f"curl -sSL {URL_TEMPLATE} -o {OUTPUT_FILE_TEMPLATE}",
        # bash_command='echo "{{ ds }}" "{{ execution_date.strftime(\'%Y-%m\') }}"', we stamp files with the execution datetime
    )

    check_file_task = BashOperator(
        task_id="check_file",
        bash_command=f"grep -q 'File not found' {OUTPUT_FILE_TEMPLATE} && exit 1 || exit 0",
    )

    def ingest_data(execution_date, **kwargs):
        execution_date_str = execution_date.add(years=-1).strftime("%Y-%m")

        print(f"Executing task for execution date: {execution_date}")
        print(f"{OUTPUT_FILE_TEMPLATE}")
        print(f"real file name: ./output_{execution_date_str}.parquet")
        output_file = f"./output_{execution_date_str}.parquet"

        df = pd.read_parquet(output_file)

        df = df.head(10)
        print(df)
        df.to_parquet(output_file)

    ingest_task = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data,
        provide_context=True,
    )

    list_files_task = BashOperator(
        task_id="list_files",
        bash_command=f"ls {AIRFLOW_HOME}",
    )


wget_task >> check_file_task >> ingest_task >> list_files_task
