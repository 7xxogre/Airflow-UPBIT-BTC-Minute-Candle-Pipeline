from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook
import pandas as pd
import sqlalchemy
from airflow import macros

class UpbitCandleApiSaveToMysql(BaseOperator):
    template_fields = ("exec_date")
    def __init__(self, end_point, db_conn_id, table_nm, symbol, exec_date, **kwargs):
        super().__init__(**kwargs)
        self.api_base_url = "https://api.upbit.com/v1/"
        self.end_point = end_point
        self.db_conn_id = db_conn_id
        self.table_nm = table_nm
        self.symbol = symbol
        self.exec_date = exec_date
        

    def execute(self, context):
        candle_df = self._call_api()
        
        connection = BaseHook.get_connection(self.db_conn_id)
        db_connection_url = f"mysql+mysqlconnector://{connection.login}:{connection.password}@{connection.host}/{connection.schema}"
        connection = sqlalchemy.create_engine(db_connection_url)
        candle_df.to_sql(name = self.table_nm,
                         con = connection,
                         index = False,
                         if_exists = 'append')
    
    def _call_api(self):
        import requests
        from datetime import datetime, timedelta
        import time
        
        start_time = (datetime.strptime(self.exec_date, "%Y-%m-%d") + timedelta(days = 1)).strftime("%Y-%m-%d") + ' 00:00:00'
        result_lst = []
        self.log.info(start_time)
        for i in range(60 * 24 // 200 + 1):
            url = self.api_base_url + self.end_point + '?market=' + self.symbol + '&count=200&to=' + start_time
            self.log.info(url)
            response = requests.get(url).json()
            is_break = False
            print(response)
            for elem in response:
                if self.exec_date not in elem['candle_date_time_utc']:
                    is_break = True
                    break
                result_lst.append(elem)
                
            if is_break or len(response) < 200:
                break
            start_time = response[-1]['candle_date_time_utc']
            time.sleep(1)
            
        data_sample = pd.json_normalize(result_lst)
        data_sample['made_date'] = self.exec_date
        return data_sample