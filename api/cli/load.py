from sqlalchemy import exc
from loggers import Logger
from loaders import RawLoader

log = Logger()

file_path = "../data/coins_2017-01-01_2017-01-02.csv"
table_name = "coin_data"


def run_load():
    try:
        RawLoader(table_name).load_table(file_path)
        log.info(f"Data {table_name} loaded correctly")

    except exc.SQLAlchemyError as e:

        log.error(f"Error loading data {table_name}: {e}")

    except Exception as e:

        log.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    run_load()
