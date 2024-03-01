from sqlalchemy import create_engine
from cfg import DB_CONNSTR
import pandas as pd


engine = create_engine(DB_CONNSTR)


class BaseLoader:
    def load_table(self, df):
        df.to_sql(self.table_name, con=engine, index=False, if_exists="append")


class RawLoader(BaseLoader):
    def __init__(self, table_name):
        self.table_name = table_name

    def load_table(self, file_path):
        df_raw = pd.read_csv(file_path, sep=';')
        return super().load_table(df_raw)
