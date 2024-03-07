from airflow import DAG, macros
import pendulum
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from operators.upbit_candle_api_save_to_mysql import UpbitCandleApiSaveToMysql

default_args = {
    'owner': 'airflow',
    'start_date': pendulum.datetime(2024, 3, 4, 0, 0),
    'schedule_interval': '0 0 * * *',
}

with DAG(
    dag_id = 'dags_get_upbit_BTC_1m_candle',
    default_args = default_args
) as dag:
    sql_already_data_delete = MySqlOperator(
        task_id = 'sql_already_data_delete',
        mysql_conn_id = 'conn-db-mysql',
        sql= "DELETE FROM airflow_test.upbit_btc_1m_candle WHERE made_date='{{ execution_date.strftime('%Y-%m-%d') }}'"
    )
    print("sql" + "DELETE FROM airflow_test.upbit_btc_1m_candle WHERE made_date='{{ execution_date.strftime('%Y-%m-%d') }}'")

    upbit_BTC_1m_candle_api_save_to_mysql = UpbitCandleApiSaveToMysql(
        task_id = "upbit_BTC_1m_candle_api_save_to_mysql",
        end_point = "candles/minutes/1", 
        db_conn_id = "conn-db-mysql", 
        table_nm = "upbit_btc_1m_candle",
        symbol = "KRW-BTC",
        exec_date = '{{ execution_date.strftime("%Y-%m-%d") }}'
        )
    

    
    sql_already_data_delete >> upbit_BTC_1m_candle_api_save_to_mysql

    
    
    