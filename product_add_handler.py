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
import glob

from basehandler import BaseHandler
from globals import port, debugMode, carpeta_img, userMode, Menu
from model.product import Product
from model.category import Category
from model.brand import Brand

from basehandler import BaseHandler

class ProductAddHandler(BaseHandler):

	global load

	load="new"	

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA) #change menu active item

		prod = Product()
		self.render("product/add.html", dn="", side_menu=self.side_menu, product=prod, tit="add")


	def saveImage( self, imagedata, sku, image_number ):

		final_name = "{}_{}.png".format( image_number, sku )

		try:
			fn = imagedata["filename"]

			# print "filename:{}".format(fn)

			file_path = 'uploads/images/' + final_name

			self.deleteOtherImages( final_name )

			open(file_path, 'wb').write(imagedata["body"])

		except Exception, e:
			print str(e)
			pass

		return final_name

	def deleteOtherImages(self, image_name):
		
		identificador = self.get_argument("id","")

		# print "files {}".format( image_name )
		
		if image_name != "":
			os.chdir( "uploads/images" )
			for file in glob.glob("*" + image_name):
				try:
					os.remove( file )
				except Exception, e:
					print "no se elimino : {}".format( str(e) )
					pass

			os.chdir("../../")

			self.write("imagen eliminada")
		else:
			self.write( "imagen no existe " )


	@tornado.web.authenticated
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

		img1 = "{}_{}.png".format( 0, self.get_argument("sku", "").encode('utf-8') )
		img2 = "{}_{}.png".format( 1, self.get_argument("sku", "").encode('utf-8') )
		img3 = "{}_{}.png".format( 2, self.get_argument("sku", "").encode('utf-8') )

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


		try:
			res = prod.InitWithSku(self.get_argument("sku", ""))

			if res != "ok":

				if prod.sku and load=="old":

					prod.category 	= self.get_argument("category", "")
					prod.sku 		= self.get_argument("sku", "")
					prod.name		= self.get_argument("name", "").encode('utf-8')
					prod.upc		= self.get_argument("upc", "")
					prod.description= self.get_argument("description", "")
					prod.brand 		= self.get_argument("brand", "")
					prod.manufacturer= self.get_argument("manufacturer", "")
					prod.size 		= self.get_argument("size", "").split(",")
					prod.color 		= self.get_argument("color", "")
					prod.material 	= self.get_argument("material", "")
					prod.bullet_1 	= self.get_argument("bullet_1", "")
					prod.bullet_2 	= self.get_argument("bullet_2", "") 
					prod.bullet_3 	= self.get_argument("bullet_3", "")
					prod.currency 	= self.get_argument("currency", "")
					prod.price		= self.get_argument("price", "")
					prod.image 		= img1
					prod.image_2 	= img2
					prod.image_3 	= img3
					prod.sell_price = self.get_argument("sell_price",0)
					

					tags = self.get_argument("tags","").split(",")
					tags = [t.encode("utf-8") for t in tags]
					

					prod.tags       = ",".join(tags) # entra como string



					prod.Save("one")
					self.redirect("/product/list")	
				else:
					self.render("product/add.html", dn="bpf", side_menu=self.side_menu, product=prod, tit="add")

			else:

				self.render("product/add.html", dn="bpf", side_menu=self.side_menu, product=prod, tit="add")

		except Exception,e:

			print str(e)
			
			prod.category 	= self.get_argument("category", "").encode("utf-8")
			prod.sku 		= self.get_argument("sku", "").encode("utf-8")
			prod.name		= self.get_argument("name", "").encode("utf-8")
			prod.upc		= self.get_argument("upc", "").encode("utf-8")
			prod.description= self.get_argument("description", "").encode("utf-8")
			prod.brand 		= self.get_argument("brand", "").encode("utf-8")
			prod.manufacturer= self.get_argument("manufacturer", "").encode("utf-8")
			
			prod.color 		= self.get_argument("color", "").encode("utf-8")
			prod.material 	= self.get_argument("material", "").encode("utf-8")
			prod.bullet_1 	= self.get_argument("bullet_1", "").encode("utf-8")
			prod.bullet_2 	= self.get_argument("bullet_2", "").encode("utf-8")
			prod.bullet_3 	= self.get_argument("bullet_3", "").encode("utf-8")
			prod.currency 	= self.get_argument("currency", "").encode("utf-8")
			prod.price		= self.get_argument("price", "").encode("utf-8")
			prod.image 		= img1.encode("utf-8")
			prod.image_2 	= img2.encode("utf-8")
			prod.image_3 	= img3.encode("utf-8")
			prod.sell_price = self.get_argument("sell_price",0).encode("utf-8")


			size_arr = self.get_argument("size", "").split(",")
			size_arr = [s.encode("utf-8") for s in size_arr]

			tags_arr = self.get_argument("tags", "").split(",")
			tags_arr = [s.encode("utf-8") for s in tags_arr]

			prod.size 		= ",".join(size_arr)
			prod.tags       = ",".join(tags_arr) # entra como string

			respose = prod.Save("one")

			# print respose
			
			self.redirect("/product/list")

class ProductEditHandler(BaseHandler):
 	"""docstring for ClassName"""
 	def get(self):
 		self.set_active(Menu.PRODUCTOS_CARGA)

 		global load

 		load="old"

		prod = Product()
		res = prod.InitWithId(self.get_argument("id", ""))
		if res == "ok":
			self.render("product/add.html", dn="", side_menu=self.side_menu, product=prod, tit="edit")
		else:
			self.render("product/add.html", dn="bpf", side_menu=self.side_menu, product=prod, tit="edit")

 		 
		

