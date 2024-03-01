import json
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError
from datetime import datetime, timedelta
from loggers import Logger


log = Logger()

class GetCoinsThread(threading.Thread):
    def __init__(self, url, id, date, start_date, end_date):
        threading.Thread.__init__(self)
        self.url = url
        self.id = id
        self.date = date
        self.file_f = f"../data/coins_{start_date}_{end_date}.csv"
        

    def run(self):
        try:
            date_f = datetime.strptime(self.date, '%Y-%m-%d').strftime('%d-%m-%Y')
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
            with open(self.file_f, 'a') as file:
                file.write(f'{coin};{date};{price};{json_data}\n')
                log.info(f"{coin}_{date} - Data written correctly")
        except Exception as e:
            log.error(f"{coin}_{date} - Unexpected error written: {e}")     


def main():
    url = 'https://api.coingecko.com/api/v3/coins/'
    start_date = '2017-01-01'
    end_date_str = '2017-01-31'
    max_threads = 3
    coins = ['bitcoin', 'ethereum', 'cardano']
    
    file_f = f"../data/coins_{start_date}_{end_date_str}.csv"
    with open(file_f, 'w') as file:
            file.write('coin;date;price;json\n')
    
    executor = ThreadPoolExecutor(max_workers=max_threads)
    
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')



    while current_date <= end_date:
        date = current_date.strftime('%Y-%m-%d')
        for coin in coins:
            thread = GetCoinsThread(url, coin, date, start_date, end_date_str)
            executor.submit(thread.run)
            
        current_date += timedelta(days=1)
                
    executor.shutdown(wait=True)