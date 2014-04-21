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

from tornado.options import define, options

from basehandler import BaseHandler
from model.product import Product
from globals import port, debugMode, domainName, carpeta_img, userMode, Menu

class HomeHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA_MASIVA) #change menu active item

		dn = self.get_argument("dn", "f")
		

		doc = xlrd.open_workbook(r'C:\\Users\\Estefi\\Desktop\\git\\bodegas\\static\\Planilla Tipo Inventario.xlsx')
		sheet = doc.sheet_by_index(0)

		nrows = sheet.nrows
		ncols = sheet.ncols


		matriz=[]

		for i in range(nrows):
			matriz.append([])
			for j in range(ncols):
				matriz[i].append(sheet.cell_value(i,j).encode('ascii', 'ignore'))
		#self.write("{}".format(matriz[3][4].encode('ascii', 'ignore')))			

		# for i in range(nrows):
		# 	string = ''
		# 	for j in range(ncols):
		# 		string += '%st'%sheet.cell_value(i,j)
			#self.write("{}".format(string.encode('ascii', 'ignore')))
			#print(string)

		self.render("product/home.html", side_menu=self.side_menu, dn=dn, matriz=matriz, nrows=nrows, ncols=ncols)

class ProductRemoveHandler(BaseHandler):
	
	def get(self):

		prod = Product()
		prod.InitWithId(self.get_argument("id", ""))
		prod.Remove()

		self.redirect("/product/list")
