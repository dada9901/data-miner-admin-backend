import tornado.web
from mysqlConnector import mysqlConnector
import json
class resHandler(tornado.web.RequestHandler):
    error_code=""
    def post(self,*args,**kwargs):
        paraments={}
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        #print(post_data)
        paraments['user_id']=post_data.get("user_id",None)
        paraments['start_time']=post_data.get("start_time",None)
        paraments['end_time'] = post_data.get("start_time",None)
        paraments['url']=post_data.get("url",None)
        sql_connector = mysqlConnector()
        if paraments['start_time'] is None:
            if paraments['url'] == '':
                sql = 'select * from data where user_id = %s'
                values = [paraments['user_id']]
                res = sql_connector.query(sql, values)
            else:
                sql= 'select * from data where user_id = %s and url = %s'
                values = [paraments['user_id'],paraments['url']]
                res = sql_connector.query(sql, values)
        else:
            t = post_data.get('start_time', '')
            t = t[:-6]
            a = t.split("T")
            paraments['start_time'] = a[0] + " " + a[1]
            t = post_data.get('end_time', '')
            t = t[:-6]
            a = t.split("T")
            paraments['end_time'] = a[0] + " " + a[1]
            if paraments['url'] == '':
                #print(1)
                sql = 'select * from data where user_id = %s and start_time between %s and %s'
                values = [paraments['user_id'], paraments['start_time'],paraments['end_time']]
                res = sql_connector.query(sql, values)
            else:
                sql = 'select * from data where user_id = %s and start_time between %s and %s and url = %s'
                values = [paraments['user_id'], paraments['start_time'], paraments['end_time'],paraments['url']]
                res = sql_connector.query(sql, values)
        #print(res)
        reslist=[]
        for i in res:
            js={}
            js['data']=json.loads(i[1])
            js['start_time']=i[2].strftime('%Y-%m-%d %H:%M')
            js['url']=i[3]
            reslist.append(js)
        #print(reslist)
        fin={}
        fin['data']=reslist
        self.write(fin)