import click, os, schedule, time, logging
from models.db_loaders import RawLoader
from models.coins import Coin
from models.coins_threading import CoinsThread
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from sqlalchemy import exc
from decouple import config

URL = config("URL")

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(script_dir, "../data"))


@click.group()
def cli():
    pass


@cli.command()
@click.option("--coin", help="Insert a Cripto Id")
@click.option("--date", help="Run a specific date in format yyyy-mm-dd")
def one_query(coin, date):
    file_f = f"{data_dir}/{coin}_{date}.csv"
    try:
        coin = Coin(URL, coin, date, data_dir)
        response = coin.api_consult()
        coin.write_file(response)
        log.info(f"The file {coin}_{date}.csv has been created correctly")

        return file_f
    except Exception as e:
        log.error(f"{e}")


@cli.command()
@click.option("--start_date", help="Date of first request")
@click.option("--end_date", help="Date of last request")
@click.option("--max_threads", help="Number max of threads")
@click.option(
    "--load", help="Optional argument to load data into Postgres table", is_flag=True
)
def run_multi_threading(start_date, end_date, max_threads, load):
    coins = ["bitcoin", "ethereum", "cardano"]

    file_f = f"{data_dir}/coins_{start_date}_{end_date}.csv"
    if not os.path.exists(file_f):
        with open(file_f, "w") as file:
            file.write("coin;date;price;json\n")
    executor = ThreadPoolExecutor(max_workers=int(max_threads))
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_str = datetime.strptime(end_date, "%Y-%m-%d")
    while current_date <= end_date_str:
        date = current_date.strftime("%Y-%m-%d")
        for coin in coins:
            thread = CoinsThread(URL, coin, date, start_date, end_date)
            executor.submit(thread.run)
        current_date += timedelta(days=1)
    executor.shutdown(wait=True)

    if load:
        run_load(file_f)


def schedule_multi_extractors(
    start_date: str, end_date: str, max_threads: int, load
) -> None:
    """Schedule the execution of multiple extractors using multithreading.

    This function schedules the execution of multiple extractors to run daily at 03:00 AM.

    Args:
        start_date (str): The start date for the extraction tasks.
        end_date (str): The end date for the extraction tasks.
        max_threads (int): The maximum number of threads to be used for multithreading.
        load (bool): A flag indicating whether to load extracted data after extraction.

    Returns:
        None

    Note:
        This function runs indefinitely, continuously checking for scheduled tasks
        and executing them while sleeping for 1 second between iterations.
    """
    schedule.every().day.at("03:00").do(
        run_multi_threading,
        start_date=start_date,
        end_date=end_date,
        max_threads=max_threads,
        load=load,
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


def run_load(file: str) -> None:
    """
    Load data from a CSV file into a database table.

    Args:
        file (str): The name of the CSV file containing the data.

    Returns:
        None
    """
    table_name = "coin_data"
    try:
        RawLoader(table_name).load_table(file)
        log.info(f"Data {table_name} loaded correctly")
    except exc.SQLAlchemyError as e:
        log.error(f"Error loading data {table_name}: {e}")
    except Exception as e:
        log.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    cli()
