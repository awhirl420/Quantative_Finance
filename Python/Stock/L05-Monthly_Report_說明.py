#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
import pandas as pd
from io import StringIO

# 讀取資料
url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_106_1_0.html'
r = requests.get(url)
r.encoding = 'big5'
dfs = pd.read_html(StringIO(r.text))


# In[31]:


# check pandas版本
pd.__version__


# In[52]:


# 將dfs中，row長度介於5~11的table合併(這才是我們需要的table)
df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])

# 使用 concat 合併 axis=0 為直向合併
# res = pd.concat([df1,df2,df3],axis=0)

# 建立一個3×3的單位矩陣e, e.shape為（3，3），表示3行3列,第一維的長度為3，第二維的長度也為3

# 設定column名稱
# get_level_values(0)，可以得到第0 index的資料
df.columns = df.columns.get_level_values(1)

# 將df中的當月營收用 .to_numeric變成數字，再把其中不能變成數字的部分以NaN取代(errors='coerce')
df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')

# 再把當月營收中，出現NaN的row用.dropna整行刪除
df = df[~df['當月營收'].isnull()]

# 刪除公司代號中出現合計的行數
df = df[df['公司代號'] != '合計']

# 將公司代號與公司名稱共同列為df的indexes
df = df.set_index(['公司代號','公司名稱'])

df.head()


# In[54]:


# 存檔 csv
df.to_csv('test.csv', encoding='utf_8_sig')

# 讀取 csv
df = pd.read_csv('test.csv', index_col=['公司代號','公司名稱'])
df.head()


# In[55]:


# 存檔 sqlite3
import sqlite3

conn = sqlite3.connect('test.sqlite3')
df.to_sql('monthly_report', conn, if_exists='replace')

# 讀取 sqlite3
df = pd.read_sql('select * from monthly_report', conn, index_col=['公司代號','公司名稱'])
df.head()
