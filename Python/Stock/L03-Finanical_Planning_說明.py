#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Financial Planning
起始資金 = 30
每月薪水 = 3
每月開銷 = 1 # 不含房租
每月房租 = 1
退休年齡 = 65
預測時段 = range(25, 90, 1)


# In[8]:


import pandas as pd

# 每年淨額
每年淨額 = pd.Series(0, index=預測時段)
每年淨額.iloc[0] = 起始資金
每年淨額.loc[:退休年齡] += 每月薪水 * 12
每年淨額 -= (每月開銷 + 每月房租) * 12

get_ipython().run_line_magic('matplotlib', 'inline')
每年淨額.plot()


# In[11]:


"""
沒有投資的總資產變化情況
"""

無投資總資產 = 每年淨額.cumsum()
無投資總資產.plot()


# In[14]:


"""
有投資的總資產變化情況
"""
投資部位 = 0.7
投資年利率 = 0.05

def compound_interest(arr, ratio, return_rate):
    ret = [arr.iloc[0]]
    for v in arr[1:]:
        ret.append(ret[-1] * ratio * (1 + return_rate) + ret[-1] * (1 - ratio) + v)
    return pd.Series(ret, 預測時段)

投資總資產 = compound_interest(每年淨額, 投資部位, 投資年利率)
投資總資產.plot()
無投資總資產.plot()


# In[15]:


"""
考慮買房的話
"""

買房價格 = 300
買房頭期款 = 100
買房年紀 = 35
房貸利率 = 3
貸款年數 = 20


# In[17]:


買房花費 = pd.Series(0, index=預測時段)
買房花費[買房年紀] = 買房頭期款
買房花費.loc[買房年紀:買房年紀+貸款年數-1] += (買房價格 - 買房頭期款) / 貸款年數
買房花費.plot()


# In[25]:


"""
計算貸款的利息
"""
# 先計算有多少欠款
欠款 = pd.Series(0, index=預測時段)
欠款[買房年紀] = 買房價格
欠款 = 欠款.cumsum()
欠款 = 欠款 - 買房花費.cumsum()
get_ipython().run_line_magic('matplotlib', 'inline')
欠款.plot()


# In[26]:


# 欠款.shift(): 去年欠款
利息 = 欠款.shift().fillna(0) * 房貸利率 / 100
get_ipython().run_line_magic('matplotlib', 'inline')
利息.plot()


# In[28]:


"""
計算繳房租
"""
房租年繳 = pd.Series(每月房租*12, index=預測時段)
房租年繳.loc[買房年紀:] = 0
房租年繳.plot()


# In[34]:


# 每年淨額與存款無關
每年淨額_買房 = pd.Series(0, index=預測時段)
每年淨額_買房.iloc[0] = 起始資金
每年淨額_買房.loc[:退休年齡] += 每月薪水 * 12
每年淨額_買房 -= (每月開銷*12 + 房租年繳 + 利息 + 買房花費)
每年淨額_買房.cumsum().plot()


# In[37]:


投資_買房_總資產 = compound_interest(每年淨額_買房, 投資部位, 投資年利率)

# 四個狀況比較
投資總資產.plot(color='green')
投資_買房_總資產.plot(color='blue')
每年淨額_買房.cumsum().plot(color='red')
無投資總資產.plot(color='black')

