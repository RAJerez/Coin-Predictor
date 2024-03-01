import click
from extractors import GetCoins
from cfg import URL
from datetime import datetime, timedelta
from multi_extractors import GetCoinsThread
from concurrent.futures import ThreadPoolExecutor

path = "../data"

@click.group()
def cli():
    pass
    

@cli.command()
@click.option('--coin', help="Insert a Cripto Id")
@click.option('--date', help="Run a specific date in format yyyy-mm-dd")
def one_query(coin, date):
    data = GetCoins(URL, coin, date, path)
    df = data.extract()
    data.write_csv(df)
# COMMAND: python3 cli.py one-query --coin bitcoin --date 2017-12-31

@cli.command()
@click.option('--start_date', help="Date of first request")
@click.option('--end_date', help="Date of last request")
@click.option('--max_threads', help="Number max of threads")
def multi_extractors(start_date, end_date, max_threads):
    coins = ['bitcoin', 'ethereum', 'cardano']
    
    file_f = f"../data/coins_{start_date}_{end_date}.csv"
    with open(file_f, 'w') as file:
            file.write('coin;date;price;json\n')
    
    executor = ThreadPoolExecutor(max_workers=int(max_threads))
    
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_str = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date_str:
        date = current_date.strftime('%Y-%m-%d')
        for coin in coins:
            thread = GetCoinsThread(URL, coin, date, start_date, end_date)
            executor.submit(thread.run)
             
        current_date += timedelta(days=1)
    
    executor.shutdown(wait=True)     
# COMMAND: python3 cli.py multi-extractors --start_date 2017-01-01 --end_date 2017-01-02 --max_threads 3

@cli.command()
@click.argument('load-db', type=int)
def load():
    pass



if __name__ == "__main__":
    cli()