#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from model10.shipping import Shipping

from base_handler import BaseHandler
from bson import json_util

class SaveHandler(BaseHandler):

	def post(self):

		if not self.ValidateToken():
			self.write(json_util.dumps({"error":"invalid token"}))

		shipping = Shipping()
		shipping.identifier = int(self.get_argument("identifier",0))
		shipping.from_city_id = self.get_argument("from_city_id",0)
		shipping.to_city_id = self.get_argument("to_city_id",0)
		shipping.correos_price = self.get_argument("correos_price",0)
		shipping.chilexpress_price = self.get_argument("chilexpress_price",0)
		shipping.price = self.get_argument("price",0)
		shipping.charge_type = self.get_argument("charge_type",1)

		if shipping.identifier == 0:
			shipping.edited = False
		else:
			shipping.edited = True
			
		self.write(json_util.dumps(shipping.Save()))


class ListHandler(BaseHandler):
	
	def post(self):

		if not self.ValidateToken():
			self.write(json_util.dumps({"error":"invalid token"}))

		shipping = Shipping()
		self.write(json_util.dumps(shipping.List()))

class ActionHandler(BaseHandler):

	def post(self):

		if not self.ValidateToken():
			self.write(json_util.dumps({"error":"invalid token"}))

		action = self.get_argument("action","")

		shipping = Shipping()
		self.write(json_util.dumps(shipping.Action(action)))
	
class InitByIdHandler(BaseHandler):

	def post(self):

		if not self.ValidateToken():
			self.write(json_util.dumps({"error":"invalid token"}))

		identifier = int(self.get_argument("identifier",0))

		shipping = Shipping()
		shipping.identifier = identifier

		if identifier == 0:
			self.write(json_util.dumps({"error":"Debe especificar identificador"}))
		else:
			self.write(json_util.dumps(shipping.InitById()))

class RemoveHandler(BaseHandler):

	def post(self):

		if not self.ValidateToken():
			self.write(json_util.dumps({"error":"invalid token"}))

		identifier = int(self.get_argument("identifier",0))

		shipping = Shipping()
		shipping.identifier = identifier


		if identifier == 0:
			self.write(json_util.dumps({"error":"Debe especificar identificador"}))
		else:
			self.write(json_util.dumps(shipping.Remove()))

class SaveTrackingHandler(BaseHandler):

	def post(self):

		if not self.ValidateToken():
			self.write(json_util.dumps({"error":"invalid token"}))

		else:

			order_id = self.get_argument("order_id","")
			tracking_code = self.get_argument("tracking_code","")
			provider_id = self.get_argument("provider_id","")

			if order_id == "":
				self.write(json_util.dumps({"error":"invalid order_id"}))
			elif tracking_code == "":
				self.write(json_util.dumps({"error":"invalid tracking_code"}))
			elif provider_id == "":
				self.write(json_util.dumps({"error":"invalid provider_id"}))
			else:
				shipping = Shipping()
				res = shipping.SaveTrackingCode(order_id,tracking_code,provider_id)
				self.write(json_util.dumps(res))