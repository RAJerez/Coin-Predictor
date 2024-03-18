import requests
import pandas as pd
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
        df = pd.read_csv(file, sep=";")
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df_month = (
            df.groupby(["coin", "year", "month"])
            .agg({"price": ["max", "min"]})
            .reset_index()
        )
        df_month.columns = ["coin", "year", "month", "max_price", "min_price"]
        return df_month
