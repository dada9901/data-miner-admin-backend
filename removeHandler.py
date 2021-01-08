import tornado.web
from mysqlConnector import mysqlConnector
import json
class removeHandler(tornado.web.RequestHandler):
    error_code=""
    def post(self,*args,**kwargs):
        paraments={}
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        print(post_data)
        paraments['user_id']=post_data.get("user_id",None)
        paraments['start_time']=post_data.get("start_time",None)+':00'
        paraments['url']=post_data.get("url",None)
        print(paraments['start_time'])
        sql_connector = mysqlConnector()
        sql = 'delete from data where user_id = %s and start_time between %s and %s and url = %s'
        values = [paraments['user_id'], paraments['start_time'],post_data.get("start_time",None)+':59', paraments['url']]
        res = sql_connector.executeSql(sql, values)
        print(res)
        self.write("OK")