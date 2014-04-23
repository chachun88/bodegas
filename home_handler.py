 #!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import pymongo

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import xlrd #lib excel
import os
import commands
import cgi, cgitb
import cgi, os
import cgitb; cgitb.enable()
import sys

from tornado.options import define, options

from basehandler import BaseHandler
from model.product import Product
from globals import port, debugMode, domainName, carpeta_img, userMode, Menu

class HomeHandler(BaseHandler):

	fn =''

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA_MASIVA) #change menu active item

		dn = self.get_argument("dn", "f")

		self.render("product/home.html", side_menu=self.side_menu, dn=dn)

	def post(self):
		
		#upload file 
		try: # Windows needs stdio set for binary mode.
		    import msvcrt
		    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
		except ImportError:
		    pass

		  
		form = cgi.FieldStorage()
		
		# A nested FieldStorage instance holds the file
		fileitem = self.request.files['file'][0]
	
		# strip leading path from file name to avoid directory traversal attacks
		global fn 
		fn = fileitem['filename']
		
		#print fn 
		open('uploads/entradas_masivas/' + fn, 'wb').write(fileitem["body"])
		#message = 'The file "' + fn + '" was uploaded successfully'

		try:
			dn = self.get_argument("dn", "f")
		
			doc = xlrd.open_workbook('uploads\\entradas_masivas\\'+fn)

			sheet = doc.sheet_by_index(0)

			nrows = sheet.nrows
			ncols = sheet.ncols
			#print ncols
			#self.write("{}".format(ncols))

			matriz=[]

			for i in range(nrows):
				matriz.append([])
				for j in range(ncols):
					matriz[i].append(sheet.cell_value(i,j))

			self.render("product/home.html", side_menu=self.side_menu, dn=dn, matriz=matriz, nrows=nrows, ncols=ncols)

		except ImportError:
			pass

class ProductLoadHandler(BaseHandler):
	def get(self):
		pass

	def post(self):	

		doc = xlrd.open_workbook('uploads\\entradas_masivas\\'+fn)

		sheet = doc.sheet_by_index(0)

		nrows = sheet.nrows
		ncols = sheet.ncols
		#print ncols
		#self.write("{}".format(ncols))

		matriz=[]

		prod = Product()

		for i in range(nrows):
			matriz.append([])
			for j in range(ncols):				
				matriz[i].append(sheet.cell_value(i,j))
				if i > 3:
					if j == 0:
						prod.category = matriz[i][j]
					elif j == 1:
						prod.sku = str(int(matriz[i][j]))
					elif j == 2:
						prod.name = matriz[i][j]
					elif j == 3:
						prod.description = matriz[i][j]
					elif j == 5:
						prod.price = str(int(matriz[i][j]))
					elif j == 9:
						prod.brand = matriz[i][j]
			prod.Save()	

		self.write("{}".format(prod.category))		

		#self.redirect("/product/list")				
				
		#self.write("{}".format(matriz[4][0]))

		#prod = Product()

		#prod.name		= self.get_argument("name", "")
		#prod.price 		= self.get_argument("price", "")
		#prod.description= self.get_argument("description", "")
		#prod.quantity 	= self.get_argument("quantity", "")
		#prod.brand 		= self.get_argument("brand", "")
		#prod.sku 		= self.get_argument("sku", "")
		#prod.category 	= self.get_argument("category", "")

		#prod.Save()


		self.redirect("/")	

class ProductRemoveHandler(BaseHandler):
	
	def get(self):

		prod = Product()
		prod.InitWithId(self.get_argument("id", ""))
		prod.Remove()		

		self.redirect("/product/list")
