import pandas as pd

file = "/home/agustin/Documentos/exam-rodrigo-jerez/tmp/bitcoin_2017-12-31.csv"

def coin_month_transform(file):
    file = "/home/agustin/Documentos/exam-rodrigo-jerez/tmp/bitcoin_2017-12-31.csv"
    df = pd.read_csv(file, sep = ';')
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df_new = df.groupby(['coin', 'year', 'month']).agg({'price': ['max', 'min']}).reset_index()
    df_new.columns = ['coin', 'year', 'month', 'max_price', 'min_price']
    df_new # READY TO LOAD TO COIN_MONTH_DATA TABLE
    return df_new