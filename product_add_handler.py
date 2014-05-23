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

import xlrd #lib excel
import os
import commands
import cgi, cgitb
import cgi, os
import cgitb; cgitb.enable()
import sys

from basehandler import BaseHandler
from globals import port, debugMode, carpeta_img, userMode, Menu
from model.product import Product
from model.category import Category
from model.brand import Brand

from basehandler import BaseHandler

class ProductAddHandler(BaseHandler):

	#@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA) #change menu active item

		prod = Product()
		self.render("product/add.html", side_menu=self.side_menu, product=prod)

	def post(self):
		try: # Windows needs stdio set for binary mode.
		    import msvcrt
		    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
		except ImportError:
		    pass

		fn =""    
		try:   
			form = cgi.FieldStorage()
			
			# A nested FieldStorage instance holds the file
			fileitem = self.request.files['image'][0]
		
			# strip leading path from file name to avoid directory traversal attacks
			fn = fileitem['filename']
		except:
			pass

		if fn != "":
			#print fn 
			open('uploads/images/' + self.get_argument("sku", "")+'.png', 'wb').write(fileitem["body"])
			image_name=self.get_argument("sku", "")+'.png'
		else:
			image_name=''

		##if the category does not exist is created
		category = Category()

		try:
			category.InitWithName(self.get_argument("category", ""))
		except:		
			category.name = self.get_argument("category", "")
			category.Save()
		
		##if the brand does not exist is created
		brand=Brand()	

		try:
			brand.InitWithName(self.get_argument("brand", ""))
		except:		
			brand.name = self.get_argument("brand", "")
			brand.Save()	

		prod = Product()

		prod.category 	= self.get_argument("category", "")
		prod.sku 		= self.get_argument("sku", "")
		prod.name		= self.get_argument("name", "")
		prod.upc		= self.get_argument("upc", "")
		prod.description= self.get_argument("description", "")
		prod.brand 		= self.get_argument("brand", "")
		prod.manufacturer= self.get_argument("manufacturer", "")
		prod.size 		= self.get_argument("size", "").split(",")
		prod.color 		= self.get_argument("color", "").split(",")
		prod.material 	= self.get_argument("material", "")
		prod.bullet_1 	= self.get_argument("bullet_1", "")
		prod.bullet_2 	= self.get_argument("bullet_2", "")
		prod.bullet_3 	= self.get_argument("bullet_3", "")
		prod.currency 	= self.get_argument("currency", "")
		prod.image 		= image_name
		prod.image2 	= self.get_argument("image2", "")
		prod.image3 	= self.get_argument("image3", "")

		prod.Save()
		self.redirect("/product/list")

class ProductEditHandler(BaseHandler):
 	"""docstring for ClassName"""
 	def get(self):
 		self.set_active(Menu.PRODUCTOS_CARGA)

		prod = Product()
		prod.InitWithId(self.get_argument("id", ""))
		self.render("product/add.html", side_menu=self.side_menu, product=prod)

 		 
		

