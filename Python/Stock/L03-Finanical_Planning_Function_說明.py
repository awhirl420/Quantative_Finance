#!/usr/bin/env python
# coding: utf-8

# In[5]:


# 環境設定
import pandas as pd
import random
get_ipython().run_line_magic('matplotlib', 'inline')

# 總資產函數
def asset_prediction(起始資金, 起始年紀,
                     每月薪水,
                     每月開銷,
                     每月房租,
                     退休年齡,
                     投資部位,
                     投資年利率,
                     買房價格,
                     買房頭期款,
                     買房年紀,
                     房貸利率,
                     貸款年數,):
    # 創立淨額序列
    預測時段 = range(起始年紀, 100)
    每年淨額 = pd.Series(0, index=預測時段)
    每年淨額.iloc[0] = 起始資金
    每年淨額.loc[:退休年齡] += 每月薪水 * 12
    每年淨額 -= (每月開銷 + 每月房租) * 12
    
    # 投資函數
    def compound_interest(arr, ratio, return_rate):
        ret = [arr.iloc[0]]
        for v in arr[1:]:
            ret.append(ret[-1] * ratio * (return_rate/100 + 1) + ret[-1] * (1 - ratio) + v)
        return pd.Series(ret, 預測時段)
    
    # 每年買房實際花費
    買房花費 = pd.Series(0, index=預測時段)
    買房花費[買房年紀] = 買房頭期款
    買房花費.loc[買房年紀:買房年紀+貸款年數-1] += (買房價格 - 買房頭期款) / 貸款年數
    
    # 累積欠款
    欠款 = pd.Series(0, index=預測時段)
    欠款[買房年紀] = 買房價格
    欠款 = 欠款.cumsum()
    欠款 = 欠款 - 買房花費.cumsum()
    利息 = 欠款.shift().fillna(0) * 房貸利率 / 100
    
    # 房租
    房租年繳 = pd.Series(每月房租*12, index=預測時段)
    房租年繳.loc[買房年紀:] = 0
    
    # 有買房的每年淨額
    每年淨額_買房 = pd.Series(0, index=預測時段)
    每年淨額_買房.iloc[0] = 起始資金
    每年淨額_買房.loc[:退休年齡] += 每月薪水 * 12
    每年淨額_買房 -= (每月開銷*12 + 房租年繳 + 利息 + 買房花費)
    
    # 製作放入四種狀況的DataFrame
    pd.DataFrame({
        'no invest, no house': 每年淨額.cumsum(),
        'invest, no house': compound_interest(每年淨額, 投資部位, 投資年利率),
        'no inevest, house': 每年淨額_買房.cumsum(),
        'invest, house': compound_interest(每年淨額_買房, 投資部位, 投資年利率),
    }).plot()
    
# GUI控制參數
import ipywidgets as widgets
widgets.interact(asset_prediction,
                起始資金=widgets.FloatSlider(min=0, max=100, step=10, value=20),
                起始年紀=widgets.IntSlider(min=0, max=100, step=1, value=30),
                每月薪水=widgets.FloatSlider(min=0, max=20, step=0.1, value=3),
                每月開銷=widgets.FloatSlider(min=0, max=20, step=0.2, value=1),
                每月房租=widgets.FloatSlider(min=0, max=20, step=0.5, value=1),
                退休年齡=widgets.IntSlider(min=0, max=100, step=1, value=60),
                投資部位=widgets.FloatSlider(min=0, max=1, step=0.1, value=0.7),
                投資年利率=widgets.FloatSlider(min=0, max=20, step=0.5, value=5),
                買房價格=widgets.IntSlider(min=100, max=2000, step=50, value=300),
                買房頭期款=widgets.IntSlider(min=100, max=2000, step=50, value=100),
                買房年紀=widgets.IntSlider(min=20, max=100, step=1, value=40),
                房貸利率=widgets.FloatSlider(min=1, max=5, step=0.1, value=2.4),
                貸款年數=widgets.IntSlider(min=0, max=40, step=1, value=20)
                )



