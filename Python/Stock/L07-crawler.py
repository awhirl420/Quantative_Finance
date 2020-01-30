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
    lines = list(filter(lambda l:len(l.split('",')) > 10, lines))
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



def crawl_monthly_report(date):
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_' + str(date.year - 1911) + '_' + str(date.month) + '.html'
    
    print(url)
    
    # 下載該年月的網站，並用pandas轉換成dataframe
    try:
        r = requests_get(url, headers=headers)
        r.encoding = 'big5'
    except:
        print('**WARRN: requests cannot get html')
        return None
    
    import lxml
    
    try:
        html_df = pd.read_html(StringIO(r.text))
    except:
        print('**WARRN: Pandas cannot find any table in the HTML file')
        return None
    
    # 處理一下資料
    if html_df[0].shape[0] > 500:
        df = html_df[0].copy()
    else:
        df = pd.concat([df for df in html_df if df.shape[1] <= 11 and df.shape[1] > 5])
               
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0, 10))]
        column_index = df.index[(df[0] == '公司代號')]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    
    next_month = datetime.date(date.year + int(date.month / 12), ((date.month % 12) + 1), 10)
    df['date'] = pd.to_datetime(next_month)
    
    df = df.rename(columns={'公司代號':'stock_id'})
    df = df.set_index(['stock_id', 'date'])
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    df = df[df.columns[df.isnull().all() == False]]
    
    return df

import requests
import os
import time
import datetime
import random
import io
import shutil
import zipfile
import sys
import urllib.request
from tqdm import tqdm

def crawl_finance_statement2019(year, season):
               
    def ifrs_url(year, season):
        url = "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&fileName=tifrs-"+str(year)+"Q"+str(season)\
               +".zip&filePath=/home/html/nas/ifrs"+str(year)+"/"
        print(url)
        return url
    
    print('start download')
    
    class DownloadProgressBar(tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)
    
    def download_url(url, output_path):
        with DownloadProgressBar(unit='B', unit_scale=True,
                                 miniters=1, desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)
    
    def ifrs_url(year, season):
        url = "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&fileName=tifrs-"+str(year)+"Q"+str(season)\
               +".zip&filePath=/home/html/nas/ifrs/"+str(year)+"/"
        print(url)
        return url
               
    url = ifrs_url(year, season)
    download_url(url, 'temp.zip')
    
    print('finish download')
    
    path = os.path.join('date', 'financial_statement', str(year) + str(season))
    
    if os.path.isdir(path):
        shutil.rmtree(path)
    
    print('create new dir')
    
    zipfiles = zipfile.ZipFile(open('temp.zip', 'rb'))
    zipfiles.extractall(path=path)
    
    print('extract all files')
    
    fnames = [f for f in os.listdir(path) if f[-5:] == '.html']
    fnames = sorted(fnames)
    
    newfnames = [f.spilt("-")[5] + '.html' for f in fname]
    
    for fold, fnew in zip(fname, newfnames):
               if len(fnew) != 9:
                   print('remove strange code id', fnew)
                   os.remove(os.path.join(path, fold))
                   continue
               
               if not os.path.exists(os.path.join(path, fnew)):
                   os.rename(os.path.join(path, fold), os.path.join(path, fnew))
               else:
                   os.remove(os.path.join(path, fold))
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
