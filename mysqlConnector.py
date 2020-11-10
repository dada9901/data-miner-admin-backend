import pymysql
from config import options
class mysqlConnector():
    connection=""
    def connect(self):
        host=options['mysql']
        port=options['mysql_port']
        db=options['dbname']
        user=options['mysql_user']
        password=options['mysql_password']
        self.connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                                     charset='utf8')
    def test(self):
        cur = self.connection.cursor()
        cur.execute('select * from user limit 10')
        print(cur.fetchall())

    def executeSql(self,sql,values):
        try:
            self.connect()
            cur=self.connection.cursor()
            cur.execute(sql,values)
            self.connection.commit()
            cur.close()
            self.connection.close()
            return None
        except Exception as ex:
            return ex

    def query(self,sql,values):
        try:
            self.connect()
            cur=self.connection.cursor()
            cur.execute(sql,values)
            result=cur.fetchall()
            cur.close()
            self.connection.close()
            return result
        except Exception as ex:
            return ex