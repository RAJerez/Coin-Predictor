import requests
import pandas as pd
import os
from loggers import Logger
from datetime import datetime

log = Logger()


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
            data = [
                {
                    "coin": str(result["id"]),
                    "date": self.date,
                    "price": float(result["market_data"]["current_price"]["usd"]),
                    "json": str(response.text),
                }
            ]
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            log.error(f"Error: {e}")

    def write_csv(self, df):
        path_f = self.path + f"/{self.id}_{self.date}.csv"
        if not os.path.exists(path_f):
            df.to_csv(path_f, index=False, sep=";")
            log.info(f"The file {self.id}_{self.date}.csv has been created correctly")
        else:
            log.error(
                f"The file {self.id}_{self.date}.csv already exists. Charge canceled."
            )