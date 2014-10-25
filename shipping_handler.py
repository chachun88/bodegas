#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basehandler import BaseHandler
from model.city import City
from model.shipping import Shipping
from bson import json_util

class ListHandler(BaseHandler):

	def get(self):
		city = City()
		cities = city.List()
		if "success" in cities:
			self.render("shipping/addcity.html",cities=cities["success"])
		else:
			self.write(cities["error"])

	def post(self):

		city = City()
		city.name = self.get_argument("name","")
		self.write(json_util.dumps(city.Save()))

class SaveHandler(BaseHandler):

	def post(self):

		shipping = Shipping()
		shipping.identifier = self.get_argument("identifier",0)
		shipping.from_city_id = self.get_argument("from_city_id",0)
		shipping.to_city_id = self.get_argument("to_city_id",0)
		shipping.correos_price = self.get_argument("correos_price",0)
		shipping.chilexpress_price = self.get_argument("chilexpress_price",0)
		shipping.price = self.get_argument("price",0)
		shipping.edited = self.get_argument("edited",False)
		self.write(json_util.dumps(shipping.Save()))

