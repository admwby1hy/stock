from mystock import *
import time
#import csv

ms = mystock()
#stock_df = ms.get_stock_df_from_tdx('510300')
shanghai_df = ms.get_shanghai_from_tushare()
#print(df)
#ms.set_ndays_average_pb_and_pe5(df,1220)

starttime = time.process_time()
ndays  = 1708
history_pb_dif_dict = {}

tmpdate = datetime.date.today()  + datetime.timedelta(days = -365)
startdate = datetime.datetime.strftime(tmpdate,'%Y%m%d')
print(startdate)
while ndays >= 100:
    history_pb_dif_dict = ms.get_ndays_average_pb_dif(shanghai_df,ndays)
    #startdate = history_pb_dif_dict['0']
    #startdate = '20180501'

    stock_df = ms.get_stock_df_from_tdx('510300')
    stock_df = stock_df[stock_df['trade_date']>=startdate]
    stock_df = stock_df.sort_values(by = 'trade_date',axis = 0,ascending = True).reset_index(drop=True)

    print(ms.moni(history_pb_dif_dict,stock_df,ndays))

    ndays = ndays - 20
endtime = time.process_time()
print (endtime - starttime)

"""
#
starttime = time.process_time()
#while ndays >= 20:
list = ms.set_ndays_average_pb_and_pe(df,1220)
    #ndays = ndays - 10
endtime = time.process_time()
print (endtime - starttime)

starttime = time.process_time()
list = ms.set_ndays_average_pb_and_pe1(df,1220)
endtime = time.process_time()
print (endtime - starttime)


#df.to_csv('d:/11.csv')
print(len(df))

starttime = time.process_time()
for i in (1,len(df)-1220):
    df1 = df.loc[i-1:i+1220-1]
    a = df1[['pe_ttm','pb']].mean()
endtime = time.process_time()
print (endtime - starttime)
print(i)
print(a[0])
print(a[1])
starttime = time.process_time()
list = ms.set_ndays_average_pb_and_pe(df,1220)
endtime = time.process_time()
print (endtime - starttime)

#print(list)
#print(len(df))

#df.loc[1:499,"pb"].mean()
"""
