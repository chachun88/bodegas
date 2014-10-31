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
		cellar.id = self.get_argument("id", "")
		cellar.city = self.get_argument("city",0)

		self.write(json_util.dumps((cellar.Save())))


class CellarListHandler(BaseHandler):
	"""docstring for CellarListHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		page = self.get_argument("page", 1)
		items = self.get_argument("items", 10)

		self.write(Cellar().GetList(int(page), int(items)))
		

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
		response_obj = cellar.InitById(idd)

		if "success" in response_obj:
			self.write(json_util.dumps(cellar.ListProducts(page, items)))
		else:
			self.write(response_obj["error"])

class CellarProductsKardex(BaseHandler):
	"""docstring for CellarProductsListHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		page = self.get_argument("page", 1)
		items = self.get_argument("items", 10)
		day= self.get_argument("day","")
		fromm= self.get_argument("from","")
		until= self.get_argument("until","")

		cellar = Cellar()
		self.write(json_util.dumps(cellar.ListKardex(page, items, day, fromm, until)))
		pass		

class CellarProductsAddHandler(BaseHandler):
	"""docstring for CellarProductsAddHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		cellar_id = self.get_argument("cellar_id", "")
		product_sku = self.get_argument("product_sku", "")
		quantity = self.get_argument("quantity", 0)
		operation = self.get_argument("operation", Kardex.OPERATION_BUY)
		price = self.get_argument("price", 0)
		size = self.get_argument("size", "")
		color = self.get_argument("color", "")
		user = self.get_argument("user", "")

		# self.write(quantity)

		kardex = Kardex()

		kardex.product_sku = product_sku
		kardex.cellar_identifier = cellar_id
		kardex.date = str(datetime.datetime.now().isoformat())

		kardex.operation_type = operation
		kardex.units = quantity
		kardex.price = price
		kardex.size = size

		print color

		kardex.color= color
		kardex.user = user

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

class CellarExistsHandler(BaseHandler):
	
	def get(self):
		#validate access token
		cellar_name = self.get_argument("cellar_name", "")
		cellar_exist = Cellar.CellarExists( cellar_name )

		self.write( json_util.dumps( { "exists" : cellar_exist } ) )
		pass

class CellarProductFind(BaseHandler):
	
	def get(self):
		if not self.ValidateToken():
			return

		cellar_id = self.get_argument("cellar_id", "")
		product_sku = self.get_argument("product_sku", "")
		size = self.get_argument("size", "")

		cellar = Cellar()
		self.write(json_util.dumps(cellar.FindProductKardex(product_sku, cellar_id, size)))
		pass