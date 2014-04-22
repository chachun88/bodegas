#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from base_handler import BaseHandler

class DocHandler(BaseHandler):
	def get(self):
		self.render("base.html")


class DocCellarHandler(BaseHandler):
	"""docstring for DocCellarHandler"""
	def get(self):
		self.render("cellar.html")
		

class DocBrandHandler(BaseHandler):
	"""docstring for DocCellarHandler"""
	def get(self):
		self.render("brand.html")
		

class DocCategoryHandler(BaseHandler):
	"""docstring for DocCellarHandler"""
	def get(self):
		self.render("category.html")
		

class DocSalesmanHandler(BaseHandler):
	"""docstring for DocCellarHandler"""
	def get(self):
		self.render("salesman.html")
		