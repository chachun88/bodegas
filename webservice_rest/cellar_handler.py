#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime

from bson import json_util

from base_handler import BaseHandler
from model10.cellar import Cellar
from model10.kardex import Kardex

class CellarAddHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken(): 
			return

		cellar = Cellar()

		cellar.name = self.get_argument("name", "")
		cellar.description = self.get_argument("description", "")
		cellar.identifier = self.get_argument("id", "")

		self.write(json_util.dumps((cellar.Save())))


class CellarListHandler(BaseHandler):
	"""docstring for CellarListHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		page = self.get_argument("page", 1)
		items = self.get_argument("items", 10)

		self.write(json_util.dumps(Cellar().GetList(int(page), int(items))))
		pass

class CellarRemoveHandler(BaseHandler):
	
	"""docstring for CellarRemoveHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return
		
		idd = self.get_argument("id", "")
		
		cellar = Cellar()
		cellar.InitById(idd)

		self.write(json_util.dumps(cellar.Remove()))
		pass
		

class CellarFindHandler(BaseHandler):
	"""docstring for CellarFindHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		name = self.get_argument("name", "")
		
		cellar = Cellar()

		if idd != "":
			cellar.InitById(idd)
		else:
			cellar.InitByName(name)
		
		self.write(json_util.dumps(cellar.Print()))
		pass

class CellarProductsListHandler(BaseHandler):
	"""docstring for CellarProductsListHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")

		page = self.get_argument("page", 1)
		items = self.get_argument("items", 10)

		cellar = Cellar()
		cellar.InitById(idd)
		self.write(json_util.dumps(cellar.ListProducts(page, items)))
		pass

class CellarProductsAddHandler(BaseHandler):
	"""docstring for CellarProductsAddHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		cellar_id = self.get_argument("cellar_id", "")
		product_id = self.get_argument("product_id", "")
		quantity = self.get_argument("quantity", "0")
		operation = self.get_argument("operation", Kardex.OPERATION_BUY)
		price = self.get_argument("price", "0")

		kardex = Kardex()

		kardex.product_identifier = product_id
		kardex.cellar_identifier = cellar_id
		kardex.date = str(datetime.datetime.now().time().isoformat())

		kardex.operation_type = operation
		kardex.units = float(quantity)
		kardex.price = float(price)

		self.write(json_util.dumps(kardex.Insert()))
		
		'''
		product list sample
		1231233asidoad:10,qoiewiqoej1:1
		'''
		#self.write(cellar.AddProducts(product_list, self.db.cellar_products, self.db.products))
		
class CellarProductsRemoveHandler(BaseHandler):
	"""docstring for CellarProductsRemoveHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		product_list = self.get_argument("products", "")

		cellar = Cellar()
		cellar.InitWithId(idd)

		#self.write(cellar.RemoveProducts(product_list))
		pass