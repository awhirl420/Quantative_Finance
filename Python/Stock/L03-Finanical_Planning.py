# Parameters
initial_amount = 30
monthly_salary = 3
monthly_spenditure = 1
monthly_rent = 1
retire_age = 70
periods = range(25, 90, 1)

# scenario 1
######## NAV
import pandas as pd
nav = pd.Series(0, index=periods)
nav.iloc[0] = initial_amount
nav.loc[:retire_age] += monthly_salary * 12
nav -= (monthly_spenditure + monthly_rent) * 12
%matplotlib inline
nav.plot()

######## Total Assets
asset = nav.cumsum()
asset.plot()

# scenario 2
# invest_amount = account_value * invest_ratio
# beginning of a year: account_value = account_value - invest_amount
# end of a year: account_value += invest_amount * irr

invest_ratio = 0.7
irr = 5

def compound_interest(arr, ratio, return_rate):
    ret = [arr.iloc[0]]
    for v in arr[1:]:
        ret.append(ret[-1] * ratio * (1 + return_rate / 100) + ret[-1] * (1 - ratio) + v)
    return pd.Series(ret, periods)

invest_asset = compound_interest(nav, invest_ratio, irr)
invest_asset.plot()
asset.plot()

# scenario 3
house_price = 300
endowment = 100
buy_house_age = 35
borrow_rate = 3
borrow_years = 20

house_cost = pd.Series(0, index=periods)
house_cost[buy_house_age] = endowment
house_cost.loc[buy_house_age:buy_house_age+borrow_years-1] += (house_price - endowment) / borrow_years
house_cost.plot()

###### borrow interests
borrow_amount = pd.Series(0, periods)
borrow_amount[buy_house_age] = house_price
borrow_amount = borrow_amount.cumsum()
borrow_amount = borrow_amount - house_cost.cumsum()
borrow_amount.plot()

borrow_interests = borrow_amount.shift().fillna(0) * borrow_rate / 100
borrow_interests.plot(secondary_y=True)

###### rent
annual_rent = pd.Series(monthly_rent*12, periods)
annual_rent.loc[buy_house_age:] = 0
annual_rent.plot()

###### nav_house
nav_house = pd.Series(0, periods)
nav_house.iloc[0] = initial_amount
nav_house.loc[:retire_age] += monthly_salary * 12
nav_house -= (monthly_spenditure * 12 + annual_rent + borrow_interests + house_cost)
nav_house.cumsum().plot() #account value without investment

# scenario 4
invest_house_asset = compound_interest(nav_house, invest_ratio, irr)

asset.plot(color='black')
invest_asset.plot(color='green')
invest_house_asset.plot(color='blue')
nav_house.cumsum().plot(color='red')
