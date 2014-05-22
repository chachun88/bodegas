#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from globals import Menu
from model.cellar import Cellar
from model.product import Product

class ReportHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.INFORMES_POR_BODEGA)
		# data = Cellar().List(1, 10)
		cellar = Cellar().List(1, 10)
		data = Cellar().ListKardex()
		product = Product().get_product_list()
		self.render("report/home.html", side_menu=self.side_menu, data=data, product=product, cellar=cellar)