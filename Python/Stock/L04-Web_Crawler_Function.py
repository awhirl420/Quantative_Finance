import requests
import pandas as pd
from io import StringIO

def crawl_price(date):
    
    # translate date into string
    datestr = date.strftime('%Y%m%d')
    
    # get data
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999')
    
    # delete '='
    content = r.text.replace('=', '')
    
    # delete lines that len(columns) < 10
    lines = content.split('\n')
    lines = list(filter(lambda l:len(l.split('",')) > 10, lines))
    
    # re-combine
    content = "\n".join(lines)
    
    # if fail to get data, show "None"
    if content == '':
        return None
    
    # read
    df = pd.read_csv(StringIO(content))
    
    # string
    df = df.astype(str)
    
    # delete ','    
    df = df.apply(lambda s: s.str.replace(',', ''))
    
    # save date as series
    df['date'] = pd.to_datetime(date)
    
    # change '證券代號' as 'stock_id'
    df = df.rename(columns={'證券代號':'stock_id'})
    
    # take both stock_id and date as index
    df = df.set_index(['stock_id', 'date'])
    
    # values
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    
    # delete non-necessary columns
    df = df[df.columns[df.isnull().all() == False]]
    
    return df

import datetime
crawl_price(datetime.datetime(2018,1,2))
