import baostock as bs
import pandas as pd
import datetime

import csv
from mypublic import *



#market = input("请输入交易市场(sh/sz,默认sh):")
market = ''
if len(market) == 0:
    market = 'sh'

#code = input("请输入股票代码:")
code = ''
if len(code) == 0:
    code = '601375'

#strenddate = input("请输入开始日期(格式:1900-01-01):")
strenddate = ''
if len(strenddate) == 0:
    enddate = datetime.date.today()  + datetime.timedelta(days = -1)
else:
    enddate = datetime.datetime.strptime(strenddate,'%Y-%m-%d')

startdate = enddate + datetime.timedelta(days = -365*2+1)

datafilename = "D:/csv/"+code+"-"+startdate.strftime( '%Y-%m-%d' )+".csv"
save_stock_k_data_from_baostock(startdate,enddate,code,datafilename,market='sh')
print(startdate)
print(enddate)


for i in range(1,80):
    for j in range(i+10,100):
        print('规则：涨%d个点卖,跌%d个点买' % (i,j))
        simulate_detail_from_csv(datafilename,1+i/1000,1-j/1000)


"""
datafilename = "D:/csv/"+code+"-"+startdate.strftime( '%Y-%m-%d' )+".csv"
save_stock_k_data_from_baostock(startdate,enddate,code,datafilename,market='sh')
print(code)
simulate_detail_from_csv(datafilename,1+3/100,1-7/100)


i = 0
for i in range(0,30):
    strTemp = '%d' % i
    code = '600' + strTemp.rjust(3,'0')
    
    datafilename = "D:/csv/"+code+"-"+startdate.strftime( '%Y-%m-%d' )+".csv"
    save_stock_k_data_from_baostock(startdate,enddate,code,datafilename,market='sh')
    print(code)
    simulate_detail_from_csv(datafilename,1+3/100,1-4/100)



"""