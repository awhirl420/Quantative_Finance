#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 潛在成長股

# 條件一
# 市值：發行股票的總價值，發行股數 x 股價
# 市值>100億

# 條件二
# 自由現金流量 = 營業現金收入 - 投資現金收入

# 條件三
# 營業利率成長率 = (當期的營業利益-去年同期的營業利益)/去年同期的營業利益 x 100%

# 條件四
# 股東權益報酬率 = 本期淨利 / 股東權益
# 用多少錢，賺多少錢
# 缺點：
#   1.每季更新，太慢
#   2.沒有考慮股價

# 條件五
# 市值營收比 PSR < k
# 市值營收比 = 市值/月營收


# In[2]:


from finlab.data import Data
data = Data()


# In[12]:


股本 = data.get('股本合計', 1)
price = data.get('收盤價', 1000)
price.head()


# In[20]:


當天股價 = price[:股本.index[-1]].iloc[-1]
當天股本 = 股本.iloc[-1]

# 市值 = 總股數 * 股價
#      = (股本 * 1000) / 10 * 股價

市值 = 當天股本 * 1000 / 10 * 當天股價
市值['1101']


# In[32]:


import pandas as pd

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
    
    return newseason1.append(newseason2).append(newseason3).append(newseason4).sort_index()

投資現金流量 = toSeasonal(data.get('投資活動之淨現金流入（流出）', 8))
營業現金流量 = toSeasonal(data.get('營業活動之淨現金流入（流出）', 8))
自由現金流量 = (投資現金流 + 營業現金流).iloc[-4:].sum()
自由現金流量.describe()


# In[26]:


稅後淨利 = data.get('本期淨利（淨損）', 1)
權益總計 = data.get('權益總計', 1)

股東權益報酬率 = 稅後淨利.iloc[-1] / 權益總計.iloc[-1]
股東權益報酬率.describe()


# In[27]:


營業利益 = data.get('營業利益（損失）', 4)
營業利益成長率 = (營業利益.iloc[-1] / 營業利益.iloc[-4] - 1) * 100
營業利益成長率.describe()


# In[29]:


get_ipython().run_line_magic('matplotlib', 'inline')
當月營收 = data.get('當月營收', 5) * 1000
每季營收 = 當月營收.iloc[-4:].sum()
市值營收比 = 市值 / 每季營收
市值營收比.describe()


# In[33]:


condition1 = (市值 < 10000000000)
condition2 = 自由現金流量 > 0
condition3 = 股東權益報酬率 > 0
condition4 = 營業利益成長率 > 0
condition5 = 市值營收比 < 5
select_stock = condition1 & condition2 & condition3 & condition4 & condition5

select_stock[select_stock]


# In[40]:


# 綜合上述，寫成函數

import pandas as pd

from finlab.data import Data
data = Data()

def mystrategy(data):
    
    股本 = data.get('股本合計', 1)
    price = data.get('收盤價', 120)
    當天股價 = price[:股本.index[-1]].iloc[-1]
    當天股本 = 股本.iloc[-1]
    市值 = 當天股本 * 當天股價 / 10 * 1000
    
    df1 = toSeasonal(data.get('投資活動之淨現金流入（流出）', 5))
    df2 = toSeasonal(data.get('投資活動之淨現金流入（流出）', 5))
    自由現金流 = (df1 + df2).iloc[-4:].mean()
    
    稅後淨利 = data.get('本期淨利（淨損）', 1)
    
    # 股東權益有兩個名稱
    權益總計 = data.get('權益總計', 1)
    權益總額 = data.get('權益總額', 1)
    
    # 把它們合併起來
    權益總計.fillna(權益總額, inplace=True)
    
    股東權益報酬率 = 稅後淨利.iloc[-1] / 權益總計.iloc[-1]
    
    營業利益 = data.get('營業利益（損失）', 5)
    營業利益成長率 = (營業利益.iloc[-1] / 營業利益.iloc[-5] - 1) * 100
    
    當月營收 = data.get('當月營收', 4) * 1000
    當季營收 = 當月營收.iloc[-4:].sum()
    市值營收比 = 市值 / 當季營收
    
    condition1 = (市值 < 10000000000) #100億
    condition2 = 自由現金流 > 0
    condition3 = 股東權益報酬率 > 0
    condition4 = 營業利益成長率 > 0
    condition5 = 市值營收比 < 5
    
    select_stock = condition1 & condition2 & condition3 & condition4 & condition5
    
    return select_stock[select_stock]


# In[41]:


from finlab.backtest import backtest
from finlab.data import Data
import datetime

get_ipython().run_line_magic('matplotlib', 'inline')
data = Data()
backtest(datetime.date(2017,1,1), datetime.date(2018,3,10), 60, mystrategy, data)

