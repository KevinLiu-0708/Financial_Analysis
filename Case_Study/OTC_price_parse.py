import requests
import pandas as pd
import time
import json
from datetime import datetime
import plotly.io as pio


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}


from_year = int(input('from_year: '))
from_month = input('from_month: ')

to_year = datetime.today().year - 1911
to_month = datetime.today().month

if to_month < 10:
    to_month = '0' + str(to_month)
else:
    str(to_month) 
    
stock_id = input('stock_id: ')

stock_price = pd.DataFrame()

month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
for year in range(from_year, to_year+1):
    for i in range(len(month_list)):
        if year == int(from_year) and i < month_list.index(from_month):
            continue
        if year == int(to_year) and i > month_list.index(to_month):
            continue
        else:
            date = str(year) + '/' + month_list[i]
            print(date)
            url = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d={}&stkno={}&_=1652254993105'.format(date, stock_id)
    
            res = requests.get(url, headers=headers, verify=False)
            
            table = json.loads(res.text)
            df= pd.DataFrame(table['aaData'])
            
            stock_price = pd.concat([stock_price, df])
            time.sleep(3)


column_list = ['Date', '成交張數', '成交金額', 'Open', 'High', 'Low', 'Close', '漲跌', '筆數']
stock_price.columns = column_list
stock_price = stock_price.set_index('Date')

stock_price = stock_price[['成交張數', 'Open', 'High', 'Low', 'Close', '筆數']]

stock_price = stock_price.replace(',', '', regex=True)
stock_price = stock_price.astype(float)

stock_price.to_excel('C:/Users/111036/Desktop/股價/3498.xlsx')


pio.renderers.default='svg'

'''
import plotly.graph_objects as go
fig1 = go.Figure(data=[go.Candlestick(x=stock_price.index,
                open=stock_price['Open'],
                high=stock_price['High'],
                low=stock_price['Low'],
                close=stock_price['Close'])])
'''
import plotly.express as px
fig = px.line(stock_price, x=stock_price.index, y='Close')
fig.show()
