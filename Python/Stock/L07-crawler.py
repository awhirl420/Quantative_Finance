import requests
from io import StringIO
import pandas as pd
import numpy as np
from tqdm import tqdm
from financial_statement import html2db
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
import warnings

def requests_get(*args1, **args2):
    i = 3
    while i >= 0:
        try:
            return requests.get(*args1, **args2)
        except (ConnectionError, ReadTimeout) as error:
            print(error)
            print('retry one more time after 60s', i, 'times left')
            time.sleep(60)
        i -= 1
    return pd.DataFrame()
    
def requests_post(*args1, **args2):
    i = 3
    while i >= 0:
        try:
            return requests.post(*args1, **args2)
        except (ConnectionError, ReadTimeout) as error:
            print(error)
            print('retry one more time after 60s', i, 'time left')
            time.sleep(60)
        i -= 1
    return pd.DataFrame()
    
warnings.simplefilter(action='ignore', category=FutureWarning)

def crawl_price(date):
    datestr = date.strftime('%Y%m%d')
    
    try:
        r = requests_post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999')
    except Exception as e:
        print('**WARRN: cannot get stock price at', datestr)
        print(e)
        return None
    
    content = r.text.replace('=', '')
    
    lines = content.spilt('\n')
    lines = list(filter(lambda l:len(1.split('",')) > 10, lines))
    content = "\n".join(lines)
    
    if content == '':
        return None
    
    df = pd.read_csv(StringIO(content))
    df = df.astype(str)
    df = df.apply(lambda s: s.str.replace(',', ''))
    df['date'] = pd.to_datetime(date)
    df = df.rename(columns={'證券代號':'stock_id'})
    df = df.set_index(['stock_id', 'date'])
    
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    df = df[df.columns[df.isnull().all() == False]]
    df = df[~df['收盤價'].isnull()]
    
    return df
