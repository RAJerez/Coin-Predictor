import threading
import requests
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError
import pandas as pd
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
        
        with open(self.file_f, 'w') as file:
            file.write('coin,date,price,json\n')
        

    def run(self):
        try:
            date_f = datetime.strptime(self.date, '%Y-%m-%d').strftime('%d-%m-%Y')
            format = f"{self.id}/history?date={date_f}"
            endpoint = self.url + format
            response = requests.get(endpoint)
            result = response.json()
            coin = str(result["id"])
            date = self.date
            price = str(result["market_data"]["current_price"]["usd"])
            json_data = str(result)
            with open(self.file_f, 'a') as file:
                file.write(f'{coin},{date},{price},{json_data}\n')
        except RequestException as e:
            log.error(f"Error en la solicitud: {e}")    
        except Exception as e:
            log.error(f"Error inesperado al obtener datos para {self.id}: {e}")     


def main():
    url = 'https://api.coingecko.com/api/v3/coins/'
    start_date = '2017-01-01'
    end_date_str = '2017-01-02'
    max_threads = 3
    coins = ['bitcoin', 'ethereum', 'cardano']
    
    active_threads = []
        
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    while current_date <= end_date:
        date = current_date.strftime('%Y-%m-%d')
        for coin in coins:
            thread = GetCoinsThread(url, coin, date, start_date, end_date_str)
            active_threads.append(thread)
            thread.start()
            if len(active_threads) >= max_threads:
                for active_thread in active_threads:
                    active_thread.join()
                active_threads = []
            
        current_date += timedelta(days=1)
                

    for thread in active_threads:
        thread.join()

if __name__ == "__main__":
    main()