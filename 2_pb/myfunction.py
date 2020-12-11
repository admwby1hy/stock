import baostock as bs
import pandas as pd
import datetime
import csv
import pymssql 

import json
import os

import struct

def stock_csv(filepath, name):
    data = []
    with open(filepath, 'rb') as f:
        file_object_path = 'D:/' + name +'.csv'
        file_object = open(file_object_path, 'w+')
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
            stock_date = struct.unpack("l", stock_date)     # 4字节 如20091229
            stock_open = struct.unpack("l", stock_open)     #开盘价*100
            stock_high = struct.unpack("l", stock_high)     #最高价*100
            stock_low= struct.unpack("l", stock_low)        #最低价*100
            stock_close = struct.unpack("l", stock_close)   #收盘价*100
            stock_amount = struct.unpack("f", stock_amount) #成交额
            stock_vol = struct.unpack("l", stock_vol)       #成交量
            stock_reservation = struct.unpack("l", stock_reservation) #保留值

            date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
            list= date_format.strftime('%Y-%M-%d')+","+str(stock_close[0]/1000.0)+","+"\r"
            file_object.writelines(list)
        file_object.close()

#from https://blog.csdn.net/hanhf/article/details/73014926
def day2csv(source_dir, file_name, target_dir):
    # 以二进制方式打开源文件
    source_file = open(source_dir + file_name, 'rb')
    buf = source_file.read()
    source_file.close()
 
    # 打开目标文件，后缀名为CSV
    target_file = open(target_dir + file_name + '.csv', 'w+')
    buf_size = len(buf)
    rec_count = buf_size / 32
    begin = 0
    end = 32
    header = str('date') + ', ' + str('open') + ', ' + str('high') + ', ' + str('low') + ', ' \
        + str('close') + ', ' + str('amount') + ', ' + str('vol') + ', ' + str('str07') + '\n'
    target_file.write(header)
    for i in xrange(rec_count):
        # 将字节流转换成Python数据格式
        # I: unsigned int
        # f: float
        a = unpack('IIIIIfII', buf[begin:end])
        line = str(a[0]) + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
            + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
            + str(a[6]) + ', ' + str(a[7]) + ', ' + '\n'
        target_file.write(line)
        begin += 32
        end += 32
    target_file.close()

def list_saveas_csv(csvdatafilename,csvtitle,csvvalues):
    with open(csvdatafilename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile)      #这一步是创建一个csv的写入器（个人理解）
        writer.writerow(csvtitle)       #写入标签
        writer.writerows(csvvalues)     #写入样本数据

def get_pb_average_from_csv(datafilename):
    df = pd.read_csv (datafilename)
    return df['pbMRQ'].mean()

def set_his_n_days_average_pb(csvdatafilename,his_n_days_average_pb_json_filename,ndays):
    if os.path.isfile(his_n_days_average_pb_json_filename) == False:
        his_pb_dict = {}
        f = open(csvdatafilename, 'r')
        totalrows = len(list(csv.DictReader(f)))

        for i in range(1,totalrows - ndays + 1):
            total_pbMRQ = 0.0
            f = open(csvdatafilename, 'r')
            reader = csv.DictReader(f)
            for row in reader:
                if reader.line_num >= 1+i and reader.line_num <= ndays+i:
                    total_pbMRQ = total_pbMRQ + float(row['pbMRQ'])
                else:
                    if reader.line_num > ndays + i:
                        lastdate = str(row['date'])
                        break
            his_pb_dict[lastdate] = total_pbMRQ / ndays

    
        json.dump(his_pb_dict,open(his_n_days_average_pb_json_filename,'w'))


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