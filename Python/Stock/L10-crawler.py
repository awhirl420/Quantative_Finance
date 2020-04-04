#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from io import StringIO
import pandas as pd
import numpy as np
from tqdm import tqdm
from .financial_statement import html12db
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
import warnings


# In[3]:


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


# In[4]:


def requests_post(*args1, **args2):
    i = 3
    while i >= 0:
        try:
            return requests.post(*args1, **args2)
        except (ConnectionError, ReadTimeout) as error:
            print(error)
            print('retry one more time after 60s', i, 'times left')
            time.sleep(60)
        i -= 1
    return pd.DataFrame()


# In[6]:


warnings.simplefilter(action='ignore', category=FutureWarning)


# In[7]:


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


# In[9]:


def crawl_monthly_report(date):
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(date.year - 1911)+'_'+str(date.month)+'.html'
    
    print(url)
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
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
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
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


# In[11]:


import requests
import os
import time
import datetime
import random
import shutil
import zipfile
import sys
import urllib.request
from tqdm import tqdm


# In[12]:


def crawl_finance_statement2019(year, season):
    
    def ifrs_url(year, season):
        url = "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&fileName=tifrs-"+str(year)+"Q"+str(season)                +".zip&filePath=/home/html/nas/ifrs/"+str(year)+"/"
        print(url)
        return url
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
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
        url = "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&fileName=tifrs-"+str(year)+"Q"+str(season)                +".zip&filePath=/home/html/nas/ifrs/"+str(year)+"/"
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
    
    newfnames = [f.split("-")[5] + '.html' for f in fnames]
    
    for fold, fnew in zip(fnames, newfnames):
        if len(fnew) != 9:
            print('remove strange code id', fnew)
            os.remove(os.path.join(path, fold))
            continue
        
        if not os.path.exists(os.path.join(path, fnew)):
            os.rename(os.path.join(path, fold), os.path.join(path, fnew))
        else:
            os.remove(os.path.join(path, fold))


# In[13]:


def crawl_finance_statement(year, season, stock_ids):
    
    directory = os.path.join('date', 'financial_statement', str(year) + str(season))
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    def download_html(year, season, stock_ids, report_type='C'):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3''Accept-Encoding: gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'mops.twse.com.tw',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',   
        }
        pbar = tqdm(stock_ids)
        for i in pbar:
            
            # check if the html is already parsed
            file = os.path.join(directory, str(i) + 'html')
            if os.path.exists(file) and os.stat(file).st_size > 20000:
                continue
                
            pbar.set_description('parse htmls %d season %d stock %s' % (year, season, str(i)))
            
            # start parsing
            if year >= 2019:
                ty = {"C":"cr", "B":"er", "C":"ir"}
                url="https://mops.twse.com.tw/server-java/t164sb01?step=3&year=2019&file_name=tifrs-fr1-m1-ci-"+ty[report_type]+"-"+i+"-"+str(year)+"Q"+str(season)+".html"
            else:
                url = ('https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID='
                       + i + '&SYEAR=' + str(year) + '&SSEASON='+str(season)+'&REPORT_ID=' + str(report_type))
                
            print(url)
            try:
                r = requests_get(url, headers=headers, timeout=30)
            except:
                print('**WARRN: request cannot get stock', i, '.html')
                time.sleep(25 + random.uniform(0, 10))
                continue
                
            r.encoding = 'big5'
            
            # write files
            f = open(file, 'w', encoding='utf-8')
            
            f.write('<meta charset="UTF-8">\n')
            f.write(r.text)
            f.close
            
            # finish
            # print(percentage, i, 'end')
            
            # sleep a while
            time.sleep(10)
        if year < 2019:
            download_html(year, season, stock_ids, 'C')
            download_html(year, season, stock_ids, 'A')
            download_html(year, season, stock_ids, 'B')
            download_html(year, season, stock_ids, 'C')
            download_html(year, season, stock_ids, 'A')
            download_html(year, season, stock_ids, 'B')
        else:
            download_html(year, season, stock_ids, 'C')


# In[14]:


def crawl_finance_statement_by_date(date):
    year = date.year
    if date.month == 3:
        season = 4
        year = year - 1
        month = 11
    elif date.month == 5:
        season = 1
        month = 2
    elif date.month == 8:
        season = 2
        month = 5
    elif date.month == 11:
        season = 3
        month = 8
    else:
        return None
    
    if year >= 2019:
        crawl_finance_statement2019(year, season)
    else:
        df = crawl_monthly_report(datetime.datetime(year, month, 1))
        crawl_finance_statement(year, season, df.index.levels[0])
    html2db(date)
    return {}


# In[3]:


import datetime
import time
import os
import pandas as pd
from tqdm import tnrange, tqdm_notebook

from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY

def date_range(start_date, end_date):
    return [dt.date() for dt in rrule(DAILY, dtstart=start_date, until=end_date)]

def month_range(start_date, end_date):
    return [dt.date() for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)]

def season_range(start_date, end_date):
    
    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
        
    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
        
    ret = []
    for year in range(start_date.year-1, end_date.year+1):
        ret += [ datetime.date(year, 5, 15),
                datetime.date(year, 8, 14),
                datetime.date(year, 11, 14),
                datetime.date(year+1, 3, 31)]
    ret = [r for r in ret if start_date < r < end_date]
    
    return ret

def table_exist(conn, table):
    return list(conn.execute(
        "select count(*) from sqlite_master where type='table' and name='" + table + "'"))[0][0] == 1

def table_latest_date(conn, table):
    cursor = conn.execute('SELECT date FROM ' + table + ' ORDER BY date DESC LIMIT 1;')
    return datetime.datetime.strptime(list(cursor)[0][0], '%Y-%m-%d %H:%M:%S')

def table_earliest_date(conn, table):
    cursor = conn.execute('SELECT date FROM ' + table + ' ORDER BY date ASC LIMIT 1;')
    return datetime.datetime.strptime(list(cursor)[0][0], '%Y-%m-%d %H:%M:%S')

def add_to_sql(conn, name, df):
    
    # get the existing dateframe in sqlite3
    exist = table_exist(conn, name)
    ret = pd.read_sql('select * from ' + name, conn, index_col=['stock_id', 'date']) if exist else pd.DataFrame()
    
    # add new df to the dataframe
    ret = ret.append(df)
    ret.reset_index(inplace=True)
    ret['stock_id'] = ret['stock_id'].astype(str)
    ret['date'] = pd.to_datetime(ret['date'])
    ret = ret.drop_duplicates(['stock_id', 'date'], keep='last')
    ret = ret.sort_values(['stock_id', 'date']).set_index(['stock_id', 'date'])
    
    # add the combined table
    ret.to_csv('backup.csv')
    
    try:
        ret.to_sql(name, conn, if_exists='replace')
    except:
        ret = pd.read_csv('backup.csv', parse_date=['date'], dtype={'stock_id':str})
        ret['stock_id'] = ret['stock_id'].astype(str)
        ret.set_index(['stock_id', 'date'], inplace=True)
        ret.to_sql(name, conn, if_exists='replace')


# In[6]:


def update_table(conn, table_name, crawl_function, dates):
    
    print('start crawl ' + table_name + ' from', date[0], 'to', date[-1])
    
    df = pd.DataFrame()
    dfs = {}
    
    progress = tqdm_notebook(dates, )
    
    for d in progress:
        
        print('crawling', d)
        progress.set_description('crawl' + table_name + str(d))
        
        date = crawl_function(d)
        
        if data is None:
            print('fail, check if it is a holiday')
            
        # update multiple dataframe
        elif isinstance(data, dict):
            if len(dfs) == 0:
                dfs = {i:pd.DataFrame() for i in data.key()}
                
            for i, d in data.items():
                dfs[i] = dfs[i].append(d)
                
        # update single dataframe
        else:
            df = df.append(data)
            print('success')
            
        if len(df) > 50000:
            add_to_sql(conn, table_name, df)
            df = pd.DataFrame()
            print('save', len(df))
            
        time.sleep(15)
        
    if df is not None and len(df) != 0:
        add_to_sql(conn, table_name, df)
        
    if len(dfs) != 0:
        for i, d in dfs.items():
            print('saveing df', d.head(), len(d))
            if len(d) != 0:
                print('save df', d.head())
                add_to_sql(conn, i, d)


# In[10]:


def widget(conn, table_name, crawl_func, range_date):

    date_picker_from = widgets.DatePicker(
        description='from',
        disabled=False,
    )
    
    if table_exist(conn, table_name):
        date_picker_from.value = table_latest_date(conn, table_name)
    
    date_picker_to = widgets.DatePicker(
        description='to',
        disabled=False,
    )
    
    date_picker_to.value = datetime.datetime.now().date()

    btn = widgets.Button(description='update ')
    
    def onupdate(x):
        dates = range_date(date_picker_from.value, date_picker_to.value)
        
        if len(dates) == 0:
            print('no data to parse')
            
        update_table(conn, table_name, crawl_func, dates)
    
    btn.on_click(onupdate)

    if table_exist(conn, table_name):
        label = widgets.Label(table_name + 
                              ' (from ' + table_earliest_date(conn, table_name).strftime('%Y-%m-%d') + 
                              ' to ' + table_latest_date(conn, table_name).strftime('%Y-%m-%d') + ')')
    else:
        label = widgets.Label(table_name + ' (No table found)(對於finance_statement是正常情況)')

    items = [date_picker_from, date_picker_to, btn]
    display(widgets.VBox([label, widgets.HBox(items)]))

