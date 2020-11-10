import tornado.web
from mysqlConnector import mysqlConnector
import json
class registerHandler(tornado.web.RequestHandler):
    error_code=""
    def post(self,*args,**kwargs):
        paraments={}
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        print(post_data)
        paraments['account_id']=post_data.get("account_id",None)
        paraments['user_name']=post_data.get("user_name",None)
        paraments['password']=post_data.get("password",None)
        paraments['email']=post_data.get("email",None)
        if(self.check(paraments)==0):
            self.write(self.error_code)
            return
        sql_connector=mysqlConnector()
        sql = 'insert into user (account_id,user_name,password,email) values (%s,%s,%s,%s);'
        values=[paraments['account_id'],paraments['user_name'],paraments['password'],paraments['email']]
        res=sql_connector.executeSql(sql,values)
        if(res==None):
            self.write("OK")
        else:
            res=str(res)
            self.write(res)

    def check(self,paraments):
        if(paraments['account_id']==None or paraments['user_name']==None or paraments['password']==None or paraments['email']==None):
            self.error_code="输入参数缺失"
            return 0
        return 1
