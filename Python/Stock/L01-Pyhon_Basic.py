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


########## String
# use 3 " for line breaks
s = """hello
world"""
print(s)

s = 'hello world'
# show the first word
s[0]
# shoe the lst word
s[-1]
# count how many the word
s.count('l')
# find the index of the word
s.find('o')

s + s

b = "HI"
b = b.replace('I', 'A')


########## List
# show [4, 5, 'i am string']
li = [1, 4, 5, 'i am string', True]
li[1:4]
# add the new element as the last one
li.append(100)
# average income
average_income = sum(income)/len(income)

########## Dictionary
score = {'Sam': 90, 'Mike': 95}
score['Claire'] = 95
print(score)
score['Sam']
score.keys()
score.values()

a ** b # a^b

########## Function
def sub(x,y):
    z = x - y
    return z

a = sub(5,3)
print(a)

def calculate_earning(buy_price, sell_price, amount=1):
    fee_ratio = 1.425 / 1000
    tax_ratio = 3 / 1000
    ret = (sell_price - buy_price) * amount * 1000 * (1 - fee_ratio - tax_ratio)
    return ret

value = calculate_earning(30, 40, 2)
print(value)

########## Package
import datetime
datetime.datetime(1991,1,1,4,34)
datetime.datetime.now()


########## if statements
buy_price = 25
sell_price = 30

if buy_price < sell_price:
    print('make money')
elif buy_price == sell_price:
    print('break even')
else:
    print('lose money')  

    
########## for loop    
for i in [1,2,3,4]:
    print(i)

print('-------------')

for i in range(0, 4):
    print(i)

    
########## while loop   
for i in range(0, 5):
    print(i)
    
print('-------------')

i = 0
while i < 5:
    print(i)
    i = i + 1


