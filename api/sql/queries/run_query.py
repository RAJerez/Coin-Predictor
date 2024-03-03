from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os
from decouple import config

DB_CONNSTR = config("DB_CONNSTR")

file_sql = "avg_price_month.sql"

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(script_dir, file_sql))

def run_query(file_sql, db_connstr):
    try:
        engine = create_engine(db_connstr)
        with engine.connect() as con:
            with open(file_sql) as file:
                query = text(file.read())
                result = con.execute(query)
                for row in result:
                    print(row)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    run_query(data_dir, DB_CONNSTR)