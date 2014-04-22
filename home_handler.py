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

	#@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA_MASIVA) #change menu active item

		dn = self.get_argument("dn", "f")

		# doc = xlrd.open_workbook('uploads\\entradas_masivas\\Planilla Tipo Inventario.xlsx')
		# sheet = doc.sheet_by_index(0)

		# nrows = sheet.nrows
		# ncols = sheet.ncols


		# matriz=[]

		# for i in range(nrows):
		# 	matriz.append([])
		# 	for j in range(ncols):
		# 		matriz[i].append(sheet.cell_value(i,j))
		# #self.write("{}".format(matriz[3][4].encode('ascii', 'ignore')))			

		# for i in range(nrows):
		# 	string = ''
		# 	for j in range(ncols):
		# 		string += '%st'%sheet.cell_value(i,j)
			#self.write("{}".format(string.encode('ascii', 'ignore')))
			#print(string)
		#self.render("product/home.html", side_menu=self.side_menu, dn=dn, matriz=matriz, nrows=nrows, ncols=ncols)	
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
		fn = fileitem['filename']

		#print fn 
		open('uploads/entradas_masivas/' + fn, 'wb').write(fileitem["body"])
		#message = 'The file "' + fn + '" was uploaded successfully'

		# self.set_active(Menu.PRODUCTOS_CARGA_MASIVA) #change menu active item

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
		print "llega load"		

class ProductRemoveHandler(BaseHandler):
	
	def get(self):

		prod = Product()
		prod.InitWithId(self.get_argument("id", ""))
		prod.Remove()		

		self.redirect("/product/list")
