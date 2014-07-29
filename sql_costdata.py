#!/usr/bin/python3
# a sample to use mysql-connector for python3
# see details from   http://dev.mysql.com/doc/connector-python/en/index.html
 
import mysql.connector
import sys, os
from mysql.connector import errorcode
from read import pricedata
from read import inputdata


class sql:
    def __init__(self,user='root',password='',host = '127.0.0.1'):
        self._conn = mysql.connector.connect(user=user,password=password,host=host)
        self._cursor = self._conn.cursor()

    def create_database(self,db):
        try:
            db="`"+db+"`"
            self._conn.database=db
            return  1
        except:
            create_database_sql="create database if not exists  %s " %db
            try:
                self._cursor.execute(create_database_sql)
                self._conn.database=db
                return 1
            except:
                print("Failed creating database: %s"%db)
                return 0


    def create_table(self,mytable):
        create_table_sql = "CREATE TABLE IF NOT EXISTS `%s` (NUM int(5),\
            Item_ID varchar(100), Average int(10), Max int(10),Min int(10) ,Upload int(10) ) \
            CHARACTER SET utf8" %mytable
        tablenum=-1
        try:
            self._cursor.execute("SELECT * FROM `%s`" %(mytable))
            self._cursor.fetchall()
            tablenum=int(self._cursor.rowcount)
        except:
            pass
        if tablenum==-1:
            try:             
                self._cursor.execute(create_table_sql)
                return  1
            except:
                print("create table '%s' failed."%mytable)
                print(mysql.connector.errors)
                return  0
        elif tablenum>=47:
            return  0
        else:
            return 1

    def insert_sql(self,data):
	#insert_sql = "INSERT INTO 西安(Item_ID, Average, Max, Min, Upload) VALUES ('大米',12,23,22,15 ),('小麦',12,23,22,15 )"
        tablenum=0   
        try:
            self._cursor.execute("SELECT * FROM `%s` WHERE NUM=%s" %(data.city,data.num))
            self._cursor.fetchall()
            tablenum=int(self._cursor.rowcount)
        except:
            pass
        if tablenum<1:    
            insert_sql = "INSERT INTO `"+data.city+"`(NUM,Item_ID, Average, Max, Min) VALUES (%s,%s,%s,%s,%s) "
            val=[data.num,data.types,data.avg,data.high,data.low]
            try:
            	self._cursor.execute(insert_sql,val)
            except:
            	print("insert table '%s' failed."%data.city)
            	printdd(data)
            	pass  
        else:
            pass

    def close(self):
        """关闭游标和数据库连接"""
        self._conn.commit()
        self._cursor.close()
        self._conn.close()




def printdd(datad):
    print(datad.country+'\n'+datad.city+'\n'+datad.types+'\n'+datad.low+'\n'+datad.avg+'\n'+datad.high+'\n')


p=inputdata()
data=p.get_price_data()

pp=sql()

i=0
for dat in data:
    a=pp.create_database(dat.country)
    if a==1:
        b=pp.create_table(dat.city)
        if b==1:
            pp.insert_sql(dat)   
            i=i+1
            print(i-1)
pp.close()
print("insert total %s tables"%(i-1))













# user = 'root'
# pwd  = ''
# host = '127.0.0.1'
# db   = '中国'
 


# create_table_sql = "CREATE TABLE IF NOT EXISTS 西安 ( \
# 		    Item_ID varchar(20), Average int(5), Max int(5),Min int(5) ,Upload int(5) ) \
# 		    CHARACTER SET utf8"
 
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
# 	cnx.database=DB_NAME    
# except:
# 	create_database(cursor,DB_NAME)
# 	cnx.database = DB_NAME

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

