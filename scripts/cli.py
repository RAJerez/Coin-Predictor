import click
from extractors import GetCoins
from loggers import Logger
from cfg import URL

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

if  __name__ == "__main__":
    cli()