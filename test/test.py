"""
import sys
def add(a,b):
    return( a+b )

print(add(2.54,3.258))

print(sys.path)
print(sys.path[3])

Weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday']
print ( Weekday[0])

fruit = ['pineapple','pear']
fruit.insert(1,'grape')
print ( fruit )

fruit[0:1] = ['Orange']
print ( fruit )

del fruit[0:2]
print ( fruit )

a = {'key':123,'key':123}
print(a)

NASDAQ_code = {'BIDU':'Baidu','SINA':'Sina'}
NASDAQ_code['YOKU'] = 'Youku'
print (NASDAQ_code)

stack = [3,4,5]
stack.append(6)
stack.append(7)
print(stack)
print(stack.pop())
"""

import tushare as ts
import pandas as pd

# 设置token，只需要在第一次调用或者token失效时设置
# 设置完成后，之后就不再需要这一个命令了
ts.set_token('1e405fa29516d0c96f66ee71f4f2833b31b566cd6ad4f0faa895c671')

pro = ts.pro_api()
df_daily = pro.index_daily(ts_code="000001.SH")
print(df_daily.count())