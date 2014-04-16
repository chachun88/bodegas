#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from bson import json_util

from base_handler import BaseHandler
from model10.cellar import Cellar

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
		
		cellar = Cellar()
		cellar.InitById(idd)
		
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
		cellar.InitWithId(idd)
		self.write(cellar.ListProducts(page, items))
		pass

class CellarProductsAddHandler(BaseHandler):
	"""docstring for CellarProductsAddHandler"""
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return
		
		idd = self.get_argument("id", "")
		product_list = self.get_argument("products", "")

		cellar = Cellar()
		cellar.InitWithId(idd)
		
		'''
		product list sample
		1231233asidoad:10,qoiewiqoej1:1
		'''
		#self.write(cellar.AddProducts(product_list, self.db.cellar_products, self.db.products))
		pass
		
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