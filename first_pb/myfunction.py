
import pandas as pd
import datetime
import csv
import pymssql 

import json
import os

def list_saveas_csv(csvdatafilename,csvtitle,csvvalues):
    with open(csvdatafilename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile)      #这一步是创建一个csv的写入器（个人理解）
        writer.writerow(csvtitle)       #写入标签
        writer.writerows(csvvalues)     #写入样本数据

def set_pb_average_from_csv_to_csv(datafilename):
    df = pd.read_csv (datafilename)
    return df['pbMRQ'].mean()

def set_his_n_days_average_pb_to_csv(csvdatafilename,ndays):
    #if os.path.isfile(his_n_days_average_pb_json_filename) == False:
    f = open(csvdatafilename, 'r')
    csvreader = csv.reader(f)
    csvlist = list(csvreader)

    tmplist_pb = []
    tmplist_pe = []
    for i in range(1,len(csvlist) - ndays ):
        total_pb = 0.0
        total_pe = 0.0
        j = 0

        pb = 0.0
        pe = 0.0
        for row in csvlist:
            j = j + 1
            if j >= 1+i and j <= ndays+i:
                total_pe = total_pe + float(row[11])
                total_pb = total_pb + float(row[12])
            else:
                if j >= ndays + i:
                    lastdate = str(row[2])
                    pe = float(row[11])
                    pb = float(row[12])
                    break
        tmplist_pe.append([lastdate,pe,round(total_pe / ndays,2)])
        tmplist_pb.append([lastdate,pb,round(total_pb / ndays,2)])

    csvtitle = ['trade_date','PB','PBn']
    list_saveas_csv(csvdatafilename+'_pb_'+str(ndays)+'.csv',csvtitle,tmplist_pb)

    csvtitle = ['trade_date','PE','PEn']
    list_saveas_csv(csvdatafilename+'_pe_'+str(ndays)+'.csv',csvtitle,tmplist_pe)
    

def set_his_n_days_average_pe_to_csv(csvdatafilename,ndays):
    #if os.path.isfile(his_n_days_average_pb_json_filename) == False:
    f = open(csvdatafilename, 'r')
    csvreader = csv.reader(f)
    csvlist = list(csvreader)

    tmplist = []
    for i in range(1,len(csvlist) - ndays ):
        total_pe = 0.0
        j = 0

        pb = 0.0
        for row in csvlist:
            j = j + 1
            if j >= 1+i and j <= ndays+i:
                total_pe = total_pe + float(row[11])
            else:
                if j >= ndays + i:
                    lastdate = str(row[2])
                    pe = float(row[11])
                    break
        tmplist.append([lastdate,pe,round(total_pe / ndays,2)])

    csvtitle = ['交易日期','PE','PEn']

    list_saveas_csv(csvdatafilename+'_pe_'+str(ndays)+'.csv',csvtitle,tmplist)

    
                    
               

def set_his_n_days_average_pb(csvdatafilename,his_n_days_average_pb_json_filename,ndays):
    if os.path.isfile(his_n_days_average_pb_json_filename) == False:
        his_pb_dict = {}
        f = open(csvdatafilename, 'r')
        totalrows = len(list(csv.DictReader(f)))

        for i in range(1,totalrows - ndays + 1):
            total_pb = 0.0
            f = open(csvdatafilename, 'r')
            reader = csv.DictReader(f)
            for row in reader:
                if reader.line_num >= 1+i and reader.line_num <= ndays+i:
                    total_pb = total_pb + float(row['pb'])
                else:
                    if reader.line_num > ndays + i:
                        lastdate = str(row['trade_date'])
                        break
            his_pb_dict[lastdate] = round(total_pb / ndays,2)

        with open(his_n_days_average_pb_json_filename+'.csv', 'w') as f:
            for key in his_pb_dict.keys():
                f.write("%s,%s\n"%(key,his_pb_dict[key]))


        #json.dump(his_pb_dict,open(his_n_days_average_pb_json_filename,'w'))


#根据起始时间获取某只股票的前复权k线数据
def save_stock_k_data_from_baostock(startdate,enddate,code,datafilename,market='sh'):
    
    lg = bs.login()
    if lg.error_code != '0':
        # 显示登陆返回信息
        print('login respond error_code:'+lg.error_code)
        print('login respond  error_msg:'+lg.error_msg)
        exit('登陆baostock失败')

    #### 获取历史K线数据 ####
    # 详细指标参数,参见“历史行情指标参数”章节
    # frequency="d"取日k线,adjustflag="3"默认不复权
    rs = bs.query_history_k_data_plus(market+'.'+code,
                                      "date,code,open,high,low,close,preclose,volume,amount,pbMRQ",
                                      start_date=startdate.strftime( '%Y-%m-%d' ), end_date= enddate.strftime( '%Y-%m-%d' ),frequency="d", adjustflag="2") 
    if rs.error_code != '0':
        print('query_history_k_data_plus respond error_code:'+rs.error_code)
        print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
        exit('从获取K线数据失败')

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录,将记录合并在一起
        data_list.append(rs.get_row_data())

    #### 登出系统 ####
    bs.logout()

    #### 结果集输出到csv文件 ####
    result = pd.DataFrame(data_list, columns=rs.fields)
    
    result.to_csv(datafilename, encoding="gbk", index=False)

    


def insertdetail(a,b,c,d,e,f,g,h):
    # 连接服务器地址
    server = 'db-user-read-01.vancldb.com'  
    # 连接帐号
    user = 'hejiang'
    # 连接密码
    password = 'abcd@1234'

    conn = pymssql.connect(server, user, password, "trace")  #获取连接

    cursor = conn.cursor() # 获取光标

    cursor.execute("INSERT INTO detail365 VALUES (%s,%d,%d,%s,%d,%d,%d,%d)",((a),(b),(c),(d),(e),(f),(g),(h)))
    #INSERT INTO detail365 VALUES (N'sh.601398',11.08,1,N'2018-10-11',%f,5.17,38600,%f)
    #insertdetail(row['code'],tstandard,1,opdate,close,firstvolume,totalvolume,myleftmoney)
    # 你必须调用 commit() 来保持你数据的提交如果你没有将自动提交设置为true
    conn.commit()
    conn.close()

def simulate_detail_from_csv(datafilename,upstandard,downstandard):
    myleftmoney = 400000.00
    #print('总资金%.2f'%(myleftmoney))

    firstamount = 200000.00
    #print('首次买入200000')
    firstvolume = 0

    everyamount = 16000.00
    everyvolume = 0

    totalvolume = 0

    latestprice = 0.00
    latestvolume = 0
    tstandard = (upstandard - 1)*100*1000+(1-downstandard)*10*10
    close=0

    with open(datafilename,'r',encoding="gbk") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            #open = round(float(row['open']),2)
            #high = round(float(row['high']),2)
            #low = round(float(row['low']),2)
            close = round(float(row['close']),2)
            opdate = row['date']
 
            if reader.line_num == 2:
                isbuy = 1
                latestprice = close

                firstvolume = int(firstamount/close/100)*100
                totalvolume = totalvolume + firstvolume
                myleftmoney = myleftmoney - firstvolume * close
            
                #insertdetail(row['code'],tstandard,isbuy,opdate,close,firstvolume,totalvolume,myleftmoney)
                #print ('傻橙于 %s 以 %8.2f 的价格买入 %d股作为底仓,资金余额 %f' % (opdate,close,firstvolume,myleftmoney))
            else:
                #达到设定涨幅,卖出股票        
                if close > latestprice * upstandard:
                    if totalvolume <= firstvolume/4:
                        latestprice = close
                        continue
                    isbuy = 0
                    latestprice = close
                

                    #if latestvolume == 0:
                    #    latestvolume = int(everyamount/close/100)*100

                    everyvolume =  int(everyamount/close/100)*100

                
                    if totalvolume <= everyvolume:
                    
                        myleftmoney = myleftmoney + round(totalvolume * close * 0.998,2)
                    
                        print ('傻橙于 %s 以 %f 的价格卖出 %d股,上次价格%f,还剩 %d股,资金余额 %.2f' % (opdate,close,totalvolume,latestprice,0,myleftmoney))
                        print('本年任务以完成,再见,傻橙')
                        totalvolume = 0
                        #insertdetail(row['code'],tstandard,isbuy,opdate,close,totalvolume,0,myleftmoney)
                        exit
                    else:
                        totalvolume = totalvolume - everyvolume
                        myleftmoney = myleftmoney + round(everyvolume * close * 0.998,2)
                        #insertdetail(row['code'],tstandard,isbuy,opdate,close,everyvolume,totalvolume,myleftmoney)
                        #latestvolume = everyvolume

                        #print ('傻橙于 %s 以 %f 的价格卖出 %d股,上次价格%f,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,latestprice,totalvolume,myleftmoney,myleftmoney+totalvolume*close))
                #达到设定跌幅,买入股票
                elif close <= latestprice * downstandard:
                    isbuy = 1
                    latestprice = close

                    everyvolume =  int(everyamount/close/100)*100

                    totalvolume = totalvolume + everyvolume
                    myleftmoney = myleftmoney - round(everyvolume * close,2)
                    #insertdetail(row['code'],tstandard,1,opdate,close,everyvolume,totalvolume,myleftmoney)
                    #print ('傻橙于 %s 以 %f 的价格买入 %d股,上次价格%f,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,latestprice,totalvolume,myleftmoney,myleftmoney+totalvolume*close))

        print ('傻橙的总资产%.2f' % (myleftmoney+totalvolume*close))



def simulate_detail_from_csv_with_log(datafilename,upstandard,downstandard):
    myleftmoney = 400000.00
    #print('总资金%.2f'%(myleftmoney))

    firstamount = 200000.00
    #print('首次买入200000')
    firstvolume = 0

    everyamount = 16000.00
    everyvolume = 0

    totalvolume = 0

    latestprice = 0.00
    latestvolume = 0
    tstandard = (upstandard - 1)*100*1000+(1-downstandard)*10*10
    close=0

    with open(datafilename,'r',encoding="gbk") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            #open = round(float(row['open']),2)
            #high = round(float(row['high']),2)
            #low = round(float(row['low']),2)
            close = round(float(row['close']),2)
            opdate = row['date']
 
            if reader.line_num == 2:
                isbuy = 1
                latestprice = close

                firstvolume = int(firstamount/close/100)*100
                totalvolume = totalvolume + firstvolume
                myleftmoney = myleftmoney - firstvolume * close
            
                #insertdetail(row['code'],tstandard,isbuy,opdate,close,firstvolume,totalvolume,myleftmoney)
                print ('傻橙于 %s 以 %8.2f 的价格买入 %d股作为底仓,资金余额 %f' % (opdate,close,firstvolume,myleftmoney))
            else:
                #达到设定涨幅,卖出股票        
                if close > latestprice * upstandard:
                    if totalvolume <= firstvolume/4:
                        latestprice = close
                        continue
                    isbuy = 0
                    latestprice = close
                

                    #if latestvolume == 0:
                    #    latestvolume = int(everyamount/close/100)*100

                    everyvolume =  int(everyamount/close/100)*100

                
                    if totalvolume <= everyvolume:
                    
                        myleftmoney = myleftmoney + round(totalvolume * close * 0.998,2)
                    
                        print ('傻橙于 %s 以 %f 的价格卖出 %d股,上次价格%f,还剩 %d股,资金余额 %.2f' % (opdate,close,totalvolume,latestprice,0,myleftmoney))
                        print('本年任务以完成,再见,傻橙')
                        totalvolume = 0
                        #insertdetail(row['code'],tstandard,isbuy,opdate,close,totalvolume,0,myleftmoney)
                        exit
                    else:
                        totalvolume = totalvolume - everyvolume
                        myleftmoney = myleftmoney + round(everyvolume * close * 0.998,2)
                        #insertdetail(row['code'],tstandard,isbuy,opdate,close,everyvolume,totalvolume,myleftmoney)
                        #latestvolume = everyvolume

                        print ('傻橙于 %s 以 %f 的价格卖出 %d股,上次价格%f,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,latestprice,totalvolume,myleftmoney,myleftmoney+totalvolume*close))
                #达到设定跌幅,买入股票
                elif close <= latestprice * downstandard:
                    isbuy = 1
                    latestprice = close

                    everyvolume =  int(everyamount/close/100)*100

                    totalvolume = totalvolume + everyvolume
                    myleftmoney = myleftmoney - round(everyvolume * close,2)
                    #insertdetail(row['code'],tstandard,1,opdate,close,everyvolume,totalvolume,myleftmoney)
                    print ('傻橙于 %s 以 %f 的价格买入 %d股,上次价格%f,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,latestprice,totalvolume,myleftmoney,myleftmoney+totalvolume*close))

        print ('傻橙的总资产%.2f' % (myleftmoney+totalvolume*close))


def maxprofit_from_csv(datafilename,upstandard,downstandard):
    myleftmoney = 400000.00
    print('总资金%.2f'%(myleftmoney))

    firstamount = 200000.00
    print('首次买入200000')
    firstvolume = 0

    everyamount = 16000.00
    everyvolume = 0

    totalvolume = 0

    latestprice = 0.00
    latestvolume = 0

    maxmoney = 0.00

    with open(datafilename,'r',encoding="gbk") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            #open = round(float(row['open']),2)
            #high = round(float(row['high']),2)
            #low = round(float(row['low']),2)
            close = round(float(row['close']),2)
            opdate = row['date']
            tstandard = (upstandare - 1)*100*1000+(1-downdownstandard)*10*10
                                                 
 
            if reader.line_num == 2:
                isbuy = 1
                latestprice = close

                firstvolume = int(firstamount/close/100)*100
                totalvolume = totalvolume + firstvolume
                myleftmoney = myleftmoney - firstvolume * close
            
                insertdetail(row['code'],tstandard,isbuy,opdate,close,firstvolume,totalvolume,myleftmoney)
                print ('傻橙于 %s 以 %8.2f 的价格买入 %d股作为底仓,资金余额 %f' % (opdate,close,firstvolume,myleftmoney))
            else:
                #达到设定涨幅,卖出股票
                if close > latestprice * upstandard:
                    isbuy = 0
                    latestprice = close
                

                    #if latestvolume == 0:
                    #    latestvolume = int(everyamount/close/100)*100

                    everyvolume =  int(everyamount/close/100)*100

                
                    if totalvolume <= everyvolume:
                    
                        myleftmoney = myleftmoney + round(totalvolume * close * 0.998,2)
                    
                        print ('傻橙于 %s 以 %f 的价格卖出 %d股,还剩 %d股,资金余额 %f' % (opdate,close,totalvolume,0,myleftmoney))
                        print('本年任务以完成,再见,傻橙')
                        totalvolume = 0
                        insertdetail(row['code'],tstandard,isbuy,opdate,close,totalvolume,0,myleftmoney)
                        exit
                    else:
                        totalvolume = totalvolume - everyvolume
                        myleftmoney = myleftmoney + round(everyvolume * close * 0.998,2)
                        insertdetail(row['code'],tstandard,isbuy,opdate,close,everyvolume,totalvolume,myleftmoney)
                        #latestvolume = everyvolume

                        print ('傻橙于 %s 以 %f 的价格卖出 %d股,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,totalvolume,myleftmoney,myleftmoney+totalvolume*close))
                #达到设定跌幅,买入股票
                elif close <= latestprice * downstandard:
                    isbuy = 1
                    latestprice = close

                    everyvolume =  int(everyamount/close/100)*100

                    totalvolume = totalvolume + everyvolume
                    myleftmoney = myleftmoney - round(everyvolume * close,2)
                    insertdetail(row['code'],tstandard,1,opdate,close,everyvolume,totalvolume,myleftmoney)

                    print ('傻橙于 %s 以 %f 的价格买入 %d股,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,totalvolume,myleftmoney,myleftmoney+totalvolume*close))

        print ('傻橙的总资产%f' % (myleftmoney+totalvolume*close))   
        

"""
def simulatetotal(reader,upstandard,downstandard):
    myleftmoney = 400000.00
    #print('总资金%.2f'%(myleftmoney))

    firstamount = 200000.00
    #print('首次买入200000')
    firstvolume = 0

    everyamount = 16000.00
    everyvolume = 0

    totalvolume = 0

    latestprice = 0.00
    latestvolume = 0

    
    for row in reader:

        open = round(float(row['open']),2)
        high = round(float(row['high']),2)
        low = round(float(row['low']),2)
        close = round(float(row['close']),2)
        opdate = row['date']
 
        if reader.line_num == 2:
            latestprice = close

            firstvolume = int(firstamount/close/100)*100
            totalvolume = totalvolume + firstvolume
            myleftmoney = myleftmoney - firstvolume * close
            
            #print ('傻橙于 %s 以 %f 的价格买入 %d股作为底仓,资金余额 %f' % (opdate,close,firstvolume,myleftmoney))
        else:
            #达到设定涨幅,卖出股票
            if close > latestprice * upstandard:
                latestprice = close
                

                #if latestvolume == 0:
                #    latestvolume = int(everyamount/close/100)*100

                everyvolume =  int(everyamount/close/100)*100

                
                if totalvolume <= everyvolume:
                    
                    myleftmoney = myleftmoney + round(totalvolume * close * 0.998,2)
                    
                    print ('傻橙于 %s 以 %f 的价格卖出 %d股,还剩 %d股,资金余额 %f' % (opdate,close,totalvolume,0,myleftmoney))
                    print('本年任务以完成,再见,傻橙')
                    totalvolume = 0
                    exit(0)
                else:
                    totalvolume = totalvolume - everyvolume
                    myleftmoney = myleftmoney + round(everyvolume * close * 0.998,2)

                    #latestvolume = everyvolume

                    #print ('傻橙于 %s 以 %f 的价格卖出 %d股,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,totalvolume,myleftmoney,myleftmoney+totalvolume*close))
            #达到设定跌幅,买入股票
            elif close <= latestprice * downstandard:
                latestprice = close

                everyvolume =  int(everyamount/close/100)*100

                totalvolume = totalvolume + everyvolume
                myleftmoney = myleftmoney - round(everyvolume * close,2)

                #print ('傻橙于 %s 以 %f 的价格买入 %d股,还剩 %d股,资金余额 %.2f, 总资产%.2f' % (opdate,close,everyvolume,totalvolume,myleftmoney,myleftmoney+totalvolume*close))

    print ('傻橙的总资产%f' % (myleftmoney+totalvolume*close))        
"""