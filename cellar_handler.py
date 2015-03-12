#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu, debugMode

from basehandler import BaseHandler
from model.cellar import Cellar
from model.product import Product

from model.kardex import Kardex

from bson import json_util

class CellarHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		data = Cellar().List(1, 100)

		cellar = Cellar()

		web_cellar_id = None
		reservation_cellar_id = None

		res_web_cellar = cellar.GetWebCellar()
		res_reservation_cellar = cellar.GetReservationCellar()

		if "success" in res_web_cellar:
			web_cellar_id = res_web_cellar["success"]
		elif debugMode:
			print res_web_cellar["error"]

		if "success" in res_reservation_cellar:
			reservation_cellar_id = res_reservation_cellar["success"]
		elif debugMode:
			print res_web_cellar["error"]

		self.render("cellar/home.html",side_menu=self.side_menu, data=data, dn=self.get_argument("dn", ""), web_cellar_id=web_cellar_id,
			reservation_cellar_id=reservation_cellar_id)


class CellarOutputHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		data = Cellar().List(1, 10)

		product = Product()
		# product.InitWithId(product_id)

		self.render("cellar/output.html", operation="Salidas", opp="out", side_menu=self.side_menu, cellar=cellar, data=data, product=product)

	@tornado.web.authenticated
	def post(self):
		name = self.get_argument("name", "")
		price = self.get_argument("price", "0")
		size = self.get_argument("size", "")
		color = self.get_argument("color", "")
		units = self.get_argument("units", "0")
		product_id = self.get_argument("product_id", "")
		cellar_id = self.get_argument("cellar_id", "")
		operation="sell"



		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		product = Product()
		product.InitWithId(product_id)
		product_sku=product.sku

		redirect = "t"

		if "success" in cellar.RemoveProducts(product_sku, units, size, color, operation, self.get_user_email()):
			self.write("ok")
			redirect = "bpt"
		else:
			self.write("no")
			redirect = "bpf"

		self.redirect("/cellar?dn=" + redirect)
		
	def check_xsrf_cookie(self):
		pass


class CellarEasyInputHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		product = Product()
		lista = product.get_product_list()

		self.render("cellar/easyinput.html",operation="Entradas ", opp="in", side_menu=self.side_menu, cellar=cellar, products=cellar.ListProducts(), product_list=lista)
	
	@tornado.web.authenticated
	def post(self):
		cellar_id = self.get_argument("cellar_id", "")
		product_sku = self.get_argument("product_sku", "")
		quantity = self.get_argument("quantity", "")
		price = self.get_argument("price", "")
		size = self.get_argument("size", "")
		operation = "buy"


		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		product = Product()
		product.InitWithSku(product_sku)

		product.size=size
		product.description = product.description.encode("utf-8")
		product.Save()

		if "success" in cellar.AddProducts(product_sku, quantity, price, size, product.color.decode("utf-8"), operation, self.get_user_email() ):
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

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		data = Cellar().List(1, 100)
		self.render("cellar/easyoutput.html", cellar=cellar, products=cellar.ListProducts(), cellarList=data)

	@tornado.web.authenticated
	def post(self):
		cellar_id = self.get_argument("cellar_id", "")
		product_id = self.get_argument("product_id", "")
		quantity = self.get_argument("quantity", "")
		price = self.get_argument("price", "")
		balance_price=self.get_argument("balance_price", "")
		# new_cellar = self.get_argument("new_cellar", "")
		size= self.get_argument("size", "")
		color=self.get_argument("color", "")
		operation=self.get_argument("operation", "")

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		product = Product()
		product.InitWithId(product_id)
		product_sku=product.sku

		product_find =cellar.ProductKardex(product_sku, cellar_id, size)

		buy=0
		sell=0

		for p in product_find:
			if p["operation_type"] == Kardex.OPERATION_BUY or p["operation_type"] == Kardex.OPERATION_MOV_IN:
				buy+=p["total"]	

			if p["operation_type"] == Kardex.OPERATION_SELL or p["operation_type"] == Kardex.OPERATION_MOV_OUT:
				sell+=p["total"]

		units=buy-sell		

		if int(units) >= int(quantity): 

			if operation == "mov":

				if "success" in cellar.RemoveProducts(product_sku, quantity, price, size, color, Kardex.OPERATION_MOV_OUT, self.get_user_email()):
					self.write("ok")
				else:
					self.write("no")

				cellar2 = Cellar()
				cellar2.InitWithId(cellar_id)

				# redirect = "t"

				if "success" in cellar2.AddProducts(product_sku, quantity, balance_price, size, color, Kardex.OPERATION_MOV_IN, self.get_user_email()):
					self.write("ok")
					redirect = "bpt"
				else:
					self.write("no")
					redirect = "bpf"

			else:

				if "success" in cellar.RemoveProducts(product_sku, quantity, price, size, color, operation, self.get_user_email()):
					self.write("ok")
				else:
					self.write("no")

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

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		self.render("cellar/input.html",operation="Entradas ", opp="in", cellar=cellar)

	@tornado.web.authenticated
	def post(self):
		name = self.get_argument("name", "")
		price = self.get_argument("price", "0")
		units = self.get_argument("units", "0")
		product_id = self.get_argument("product_id", "")
		cellar_id = self.get_argument("cellar_id", "")
		size = self.get_argument("size", "")
		color = self.get_argument("color", "")
		operation= "buy"

		cellar = Cellar()
		response = cellar.InitWithId(cellar_id)

		if "success" in response:

			product = Product()
			response = product.InitWithId(product_id)

			if response == "ok":

				product_sku=product.sku

				product.size=size.split(",")
				product.color=color
				product.Save()

				redirect = "t"

				if "success" in cellar.AddProducts(product_sku, units, price, size, color, operation, self.get_user_email()):
					self.write("ok")
					redirect = "bpt"
				else:
					self.write("no")
					redirect = "bpf"

				self.redirect("/cellar?dn=" + redirect)

			else:
				self.write(response)

		else:
			self.write(response["error"])

class CellarDetailHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):

		idd = self.get_argument("id", "")

		cellar = Cellar()
		cellar.InitWithId(idd)
		cellar.ListProducts()

		self.render("cellar/detail.html", side_menu=self.side_menu, cellar=cellar)

	@tornado.web.authenticated
	def post(self):

		pass

class CellarComboboxHandler(BaseHandler):	

	@tornado.web.authenticated
	def get(self):
		pass

	@tornado.web.authenticated
	def post(self):
		
		product_id = self.get_argument("product_id", "")
		cellar_id = self.get_argument("cellar_id", "")

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		data = Cellar().List(1, 10)

		product = Product()
		product.InitWithId(product_id)

		self.render("cellar/combobox.html", operation="Salidas", opp="out", cellar=cellar, data=data, product=product)

	## invalidate xsfr cookie for ajax use
	def check_xsrf_cookie(self):
		pass	

class SelectForSaleHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):

		cellar = Cellar()
		selected = cellar.GetWebCellar()
		data = Cellar().List(1, 100)

		cellar_id = ""

		if "success" in selected:
			cellar_id = selected["success"]
		
		self.render("cellar/selectforsale.html",cellars=data,cellar_id=cellar_id)

	@tornado.web.authenticated
	def post(self):

		cellar_id = self.get_argument("cellar_id","")

		if cellar_id != "":
			cellar = Cellar()
			self.write(json_util.dumps(cellar.SelectForSale(cellar_id)))
		else:
			self.write(json_util.dumps({"error":"Cellar id is not valid"}))


class SelectReservationHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):

		cellar = Cellar()
		selected = cellar.GetReservationCellar()
		data = Cellar().List(1, 100)

		cellar_id = ""

		if "success" in selected:
			cellar_id = selected["success"]
		
		self.render("cellar/selectreservation.html",cellars=data,cellar_id=cellar_id)

	@tornado.web.authenticated
	def post(self):

		cellar_id = self.get_argument("cellar_id","")

		if cellar_id != "":
			cellar = Cellar()
			self.write(json_util.dumps(cellar.SelectReservation(cellar_id)))
		else:
			self.write(json_util.dumps({"error":"Cellar id is not valid"}))