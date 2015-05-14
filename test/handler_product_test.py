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


class TestProduct(unittest.TestCase): 
    http_server = None
    response = None 

    def setUp(self):
        app = Application()
        self.http_server = tornado.httpserver.HTTPServer(app) 
        self.http_server.listen(9008) 

    def tearDown(self):
        self.http_server.stop()

    def handle_request(self, response): 
        self.response = response 
        tornado.ioloop.IOLoop.instance().stop() 

    def testAddProductHandler(self):

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/product/add", 
            self.handle_request
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.code, 200)


        body = '''sku=GDF-PV14-Sirisi-C2'''
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(
            "http://localhost:9008/product/add", 
            self.handle_request
        )
        tornado.ioloop.IOLoop.instance().start()
        self.failIf(self.response.error)
        self.assertEqual(self.response.code, 200)
