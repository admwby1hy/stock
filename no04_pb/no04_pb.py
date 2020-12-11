from mystock import *
import time

strndays = input("请输入pb均线天数:")
if len(strndays) == 0:
    strndays = 488
ndays = int(strndays)

stockcode  = input("请输入证券代码:")
if len(stockcode) == 0:
    stockcode = '510300'

ms = mystock()

shanghai_df = ms.get_shanghai_from_tushare()

starttime = time.process_time()

history_pb_dif_dict = {}

tmpdate = datetime.date.today()  + datetime.timedelta(days = -365)
startdate = datetime.datetime.strftime(tmpdate,'%Y%m%d')
print(startdate)

history_pb_dif_dict = ms.get_ndays_average_pb_dif(shanghai_df,ndays)
    
stock_df = ms.get_stock_df_from_tdx(stockcode)
stock_df = stock_df[stock_df['trade_date']>=startdate]
stock_df = stock_df.sort_values(by = 'trade_date',axis = 0,ascending = True).reset_index(drop=True)

#print(['操作日期','PB-PB*','本次单价','本次买入金额','本次卖出金额','累计买入金额','累计卖出金额','股票剩余资产'])
print(ms.monimingxi(history_pb_dif_dict,stock_df,ndays))

endtime = time.process_time()
print (endtime - starttime)

