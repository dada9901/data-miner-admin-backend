import pymysql.cursors
import pymysql
connection=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='dada9901',db='a1',charset='utf8')
cur=connection.cursor()
cur.execute('select * from user')
for each in cur:
    print(each)