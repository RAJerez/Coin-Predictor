import requests, threading
from requests.exceptions import RequestException
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class CoinsThread(threading.Thread):
    def __init__(self, url, id, date, start_date, end_date):
        threading.Thread.__init__(self)
        self.url = url
        self.id = id
        self.date = date
        self.file_f = f"../data/coins_{start_date}_{end_date}.csv"

    def run(self):
        try:
            date_f = datetime.strptime(self.date, "%Y-%m-%d").strftime("%d-%m-%Y")
            format = f"{self.id}/history?date={date_f}"
            endpoint = self.url + format
            response = requests.get(endpoint)
            result = response.json()
            log.info(f"{self.id}_{self.date} - Successfully generated query")
        except RequestException as e:
            log.error(f"Error en la solicitud: {e}")
        try:
            coin = str(result["id"])
            date = str(self.date)
            price = str(result["market_data"]["current_price"]["usd"])
            json_data = str(response.text)
            with open(self.file_f, "a") as file:
                file.write(f"{coin};{date};{price};{json_data}\n")
                log.info(f"{coin}_{date} - Data written correctly")
        except Exception as e:
            log.error(f"{coin}_{date} - Unexpected error written: {e}")
