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
# Important to have ":" as the effective date
kg_watch.loc['2018-01-03':] += 5
%matplotlib inline
kg_watch.plot()

############# DataFrame
date = pd.date_range('20180101', periods=4)

s1 = pd.Series([1,2,3,4], index=date)
s2 = pd.Series([7,8,9,10], index=date)
s3 = pd.Series([11,12,8,2], index=date)

dictionary = {
    'c1': s1,
    'c2': s2,
    'c3': s3,
}

df = pd.DataFrame(dictionary)
df

%matplotlib inline
df.plot()

# get sepecific data
df.loc['2018-01-02':'2018-01-04',['c1', 'c2']]
df.iloc[0:2,[0, 2]]
df['c3']

print(df)
df.cumprod(axis=0) # cumulative product by rows
df.cumprod(axis=1) # cumulative product by columns
df.drop('c2', axis=1)
