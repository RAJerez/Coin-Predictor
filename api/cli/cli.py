import click, os, schedule, time, logging
from api.cli.models.db_loaders import RawLoader
from api.cli.models.coins import Coin
from api.cli.models.coins_threading import CoinsThread
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from sqlalchemy import exc
import logging
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
        

# COMMAND:
# python3 cli.py one-query --coin bitcoin --date 2017-12-30

@cli.command()
@click.option("--start_date", help="Date of first request")
@click.option("--end_date", help="Date of last request")
@click.option("--max_threads", help="Number max of threads")
@click.option("--load", help="Optional argument to load data into Postgres table", is_flag=True)
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
                
def schedule_multi_extractors(start_date, end_date, max_threads, load):
    schedule.every().day.at("03:00").do(run_multi_threading, start_date=start_date, end_date=end_date, max_threads=max_threads, load=load)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
# COMMAND:
# python3 cli.py run-multi-threading --start_date 2024-03-02 --end_date 2024-03-03 --max_threads 3 --load


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

"""
def run_load():
    try:
        RawLoader(table_name).load_table(file_path)
        log.info(f"Data {table_name} loaded correctly")

    except exc.SQLAlchemyError as e:

        log.error(f"Error loading data {table_name}: {e}")

    except Exception as e:

        log.error(f"Unexpected error: {e}")
"""


#### TEST ####
if __name__ == "__main__":
    cli()

"""
    from cfg import URL
    print(URL)
    coin = 'bitcoin'
    date = '2017-12-31'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    data_dir = os.path.abspath(os.path.join(script_dir, "../data"))
    print(data_dir)
    
    try:
        coin = Coin(URL, coin, date, data_dir)
        response = coin.api_consult()
        coin.write_file(response)
        log.info(f"The file {coin}_{date}.csv has been created correctly")
    except Exception as e:
        log.error(f"{e}")
"""
