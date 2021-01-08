import tornado.web
from mysqlConnector import mysqlConnector
import json
class loginHandler(tornado.web.RequestHandler):
    error_code=""
    def post(self,*args,**kwargs):
        paraments={}
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        paraments['account_id']=post_data.get('account_id',None)
        paraments['password']=post_data.get('password',None)
        if(self.check(paraments)==0):
            self.write(self.error_code)
        sql_connector=mysqlConnector()
        sql='select * from user where account_id = %s and password = %s;'
        values=[paraments['account_id'],paraments['password']]
        res=sql_connector.query(sql,values)
        print(res)
        if(type(res)==tuple and len(res)==1):
            self.write({"status":"OK","user_name":res[0][2]})
        else:
            res='输入的账号或密码不存在'
            self.write(res)

    def check(self,paraments):
        if(paraments['account_id']==None or paraments['password']==None):
            self.error_code="输入参数缺失"
            return 0
        return 1
