#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import csv


from bson import json_util
from basehandler import BaseHandler
from globals import Menu
from model.cellar import Cellar
from model.product import Product

class ReportHandler(BaseHandler):

	data=[]

	def get(self):
		self.set_active(Menu.INFORMES_POR_BODEGA)
		global data
		try:
			day = self.get_argument("day")
		except:
			day="today"	
		
		# data = Cellar().List(1, 10)
		fromm = "from"
		until = "until"
		cellar = Cellar().List(1, 100)
		data = Cellar().ListKardex(day, fromm, until)
		product = Product().get_product_list()
		self.render("report/home.html", side_menu=self.side_menu, data=data, product=product, cellar=cellar)

	def post(self):
		global data
		day = self.get_argument("day", "")
		fromm = self.get_argument("from", "")
		until = self.get_argument("until", "")

		cellar = Cellar().List(1, 100)
		data = Cellar().ListKardex(day, fromm, until)
		product = Product().get_product_list()
		self.render("report/period.html", side_menu=self.side_menu, data=data, product=product, cellar=cellar)
		# self.redirect("/")

	def check_xsrf_cookie(self):
		pass		

class ReportUploadHandler(BaseHandler):
	def get(self):
		pass

	def post(self):

		load = self.get_argument("load", "")
		cellar = Cellar().List(1, 100)
		# data = json_util.dumps(len(data))

		tit=["SKU", "Talla", "Precio U. Compra", "Precio U. Venta", "Cantidad", "Total", "Usuario", "Bodega"]

		item_length = int(json_util.dumps(len(data)))

		matriz=[]

		for i in range(item_length):
			matriz.append([])
			matriz[i].append(data[i]["product_sku"])
			matriz[i].append(data[i]["size"])
			matriz[i].append(data[i]["balance_price"])
			matriz[i].append(data[i]["sell_price"])
			matriz[i].append(data[i]["units"])
			total=int(data[i]["sell_price"])*int(data[i]["units"])
			matriz[i].append(total)
			matriz[i].append(data[i]["user"])
			for c in cellar:
				if data[i]["cellar_identifier"] == str(c["_id"]):
					matriz[i].append(c["name"])

		tras=zip(*matriz)
		
		# lol = [[1,2,3],[4,5,6],[7,8,9]]
		# print lol
		item_length = len(tras[0])

		with open('uploads/informe.csv', 'wb') as test_file:
			file_writer = csv.writer(test_file, delimiter=';')
			file_writer.writerow([x for x in tit])
			for i in range(item_length):
				file_writer.writerow([x[i] for x in tras])	

	def check_xsrf_cookie(self):
		pass