import tornado.web
from mysqlConnector import mysqlConnector
import miner.grabid
import miner.grabcontent
import miner.finalgrab
import json
import datetime
def todo():
    return
class minerConfigHandler(tornado.web.RequestHandler):
    error_code=""
    def post(self,*args,**kwargs):
        paraments={}
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        paraments['user_id']=post_data.get('user_id','')
        paraments['urls']=post_data.get('urls',[])
        paraments['header']=post_data.get('header',{})
        paraments['antiminer']=post_data.get('antiminer',False)
        paraments['miner_param'] = post_data.get('miner_param', {})
        paraments['timing']=post_data.get('timing','')
        if(paraments['timing']=="instant"):
            paraments['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(paraments)
        get=miner.finalgrab.spider(
            paraments['user_id'],
            paraments['urls'],
            paraments['header'],
            paraments['antiminer'],
            paraments['miner_param'],
            paraments['timing'],
            paraments['start_time']
        )
        print(type(get))
        print(json.dumps(get))
        s=[]
        for i in get:
            s.append({'url':i,'data':get[i]})
        sql_connector = mysqlConnector()
        sql = 'insert into data (user_id,data,start_time,url) values (%s,%s,%s,%s);'
        if(paraments['timing']=='instant'):
            paraments['start_time']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            t = post_data.get('start_time', '')
            t = t[:-6]
            a = t.split("T")
            paraments['start_time'] = a[0] + " " + a[1]
        flag=0
        print(s)
        for i in s:
            values=[paraments['user_id'],json.dumps(i['data']), paraments['start_time'],i['url']]
            res = sql_connector.executeSql(sql, values)
            if(res!=None):
                flag=1
                err=res
        if flag==0:
            self.write("OK")
        else:
            self.write(str(err))
        '''values = [paraments['user_id'], paraments['start_time']]
        res = sql_connector.executeSql(sql, values)
        print(res)
        if (res == None):
            self.write("OK")
        else:
            res = str(res)
            self.write(res)'''

    #def check(self,paraments):
        #if(paraments['account_id']==None or paraments['password']==None):
        #    self.error_code="输入参数缺失"
        #    return 0
        #return 1
def write1():
    f = open('test', mode='w', encoding='utf-8')
    data={ "project_name":"吉林大学中日联谊医院汽化过氧化氢发生器设备采购项目","money":"66.0000000（万元）"}
    json.dump(data, f, ensure_ascii=False, indent=4)
    return
def write0():
    f = open('test', mode='w', encoding='utf-8')
    data = {"project_name": "吉林大学中日联谊医院汽化过氧化氢发生器设备采购项目"}
    json.dump(data, f, ensure_ascii=False, indent=4)
    return
def write2():
    f = open('test', mode='w', encoding='utf-8')
    data = {"s_index_off_css": '''<style data-for="result" id="css_result" type="text/css">#ftCon{display:none}
#qrcode{display:none}
#pad-version{display:none}
#index_guide{display:none}
#index_logo{display:none}
#u1{display:none}
.s-top-left{display:none}
.s_ipt_wr{height:32px}
body{padding:0}
#head .c-icon-bear-round{display:none}
.index_tab_top{display:none}
.index_tab_bottom{display:none}
#lg{display:none}
#m{display:none}
#ftCon{display:none}
#bottom_layer,#bottom_space,#s_wrap{display:none}
.s-isindex-wrap{display:none}
#nv{display:none!important}
#head .head_wrapper{display:block;padding-top:0!important}
.s-bottom-ctner{display:none!important}
#head .s-upfunc-menus{display:none}
#s_skin_upload{display:none}</style>'''}
    json.dump(data, f, ensure_ascii=False, indent=4)
    return