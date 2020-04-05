from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                               LoadDimensionOperator, DataQualityOperator,
                               PostgresOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          max_active_runs=1
        )

start_execution = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables = PostgresOperator(
    task_id="create_tables",
    dag=dag,
    postgres_conn_id="redshift",
    sql="create_tables.sql"
)

stage_imm_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    redshift_conn_id='redshift',
    aws_credentials='aws_credentials',
    table='staging_imm',
    s3_bucket='udacity-dend',
    s3_key='log_data',
    copy_json_option='auto',
    region='us-west-2',
    dag=dag
)

stage_dem_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    redshift_conn_id='redshift',
    aws_credentials='aws_credentials',
    table='staging_dem',
    s3_bucket='udacity-dend',
    s3_key='song_data',
    copy_json_option='auto',
    region='us-west-2',
    dag=dag
)

load_imm_dem_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    redshift_conn_id='redshift',
    table='imm_dem',
    select_qry=SqlQueries.imm_dem_table_insert,
    dag=dag
)

load_cities_dim_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    redshift_conn_id='redshift',
    table='cities',
    select_qry=SqlQueries.city_table_insert,
    dag=dag
)

load_state_dim_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    redshift_conn_id='redshift',
    table='states',
    select_qry=SqlQueries.state_table_insert,
    dag=dag
)

load_entry_ports_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    redshift_conn_id='redshift',
    table='entry_ports',
    select_qry=SqlQueries.entry_port_table_insert,
    append_insert=True,
    primary_key='entry_port_id',
    dag=dag
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    redshift_conn_id='redshift',
    test_query='select count(*) from imm_dem where Gender is null;',
    expected_result=0,
    dag=dag
)

end_execution = DummyOperator(task_id='Stop_execution',  dag=dag)

start_execution >> create_tables

create_tables >> stage_imm_to_redshift >> load_imm_dem_table
create_tables >> stage_dem_to_redshift >> load_imm_dem_table

load_imm_dem_table >> load_cities_dim_table >> run_quality_checks
load_imm_dem_table >> load_state_dim_table >> run_quality_checks
load_imm_dem_table >> load_entry_ports_dim_table >> run_quality_checks

run_quality_checks >> end_execution
