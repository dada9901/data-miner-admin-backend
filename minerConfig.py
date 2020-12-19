import tornado.web
from mysqlConnector import mysqlConnector
import miner.grabid
import miner.grabcontent
import json
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
        #paraments['account_id']=post_data.get('account_id',None)
        '''paraments['time']=post_data.get('time',None)
        if(paraments['time']==0):
            write0()
        if(paraments['time']==1):
            write1()
        if(paraments['time']==2):
            write2()
        if(paraments['time']>=3):
            miner.grabid.run('a','b')
        self.write('1111')
        return'''
        paraments['url']=post_data.get('url',None)
        paraments['request_method']=post_data.get('request_method',None)
        paraments['antiminer']=post_data.get('antiminer',None)
        if(paraments['antiminer']=='True'):
            paraments['header']=post_data.get('header',None)
        paraments['miner_method'] = post_data.get('miner_method', None)
        if(paraments['miner_method']=='content'):
            write1()
            return
            paraments['content']=post_data.get('content',None)
        elif(paraments['miner_method']=='style'):
            write2()
            return
            paraments['get_by_id']=post_data.get('get_by_id',None)
            paraments['get_by_table'] = post_data.get('get_by_table', None)
            paraments['get_by_pic']=post_data.get('get_by_pic',None)
        paraments['timing']=post_data.get('timing',None)
        if(paraments['timing']!='instant'):
            paraments['start_time']=post_data.get('start_time',None)
            paraments['interval']=post_data.get('interval',None)
        #if(self.check(paraments)==0):
            #self.write(self.error_code)
        sql_connector=mysqlConnector()
        '''sql='select * from user where account_id = %s and password = %s;'
        values=[paraments['account_id'],paraments['password']]
        res=sql_connector.query(sql,values)
        if(type(res)==tuple and len(res)==1):
            self.write("OK")
        else:
            res='输入的账号或密码不存在'
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