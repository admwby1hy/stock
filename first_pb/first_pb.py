import pandas as pd
import datetime
import json
import os
import csv
import math
from myfunction import *

import tushare as ts


#计算从2014年9月01日买入如下股票至今的收益

code = ''
market = ''
strenddate = ''

#market = input("请输入交易市场(sh/sz,默认sh):")
if len(market) == 0:
    market = 'SH'

#工商银行，中信证券，中国石化，保利地产
#codelist = ['601398','600030','600028','600048']code = input("请输入股票代码:")
#code  = input("请输入证券代码:")
if len(code) == 0:
    code = '600016'

#strenddate = input("请输入开始日期(格式:1900-01-01):")
#strenddate = '2019-09-30'

enddate = datetime.date.today()  + datetime.timedelta(days = -1)
strenddate = datetime.datetime.strftime(enddate,'%Y%m%d')

# 设置token，只需要在第一次调用或者token失效时设置
# 设置完成后，之后就不再需要这一个命令了
ts.set_token('1e405fa29516d0c96f66ee71f4f2833b31b566cd6ad4f0faa895c671')
pro = ts.pro_api()

#通用数据接口，但我积分不够
#df1 = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
#df1.to_csv('d:/2.csv')

#获取上证历史数据
df_dailybasic1 = pro.index_dailybasic(ts_code = "000001.SH",start_date = '20001219',end_date = '20160731')
df_dailybasic2 = pro.index_dailybasic(ts_code = "000001.SH",start_date = '20160801',end_date = strenddate)
df_dailybasic = df_dailybasic2.append(df_dailybasic1)
df_dailybasic.sort_values(by = 'trade_date',axis = 0,ascending = True).to_csv('D:/000001.SH')


#一年的交易日大概244天,1220是5年，计算5年PB、PE均线数据
ndays = 244 * 5
set_his_n_days_average_pb_to_csv('D:/000001.SH',ndays)
pb_filename = 'D:/000001.SH'+'_pb_'+str(ndays)+'.csv'

#获取股票历史数据
filename = 'D:/' + code + '_' + strenddate + '.csv'
df1 = pro.daily(ts_code=code + '.' + market, start_date = '20001219',end_date = '20101218')
df2 = pro.daily(ts_code=code + '.' + market, start_date = '20101219',end_date = strenddate)
df = df2.append(df1)
df.sort_values(by = 'trade_date',axis = 0,ascending = True).to_csv(filename)



history_filename = pb_filename
result_file = 'D:/' + code + '.' + market + '_result.csv'

his_pb_dict = {}

f = open(history_filename, 'r')
reader = csv.DictReader(f)
for row in reader:
    trade_date = str(row['trade_date'])
    dif_pb = round(float(row['PB']) - float(row['PBn']),2)
    his_pb_dict[trade_date] = dif_pb

f.close()

basetrade = 1000

resultcsvtitle = ['操作日期','PB-PB*','本次单价','本次投入本金','累计投入本金','总资产','回收资金','绝对收益率','月化收益率']
resultcsvfile = 'D:/result_' + str(code) + '.csv'
resultlist = []

thisamount = 0.0
thismoney = 0.0
totalbuymoney = 0.0

totalamount = 0.0
totalvolume = 0.0
totalsellmoney = 0.0
dif_pb = 0.0


i = 0
f = open(filename,'r')
reader = csv.reader(f)
next(reader)
for row in reader:
    i = i + 1
    if i%22 == 1:
        trade_date = str(row[2])
        trade_date = trade_date.replace('-','')

        if trade_date not in his_pb_dict:
            i = 0
            continue
        
        dif_pb = float(his_pb_dict[trade_date])
        #trade_date1 = datetime.datetime.strptime(trade_date,'%Y%m%d')
        close = float(row[3])

        thismoney = abs(round(basetrade * dif_pb,2))
        #thismoney = round(-basetrade * dif_pb**3,2)

        #当前pb小于5年pb均线，买
        if dif_pb < 0: 
            
            thisamount = round(thismoney/close,2)
            totalbuymoney = totalbuymoney + thismoney
            totalamount = totalamount + thisamount
            totalvolume = totalamount * close

            #resultcsvtitle = ['操作日期','PB-PB*','本次单价','本次投入本金','累计投入本金','总资产','回收资金','绝对收益率','月化收益率']
            resultlist.append([trade_date,dif_pb,close,thismoney,totalbuymoney,totalvolume + totalsellmoney,totalsellmoney,0,0])

        #当前pb大于5年pb均线，卖    
        elif dif_pb > 0:    
            thisamount = round(thismoney/close,2)
            totalbuymoney = totalbuymoney - thismoney
            totalamount = totalamount - thisamount
            totalvolume = totalamount * close
            totalsellmoney = totalsellmoney + thismoney

            #resultcsvtitle = ['操作日期','PB-PB*','本次单价','本次投入本金','累计投入本金','总资产','回收资金','绝对收益率','月化收益率']
            resultlist.append([trade_date,dif_pb,close,0,totalbuymoney,totalvolume + totalsellmoney,totalsellmoney,0,0])
        
        #当前pb等于于5年pb均线，什么也不做
        else:               
            continue
    else:
        continue

list_saveas_csv(resultcsvfile,resultcsvtitle,resultlist)


"""
#一年的交易日大概244天
ndays = 244 * 5
csvdatafilename = 'd:/000001.SH.basic.csv'
his_n_days_average_pb_json_filename =  csvdatafilename + '.' + str(ndays) + '.json'

set_his_n_days_average_pb(csvdatafilename,his_n_days_average_pb_json_filename,ndays)

#set_his_n_days_average_pb_to_csv(csvdatafilename,ndays)




ndays = 610
his_n_days_average_pb_json_filename = (r'D:/csv/first_pb/his_' + str(ndays) + '_days_average_pb_' + code + '.json')


#默认生成的k线数据到昨天
if len(strenddate) == 0:
    enddate = datetime.date.today()  + datetime.timedelta(days = -1)
else:
    enddate = datetime.datetime.strptime(strenddate,'%Y-%m-%d')
startdate = enddate + datetime.timedelta(days = -100*365)


#从baostock.com获取历史k线数据-截止日期到2019-09-30
csvdatafilename = "D:/csv/first_pb/"+ code+ "-" + strenddate +".csv"
if os.path.isfile(csvdatafilename) == False:
    save_stock_k_data_from_baostock(startdate,enddate,code,csvdatafilename,market='sh')

#生成n天市净率均线数据到json文件
set_his_n_days_average_pb(csvdatafilename,his_n_days_average_pb_json_filename,ndays)

#获取n天市净率均线数据到数据字典
his_n_days_average_pb_dict = json.load(open(his_n_days_average_pb_json_filename))

from_date_value = list(his_n_days_average_pb_dict.keys())[0]


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
