"""
Multithreading features are missing
     Currencies: Bitcoin, Ethereum, Cardano
     The data will be grouped by date in different .csv files
     File Name: Coins_{date}.csv
"""

from extractors import GetCoins
import threading
import pandas as pd

class GetCoinsThread(GetCoins, threading.Thread):
    def __init__(self, url, id, date, output_path):
        super().__init__(self, url, id, date)
        threading.Thread.__init__(self)
        self.output_path = output_path
        
    def extract(self, url, id, date) -> pd.DataFrame:
        return super().extract(url, id, date)
    
    def write_csv(self, df, path):
        return super().write_csv(df, path)