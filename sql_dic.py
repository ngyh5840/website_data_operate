#!/usr/bin/python3
#encoding=utf8
# a sample to use mysql-connector for python3
# see details from   http://dev.mysql.com/doc/connector-python/en/index.html
 
import mysql.connector
import sys, os
from mysql.connector import errorcode
from read import pricedata
from read import inputdata


class sql:
    def __init__(self,user='root',password='',host = '127.0.0.1'):
        self._conn = mysql.connector.connect(user=user,password=password,host=host,charset='gbk')
        self._cursor = self._conn.cursor()

    def create_database(self,db):
        try:
            self._conn.database=db
            return  1
        except:
            create_database_sql= "create database if not exists  `%s`" %db            
            try:
                self._cursor.execute(create_database_sql)
                self._conn.database=db
                return 1
            except:
                print("Failed creating database: %s"%db)
                return 0


    def create_table(self,mytable):
        create_table_sql = "CREATE TABLE IF NOT EXISTS  `"+mytable+"` (COUNTRY_CN varchar(20), COUNTRY_EN varchar(20) ,\
            CITY_CN varchar(20),CITY_EN varchar(20),STATE varchar(10)) CHARACTER SET utf8"  
        try:
            self._cursor.execute(create_table_sql)
            return  1
        except:
            print("create table '%s' failed."%mytable)
            print(mysql.connector.errors)
            return  0


    def insert_sql(self,data):
        #insert_sql = "INSERT INTO 西安(Item_ID, Average, Max, Min, Upload) VALUES ('大米',12,23,22,15 ),('小麦',12,23,22,15 )"
        tablenum=0
        try:
            select_table_sql="SELECT * FROM `"+data.name+"`"
            self._cursor.execute(select_table_sql)
            self._cursor.fetchall()
            tablenum=int(self._cursor.rowcount)
        except:
            pass
        if tablenum<1:
            #insert_sql = "INSERT INTO `%s`(COUNTRY_CN,COUNTRY_EN,CITY_CN,CITY_EN) VALUES ('%s','%s','%s') "\
            #        %(data.city,data.country,data.country_en,data.city_en)
            insert_sql = "INSERT INTO `"+data.name+"` values(%s,%s,%s,%s,%s)"
            val=[data.country,data.country_en,data.city,data.city_en,data.state]
            try:
                self._cursor.execute(insert_sql,val)
            except:
                print("insert table '%s' failed."%data.name)
                print(mysql.connector.errors)
                pass  

    def close(self):
        """关闭游标和数据库连接"""
        self._conn.commit()
        self._cursor.close()
        self._conn.close()




def printdd(datad):
    print(datad.country+'\n'+datad.city+'\n'+datad.city_en+'\n'+datad.country_en+'\n')

p=inputdata()
data=p.get_city_data()
pp=sql()
i=0
a=pp.create_database('dic')
for dat in data:
    b=pp.create_table(dat.name)
    if b==1:
        pp.insert_sql(dat)   
        i=i+1
        print(i)
pp.close()
print(" total %s tables"%(i))












# user = 'root'
# pwd  = ''
# host = '127.0.0.1'
# db   = '中国'
 


# create_table_sql = "CREATE TABLE IF NOT EXISTS 西安 ( \
#           Item_ID varchar(20), Average int(5), Max int(5),Min int(5) ,Upload int(5) ) \
#           CHARACTER SET utf8"
 
# def create_database(cursor,db):
#     try:
#         cursor.execute('create database if not exists %s' %db)
#     except mysql.connector.Error as err:
#         print("Failed creating database: {}".format(err))
#         exit(1)

# cnx = mysql.connector.connect(user=user, password=pwd, host=host)

# DB_NAME='中国'
# cursor = cnx.cursor()
# try:
#   cnx.database=DB_NAME    
# except:
#   create_database(cursor,DB_NAME)
#   cnx.database = DB_NAME

# try:
#     cursor.execute(create_table_sql)
# except mysql.connector.Error as err:
#     print("create table 'mytable2' failed.")
#     print("Error: {}".format(err.msg))
#     sys.exit()


# insert_sql = "INSERT INTO 西安(Item_ID, Average, Max, Min, Upload) VALUES ('大米',12,23,22,15 ),('小麦',12,23,22,15 )"


# try:
#     cursor.execute(insert_sql)
# except mysql.connector.Error as err:
#     print("insert table 'mytable' failed.")
#     print("Error: {}".format(err.msg))
#     sys.exit()


# cnx.commit()
# cursor.close()
# cnx.close()

