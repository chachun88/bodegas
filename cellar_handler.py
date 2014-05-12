#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler
from model.cellar import Cellar
from model.product import Product

from bson import json_util

class CellarHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		data = Cellar().List(1, 10)
		self.render("cellar/home.html",side_menu=self.side_menu, data=data, dn=self.get_argument("dn", ""))


class CellarOutputHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		self.render("cellar/input.html", operation="Salidas", opp="out", side_menu=self.side_menu, cellar=cellar)

	def post(self):
		name = self.get_argument("name", "")
		price = self.get_argument("price", "0")
		units = self.get_argument("units", "0")
		product_id = self.get_argument("product_id", "")
		cellar_id = self.get_argument("cellar_id", "")

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		redirect = "t"

		if "success" in cellar.RemoveProducts(product_id, units):
			self.write("ok")
			redirect = "bpt"
		else:
			self.write("no")
			redirect = "bpf"

		self.redirect("/cellar?dn=" + redirect)


class CellarEasyInputHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		self.render("cellar/easyinput.html",operation="Entradas ", opp="in", side_menu=self.side_menu, cellar=cellar, products=Product().get_product_list())
	
	def post(self):
		cellar_id = self.get_argument("cellar_id", "")
		product_sku = self.get_argument("product_sku", "")
		quantity = self.get_argument("quantity", "")
		price = self.get_argument("price", "")
		size= self.get_argument("size", "")
		color=self.get_argument("color", "")

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		if "success" in cellar.AddProducts(product_sku, quantity, price, size, color):
			self.write("ok")
		else:
			self.write("no")

	## invalidate xsfr cookie for ajax use
	def check_xsrf_cookie(self):
		pass

######################
#### easy output #####
######################
class CellarEasyOutputHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		data = Cellar().List(1, 10)
		self.render("cellar/easyoutput.html", cellar=cellar, products=cellar.ListProducts(), cellarList=data)

	def post(self):
		cellar_id = self.get_argument("cellar_id", "")
		product_id = self.get_argument("product_id", "")
		quantity = self.get_argument("quantity", "")
		balance_price=self.get_argument("balance_price", "")
		new_cellar = self.get_argument("new_cellar", "")

		print "aca "+new_cellar

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		if "success" in cellar.RemoveProducts(product_id, quantity):
			self.write("ok")
		else:
			self.write("no")

		if new_cellar!='delete':
			
			cellar2 = Cellar()
			cellar2.InitWithId(new_cellar)

			redirect = "t"

			if "success" in cellar2.AddProducts(product_id, quantity, balance_price):
				self.write("ok")
				redirect = "bpt"
			else:
				self.write("no")
				redirect = "bpf"



	## invalidate xsfr cookie for ajax use
	def check_xsrf_cookie(self):
		pass



######################
#### cellar input ####
######################
class CellarInputHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		self.render("cellar/input.html",operation="Entradas ", opp="in", cellar=cellar)

	def post(self):
		name = self.get_argument("name", "")
		price = self.get_argument("price", "0")
		units = self.get_argument("units", "0")
		product_id = self.get_argument("product_id", "")
		cellar_id = self.get_argument("cellar_id", "")
		size = self.get_argument("size", "")
		color = self.get_argument("color", "")

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		product = Product()
		print "product idddddddddddddd "+ product_id
		product.InitWithId(product_id)
		product_sku=product.sku

		redirect = "t"

		if "success" in cellar.AddProducts(product_sku, units, price, size, color):
			self.write("ok")
			redirect = "bpt"
		else:
			self.write("no")
			redirect = "bpf"

		self.redirect("/cellar?dn=" + redirect)

class CellarDetailHandler(BaseHandler):
	def get(self):

		idd = self.get_argument("id", "")

		cellar = Cellar()
		cellar.InitWithId(idd)
		cellar.ListProducts()

		self.render("cellar/detail.html", side_menu=self.side_menu, cellar=cellar)

	def post(self):

		pass
