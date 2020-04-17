#!/usr/bin/env python
# coding: utf-8

# In[2]:


# ---------------
# 偽裝成瀏覽器
# ---------------
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1) Gecko/2010010' \
    '1 Firefox/4.0.1',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-us,en;q=0.5',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}


# In[3]:


import requests
rs = requests.session()

def get_verify_code(rs):
    res = rs.get('https://bsr.twse.com.tw/bshtm/bsMenu.aspx', headers = headers)
    # 從網頁中抓取一些關鍵字
    import re
    
    # get view state
    viewstate = re.search( 'VIEWSTATE"\s+value=.*=', res.text )
    viewstate = viewstate.group()[18:]
    
    # get eventvalidation
    eventvalidation = re.search( 'EVENTVALIDATION"\s+value=.*\w' , res.text)
    eventvalidation = eventvalidation.group()[24: ]
    
    return viewstate, eventvalidation

viewstate, eventvalidation = get_verify_code(rs)

print('----')
print('viewstate', viewstate)
print('----')
print('eventvalidation',eventvalidation)


# In[4]:


# ---------------
# 爬取資料
# ---------------

def get_data(rs, stock_id, viewstate, eventvalidation):
    import time
    payload = {
    '__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__LASTFOCUS':'',
    '__VIEWSTATE' : viewstate,                      #encode_viewstate[:-1],
    '__EVENTVALIDATION' : eventvalidation,          #encode_eventvalidation[:-1],
    'RadioButton_Normal' : 'RadioButton_Normal',
    'TextBox_Stkno' : stock_id,
    'CaptchaControl1 ' : 'Z67YB',
    'btnOK' : '%E6%9F%A5%E8%A9%A2',
    }
    rs.post( "https://bsr.twse.com.tw/bshtm/bsMenu.aspx", data=payload, headers=headers, stream = True )
    time.sleep(1)
    res = rs.get( 'https://bsr.twse.com.tw/bshtm/bsContent.aspx',verify = False ,stream = True, )
    return res

res = get_data(rs, '1101', viewstate, eventvalidation)
res.encoding='big5'
open('test.html', 'w', encoding='utf-8').write(res.text)


# In[5]:


# ---------------
# 整理資料
# ---------------

import pandas as pd
from io import StringIO

def parse_data(text):
    lines = text.split('\n')
    lines = [l for l in lines if len(l.split(',')) == 11]
    df = pd.read_csv(StringIO('\n'.join(lines)))
    
    first_df = df[df.columns[:5]]
    second_df = df[df.columns[6:]]
    second_df.columns = second_df.columns.str.replace('.1', '')
    final_df = first_df.append(second_df).set_index('序號').sort_index().dropna()
    return final_df

df = parse_data(res.text)


# In[6]:


df


# In[ ]:


# ---------------
# 完整下載範例
# ---------------
import time
import requests
from io import StringIO
import pandas as pd
import datetime

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1) Gecko/2010010' \
    '1 Firefox/4.0.1',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-us,en;q=0.5',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}

def get_data(rs, stock_id, viewstate, eventvalidation):
    import time
    payload = {
    '__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__LASTFOCUS':'',
    '__VIEWSTATE' : viewstate,                      #encode_viewstate[:-1],
    '__EVENTVALIDATION' : eventvalidation,          #encode_eventvalidation[:-1],
    'RadioButton_Normal' : 'RadioButton_Normal',
    'TextBox_Stkno' : stock_id,
    'CaptchaControl1 ' : 'Z67YB',
    'btnOK' : '%E6%9F%A5%E8%A9%A2',
    }
    rs.post( "https://bsr.twse.com.tw/bshtm/bsMenu.aspx", data=payload, headers=headers, stream = True )
    time.sleep(1)
    res = rs.get( 'https://bsr.twse.com.tw/bshtm/bsContent.aspx',verify = False ,stream = True, )
    return res

def get_verify_code(rs):
    res = rs.get('https://bsr.twse.com.tw/bshtm/bsMenu.aspx', headers = headers)
    # 從網頁中抓取一些關鍵字
    import re
    
    # get view state
    viewstate = re.search( 'VIEWSTATE"\s+value=.*=', res.text )
    viewstate = viewstate.group()[18:]
    
    # get eventvalidation
    eventvalidation = re.search( 'EVENTVALIDATION"\s+value=.*\w' , res.text)
    eventvalidation = eventvalidation.group()[24: ]
    
    return viewstate, eventvalidation

def download_stock(stock_id, path):
    rs = requests.Session()
    
    while True:
        try:
            viewstate, eventvalidation = get_verify_code(rs)
            break
        except Exception as e:
            print(e)
            print('無法拿到資料，等 31 sec')
            time.sleep(31)
            continue
    
    time.sleep(2)
    res = get_data(rs, stock_id, viewstate, eventvalidation)
    res.encoding='big5'
    open(path, 'w', encoding='utf-8').writelines(res.text)
    
def stock_list():
    res = requests.get('https://dts.twse.com.tw/opendata/t187ap03_L.csv')
    res.encoding='utf-8'
    df = pd.read_csv(StringIO(res.text), index_col=['公司代號'])
    return df

import os

# build main dir
main_dir = os.path.join('data', 'broker_history')
if not os.path.isdir(main_dir):
    os.mkdir(main_dir)
    
# build date dir
now = datetime.datetime.now()
date_dir = os.path.join(main_dir, now.strftime('%Y%m%d'))
if not os.path.isdir(date_dir):
    os.mkdir(date_dir)
    
slist = stock_list()
for s in slist.index:
    stock_path = os.path.join(date_dir, str(s) + '.csv')
    print(stock_path)
    if not os.path.isfile(stock_path):
        print('downloading...')
        download_stock(str(s), stock_path)
        time.sleep(10)


# In[7]:


# ---------------
# 券商總買賣
# ---------------
buy = df['買進股數'].astype(int).groupby(df['券商']).sum()
sell = df['賣出股數'].astype(int).groupby(df['券商']).sum()
total = buy - sell
total


# In[8]:


# ---------------
# 主力買賣超
# ---------------
total.nlargest(15)


# In[9]:


total.nsmallest(15)


# In[10]:


total.nlargest(15).sum() + total.nsmallest(15).sum()


# In[11]:


# ---------------
# 買賣家數差
# ---------------
(total > 0).sum() - (total < 0).sum()


# In[ ]:




