import tornado.web
from mysqlConnector import mysqlConnector
import miner.grabid
import miner.grabcontent
import miner.finalgrab
import json
import datetime
def todo():
    return
class siteHandler(tornado.web.RequestHandler):
    error_code=""
    def post(self,*args,**kwargs):
        paraments={}
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        paraments['domain']=post_data.get('domain','')
        paraments['prefix']=post_data.get('prefix',"")
        paraments['rehtml']=post_data.get('rehtml',"")
        paraments['template']=post_data.get('template',"")
        paraments['maxpage'] = int(post_data.get('maxpage',""))
        paraments['firstpage']=post_data.get('firstpage','')
        res=miner.finalgrab.grab_urls(paraments['domain'],paraments['prefix'],paraments['rehtml'],paraments['template'],max_page=paraments['maxpage'],first_page=paraments['firstpage'])
        print(paraments)
        self.write({"data":res})