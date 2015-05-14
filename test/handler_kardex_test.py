#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from bodegas import Application
from bson import json_util
from lp.model.basemodel import BaseModel
import authenticated
import tornado.web
import tornado.ioloop 
import tornado.httpclient
import tornado.httpserver
import urllib


class TestStock(unittest.TestCase): 
    http_server = None
    response = None 

    def setUp(self): 

        # application = tornado.web.Application([ 
        #         (r'/', MainHandler), 
        #         ])

        query = '''delete from "Kardex" where id > 2897;'''
        BaseModel.execute_query(query)

        app = Application()
        self.http_server = tornado.httpserver.HTTPServer(app) 
        self.http_server.listen(9008) 
        # self.request = tornado.web.RequestHandler(app, "http://localhost:9008/cellar")
        # self.request.set_secure_cookie("user_bodega", json_util.dumps({"cellar_permissions":[1,2,3,4,5,6]}))

    def tearDown(self):
        query = '''update "Order" set state = 3 where user_id = 733;'''
        BaseModel.execute_query(query)
        self.http_server.stop()

    def handle_request(self, response): 
        self.response = response 
        tornado.ioloop.IOLoop.instance().stop() 

    def testAddStockHandler(self):

        # cellar_id = self.get_argument("cellar_id", "")
        # sku = self.get_argument("sku", "")
        # quantity = self.get_argument("quantity", "")
        # price = self.get_argument("price", "")
        # size = self.get_argument("size", "")
        # operation = self.get_argument("operation", "")
        # new_cellar = self.get_argument("new_cellar", "")

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C39&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.body, json_util.dumps({"state": "ok", "message": "Stock agregado exitosamente"}))

    def testAddStockNotFoundHandler(self):

        # cellar_id = self.get_argument("cellar_id", "")
        # sku = self.get_argument("sku", "")
        # quantity = self.get_argument("quantity", "")
        # price = self.get_argument("price", "")
        # size = self.get_argument("size", "")
        # operation = self.get_argument("operation", "")
        # new_cellar = self.get_argument("new_cellar", "")

        body = '''cellar_id=yuiu&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertNotEqual(self.response.body, json_util.dumps({"state": "ok", "message": "Stock agregado exitosamente"}))

    def testAddStockNonExistingCellarHandler(self):

        # cellar_id = self.get_argument("cellar_id", "")
        # sku = self.get_argument("sku", "")
        # quantity = self.get_argument("quantity", "")
        # price = self.get_argument("price", "")
        # size = self.get_argument("size", "")
        # operation = self.get_argument("operation", "")
        # new_cellar = self.get_argument("new_cellar", "")

        body = '''cellar_id=10000&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertNotEqual(self.response.body, json_util.dumps({"state": "ok", "message": "Stock agregado exitosamente"}))

    def testAddStockCeroItemHandler(self):

        # cellar_id = self.get_argument("cellar_id", "")
        # sku = self.get_argument("sku", "")
        # quantity = self.get_argument("quantity", "")
        # price = self.get_argument("price", "")
        # size = self.get_argument("size", "")
        # operation = self.get_argument("operation", "")
        # new_cellar = self.get_argument("new_cellar", "")

        body = '''cellar_id=14&sku=GDF-OI14-Queltehue-C39&quantity=0&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.body, json_util.dumps({"state": "error", "message": "Debe ingresar cantidad de productos"}))

    def testAddStockPriceZeroHandler(self):

        # cellar_id = self.get_argument("cellar_id", "")
        # sku = self.get_argument("sku", "")
        # quantity = self.get_argument("quantity", "")
        # price = self.get_argument("price", "")
        # size = self.get_argument("size", "")
        # operation = self.get_argument("operation", "")
        # new_cellar = self.get_argument("new_cellar", "")

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C39&quantity=1&price=0&operation=buy&size=35'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.body, json_util.dumps({"state": "ok", "message": "Stock agregado exitosamente"}))

    def testRemoveStockHandler(self):

        # self.testAddStockHandler()

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C39&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C39&quantity=1&price=69900&size=35&operation=sell'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.body, json_util.dumps({"state": "ok", "message": "Stock sacado exitosamente"}))

    def testMoveStockHandler(self):

        # self.testAddStockHandler()

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C39&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C39&quantity=1&price=69900&size=35&operation=mov&new_cellar=12'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.body, json_util.dumps({"state": "ok", "message": "Stock movido exitosamente"}))

    def testSaveShipping(self):

        # arr_tracking_code = self.get_arguments("tracking_code")

        # arr_provider_id = self.get_arguments("provider_id")

        # arr_order_id = self.get_arguments("order_id")

        body = '''cellar_id=5&sku=GDF-PV14-Kereu-C6&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C30&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()

        body = '''cellar_id=5&sku=GDF-OI14-Queltehue-C39&quantity=3&price=33558&size=35&operation=buy'''

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/cellar/easy", 
            self.handle_request,
            body=body,
            method="POST"
        )
        tornado.ioloop.IOLoop.instance().start()

        params = urllib.urlencode({"tracking_code":['2345678fghjkl','jhgfds65'], "provider_id":[1,2], "order_id":[262, 261]}, True)

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/shipping/save_tracking?{}".format(params), 
            self.handle_request,
            method='GET'
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.body, json_util.dumps([]))

    def testCancelOrders(self):

        # def post(self):
        # valores = self.get_argument("values", "").split(",")
        # accion = self.get_argument("action","")

        params = urllib.urlencode({"values":'262,261', "action":5}, True)

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/orders/actions",
            self.handle_request,
            method='POST',
            body=params
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.body, json_util.dumps([{"success": "orden 262 ha cambiado de estado exitosamente"}, {"success": "orden 261 ha cambiado de estado exitosamente"}]))

    def testMassiveStockFail(self):

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/product/massiveoutput",
            self.handle_request,
            method='POST',
            body='filename=test_malo.xlsx',
            follow_redirects=True
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)

        self.assertNotEqual(self.response.effective_url, "http://localhost:9008/product?dn=t")

    def testMassiveStockSuccess(self):

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/product/massiveoutput",
            self.handle_request,
            method='POST',
            body='filename=test_bueno.xlsx',
            follow_redirects=True
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)

        self.assertEqual(self.response.effective_url, "http://localhost:9008/product?dn=t")