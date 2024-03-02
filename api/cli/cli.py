import click, os, schedule, time
from packages.loaders import RawLoader
from packages.extractors import Coin
from packages.multi_extractors import CoinsThread
from concurrent.futures import ThreadPoolExecutor
from cfg import URL
from datetime import datetime, timedelta
from sqlalchemy import exc
from loggers import Logger


log = Logger()
path = "../data"


@click.group()
def cli():
    pass


@cli.command()
@click.option("--coin", help="Insert a Cripto Id")
@click.option("--date", help="Run a specific date in format yyyy-mm-dd")
def one_query(coin, date):
    file_f = f"../data/{coin}_{date}.csv"
    data = Coin(URL, coin, date, path)
    df = data.api_consult()
    data.write_csv(df)
    return file_f


# COMMAND:
# python3 cli/cli.py one-query --coin bitcoin --date 2017-12-31


@cli.command()
@click.option("--start_date", help="Date of first request")
@click.option("--end_date", help="Date of last request")
@click.option("--max_threads", help="Number max of threads")
@click.option("--load", help="Optional argument to load data into Postgres table")
def run_multi_extractors(start_date, end_date, max_threads, load):
    coins = ["bitcoin", "ethereum", "cardano"]

    file_f = f"../data/coins_{start_date}_{end_date}.csv"
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
        
def schedule_multi_extractors(start_date, end_date, max_threads, load):
    schedule.every().day.at("03:55").do(run_multi_extractors, start_date=start_date, end_date=end_date, max_threads=max_threads, load=load)

    while True:
        schedule.run_pending()
        time.sleep(1)


# COMMAND:
# python3 cli/cli.py multi-extractors --start_date 2017-01-01 --end_date 2017-01-02 --max_threads 3 --load


@cli.command()
@click.argument("file", type=str)
def run_load(file):
    path = f"../data/coins_{file}.csv"
    table_name = "coin_data"
    try:
        RawLoader(table_name).load_table(file)
        log.info(f"Data {table_name} loaded correctly")
    except exc.SQLAlchemyError as e:
        log.error(f"Error loading data {table_name}: {e}")
    except Exception as e:
        log.error(f"Unexpected error: {e}")


# COMMAND:
# python3 cli.py

if __name__ == "__main__":
    cli()
