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
from globals import port, debugMode, domainName, carpeta_img, userMode, Menu
from model.product import Product

from basehandler import BaseHandler

class ProductAddHandler(BaseHandler):

	#@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA) #change menu active item

		prod = Product()
		self.render("product/add.html", side_menu=self.side_menu, product=prod)

	def post(self):
		prod = Product()

		prod.name		= self.get_argument("name", "")
		prod.price 		= self.get_argument("price", "")
		prod.description= self.get_argument("description", "")
		prod.quantity 	= self.get_argument("quantity", "")
		prod.brand 		= self.get_argument("brand", "")
		prod.sku 		= self.get_argument("sku", "")
		prod.category 	= self.get_argument("category", "")

		prod.Save()
		self.redirect("/product?dn=t")

class ProductEditHandler(BaseHandler):
 	"""docstring for ClassName"""
 	def get(self):
 		self.set_active(Menu.PRODUCTOS_CARGA)

		prod = Product()
		prod.InitWithId(self.get_argument("id", ""))
		self.render("product/add.html", side_menu=self.side_menu, product=prod)

 		 
		

