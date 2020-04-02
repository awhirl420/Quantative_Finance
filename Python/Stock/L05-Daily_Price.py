#!/usr/bin/env python
# coding: utf-8

# In[1]:


# EPS = 稅後淨利/在外流通股數
# 本益比(倍) = 股票/EPS = 投入成本/未來每年收益


# In[2]:


# 把json改成csv
# https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20200401&type=ALLBUT0999&_=1585783027241
# https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=20200401&type=ALLBUT0999&_=1585783027241


# In[41]:


import requests

response = requests.get('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=20200401&type=ALLBUT0999&_=1585783027241')
response.text[:1000]


# In[42]:


# 因表格欄位不一致，切割text檔
lines = response.text.split('\n')
lines[100]


# In[23]:


# 用FOR迴圈來檢視是否刪除該ROW
newlines = []

for line in lines:
    if len(line.split('",')) == 17:
        newlines.append(line)
        
newlines[:10]


# In[43]:


"\n".join(newlines)
newlines[:10]


# In[44]:


# 將csv存到pandas的dataframe
import pandas as pd
from io import StringIO

# 去除不必要符號
df = pd.read_csv(StringIO("\n".join(newlines).replace('=','')))
df.head()


# In[40]:


# function
def func(s):
    return s.str.replace(',', '')

df = df.apply(func)
df


# In[45]:


"""
處理資料問題
1.目前都是字串
2.某些數字中間有','
3.Unnamed: 16
"""

# 全部變成字串
df = df.astype(str)
# 拿掉逗號
# input:output
df = df.apply(lambda s:s.str.replace(",", ''))
# 將股票代號設為index
df = df.set_index('證券代號')
df


# In[46]:


df.loc['0050']


# In[48]:


# 轉換成數字
# errors='coerce' 轉換失敗，不要報錯
df = df.apply(lambda s: pd.to_numeric(s, errors='coerce'))
df.head()


# In[56]:


# 刪除整行都是NaN的資料
df = df[df.columns[df.isnull().sum() != len(df)]]
df


# In[58]:


df[df['收盤價']/df['開盤價'] > 1.05]


# In[60]:


# 存成csv檔
df.to_csv('daily_price.csv', encoding='utf_8_sig')


# In[61]:


# 讀取csv檔
df = pd.read_csv('daily_price.csv', index_col=['證券代號'],)
df.head()


# In[62]:


# 刪除沒有收盤價的ROW
df = df.loc[~df['收盤價'].isnull()]
df


# In[63]:


# 存到sqlite3中
import sqlite3
# 跟資料庫溝通的interface
conn = sqlite3.connect('test.sqlite3')
# 存檔
df.to_sql('daily_price', conn, if_exists='replace')


# In[65]:


# 讀取
df = pd.read_sql('select * from daily_price', conn, index_col=['證券代號'])
df.head()


# In[69]:


## 完整的function
import requests
import pandas as pd
from io import StringIO

def crawl_price(date):
    
    # 將date變成字串 ex.'20180525'
    datestr = date.strftime('%Y%m%d')
    
    # 從網站上依照datestr將指定日期的股價抓下來
    r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999&_=1585783027241')
    
    # 刪除'='
    content = r.text.replace('=','')
    
    # 將column數量小於等於10的行數都刪除
    lines = content.split('\n')
    lines = list(filter(lambda l:len(l.split('",')) > 10, lines))
    
    # 將每一行再合成同一行，並用肉眼看不到的換行符號'\n'分開
    content = "\n".join(lines)
    
    # 假如沒下載到，則回傳None
    if content == '':
        return None
    
    # 將content變成檔案：StringIO，並且用pd.read_csv將表格讀取進來
    df = pd.read_csv(StringIO(content))
    
    # 將表格中的元素都換成字串，並將逗號刪除
    df = df.astype(str)
    df = df.apply(lambda s: s.str.replace(',', ''))
    
    # 將爬取的日期存入dataframe
    df['date'] = pd.to_datetime(date)
    
    # 將證券代號的欄位名改成stock_id
    df = df.rename(columns={'證券代號':'stock_id'})
    
    # 將stock_id與date設定成index
    df = df.set_index(['stock_id', 'date'])
    
    # 將所有的表格元素都轉換成數字，error='coerce'的意思是說，假如無法轉換成數字，用NaN取代
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    
    # 刪除不必要的欄位
    df = df[df.columns[df.isnull().all() == False]]
    
    return df


# In[70]:


import datetime
crawl_price(datetime.datetime(2018,1,2))


