import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from cfg import DB_CONNSTR, TABLE_NAMES
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


engine = create_engine(DB_CONNSTR)

sql_dir = "../sql/create_tables/"


def create_tables():
    """Create db tables"""
    try:
        with engine.connect() as con:
            for file in TABLE_NAMES:
                log.info(f"Creating table {file}")
                with open(sql_dir + f"{file}.sql") as f:
                    query = text(f.read())
                    log.info(f"Query for {file}: {query}")
                con.execute(query)
                con.commit()
        log.info("Tables created successfully.")

    except sa.exc.SQLAlchemyError as e:
        log.info(f"Error creating tables: {e}")
    except Exception as e:
        log.info(f"Unexpected error: {e}")


if __name__ == "__main__":
    create_tables()
