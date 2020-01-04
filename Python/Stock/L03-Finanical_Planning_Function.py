# define a function in a function
# provide control bars and show the dynamic graph

import pandas as pd
import random
%matplotlib inline

# function
def asset_prediction(
    intitial_amount,
    intitial_age,
    monthly_salary,
    monthly_spenditure,
    monthly_rent,
    retire_age,
    invest_ratio,
    irr,
    house_price,
    endowment,
    buy_house_age,
    borrow_rate,
    borrow_years,):
    
    periods = range(intitial_age, 100)
    annual_nav = pd.Series(0, index=periods)
    annual_nav.iloc[0] = intitial_amount
    annual_nav.loc[:retire_age] += monthly_salary * 12
    annual_nav -= (monthly_spenditure + monthly_rent) * 12
    
    def compound_interest(arr, ratio, return_rate):
        ret = [arr.iloc[0]]
        for v in arr[1:]:
            ret.append(ret[-1] * ratio * (return_rate/100 + 1) + ret[-1] * (1 - ratio) + v)
        return pd.Series(ret, periods)
    
    house_cost = pd.Series(0, index=periods)
    house_cost[buy_house_age] = endowment
    house_cost.loc[buy_house_age:buy_house_age+borrow_years-1] += (house_price - endowment) / borrow_years
    
    borrow_amount = pd.Series(0, index=periods)
    borrow_amount[buy_house_age] = house_price
    borrow_amount = borrow_amount.cumsum()
    borrow_amount = borrow_amount - house_cost.cumsum()
    borrow_interests = borrow_amount.shift().fillna(0) * borrow_rate / 100
    
    annual_rent = pd.Series(monthly_rent * 12, periods)
    annual_rent.loc[buy_house_age:] = 0
    
    annual_nav_house = pd.Series(0, index=periods)
    annual_nav_house.iloc[0] = intitial_amount
    annual_nav_house.loc[:retire_age] += monthly_salary * 12
    annual_nav_house -= (monthly_spenditure*12 + annual_rent + borrow_interests + house_cost)
    
    
    pd.DataFrame({
        'no invest, no house': annual_nav.cumsum(),
        'invest, no house': compound_interest(annual_nav, invest_ratio, irr),
        'no invest, house': annual_nav_house.cumsum(),
        'invest, house': compound_interest(annual_nav, invest_ratio, irr)
        
    }).plot()
    
    
    import matplotlib.pylab as plt
    plt.ylim(0, None)
    
    print('mothly mortgage', (house_price - endowment) / borrow_years / 12)
    print('paid interests', borrow_interests.sum() / borrow_years)
    print('')
    
import ipywidgets as widgets
widgets.interact(asset_prediction,
                intitial_amount=widgets.FloatSlider(min=0, max=100, step=10, value=20),
                intitial_age=widgets.IntSlider(min=0, max=100, step=1, value=30),
                monthly_salary=widgets.FloatSlider(min=0, max=20, step=0.1, value=3),
                monthly_spenditure=widgets.FloatSlider(min=0, max=20, step=0.2, value=1),
                monthly_rent=widgets.FloatSlider(min=0, max=20, step=0.5, value=1),
                retire_age=widgets.IntSlider(min=0, max=100, step=1, value=60),
                invest_ratio=widgets.FloatSlider(min=0, max=1, step=0.1, value=0.7),
                irr=widgets.FloatSlider(min=0, max=20, step=0.5, value=5),
                house_price=widgets.IntSlider(min=100, max=2000, step=50, value=300),
                endowment=widgets.IntSlider(min=100, max=2000, step=50, value=100),
                buy_house_age=widgets.IntSlider(min=20, max=100, step=1, value=40),
                borrow_rate=widgets.FloatSlider(min=1, max=5, step=0.1, value=2.4),
                borrow_years=widgets.IntSlider(min=0, max=40, step=1, value=20)
)

