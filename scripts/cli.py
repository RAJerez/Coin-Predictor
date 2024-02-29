import click
from extractors import GetCoins
from loggers import Logger
from decouple import config
from cfg import URL, DATA_DIR
import os


@click.group()
def cli():
    pass

@cli.command()
@click.option("--coin", required=True, help="Insert a Cripto Id")
@click.option("--date", required=True, help="Run a specific date in format yyyy-mm-dd")
def one_query(coin, date):
    """Description"""
    data = GetCoins(URL, coin, date, DATA_DIR)
    df = data.extract()
    if not os.path.exists(DATA_DIR):
        data.write_csv(df)
        print("File created")
    else:
        print("Ya existe...Crear")
    
    



if  __name__ == "__main__":
    cli()