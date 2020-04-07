#!/usr/bin/env python
# coding: utf-8

# In[3]:


# 股價淨值比 = 股價/每股淨值 < 1 -> 便宜
# 大部分企業股價淨值比>1，因為企業不是單純的資產，企業會獲利、會成長！


# In[2]:


from finlab.data import Data
data = Data()


# In[20]:


price = data.get('收盤價', 1000)
price.head()

# 股價淨值比 = 股價 / 每股淨值
# 每股淨值 = 股東權益 / 流通股數
# 流通股數 = 股本 / 10

股東權益 = data.get('歸屬於母公司業主之權益合計', 1)
股本 = data.get('普通股股本', 1)


# In[21]:


pb = price.iloc[-1] / (股東權益 / (股本 / 10))
pb.transpose().dropna()


# In[22]:


# 將股價淨值比寫成function
def 股價淨值比(n):
    
    股東權益 = data.get('歸屬於母公司業主之權益合計', n)
    股本 = data.get('普通股股本', n)
    price = data.get('收盤價', 100*n)
    return price.reindex(股本.index, method='ffill')/(股東權益 / 股本)/10

pb = 股價淨值比(4).dropna(axis=1)
pb.head()


# In[23]:


get_ipython().run_line_magic('matplotlib', 'inline')
pb.iloc[0].hist(bins=[i/10 for i in range(40)])


# In[31]:


import pandas as pd
pb.index[0]
gain = price.iloc[-1]/price.loc[pb.index[0]]
# 只選上市公司股票
gain = gain[pb.columns]
gain

gain[pb.iloc[0] < 0.5].mean()


# In[33]:


pb.iloc[0]


# In[34]:


pb.columns


# In[37]:


price[pb.columns[pb.iloc[0] < 0.5]][pb.index[0]:].mean(axis=1).plot()


# In[39]:


price[pb.columns[pb.iloc[0] > 3]][pb.index[0]:].mean(axis=1).plot()


# In[71]:


# 將股價淨值比包裝成 function直接使用
def 新股價淨值比(n):
    
    新股東權益 = data.get('歸屬於母公司業主之權益合計', n)
    新股本 = data.get('普通股股本', n)
    price = data.get('收盤價', 1000*n)
    
    return price.reindex(新股本.index, method='ffill')/(新股東權益/新股本)/10

股價淨值比pb = 新股價淨值比(4)


# In[72]:


# 畫圖的起手式
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# 找出最後一筆股價淨值比（第一條row）
起始股價淨值比pb = 股價淨值比pb.iloc[0]

# 畫出 histogram 分佈圖
起始股價淨值比pb.hist(bins=1000)

plt.xlim(0,5)

# X軸為股價淨值比，Y軸為股票的數量


# In[73]:


import pandas as pd

結束股價 = price.iloc[-1] # 最後一筆股價
起始股價 = price.loc[股價淨值比pb.index[0]] # 淨值比公佈當天

起始股價淨值比 = 股價淨值比pb.iloc[0]

獲利 = (結束股價/起始股價 - 1) * 100

print('買入股價淨值比小於0.5的股票，與其獲利(%)：')
獲利[起始股價淨值比 < 0.5]


# In[74]:


# 條件
condition = (起始股價淨值比 < 0.5)

# 選出符合條件的股票
stocks = condition[condition].index

# 印出股票和其股價
stocks_price = price[stocks]
stocks_price.head()


# In[75]:


# 設定起始時間：我們看到 股價淨值比 的當下
start_time = 股價淨值比pb.index[0]

# 設定結束時間：我們股價最後一筆
end_time = price.index[-1]

# 將 stocks_price 的股價，選出時間段（start_time ~ end_time），將每天股票平均，並畫出來，當作是買入一籃子股票（類似於每檔買一張）
stocks_price.loc[start_time:end_time].mean(axis=1).plot()

# 跟上面一樣，但是將資產平均分散買入
#stock_price = stocks_price.loc[start_time:end_time]
#(stock_price/stock_price.iloc[0]).mean(axis=1).plot()


# In[ ]:
