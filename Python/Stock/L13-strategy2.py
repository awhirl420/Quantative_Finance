#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
# 將累積數字轉換成單季數字

def toSeasonal(df):
    season4 = df[df.index.month == 3]
    season1 = df[df.index.month == 5]
    season2 = df[df.index.month == 8]
    season3 = df[df.index.month == 11]
    
    season1.index = season1.index.year
    season2.index = season2.index.year
    season3.index = season3.index.year
    season4.index = season4.index.year
    
    newseason1 = season1
    newseason2 = season2 - season1.reindex_like(season2)
    newseason3 = season3 - season2.reindex_like(season3)
    newseason4 = season4 - season3.reindex_like(season4)
    
    newseason1.index = pd.to_datetime(newseason1.index.astype(str) + '-05-15')
    newseason2.index = pd.to_datetime(newseason2.index.astype(str) + '-08-14')
    newseason3.index = pd.to_datetime(newseason3.index.astype(str) + '-11-14')
    newseason4.index = pd.to_datetime((newseason4.index + 1).astype(str) + '-03-31')
    
    return newseason1.append(newseason2).append(newseason3).append(newseason4).sort_index()


# In[2]:


from finlab.data import Data
data = Data() 

# 策略
def mystrategy(data):
    股本 = data.get('股本合計', 1)
    price = data.get('收盤價', 200)
    當天股價 = price[:股本.index[-1]].iloc[-1]
    當天股本 = 股本.iloc[-1]
    市值 = 當天股本 * 當天股價 / 10 * 1000
    
    df1 = toSeasonal(data.get('投資活動之淨現金流入（流出）', 5))
    df2 = toSeasonal(data.get('營業活動之淨現金流入（流出）', 5))
    自由現金流 = (df1 + df2).iloc[-4:].mean()
    
    稅後淨利 = data.get('本期淨利（淨損）', 1)
    
    # 股東權益有兩個名稱
    權益總計 = data.get('權益總計', 1)
    權益總額 = data.get('權益總額', 1)
    
    # 把它們合起來
    權益總計.fillna(權益總額, inplace=True)
    
    股東權益報酬率 = 稅後淨利.iloc[-1] / 權益總計.iloc[-1]
    
    
    營業利益 = data.get('營業利益（損失）', 5)
    營業利益成長率 = (營業利益.iloc[-1] / 營業利益.iloc[-5] - 1) * 100
    
    當月營收 = data.get('當月營收', 4) * 1000
    當季營收 = 當月營收.iloc[-4:].sum()
    市值營收比 = 市值 / 當季營收
    
    condition1 = (市值 < 10000000000)
    condition2 = 自由現金流 > 0
    condition3 = 股東權益報酬率 > 0
    condition4 = 營業利益成長率 > 0
    condition5 = 市值營收比 < 5
    
    select_stock = condition1 & condition2 & condition3 & condition4 & condition5
    
    return select_stock[select_stock]


# In[3]:


from finlab.backtest import backtest
from finlab.data import Data
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')

data = Data()
backtest(datetime.date(2014,8,1), datetime.date(2019,5,25), 60, mystrategy, data)


# In[4]:


# 策略2
def mystrategy2(data):
    股本 = data.get('股本合計', 1)
    price = data.get('收盤價', 200)
    當天股價 = price[:股本.index[-1]].iloc[-1]
    當天股本 = 股本.iloc[-1]
    市值 = 當天股本 * 當天股價 / 10 * 1000
    
    df1 = toSeasonal(data.get('投資活動之淨現金流入（流出）', 5))
    df2 = toSeasonal(data.get('營業活動之淨現金流入（流出）', 5))
    自由現金流 = (df1 + df2).iloc[-4:].mean()
    
    稅後淨利 = data.get('本期淨利（淨損）', 1)
    
    # 股東權益有兩個名稱
    權益總計 = data.get('權益總計', 1)
    權益總額 = data.get('權益總額', 1)
    
    # 把它們合起來
    權益總計.fillna(權益總額, inplace=True)
    
    股東權益報酬率 = 稅後淨利.iloc[-1] / 權益總計.iloc[-1]
    
    
    營業利益 = data.get('營業利益（損失）', 5)
    營業利益成長率 = (營業利益.iloc[-1] / 營業利益.iloc[-5] - 1) * 100
    
    當月營收 = data.get('當月營收', 4) * 1000
    當季營收 = 當月營收.iloc[-4:].sum()
    市值營收比 = 市值 / 當季營收
    
    rsv = (price.iloc[-1] - price.iloc[-150:].min()) / (price.iloc[-150:].max() - price.iloc[-150:].min())
    
    condition1 = (市值 < 10000000000)
    condition2 = 自由現金流 > 0
    condition3 = 股東權益報酬率 > 0
    condition4 = 營業利益成長率 > 0
    condition5 = 市值營收比 < 5
    condition6 = rsv > 0.5
    
    select_stock = condition1 & condition2 & condition3 & condition4 & condition5 & condition6
    
    return select_stock[select_stock]


# In[5]:


from finlab.backtest import backtest
from finlab.data import Data
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')

data = Data()
backtest(datetime.date(2014,8,1), datetime.date(2019,5,25), 60, mystrategy2, data)


# In[6]:


# 策略3
def mystrategy3(data):
    股本 = data.get('股本合計', 1)
    price = data.get('收盤價', 200)
    當天股價 = price[:股本.index[-1]].iloc[-1]
    當天股本 = 股本.iloc[-1]
    市值 = 當天股本 * 當天股價 / 10 * 1000
    
    df1 = toSeasonal(data.get('投資活動之淨現金流入（流出）', 5))
    df2 = toSeasonal(data.get('營業活動之淨現金流入（流出）', 5))
    自由現金流 = (df1 + df2).iloc[-4:].mean()
    
    稅後淨利 = data.get('本期淨利（淨損）', 1)
    
    # 股東權益有兩個名稱
    權益總計 = data.get('權益總計', 1)
    權益總額 = data.get('權益總額', 1)
    
    # 把它們合起來
    權益總計.fillna(權益總額, inplace=True)
    
    股東權益報酬率 = 稅後淨利.iloc[-1] / 權益總計.iloc[-1]
    
    # 新淨值股價比
    股數 = data.get('普通股股本', 1) / 10
    每股淨值 = 權益總計.iloc[-1] / 股數.iloc[-1]
    新淨值股價比 = 每股淨值 / price.iloc[-1]
    
    # 新益本比
    每股盈餘 = data.get('基本每股盈餘合計', 1)
    新益本比 = 每股盈餘.iloc[-1] / price.iloc[-1]

    rsv = (price.iloc[-1] - price.iloc[-150:].min()) / (price.iloc[-150:].max() - price.iloc[-150:].min())
    
    condition1 = (市值 < 10000000000)
    condition2 = 自由現金流 > 0
    condition3 = 股東權益報酬率 > 0
    condition4 = 新淨值股價比.rank(pct=True) > 0.75
    condition5 = 新益本比.rank(pct=True) > 0.75
    condition6 = rsv > 0.5
    
    select_stock = condition1 & condition2 & condition3 & condition4 & condition5 & condition6
    
    return select_stock[select_stock]


# In[7]:


from finlab.backtest import backtest
from finlab.data import Data
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')

data = Data()
backtest(datetime.date(2014,8,1), datetime.date(2020,2,1), 60, mystrategy3, data)


# In[ ]:




