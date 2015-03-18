#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import os

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

from bson import json_util

from basehandler import BaseHandler
from globals import port, debugMode, carpeta_img, userMode, Menu
from model.product import Product
from model.category import Category
from model.brand import Brand
from model.tag import Tag
from model.kardex import Kardex
from model.size import Size
from basehandler import BaseHandler

class ProductAddHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA) #change menu active item

		tags = []
		tag = Tag()
		res_tags = tag.List(1,100000)

		if "success" in res_tags:
			tags = res_tags["success"]

		prod = Product()
		self.render("product/add.html", dn="", side_menu=self.side_menu, product=prod, tit="add", tags=tags)


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
			os.chdir( "uploads/images/" )
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
		img4 = "{}_{}.png".format( 3, self.get_argument("sku", "").encode('utf-8') )
		img5 = "{}_{}.png".format( 4, self.get_argument("sku", "").encode('utf-8') )
		img6 = "{}_{}.png".format( 5, self.get_argument("sku", "").encode('utf-8') )

		if ( "image" in self.request.files ):
			img1 = self.saveImage( self.request.files['image'][0], self.get_argument("sku", ""), 0 )
		if ( "image-1" in self.request.files ):
			img2 = self.saveImage( self.request.files['image-1'][0], self.get_argument("sku", ""), 1 )
		if ( "image-2" in self.request.files ):
			img3 = self.saveImage( self.request.files['image-2'][0], self.get_argument("sku", ""), 2 )
		if ( "image-3" in self.request.files ):
			img3 = self.saveImage( self.request.files['image-3'][0], self.get_argument("sku", ""), 3 )
		if ( "image-4" in self.request.files ):
			img3 = self.saveImage( self.request.files['image-4'][0], self.get_argument("sku", ""), 4 )
		if ( "image-5" in self.request.files ):
			img3 = self.saveImage( self.request.files['image-5'][0], self.get_argument("sku", ""), 5 )

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

		

		res = prod.InitWithId(self.get_argument("sku", ""))

		print res

		# print "type:{} value:{}".format(type(res),res)

		if "success" in res:

			prod.category 	= self.get_argument("category", "")
			prod.sku 		= self.get_argument("sku", "")
			prod.name		= self.get_argument("name", "").encode('utf-8')
			prod.upc		= self.get_argument("upc", "")
			prod.description= self.get_argument("description", "").encode('utf-8')
			prod.brand 		= self.get_argument("brand", "").encode('utf-8')
			prod.manufacturer= self.get_argument("manufacturer", "")
			prod.size_id 		= ",".join(self.get_arguments("size"))
			prod.color 		= self.get_argument("color", "").encode('utf-8')
			prod.material 	= self.get_argument("material", "")
			prod.bullet_1 	= self.get_argument("bullet_1", "")
			prod.bullet_2 	= self.get_argument("bullet_2", "") 
			prod.bullet_3 	= self.get_argument("bullet_3", "")
			prod.currency 	= self.get_argument("currency", "")
			prod.price		= self.get_argument("price", "")
			prod.image 		= img1
			prod.image_2 	= img2
			prod.image_3 	= img3
			prod.image_4    = img4
			prod.image_5    = img5
			prod.image_6    = img6
			prod.sell_price = self.get_argument("sell_price",0)
			prod.delivery   = self.get_argument("delivery","").encode('utf-8')
			prod.which_size = self.get_argument("which_size","").encode('utf-8')
			prod.tags       = ",".join([t.encode("utf-8") for t in self.get_arguments("tags")])
			prod.for_sale   = self.get_argument("for_sale",0)
			prod.promotion_price = self.get_argument("promotion_price", 0)


			# print self.get_arguments("tags")

			res_save = prod.Save("one")

			if "success" in res_save:
				self.redirect("/product/list")
			else:
				# self.redirect("/product/edit?id={}".format(prod.identifier))
				self.write(res_save["error"])

		else:

			
			
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
			prod.image_4	= img4.encode("utf-8")
			prod.image_5 	= img5.encode("utf-8")
			prod.image_6 	= img6.encode("utf-8")
			prod.sell_price = self.get_argument("sell_price",0).encode("utf-8")
			prod.delivery   = self.get_argument("delivery","").encode("utf-8")
			prod.which_size = self.get_argument("which_size","").encode("utf-8")
			prod.for_sale   = self.get_argument("for_sale",0)
			prod.promotion_price = self.get_argument("promotion_price", 0)


			# size_arr = self.get_argument("size", "").split(",")
			# size_arr = [s.encode("utf-8") for s in size_arr]

			prod.size_id	= ",".join([t.encode("utf-8") for t in self.get_arguments("size")])
			prod.tags       = ",".join([t.encode("utf-8") for t in self.get_arguments("tags","")])

			respose = prod.Save("one")

			# print respose
			
			if "success" in respose:
				self.redirect("/product/list")
			else:
				self.write(respose["error"])


class ProductEditHandler(BaseHandler):
 	
 	@tornado.web.authenticated
 	def get(self):
 		self.set_active(Menu.PRODUCTOS_CARGA)

		prod = Product()
		res = prod.InitWithId(self.get_argument("id", ""))

		

		tags = []
		tag = Tag()
		res_tags = tag.List(1,100000)

		sizes = []
		size = Size()
		res_sizes = size.list()

		if "success" in res_sizes:
			sizes = res_sizes["success"]

		if "success" in res_tags:
			tags = res_tags["success"]

		if "success" in res:
			self.render("product/add.html", dn="", side_menu=self.side_menu, product=prod, tit="edit", tags=tags, sizes=sizes)
		else:
			self.render("product/add.html", dn="bpf", side_menu=self.side_menu, product=prod, tit="edit", tags=tags, sizes=sizes)

 		 
class FastEditHandler(BaseHandler):

	@tornado.web.authenticated
	def post(self):

		prod = Product()

		res = prod.InitWithId(self.get_argument("id", ""))

		if "success" in res:

			prod.name		= self.get_argument("name", "").encode('utf-8')
			prod.description= self.get_argument("description", "").encode('utf-8')
			prod.color 		= self.get_argument("color", "").encode('utf-8')
			prod.price= self.get_argument("price", "").encode('utf-8')
			prod.sell_price 	= self.get_argument("sell_price", "").encode('utf-8')
			prod.category = self.get_argument("category","").encode("utf-8")
			prod.sku = self.get_argument("sku","").encode("utf-8")
			prod.manufacturer = self.get_argument("manufacturer","").encode("utf-8")
			prod.brand = self.get_argument("brand","").encode("utf-8")
			prod.delivery = self.get_argument("delivery","").encode("utf-8")
			prod.which_size = self.get_argument("which_size","").encode("utf-8")
			prod.for_sale = self.get_argument("for_sale",0)
			prod.upc = prod.upc.encode("utf-8")
			prod.size = ",".join(prod.size).encode("utf-8")
			prod.size_id = ','.join(str(v) for v in prod.size_id)
			prod.material = prod.material.encode("utf-8")
			prod.bullet_1 = prod.bullet_1.encode("utf-8")
			prod.bullet_2 = prod.bullet_2.encode("utf-8")
			prod.bullet_3 = prod.bullet_3.encode("utf-8")
			prod.currency = prod.currency.encode("utf-8")
			prod.image = prod.image.encode("utf-8")
			prod.image_2 = prod.image_2.encode("utf-8")
			prod.image_3 = prod.image_3.encode("utf-8")
			prod.image_4 = prod.image_4.encode("utf-8")
			prod.image_5 = prod.image_5.encode("utf-8")
			prod.image_6 = prod.image_6.encode("utf-8")
			prod.promotion_price = self.get_argument("promotion_price",0)

			# print "type:{} value:{}".format(type(prod.tags),prod.tags)

			prod.tags = ','.join(str(v) for v in prod.tags)
			
			
			respuesta = prod.Save()

			self.write(respuesta)
				

		else:
			self.write(res)

class ForSaleHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):

		product_id = self.get_argument("product_id","")

		if product_id.isnumeric():
			prod = Product()
			self.write(json_util.dumps(prod.ForSale(product_id)))
		else:
			self.write(json_util.dumps({"error":"Product ID proporcionado es inválido"}))

class CheckStockHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):

		product_id = self.get_argument("product_id", "")
		size_id = self.get_argument("size_id", "")

		if product_id != "":

			if size_id != "":

				kardex = Kardex()
				res_stock = kardex.stockByProductId(product_id, size_id)

				self.write(json_util.dumps(res_stock))

			else:
				self.write(json_util.dumps(self.showError("size_id esta vacio")))

		else:
			self.write(json_util.dumps(self.showError("product_id esta vacio")))
		
		