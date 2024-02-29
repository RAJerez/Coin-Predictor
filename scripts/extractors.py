import requests
import pandas as pd
from decouple import config
import os
import threading
from datetime import datetime

class GetCoins:
    def __init__(self, url, id, date, path):
        self.url = url
        self.id = id
        self.date = date
        self.path = path + f"{id}_{date}.csv"


    def extract(self) -> pd.DataFrame:
        try:
            date_f = datetime.strptime(self.date, '%Y-%m-%d').strftime('%d-%m-%Y')
            format = f"{self.id}/history?date={date_f}"
            endpoint = self.url + format
            response = requests.get(endpoint)
            result = response.json()           
            data = [{"coin": str(result["id"]),
                     "date": self.date,
                     "price": float(result["market_data"]["current_price"]["usd"]),
                     "json": str(result)}]
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error: {e}")
    
    def write_csv(self, df, path):
        if not os.path.exists(path):
            df.to_csv(path, index=False)
        else:
            print("The file already exists")


if __name__ == "__main__":
    url_base = config("URL") # env
    coin_id = "bitcoin" #arg cli
    date = "2017-12-30" #arg cli
    path = f"/home/agustin/Documentos/exam-rodrigo-jerez/data/"  #{coin_id}_{date}.csv # env

    data = GetCoins(url_base, coin_id, date, path).extract()
    
    
    