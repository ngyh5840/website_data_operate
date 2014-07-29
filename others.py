#-*- coding:utf-8 -*-
import xlrd
import os,sys


def readexcel(path=''):
    try:
        data = xlrd.open_workbook(path)
    except:
        print("open excel file error!\n")
        print(path)
        exit(0)
    table=data.sheets()[0] 
    return table


path=os.path.dirname(os.path.abspath(sys.argv[0]))

cn_dic={}
path1=path+"\map.xlsx"
key_val=readexcel(path1)
for i in range(1,key_val.nrows):
    cn_dic[key_val.row_values(i)[1]]=key_val.row_values(i)[0]


path2=path+'\\country.xlsx'


countrylist=[]
key_val=readexcel(path2)
for i in range(1,key_val.nrows):
    countrylist.append(key_val.row_values(i)[1])


path3=path+"\\abc.txt"
fo=open(path3,"w+",encoding='utf-8')
for country in countrylist:
    try:
        code=cn_dic[country]
        fo.write(country)
        fo.write(',')
        fo.write(code+"\n")
    except:
        fo.write(country)
        fo.write(',')
        fo.write("000\n")
