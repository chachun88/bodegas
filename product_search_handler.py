#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from model.product import Product

from basehandler import BaseHandler

class ProductSearchHandler(BaseHandler):
	def get(self):
		query = self.get_argument("q", "")

		product = Product()

		self.render("product/list.html", side_menu=self.side_menu, product_list=product.Search(query))

