#!/usr/bin/python3
#encoding=utf8
# a sample to use mysql-connector for python3
# see details from   http://dev.mysql.com/doc/connector-python/en/index.html
 
import mysql.connector
import sys, os
from mysql.connector import errorcode
from read import pricedata
from read import inputdata
from read import readexcel

class sql:
    def __init__(self,user='root',password='',host = '127.0.0.1'):
        self._conn = mysql.connector.connect(user=user,password=password,host=host)
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


    def create_table(self,mytable,num,start):
        sql=""
        for i in range(num):
            sql=sql+"upload%s int(10) ," %(i+start)
        sql=sql.rstrip(",")

        create_table_sql = "CREATE TABLE IF NOT EXISTS  `"+mytable+ "` ("+sql+") CHARACTER SET utf8" 
        try:
            self._cursor.execute(create_table_sql)
            return  1
        except:
            print("create table '%s' failed."%mytable)
            return  0

    def close(self):
        """关闭游标和数据库连接"""
        self._conn.commit()
        self._cursor.close()
        self._conn.close()


p=inputdata()
data2=p.get_china_data()
pp=sql()
i=0
data=[]
path=os.path.dirname(os.path.abspath(sys.argv[0]))+"\cn\\upload_type.xlsx"
key_val=readexcel(path)
for i in range(key_val.nrows):
    data.append((key_val.row_values(i)[0],key_val.row_values(i)[1],int(key_val.row_values(i)[2])))

num=1
for uptype in data:
    a=pp.create_database("upload_"+uptype[1])
    for dat in data2:
        b=pp.create_table(dat.city,uptype[2],num)
        # if b==1:
        #     pp.insert_sql(dat)   
        #     i=i+1
        i=i+1
        print(i)
    num=num+uptype[2]
pp.close()
print("insert total %s tables"%(i))












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

