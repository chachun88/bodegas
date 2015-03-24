#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import pymongo

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from basehandler import BaseHandler
from globals import port, debugMode, carpeta_img, userMode, Menu

from basehandler import BaseHandler

from model.product import Product

class ProductListHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_LISTA) #change menu active item

		product = Product()

		self.render("product/list.html", dn="", side_menu=self.side_menu, product_list=product.get_product_list())