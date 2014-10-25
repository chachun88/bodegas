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
		shipping.identifier = self.get_argument("identifier",0)
		shipping.from_city_id = self.get_argument("from_city_id",0)
		shipping.to_city_id = self.get_argument("to_city_id",0)
		shipping.correos_price = self.get_argument("correos_price",0)
		shipping.chilexpress_price = self.get_argument("chilexpress_price",0)
		shipping.price = self.get_argument("price",0)
		shipping.edited = self.get_argument("edited",False)
		self.write(json_util.dumps(shipping.Save()))