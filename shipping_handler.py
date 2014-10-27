#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basehandler import BaseHandler
from model.city import City
from model.shipping import Shipping
from bson import json_util

class AddCityHandler(BaseHandler):

	def post(self):

		city = City()
		city.name = self.get_argument("name","").encode("utf-8")
		guardado = city.Save()
		
		if "success" in guardado:
			self.redirect("/shipping/save")
		else:
			self.write(guardado["error"])

class SaveHandler(BaseHandler):

	def get(self):
		city = City()
		cities = city.List()
		if "success" in cities:
			self.render("shipping/add.html",cities=cities["success"])
		else:
			self.write(cities["error"])

	def post(self):

		shipping = Shipping()
		shipping.identifier = self.get_argument("identifier",0)
		shipping.from_city_id = self.get_argument("from_city_id",0)
		shipping.to_city_id = self.get_argument("to_city_id",0)
		shipping.correos_price = self.get_argument("correos_price",0)
		shipping.chilexpress_price = self.get_argument("chilexpress_price",0)
		shipping.price = self.get_argument("price",0)
		shipping.edited = self.get_argument("edited",0)
		
		guardado = shipping.Save()
		
		if "success" in guardado:
			self.redirect("/shipping/save")
		else:
			self.write(guardado["error"])

class ListHandler(BaseHandler):

	def get(self):

		shipping = Shipping()
		res_lista = shipping.List()
		if "success" in res_lista:
			self.render("shipping/list.html",lista=res_lista["success"])
		else:
			self.write(res_lista["error"])