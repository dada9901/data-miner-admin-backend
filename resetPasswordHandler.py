import tornado.web
from mysqlConnector import mysqlConnector
import json
class resetPasswordHandler(tornado.web.RequestHandler):
    error_code=""
    def post(self,*args,**kwargs):
        paraments={}
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        paraments['account_id']=post_data.get("account_id",None)
        paraments['new_password']=post_data.get("new_password",None)
        if(self.check(paraments)==0):
            self.write(self.error_code)
        sql_connector=mysqlConnector()
        sql = 'update user set password = %s where account_id= %s'
        values=[paraments['new_password'],paraments['account_id']]
        res=sql_connector.executeSql(sql,values)
        if(res==None):
            self.write("OK")
        else:
            res=str(res)
            self.write(res)

    def check(self,paraments):
        if(paraments['account_id']==None or paraments['new_password']==None):
            self.error_code="输入参数缺失"
            return 0
        return 1
