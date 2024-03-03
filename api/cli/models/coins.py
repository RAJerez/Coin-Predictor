import requests
import pandas as pd
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class Coin:
    def __init__(self, url, id, date, path):
        self.url = url
        self.id = id
        self.date = date
        self.path = path

    def api_consult(self) -> pd.DataFrame:
        try:
            date_f = datetime.strptime(self.date, "%Y-%m-%d").strftime("%d-%m-%Y")
            format = f"{self.id}/history?date={date_f}"
            endpoint = self.url + format
            response = requests.get(endpoint)
            result = response.json()
            coin = str(result["id"])
            date = self.date
            price = float(result["market_data"]["current_price"]["usd"])
            json = str(response.text)
            data_f = f"{coin};{date};{price};{json}"
            return data_f
        except Exception as e:
            log.error(f"Error: {e}")
            
    
    def write_file(self, data_f):
        path_f = self.path + f"/{self.id}_{self.date}.csv"
        head = "coin;date;price;json"
        with open(path_f, "w") as file:
            file.write(f"{head}\n{data_f}\n")
            log.info(f"{self.id}_{self.date} - Data written correctly")
            return path_f
    
    def coin_month_transform(file):
        file = "/home/agustin/Documentos/exam-rodrigo-jerez/tmp/bitcoin_2017-12-31.csv"
        df = pd.read_csv(file, sep = ';')
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df_month = df.groupby(['coin', 'year', 'month']).agg({'price': ['max', 'min']}).reset_index()
        df_month.columns = ['coin', 'year', 'month', 'max_price', 'min_price']
        return df_month




#### TEST ####

#python3 cli.py one-query --coin bitcoin --date 2017-12-31

def one_query(coin, date):
    try:
        data = Coin(url, coin, date, path)
        data_d = data.api_consult()
        data.write_file(data_d)
        print(f"The file {coin}_{date}.csv has been created correctly")
        df_month = data.coin_month_transform(path)
    except Exception as e:
        print(f"{e}")
             
if __name__ == "__main__":
    # Obtener la ruta del directorio actual del script
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_data = os.path.abspath(os.path.join(directorio_script, "../../data"))
    
    # Declaro variables
    path = ruta_data
    url = 'https://api.coingecko.com/api/v3/coins/'    
    coin = 'bitcoin'
    date = '2017-12-31'
    
    one_query(coin, date)
    
    ###################
    
    def one_query(coin, date):
        try:
            coin = Coin(URL, coin, date, data_dir)
            response = coin.api_consult()
            coin.write_file(response)
            log.info(f"The file {coin}_{date}.csv has been created correctly")
            df_month = coin.month_transform(file_f)
            return file_f
        except Exception as e:
            log.error(f"{e}")