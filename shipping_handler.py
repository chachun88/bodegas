#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basehandler import BaseHandler
from model.city import City
from model.shipping import Shipping
from bson import json_util

from globals import Menu

class AddCityHandler(BaseHandler):

	def post(self):

		city = City()
		city.name = self.get_argument("name","").encode("utf-8")
		guardado = city.Save()
		
		identifier = int(self.get_argument("identifier",0))

		if "success" in guardado:
			if identifier == 0:
				self.redirect("/shipping/save")
			else:
				self.redirect("/shipping/save?identifier={id}".format(id=identifier))
		else:
			self.redirect("/shipping/save?dn=error&mensaje="+guardado["error"])

class SaveHandler(BaseHandler):

	def get(self):

		self.set_active(Menu.SHIPPING_SAVE)

		city = City()
		cities = city.List()

		identifier = int(self.get_argument("identifier",0))
		dn = self.get_argument("dn","")
		mensaje = self.get_argument("mensaje","")

		shipping = Shipping()

		if identifier != 0:
			
			shipping.identifier = identifier
			res = shipping.InitById()

			if "error" in res:
				self.write(res["error"])
				return

		if "success" in cities:
			self.render("shipping/add.html",cities=cities["success"],shipping=shipping,dn=dn,mensaje=mensaje)
		else:
			self.write(cities["error"])

	def post(self):

		shipping = Shipping()
		shipping.identifier = int(self.get_argument("identifier",0))
		shipping.from_city_id = self.get_argument("from_city_id",0)
		shipping.to_city_id = self.get_argument("to_city_id",0)
		shipping.correos_price = self.get_argument("correos_price",0)
		shipping.chilexpress_price = self.get_argument("chilexpress_price",0)
		shipping.price = self.get_argument("price",0)
		shipping.edited = self.get_argument("edited",0)
		
		guardado = shipping.Save()
		
		if "success" in guardado:
			if shipping.identifier == 0:
				self.redirect("/shipping/list")
			else:
				self.redirect("/shipping/save?identifier={id}".format(id=shipping.identifier))
		else:
			self.write(guardado["error"])

class ListHandler(BaseHandler):

	def get(self):

		self.set_active(Menu.SHIPPING_LIST)

		shipping = Shipping()
		res_lista = shipping.List()
		if "success" in res_lista:
			self.render("shipping/list.html",lista=res_lista["success"])
		else:
			self.write(res_lista["error"])

class ActionHandler(BaseHandler):

	def post(self):

		action = self.get_argument("action","")
		shipping = Shipping()

		if action == "":
			self.write("Debe seleccionar una acción")
		else:
			
			res = shipping.Action(action)
			if "success" in res:
				self.redirect("/shipping/list")
			else:
				self.write(res["error"])

class RemoveHandler(BaseHandler):

	def get(self):

		identifier = int(self.get_argument("identifier",0))

		if identifier != 0:
			shipping = Shipping()
			shipping.identifier = identifier
			res = shipping.Remove()

			if "success" in res:
				self.redirect("/shipping/list")
			else:
				self.write(res["error"])

		else:

			self.write("Identificador no válido")