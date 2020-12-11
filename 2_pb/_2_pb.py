import pandas as pd
import datetime
import json
import os
import csv
import math
from myfunction import *



market = ''
code = ''
strenddate = ''

#market = input("请输入交易市场(sh/sz,默认sh):")
#if len(market) == 0:
market = 'sh'

#工商银行，中信证券，中国石化，保利地产
#codelist = ['601398','600030','600028','600048']code = input("请输入股票代码:")
#code  = input("请输入证券代码:")
#if len(code) == 0:
code = '510300'

#strenddate = input("请输入开始日期(格式:1900-01-01):")
#strenddate = ''


#默认生成的k线数据到昨天
if len(strenddate) == 0:
    enddate = datetime.date.today()  + datetime.timedelta(days = -1)
else:
    enddate = datetime.datetime.strptime(strenddate,'%Y-%m-%d')
startdate = enddate + datetime.timedelta(days = -100*365)

if market == 'sh':
    print('shanghai')
elif market == 'sz':
    print('shenzhen')
else:
    print('目前不支持其它市场，程序退出')
    exit

#stock_csv('D:/sh510300.day', code)

filename = 'D:/' + code + '.csv'
history_filename = 'D:/' + 'compare.csv'
result_file = 'D:/' + 'result.csv'

his_pb_dict = {}

f = open(history_filename, 'r')
reader = csv.DictReader(f)
for row in reader:
    trade_date = str(row['trade_date'])
    dif_pb = round(float(row['pb']) - float(row['pb1220']),2)
    his_pb_dict[trade_date] = dif_pb

f.close()

#print(his_pb_dict['20130902'])

basetrade = 2100

i = 0
f = open(filename,'r')
reader = csv.reader(f)
for row in reader:
    i = i + 1
    if i%22 == 1:
        trade_date = str(row[0])
        trade_date = trade_date.replace('-','')
        dif_db = his_pb_dict[trade_date]
        #trade_date1 = datetime.datetime.strptime(trade_date,'%Y%m%d')
        close = row[1]
        if dif_pb < 0:      #当前pb小于5年pb均线，买
            buymoney = round(basetrade * dif_db**3,2)
            print(trade_date+'|'+str(buymoney))
            
            
        elif dif_pb > 0:    #当前pb大于5年pb均线，卖
            buymoney = round(2 * basetrade * dif_db**3,2)
            print(trade_date+'|'+str(buymoney))
        else:               #当前pb等于于5年pb均线，什么也不做
            buymoney = 0
            print(buymoney)
            continue
    else:
        continue



#print(his_pb_dict)

#
"""
def day2csv(source_dir, file_name, target_dir):

def trade_stock(rate,)
TotalBuyAmount = 0.00
TotalSellAmount = 0.00

TotalVolume = 0

EveryAmount = 0.00
EveryVolume = 0

csvvalues = []

f = open(csvdatafilename, 'r')
reader = csv.DictReader(f)
for row in reader:
    if reader.line_num >= 2 + ndays:
        DATE = row['date']
        PB = round(float(row['pbMRQ']),2)    
        AVG_PB = round(float(his_n_days_average_pb_dict[DATE]),2)
        EveryAmount = 2600 * math.pow(AVG_PB - PB,2)
        CLOSE = round(float(row['close']),2)

        if DATE == '2010-07-01':
            print(DATE)

        if EveryAmount > 2000:
            
            EveryVolume = int(EveryAmount/CLOSE/100)*100
            EveryAmount = EveryVolume * CLOSE

            #PB < PB*,买
            if PB <= AVG_PB:
                buyorsell = '买'
                if TotalSellAmount >= EveryAmount:
                    TotalSellAmount = TotalSellAmount - EveryAmount
                    IsSalary = 0
                else:
                    TotalBuyAmount = TotalBuyAmount + EveryAmount
                    IsSalary = 1

                TotalVolume = TotalVolume + EveryVolume
                csvvalues.append([DATE,IsSalary,buyorsell,CLOSE,EveryVolume,TotalVolume])
                

            #PB > PB*,卖
            else:
                buyorsell = '卖'
                if EveryAmount < TotalBuyAmount:
                    TotalSellAmount = TotalSellAmount + EveryAmount

                TotalVolume = TotalVolume - EveryVolume
                IsSalary = -1
                csvvalues.append([DATE,IsSalary,buyorsell,CLOSE,EveryVolume,TotalVolume])
                
        
                    

#print(TotalBuyAmount,TotalSellAmount,TotalVolume*22.48)
            
csvtitle = ['操作日期','工资买','买/卖','价格','成交股数','总仓位']
list_saveas_csv("D:/csv/first_pb/result_" + code + '_' + str(ndays) + '.csv',csvtitle,csvvalues)

    
    

n=[["路飞","男",100],["索隆","男",99],["娜美","女",90]]
b=["姓名","性别","武力值"]
list_saveas_csv("D:/csv/first_pb/result_" + code + '_' + str(ndays) + '.csv',b,n)

def list_saveas_csv(csvdatafilename,csvtitle,csvvalues):
    with open(csvdatafilename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile)      #这一步是创建一个csv的写入器（个人理解）
        writer.writerow(csvtitle)       #写入标签
        writer.writerows(csvvalues)     #写入样本数据
"""
