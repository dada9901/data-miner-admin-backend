import tornado.ioloop
import tornado.web
import registerHandler
import loginHandler
import resetPasswordHandler
import tornado.httpserver
from config import options
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Index")
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/register",registerHandler.registerHandler),
        (r"/login",loginHandler.loginHandler),
        (r"/resetpassword",resetPasswordHandler.resetPasswordHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(options['port'])
    tornado.ioloop.IOLoop.current().start()