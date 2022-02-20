#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from pandas import Series,DataFrame

df = DataFrame(pd.read_excel('./data.xlsx'))

#对列进行重命名
df.rename(columns={0:'姓名',1:'性别',2:'年龄',3:'体重',4:'身高'},inplace=True)

#完整性检查
#1.存在空行->删除
df.dropna(how='all',inplace=True)
#2.体重列出现空值->使用均值进行填充
df[u'体重'].fillna(int(df[u'体重'].mean()),inplace=True)

#全面性检查
#1.发现身高列使用的度量不统一，有用厘米，有用米的，统一成米
def format_height(df):
    if(df['身高'] < 3):
        return df['身高'] * 100
    else:
        return df['身高']    
df['身高'] =  df.apply(format_height,axis=1)
#2.姓名首字母大小写不统一，统一成首字母大写
df.columns = df.columns.str.upper()

#合法性检查
#1.英文名字出现中文->删除非ASCII码的字符
df['姓名'].replace({r'[^\x00-\x7f]+':''},regex=True,inplace=True)
#2.英文名字出现了问号->删除问号
df['姓名'].replace({r'\?+':''},regex=True,inplace=True)
#3.名字前出现空格->删除空格
df['姓名'] = df['姓名'].map(str.lstrip)
#4.年龄出现了负数->负数转化成正数
def format_sex(df):
    return abs(df['年龄'])
df['年龄'] = df.apply(format_sex,axis=1)

#唯一性检查
#姓名为Emma一行记录存在重复->删除
df.drop_duplicates(['姓名'],inplace=True)

#保存至excel
df.to_excel('./data02.xlsx',index=False)