
from mystock import *
import time
#import csv

strndays = input("请输入pb均线天数:")
if len(strndays) == 0:
    strndays = 488
ndays = int(strndays)

stockcode  = input("请输入证券代码:")
if len(stockcode) == 0:
    stockcode = '510300'

ms = mystock()

shanghai_df = ms.get_shanghai_from_tushare()
history_pb_dif_dict = {}
history_pb_dif_dict = ms.get_ndays_average_pb_dif(shanghai_df,ndays)

stock_df = ms.get_stock_df_from_tdx(stockcode)
startdate = history_pb_dif_dict['0']
if startdate >= stock_df.loc[0,'trade_date']:
    startdate = stock_df.loc[0,'trade_date']
else:
    stock_df = stock_df[stock_df['trade_date']>=startdate]
    stock_df = stock_df.sort_values(by = 'trade_date',axis = 0,ascending = True).reset_index(drop=True)

tmpdf = stock_df

starttime = time.process_time()

i = 0
resultlist = []
while i < len(stock_df) - 200:

    tmpdf = stock_df[i:244+i]
    tmpdf = tmpdf.sort_values(by = 'trade_date',axis = 0,ascending = True).reset_index(drop=True)

    tmplist = ms.moni(history_pb_dif_dict,tmpdf,ndays)
    if len(tmplist):
        resultlist.append(tmplist)
        

    i += 1
    #startdate = datetime.datetime.strftime((datetime.datetime.strptime(startdate,'%Y%m%d')+datetime.timedelta(days = 1)),'%Y%m%d')

df = pd.DataFrame(data=resultlist,columns=['均线','买入金额','卖出金额','持仓金额','赚取','开始日期','结束日期'])
df.to_csv('a.csv',encoding='utf_8_sig')

endtime = time.process_time()
print (endtime - starttime)

