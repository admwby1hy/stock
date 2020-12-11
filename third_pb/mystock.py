import tushare as ts
import datetime
import pandas as pd
import numpy as np
import struct
from statistics import mean

tushare_token = '1e405fa29516d0c96f66ee71f4f2833b31b566cd6ad4f0faa895c671'

class mystock:
    def __init__(self):
        self.tushare_token = '1e405fa29516d0c96f66ee71f4f2833b31b566cd6ad4f0faa895c671'
        self.tdx_path = ''

    #获取上证综指历史数据，含市净率，市盈率
    def get_shanghai_from_tushare(self):
        enddate = datetime.date.today()  + datetime.timedelta(days = -1)
        strenddate = datetime.datetime.strftime(enddate,'%Y%m%d')
        ts.set_token(self.tushare_token)
        pro = ts.pro_api()
        df1 = pro.index_dailybasic(ts_code = "000001.SH",start_date = '20001219',end_date = '20160731')
        df2 = pro.index_dailybasic(ts_code = "000001.SH",start_date = '20160801',end_date = strenddate)
        df = df2.append(df1)

        
        #print(train_x_list)

        return df.sort_values(by = 'trade_date',axis = 0,ascending = True).reset_index(drop=True)

    #获取深证成指历史数据
    def get_shenzhen_from_tushare(self):
        tushare_token = '1e405fa29516d0c96f66ee71f4f2833b31b566cd6ad4f0faa895c671'
        enddate = datetime.date.today()  + datetime.timedelta(days = -1)
        strenddate = datetime.datetime.strftime(enddate,'%Y%m%d')
        ts.set_token(self.tushare_token)
        pro = ts.pro_api()
        df1 = pro.index_dailybasic(ts_code = "399001.SH",start_date = '20001219',end_date = '20160731')
        df2 = pro.index_dailybasic(ts_code = "399001.SH",start_date = '20160801',end_date = strenddate)
        df = df2.append(df1)
        return df.sort_values(by = 'trade_date',axis = 0,ascending = True).reset_index(drop=True)

    def get_stock_from_tushare(self,code):
        enddate = datetime.date.today()  + datetime.timedelta(days = -1)
        strenddate = datetime.datetime.strftime(enddate,'%Y%m%d')
        ts.set_token(self.tushare_token)
        pro = ts.pro_api()
        df1 = pro.daily_basic(ts_code=code, start_date = '20001219',end_date = '20101218')
        df2 = pro.daily_basic(ts_code=code, start_date = '20101219',end_date = strenddate)
        df = df2.append(df1)
        return df.sort_values(by = 'trade_date',axis = 0,ascending = True).reset_index(drop=True)
    
    def get_stock_list_from_tdx(self,code):
        #df = pd.DataFrame(columns=['trade_date', 'open', 'high', 'low', 'close', 'amount', 'volume', 'reservation'])
        df = pd.DataFrame(columns=['trade_date', 'open', 'high', 'low', 'close'])
        list = []
        file = 'D:/new_tdx/vipdoc/sh/lday/sh' + code + '.day'
        with open(file, 'rb') as f:
            while True:
                stock_date = f.read(4)
                stock_open = f.read(4)
                stock_high = f.read(4)
                stock_low= f.read(4)
                stock_close = f.read(4)
                stock_amount = f.read(4)
                stock_vol = f.read(4)
                stock_reservation = f.read(4)

                # date,open,high,low,close,amount,vol,reservation
                if not stock_date:
                    break

                stock_date = struct.unpack("l", stock_date)     #4字节 如20091229
                stock_open = struct.unpack("l", stock_open)     #开盘价*100
                stock_high = struct.unpack("l", stock_high)     #最高价*100
                stock_low= struct.unpack("l", stock_low)        #最低价*100
                stock_close = struct.unpack("l", stock_close)   #收盘价*100
                stock_amount = struct.unpack("f", stock_amount) #成交额
                stock_vol = struct.unpack("l", stock_vol)       #成交量
                stock_reservation = struct.unpack("l", stock_reservation) #保留

                if str(stock_date[0]) == '20120709':
                    print(stock_date)
                
                #list.append([str(stock_date[0]),stock_open[0],stock_high[0],stock_low[0],stock_close[0],stock_amount[0],stock_vol[0],stock_reservation[0]])
                list.append([stock_date[0],stock_open[0],stock_high[0],stock_low[0],stock_close[0]])
        print(list)
        df = pd.DataFrame(list, index=['trade_date', 'open', 'high', 'low', 'close'])  #, ignore_index=True
        return df

    def get_stock_df_from_tdx(self,code):
        #df = pd.DataFrame(columns=['trade_date','open','high','low','close','amount','vol']))

        ls = []
        file = 'C:/new_tdx/vipdoc/sh/lday/sh' + code + '.day'
        with open(file, 'rb') as f:
            buffer=f.read()                         #读取数据到缓存
            size=len(buffer) 
            rowSize=32                              #通信达day数据，每32个字节一组数据
            for i in range(0,size,rowSize):         #步长为32遍历buffer
                row = list( struct.unpack('IIIIIfII',buffer[i:i+rowSize]) )
                row[0]=str(row[0])
                row[1]=row[1]/1000
                row[2]=row[2]/1000
                row[3]=row[3]/1000
                row[4]=row[4]/1000
                row.pop()                           #移除后面其它字段
                #row.insert(0,code)
                ls.append(row)
            df = pd.DataFrame(data=ls,columns=['trade_date','open','high','low','close','amount','vol'])
        return df

    def set_ndays_average_pb_and_pe(self,df,ndays):
        list_from_df = np.array(df).tolist()
        tmplist = []

        for i in range( len(list_from_df) - ndays ):
            total_pb = 0.0
            total_pe = 0.0
            
            j = i
            
            while j<ndays+i:
                total_pe = total_pe + list_from_df[j][10]               #11列pe_ttm
                total_pb = total_pb + list_from_df[j][11]               #12列pb
                j += 1
                
            trade_date = list_from_df[j][1]
            pe = list_from_df[j][10]
            pb = list_from_df[j][11]
            tmplist.append([trade_date,pe,round(total_pe / ndays,2),pb,round(total_pb / ndays,2)])
        return tmplist   
    
    def get_ndays_average_pb_dif(self,df,ndays):
        list_from_df = np.array(df).tolist()
        history_pb_dif_dict = {}
        history_pb_dif_dict['0'] = list_from_df[0][1]
        for i in range( len(list_from_df) - ndays ):
            total_pb = 0.0
            #total_pe = 0.0
            
            j = i
            
            while j<ndays+i:
                #total_pe = total_pe + list_from_df[j][10]               #11列pe_ttm
                total_pb = total_pb + list_from_df[j][11]                #12列pb
                j += 1
  
            trade_date = list_from_df[j][1]
            if i == 0:
                history_pb_dif_dict['0'] = trade_date
            #pe = list_from_df[j][10]
            pb = list_from_df[j][11]
            history_pb_dif_dict[trade_date] = pb - round(total_pb / ndays,2)
        return history_pb_dif_dict   

    def moni(self,dif_pb_dict,stock_df,ndays):
        result_list = []
        basetrade = 10000

        totalbuymoney = 0.0
        totalamount = 0.0
        totalvolume = 0.0

        totalsellmoney = 0.0

        begindate = ''
        enddate = ''

        for i in range(len(stock_df)):
            
            if i%22 == 0:
                trade_date = stock_df.loc[i]['trade_date']
                if i==0:
                    begindate = trade_date

                dif_pb = float(dif_pb_dict[trade_date])
                close = float(stock_df.loc[i]['close'])

                if abs(dif_pb)>=1:
                    thismoney = abs(round(basetrade * dif_pb ** 1,2))
                else:               
                    thismoney = abs(round(basetrade * dif_pb,2))
                #当前pb小于ndays天pb均线，买
                if dif_pb < 0:  
                    thisamount = round(thismoney/close,4)
                    totalbuymoney = totalbuymoney + thismoney
                    totalamount = totalamount + thisamount
                    totalvolume = round(totalamount * close,2)

                    #resultcsvtitle = ['操作日期','PB-PB*','本次单价','本次投入本金','累计投入本金','总资产','回收资金','绝对收益率','月化收益率']
                    #resultlist.append([trade_date,dif_pb,close,thismoney,totalbuymoney,totalvolume + totalsellmoney,totalsellmoney,0,0])

                #当前pb大于ndays天pb均线，卖    
                elif dif_pb > 0:
                    thisamount = round(thismoney/close,4)
                    if totalamount<thisamount:
                        continue
                    #totalbuymoney = totalbuymoney - thismoney
                    totalamount = totalamount - thisamount
                    totalvolume = round(totalamount * close,2)
                    totalsellmoney = totalsellmoney + thismoney

                    #resultcsvtitle = ['操作日期','PB-PB*','本次单价','本次投入本金','累计投入本金','总资产','回收资金','绝对收益率','月化收益率']
                    #resultlist.append([trade_date,dif_pb,close,0,totalbuymoney,totalvolume + totalsellmoney,totalsellmoney,0,0])
        
                #当前pb等于ndays天pb均线，什么也不做
                else:               
                    continue
            else:
                continue
        enddate = trade_date
        return [ndays,round(totalbuymoney,2),round(totalsellmoney,2),round(totalvolume,2),round((totalvolume+totalsellmoney)/totalbuymoney,2),begindate,enddate]

    def monimingxi(self,dif_pb_dict,stock_df,ndays):
        result_list = []
        basetrade = 10000

        totalbuymoney = 0.0
        totalamount = 0.0
        totalvolume = 0.0

        totalsellmoney = 0.0

        for i in range(len(stock_df)):
            
            if i%22 == 0:
                trade_date = stock_df.loc[i]['trade_date']
                dif_pb = float(dif_pb_dict[trade_date])
                close = float(stock_df.loc[i]['close'])

                if abs(dif_pb)>=1:
                    thismoney = abs(round(basetrade * dif_pb ** 1,2))
                else:               
                    thismoney = abs(round(basetrade * dif_pb,2))
                #当前pb小于ndays天pb均线，买
                if dif_pb < 0:  
                    thisamount = round(thismoney/close,4)
                    totalbuymoney = totalbuymoney + thismoney
                    totalamount = totalamount + thisamount
                    totalvolume = round(totalamount * close,2)

                    #resultcsvtitle = ['操作日期','PB-PB*','本次单价','本次买入金额','本次卖出金额','累计买入金额','累计卖出金额','股票剩余资产']
                    result_list.append([trade_date,round(dif_pb,2),close,thismoney,0,totalbuymoney,totalsellmoney,totalvolume])

                #当前pb大于ndays天pb均线，卖    
                elif dif_pb > 0:
                    thisamount = round(thismoney/close,4)
                    if totalamount<thisamount:
                        continue
                    #totalbuymoney = totalbuymoney - thismoney
                    totalamount = totalamount - thisamount
                    totalvolume = round(totalamount * close,2)
                    totalsellmoney = totalsellmoney + thismoney

                    #resultcsvtitle = ['操作日期','PB-PB*','本次单价','本次买入金额','本次卖出金额','累计买入金额','累计卖出金额','股票剩余资产']
                    result_list.append([trade_date,round(dif_pb,2),close,0,thismoney,totalbuymoney,totalsellmoney,totalvolume])
        
                #当前pb等于ndays天pb均线，什么也不做
                else:               
                    continue
            else:
                continue
        df = pd.DataFrame(data=result_list,columns=['操作日期','PB-PB*','本次单价','本次买入金额','本次卖出金额','累计买入金额','累计卖出金额','股票剩余资产'])
        return df

"""   
    def set_ndays_average_pb_and_pe1(self,df,ndays):
        tmplist = []

        for i in range(len(df) - ndays ):

            average_df = df.loc[i-1:i+ndays-1]
            average_value = average_df[['pe_ttm','pb']].mean()
            averagepe = average_value[0]
            averagepb = average_value[1]

            nextendrow = df.iloc[i+ndays]
            #print(nextendrow[0])
            trade_date = str(nextendrow['trade_date'])
            pe = float(nextendrow['pe_ttm'])
            pb = float(nextendrow['pb'])
            
            #tmplist.append([trade_date,pe,pb,averagepe,averagepb])
            #print([trade_date,pe,pb,averagepe,averagepb])

        return tmplist
 

    def set_ndays_average_pb_and_pe2(self,df,ndays):
        list_from_df = np.array(df).tolist()
        tmplist = []
        
        for i in range( len(list_from_df) - ndays):
            total_pb = 0.0
            total_pe = 0.0
            j = 0

            pb = 0.0
            pe = 0.0

            tmplist = list_from_df[i:ndays][1]
            k= tmplist(lambda tmplist:tmplist[10])
            
            print(tmplist)
            
            for row in list_from_df:
                j = j + 1
                if j >= 1+i and j <= ndays+i:
                    total_pe = total_pe + float(row[10])                #12列pe_ttm
                    total_pb = total_pb + float(row[11])                #13列pb
                else:
                    if j >= ndays + i:
                        lastdate = str(row[1])
                        pe = float(row[10])
                        pb = float(row[11])
                        break
            tmplist.append([lastdate,pe,pb,round(total_pe / ndays,2),round(total_pb / ndays,2)])
            #print([lastdate,pe,pb,round(total_pe / ndays,2),round(total_pb / ndays,2)])
        
        return tmplist


    def set_ndays_average_pb_and_pe3(self,df,ndays):
        tmplist = []

        for i in range(len(df) - ndays ):

            #average_df = df[['pe_ttm','pb']].iloc[i:ndays+i-1]
            average_df = df[(df.index>=i) & (df.index<=ndays+i-1)]

            average_value = average_df[['pe_ttm','pb']].mean()
            averagepe = average_value[0]
            averagepb = average_value[1]

            #nextendrow = df.iloc[i+ndays]
            #print(nextendrow[0])
            trade_date = df.at[i+ndays,'trade_date']
            pe = df.at[i+ndays,'pe_ttm']
            pb = df.at[i+ndays,'pb']
            
            tmplist.append([trade_date,pe,pb,averagepe,averagepb])
            #print([trade_date,pe,pb,averagepe,averagepb])

        return tmplist
"""



