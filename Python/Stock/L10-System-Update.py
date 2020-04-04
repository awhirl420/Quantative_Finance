#!/usr/bin/env python
# coding: utf-8

# In[1]:


from finlab.crawler import(
    widget, crawl_price, crawl_monthly_report, crawl_finance_statement_by_date,
    date_range, month_range, season_range
)

import sqlite3
import os
conn = sqlite3.connect(os.path.join('data', "data.db"))

widget(conn, 'price', crawl_price, date_range)
widget(conn, 'monthly_revenue', crawl_monthly_report, month_range)
widget(conn, 'finance_statement', crawl_finance_statement_by_date, season_range)


# In[2]:


"""
每季財報 時間區間補充：

2010年3月31號 --> 2009 第四季
2010年5月15號 --> 2010 第一季
2010年8月14號 --> 2010 第二季
2010年11月14號 --> 2010 第三季
"""


# In[4]:


import datetime
print('2010年抓取財報的時間點是')
season_range(datetime.date(2010,1,1), datetime.date(2011,1,1))


# In[7]:


# 程式化更新資料
import datetime
from finlab.crawler import update_table
#update_table(conn, 'price', crawl_price, [datetime.date(2018,3,26)])
#update_table(conn, 'monthly_revenue', crawl_monthly_report, [datetime.date(2018,3,1)])
#update_table(conn, 'finance_statement', crawl_finance_statement_by_date, [datetime.date(2018,3,31)])
