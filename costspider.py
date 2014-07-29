#-*- coding:utf-8 -*-
import re,sys,os,time
from bs4 import BeautifulSoup
import urllib.request
import io
import gzip

def readurl(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36", "Accept-Encoding": "gzip"})
    bs = urllib.request.urlopen(req).read()
    bi = io.BytesIO(bs)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    html=gf.read().decode("utf-8")
    return html

class spider:
    def __init__(self,*args):
        return super().__init__(*args)

    def getcountry(self,url):
        print("\nstart to get country list")
        html=readurl(url)
        html=BeautifulSoup(html)
        option=html.find_all('option')  #find all counties
        countrylist=[]
        for op in option:
            pp=op.string.replace(" ","+")
            countrylist.append(pp)
        del countrylist[0]
        print("\nget country list finished")
        return countrylist
    
    def getcity(self,country):
        print("\nstart to get city list in  "+country)
        url="http://www.numbeo.com/cost-of-living/country_result.jsp?country="+country    #example china
        try:
            html=readurl(url)
            html=BeautifulSoup(html)
            tag=html.b
            option=tag.find_all('option')
            citylist=[]
            for op in option:
                citylist.append(op.string)
            citylist[0]=''
            print("\nget city list finished")
            return citylist
        except:
            print(url)
            print("url open failed!")
            exit(0)
    
    def getprice(self,country,city=''):
        price=pricedata()
        city=city.replace(', ','%2C+')
        city=city.replace(' ','+')
        if city=="":
            url="http://www.numbeo.com/cost-of-living/country_result.jsp?country="+country+'&displayCurrency=CNY'
            price.city=country
        else:
            url="http://www.numbeo.com/cost-of-living/city_result.jsp?country="+country+"&city="+city+'&displayCurrency=CNY'
            price.city=city  
        try:
            html=readurl(url)
            html=BeautifulSoup(html)
        except:
            print(url)
            print("open url error!!!")
            exit(0)
        option1=html.find_all(attrs={"class":"tr_highlighted"})
        option2=html.find_all(attrs={"class":"tr_standard"})
        prices=[]
        for option in option1:
            pp=pricedata()
            pp.country=country
            pp.city=city 
            low=option.find(attrs={"class":"barTextLeft"})
            high=option.find(attrs={"class":"barTextRight"})
            avg=option.find(attrs={"class":"priceValue"})
            if low!=None:
                pp.low=low.next
                pp.low=pp.low.strip(',')
            if high!=None:
                pp.high=high.next
                pp.high=pp.high.strip(',')
            if avg!=None:
                pp.avg=avg.next.strip(' ¥')
                pp.avg=pp.avg.strip(' ')
                pp.avg=pp.avg.strip(',')
            pp.types=option.td.string
            prices.append(pp)
        i=1
        for option in option2:
            pp=pricedata()
            pp.country=country
            pp.city=city
            low=option.find(attrs={"class":"barTextLeft"})
            high=option.find(attrs={"class":"barTextRight"})
            avg=option.find(attrs={"class":"priceValue"})
            if low!=None:
                pp.low=low.next
            if high!=None:
                pp.high=high.next
            if avg!=None:
                pp.avg=avg.next
            pp.types=option.td.string
            prices.insert(i,pp)
            i=i+2
        return prices
        
            
    def updatalist(self,name):    #file operate       
        path=os.path.dirname(os.path.abspath(sys.argv[0]))
        try:
            os.mkdir(path+'\cn\data')
        except:
            pass
        path=os.path.join(path+'\cn\data',name+'.txt')
        try:
            file=open(path,'r+')
        except:
            file=open(path,'w+')
        time_ymd=time.strftime("%Y-%m-%d", time.localtime())
        timedata=file.read(len(time_ymd))
        citylist=[]
        if timedata==time_ymd:
            print("\nno need to updata data of %s" %name)
            citylist=file.readlines()
            del citylist[0]
            for n in range(len(citylist)):
                citylist[n]=citylist[n].strip('\n')
        else:
            file.truncate()
            file.write(' '*len(time_ymd))
            citylist=costspider.getcity(country)
            for city in citylist:
                file.writelines('\n'+city)
            file.seek(0,0)
            file.write(time_ymd)   
        file.close()
        return citylist
        
    def updataprice(self,country,city=''):    #file operate
        path=os.path.dirname(os.path.abspath(sys.argv[0]))
        try:
            os.mkdir(path+'\cn\data')
        except:
            try:
                os.mkdir(path+'\cn\data\\'+country)
            except:
                pass
        
        path=path+'\cn\data\\'+country
        if city=='':
            path=os.path.join(path,country+'.txt')
        else:
            path=os.path.join(path,city+'.txt')
        try:
            file=open(path,'r+',encoding='utf-8')
        except:
            file=open(path,'w+',encoding='utf-8')
        time_ymd=time.strftime("%Y-%m-%d", time.localtime())
        timedata=file.read(len(time_ymd))
        if timedata==time_ymd:
            print("\nno need to updata data of %s in %s" %(country,city))
        else:
            file.truncate()
            file.write(' '*len(time_ymd))
            pricelist=costspider.getprice(country,city)
            for price in pricelist:
                if price.low=='\n':
                    price.low=price.low.replace('\n','0')
                else:
                    price.low=price.low.strip('\n')
                price.low=price.low.replace('?','0')
                price.low=price.low.replace(',','')

                price.high=price.high.replace('?','0')
                price.high=price.high.replace(',','')

                price.avg=price.avg.replace('?','0')
                price.avg=price.avg.replace(',','')
                price.avg=price.avg.strip(' ¥')
                price.avg=price.avg.strip(' ')
                if price.high=='\n':
                    price.high=price.high.replace('\n','0')
                else:
                    price.high=price.high.strip('\n')
                price.high=price.high.replace('?','0')
                file.write('\n'+price.types+"\n"+price.low+"\n"+price.avg+"\n"+price.high)
            file.seek(0,0)
            file.write(time_ymd)   
        file.close()


        
class pricedata:
    country="China"
    city="China"
    low='0.0'
    high='0.0'
    avg='0.0'
    types="price"
    currency='CNY'
def state():
	aa=input("\nplease uncomment the code in the main function!\n")


if __name__== "__main__":
    url="http://www.numbeo.com/cost-of-living/"
    state()
    # costspider=spider()
    # #countrylist=costspider.getcountry(url)
    # #countrylist=['China','United+States']
    # countrylist=['China']
    # for country in countrylist:
    #     citylist=costspider.updatalist(country)        
    #     for city in citylist:
    #         if city=='':
    #             print("\nstart to updata  price in "+country)
    #         else:
    #             print("\nstart to updata  price in "+city)
    #         costspider.updataprice(country,city)

