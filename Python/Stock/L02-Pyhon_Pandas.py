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




