# like excel
# DataFrame = N Series with the same index
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

import pandas as pd
s = pd.Series([1,2,3,4])

date = pd.date_range('20180101', periods=4)
s = pd.Series([1,2,3,4], index=date)
s

# look for
s.loc['20180102':'2018-01-04'] # include '2018-01-04'
s.iloc[0:3] # not include s.iloc[3]

# functions
s.max()
s.min()
s.mean()
s.std()
s.cumsum() 
s.cumprod()

# rolling window
s.rolling(2).sum()
s.rolling(2).max()
s.rolling(2).min()
s.rolling(2).mean()
s.rolling(2).std()

s > 3 # True or False

larger_than_3 = s > 3
s.loc[larger_than_3] = s.loc[larger_than_3] + 1
S

# Graph
%matplotlib inline
s.plot()

# Generate a time series and replace 1 values; then plot the graph
date = pd.date_range('2018-01-01', periods=10)
kg_watch = pd.Series(60, index=date)
# Important to have ":" so the chang would apply from the given date till the last date
kg_watch.loc['2018-01-03':] += 5
%matplotlib inline
kg_watch.plot()

