# take TW stock market as example
# Fee: stock price* fee rate(1.425/1000)* (1-discount off) for buy/sell
# Tax: stock price* tax rate(3/1000) for sell
# Board lot: 1000 shares

# Variable Name
account = 1000000
stock_price = 50
buy_amount = 1
fee_ratio	= 1.425/1000
tax_ratio = 3/1000
stock_value = stock_price * buy_amount * 1000

# Buy stock, and then sell the stock when price raise 40%
account = account - stock_value * (1 + fee_ratio)
stock_price = stock_price * 1.4
stock_value = stock_price * buy_amount * 1000
account = account + stock_value * (1 - fee_ratio - tax_ratio)


