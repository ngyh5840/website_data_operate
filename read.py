#-*- coding:utf-8 -*-
import os,shutil,re,sys
import urllib.request
import json
import goslate
import xlrd


class pricedata:
    country="China"
    city="China"
    city_en="中国"
    country_en="中国"
    low=0.0
    high=0.0
    avg=0.0
    types="price"
    currency="CNY"
    num=0

class citydata:
    """docstring for ClassName"""
    name="china-中国"
    country="中国"
    city="中国"
    city_en="China"
    country_en="China"
    state="亚洲"

class countrydata:
    """docstring for ClassName"""
    country="中国"
    country_en="china"
    state="亚洲"
    state_num=1
    favorite=1
    default=1
    describe="人口最多"

class chinadata:
    area="华北"
    area_num=1
    area_en="NorthChina"
    province="河北"
    province_en="HebeiProvince"
    city="石家庄"
    city_en="Shijiazhuang"

    
def tran(word):
    gs = goslate.Goslate()
    dd=gs.translate(word,'zh-CN')
    return (dd)
    
def readexcel(path=''):
    try:
        data = xlrd.open_workbook(path)
    except:
        print("open excel file error!\n")
        print(path)
        exit(0)
    table=data.sheets()[0] 
    return table


class inputdata:
    def __init__(self,*args): 
        return super().__init__(*args)
    
    def getcountry(self):
        path=os.path.dirname(os.path.abspath(sys.argv[0]))
        path=path+'\cn\data'
        list=os.listdir(path)  #列出目录下的所有文件和目录
        countrylist=[]
        countryadd=[]
        for line in list:
            filepath = os.path.join(path,line)
            if os.path.isfile(filepath):   #如果filepath是文件，直接列出文件名
                linep=line.split('.')
                countrylist.append(linep[0])
                countryadd.append(filepath)
        return countrylist,countryadd

    def getcity(self,add,country):
        try:
            fi=open(add,'r+')
        except:
            fi=open(add,'w+')
        citys=fi.readlines()
        if citys==[]:
            print("nothing in %s.txt" %country)
            citys=[]
            path=[]
        else:
            del citys[0]
            citys[0]=country
            i=1
            while i<len(citys):
                citys[i]=citys[i].strip('\n')
                i=i+1
            path=os.path.dirname(os.path.abspath(sys.argv[0]))
            path=path+'\cn\data\\'+country
        return citys,path

    def getdata(self,country,city,path,cn_dic,num_dic,data):
        #city=city.replace(', ','%2c+')
        filepath=os.path.join(path,city+'.txt')
        try:
            fo=open(filepath)
        except:
            print("open %s.txt failed!"%city)
            exit(0)
        datap=fo.readlines()
        i=1
        if len(datap)>1:
            while i<197:            #len(data)
                price=pricedata()
                try:
                    price.num=num_dic[datap[i].strip('\n')]
                    price.currency='CNY'
                    try:
                        price.types=cn_dic[datap[i].strip('\n')].rstrip(" ").lstrip(" ")
                    except:
                        print('types: %s cannot be translated!',types)
                    try:
                        price.country=cn_dic[country.replace('+',' ')].rstrip(' ').lstrip(" ")
                    except:
                        print('country: %s cannot be translated!',country)
                    try:
                        price.city=cn_dic[city.replace('+',' ')].rstrip(' ').lstrip(" ")
                    except:
                        print('city: %s cannot be translated!',city)
                    price.country_en=country.replace('+',' ').rstrip(' ').lstrip(" ")
                    price.city_en=city.replace('+',' ').rstrip(' ').lstrip(" ")
                    i=i+1
                    price.low=datap[i]
                    i=i+1
                    price.avg=datap[i]
                    i=i+1
                    price.high=datap[i]
                    i=i+1
                    data.append(price)
                except:
                    i=i+4
        
    def translate(self,country,trans):
        path=os.path.dirname(os.path.abspath(sys.argv[0]))
        if country=='China':
            fi=open(path+'\cn\data\\'+country+'.txt')
            listd=fi.read()
            word=tran(listd)
            trans[listd]=word
            country=country.replace('+',' ')
            countrycn=tran(country)
            trans[country]=countrycn
        elif country=='type':
            fi=open(path+"\cn\\"+country+'.txt')
            listd=fi.read()
            word=tran(listd)
            trans[listd]=word
        else:
            country=country.replace('+',' ')
            countrycn=tran(country)
            trans[country]=countrycn

    def get_dic(self,cn_dic):
        path=os.path.dirname(os.path.abspath(sys.argv[0]))+"\cn\key_val.xlsx"
        key_val=readexcel(path)
        for i in range(1,key_val.nrows):
            cn_dic[key_val.row_values(i)[0]]=key_val.row_values(i)[1].rstrip(" ").lstrip(" ")

    def get_type_dic(self,type_dic):
        path=os.path.dirname(os.path.abspath(sys.argv[0]))+"\cn\\type.xlsx"
        key_val=readexcel(path)
        for i in range(1,key_val.nrows):
            type_dic[key_val.row_values(i)[0]]=int(key_val.row_values(i)[1])

#----------------------------------------------------------------------------------------
    def translate_all(self):                  #translate all
        path=os.path.dirname(os.path.abspath(sys.argv[0]))
        trans={}
        self.translate('type',trans)     #translate type
        (countrylist,countryadd)=self.getcountry()
        for i in range(len(countrylist)):
            self.translate(countrylist[i],trans)     #translate citylist
        try:
            os.mkdir(path+'\cn')
        except:
        	pass
        path1=path+'\cn\\'+'key.txt'
        path2=path+'\cn\\'+'val.txt'
        fo1=open(path1,'w+',encoding='utf-8')
        fo2=open(path2,'w+',encoding='utf-8')
        for(key,val) in trans.items():
        	fo1.write(key+'\n')
        	fo2.write(str(val)+'\n')

    def get_all_key(self):             #get all country and city names  output:/cn/key_all.txt
        path=os.path.dirname(os.path.abspath(sys.argv[0]))
        (countrylist,countryadd)=self.getcountry()
        key=[]
        path1=path+'\cn\\'+'key_all.txt'
        fo1=open(path1,'w+',encoding='utf-8')
        for i in range(len(countrylist)):
            fi=open(path+'\data\\'+countrylist[i]+'.txt')
            city=fi.readlines()
            country=countrylist[i].replace('+',' ')+'\n'
            fo1.write(country)
            del city[0]
            del city[0]
            for c in city:
                fo1.write(c.strip('\n')+'\n')

    def get_all_country(self):      #get all country names  output:/cn/key_all.txt
        path=os.path.dirname(os.path.abspath(sys.argv[0]))
        cn_dic={}
        self.get_dic(cn_dic)
        (countrylist,countryadd)=self.getcountry()
        fo1=open(path+'\\countrylist_en.txt','w+',encoding='utf-8')
        fo2=open(path+'\\countrylist_cn.txt','w+',encoding='utf-8')
        for country in countrylist:
            fo1.write(country.replace('+',' ')+'\n')
            fo2.write(cn_dic[country.replace('+',' ')]+'\n')

#---------------------------------------------------------------------------------------
    def get_price_data(self):            #get all price data
        (countrylist,countryadd)=self.getcountry()
        cn_dic={}
        num_dic={}  
        data=[]
        self.get_dic(cn_dic)
        self.get_type_dic(num_dic)
        for i in range(len(countrylist)):
            (citys,path)=self.getcity(countryadd[i],countrylist[i])
            for j in range(len(citys)):
                self.getdata(countrylist[i],citys[j],path,cn_dic,num_dic,data)
        return data

    def get_city_data(self):            #get all price data
        (countrylist,countryadd)=self.getcountry()
        cn_dic={} 
        state_dic={}
        data=[]
        state=self.get_country_data()
        for s in state:
            state_dic[s.country_en]=s

        self.get_dic(cn_dic)
        for i in range(len(countrylist)):
            (citys,path)=self.getcity(countryadd[i],countrylist[i])
            for j in range(len(citys)):
                city=citydata()
                city.city_en=citys[j].replace("+"," ").rstrip(" ").lstrip(" ")
                city.city=cn_dic[citys[j].replace('+',' ')].rstrip(" ").lstrip(" ")
                city.country_en=countrylist[i].replace("+"," ").rstrip(" ").lstrip(" ")
                city.country=cn_dic[countrylist[i].replace('+',' ')].rstrip(" ").lstrip(" ")
                city.state=state_dic[city.country_en].state
                if city.city==city.country:
                    city.name=city.city+"("+city.city_en+"),"+city.state
                else:
                    city.name=city.city+"("+city.city_en+"),"+city.country
                data.append(city)
        return data

    def get_country_data(self):
        path=os.path.dirname(os.path.abspath(sys.argv[0]))+"\cn\country.xlsx"
        countrylist=readexcel(path)
        data=[]
        state_cn={1:'亚洲',2:'欧洲',3:'非洲',4:'北美洲',5:'南美洲',6:'大洋洲',7:'南极洲'}
        for i in range(1,countrylist.nrows):
            country=countrydata()
            country.country=countrylist.row_values(i)[0].rstrip(" ").lstrip(" ")
            country.country_en=countrylist.row_values(i)[1].rstrip(" ").lstrip(" ")
            country.state=state_cn[int(countrylist.row_values(i)[2])]
            country.state_num=int(countrylist.row_values(i)[2])
            country.favorite=int(countrylist.row_values(i)[3])
            default=countrylist.row_values(i)[4]
            if default==0:
                country.default=0
            else:
                country.default=1
            country.describe=countrylist.row_values(i)[5].rstrip(" ").lstrip(" ")
            data.append(country)
        return data

    def get_map_data(self):
        state=self.get_country_data()
        cn_dic={}
        for s in state:
            cn_dic[s.country_en]=s.country
        path=os.path.dirname(os.path.abspath(sys.argv[0]))+"\cn\map.xlsx"
        key_val=readexcel(path)
        data=[]
        for i in range(key_val.nrows):
            try:
                cn=cn_dic[key_val.row_values(i)[0]]
                code=key_val.row_values(i)[1]
            except:
                print("cannot match country code!")
                print(key_val.row_values(i)[0])
                exit(0)
            data.append((code,cn))
        return data

    def get_china_data(self):
        path=os.path.dirname(os.path.abspath(sys.argv[0]))+"\cn\chinacity.xlsx"
        citylist=readexcel(path)
        data=[]
        state_cn={'华北':1,'东北':2,'华东':3,'中南':4,'西南':5,'西北':6}
        for i in range(1,citylist.nrows):
            city=chinadata()
            city.area=citylist.row_values(i)[0].rstrip(" ").lstrip(" ")
            city.area_num=state_cn[city.area]
            city.province=citylist.row_values(i)[1].rstrip(" ").lstrip(" ")
            city.city=citylist.row_values(i)[2].rstrip(" ").lstrip(" ")
            city.province_en=citylist.row_values(i)[3].rstrip(" ").lstrip(" ")
            city.area_en=citylist.row_values(i)[3].rstrip(" ").lstrip(" ")
            city.province_en=citylist.row_values(i)[4].rstrip(" ").lstrip(" ")
            city.city_en=citylist.row_values(i)[5].rstrip(" ").lstrip(" ")
            data.append(city)
        return data


if __name__== "__main__":
    p=inputdata()
    #p.get_country_data()
    #data=p.get_price_data()
    #data=p.get_city_data()
    #print(p.get_map_data())

#filepath=[]
#for parent,dirnames,filenames in os.walk(path):
#    for  filename in filenames:
 #      filepath.append(os.path.join(parent,filename))
      #  print(os.path.join(parent,filename),'\n')



#print(filepath)
