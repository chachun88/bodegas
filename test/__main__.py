# import unittest

# from test.model_kardex_test import ModelKardexTest

from config import *
# from lp.globals import *
# from tornado.options import define

# define("protocol", default="https", help="run on the given port", type=str)

# define("db_name", default=ONTEST_DB_NAME, help="", type=str)
# define("db_user", default=ONTEST_USER, help="", type=str)
# define("db_host", default=ONTEST_HOST, help="", type=str)
# define("db_password", default=ONTEST_PASSWORD, help="", type=str)

# # import dbscripts.ontest_schema_loader

# if __name__ == "__main__":
#     unittest.main()

import authenticated
import tornado.httpserver 
import tornado.httpclient 
import tornado.ioloop 
import tornado.web 
import unittest
from tornado.options import define, options
import mock
from bodegas import Application

define("protocol", default="https", help="run on the given port", type=str)

define("db_name", default=ONTEST_DB_NAME, help="", type=str)
define("db_user", default=ONTEST_USER, help="", type=str)
define("db_host", default=ONTEST_HOST, help="", type=str)
define("db_password", default=ONTEST_PASSWORD, help="", type=str)


class MainHandler(tornado.web.RequestHandler): 
    def get(self): 
        self.write('Hello, world...')

    def post(self):
        self.write(self.get_argument("arg"))


class TestTornadoWeb(unittest.TestCase): 
    http_server = None                                                                                                                                                                                                                                                                                                                                                    
    response = None 

    def setUp(self): 

        # application = tornado.web.Application([ 
        #         (r'/', MainHandler), 
        #         ])  
        self.http_server = tornado.httpserver.HTTPServer(Application()) 
        self.http_server.listen(options.port) 

    def tearDown(self):
        self.http_server.stop()

    def handle_request(self, response): 
        self.response = response 
        tornado.ioloop.IOLoop.instance().stop() 

    def testHelloWorldHandler(self): 

        http_client = tornado.httpclient.AsyncHTTPClient() 
        http_client.fetch('http://localhost:9008/auth/login', self.handle_request, method="POST", body="user=yi.neko@gmail.com&password=chachun88") 
        print self.response
        tornado.ioloop.IOLoop.instance().start() 
        self.failIf(self.response.error) 
        self.assertEqual(self.response.code, 200)

    # def testHelloWorldHandler2(self): 
    #     http_client = tornado.httpclient.AsyncHTTPClient() 
    #     http_client.fetch('http://localhost:9008/', self.handle_request) 
    #     tornado.ioloop.IOLoop.instance().start() 
    #     self.failIf(self.response.error) 
    #     self.assertEqual(self.response.body, 'Hello, world') 

if __name__ == '__main__': 
    unittest.main() 