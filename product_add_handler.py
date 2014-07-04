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
		self.render("product/add.html", side_menu=self.side_menu, product=prod, tit="add")


	def saveImage( self, imagedata, sku, image_number ):

		final_name = "{}_{}.png".format( image_number, sku )

		try:
			fn = imagedata["filename"]
			file_path = 'uploads/images/' + final_name

			open(file_path, 'wb').write(imagedata["body"])
		except Exception, e:
			print "herreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
			print str(e)
			pass

		return final_name


	def post(self):
		try: # Windows needs stdio set for binary mode.
		    import msvcrt
		    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
		except ImportError:
		    pass

		''' 
		fn =""    
		try:   
			form = cgi.FieldStorage()
			
			# A nested FieldStorage instance holds the file
			fileitem = self.request.files['image'][0]

			for i in self.request.files:
				self.write("llega : {} <br>".format( self.request.files[i][0]["filename"] ))
		
			# strip leading path from file name to avoid directory traversal attacks
			fn = fileitem['filename']
		except:
			pass

		return
		'''

		'''
		if fn != "":
			#print fn 
			open('uploads/images/' + self.get_argument("sku", "")+'.png', 'wb').write(fileitem["body"])
			image_name=self.get_argument("sku", "")+'.png'
		else:
			image_name=''
		'''

		img1 = "{}_{}.png".format( 0, self.get_argument("sku", "") )
		img2 = "{}_{}.png".format( 1, self.get_argument("sku", "") )
		img3 = "{}_{}.png".format( 2, self.get_argument("sku", "") )

		if ( "image" in self.request.files ):
			img1 = self.saveImage( self.request.files['image'][0], self.get_argument("sku", ""), 0 )
		if ( "image-1" in self.request.files ):
			img2 = self.saveImage( self.request.files['image-1'][0], self.get_argument("sku", ""), 1 )
		if ( "image-2" in self.request.files ):
			img3 = self.saveImage( self.request.files['image-2'][0], self.get_argument("sku", ""), 2 )

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
		prod.price		= self.get_argument("price", "")
		prod.image 		= img1
		prod.image_2 	= img2
		prod.image_3 	= img3

		prod.Save("one")
		self.redirect("/product/list")

class ProductEditHandler(BaseHandler):
 	"""docstring for ClassName"""
 	def get(self):
 		self.set_active(Menu.PRODUCTOS_CARGA)

		prod = Product()
		prod.InitWithId(self.get_argument("id", ""))
		self.render("product/add.html", side_menu=self.side_menu, product=prod, tit="edit")

 		 
		

