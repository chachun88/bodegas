#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from model10.shipping import Shipping
from model10.cellar import Cellar
from model10.product import Product
from model10.kardex import Kardex
from model10.order_detail import OrderDetail

from base_handler import BaseHandler
from bson import json_util

import datetime

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
			new_cellar_id = self.get_argument("new_cellar_id","")

			if order_id == "":
				self.write(json_util.dumps({"error":"invalid order_id"}))
			elif tracking_code == "":
				self.write(json_util.dumps({"error":"invalid tracking_code"}))
			elif provider_id == "":
				self.write(json_util.dumps({"error":"invalid provider_id"}))
			else:

				cellar = Cellar()

				order_detail = OrderDetail()
				details_res = order_detail.ListByOrderId(order_id)

				if "success" in details_res:
					details = details_res["success"]

				for detail in details:

					sku = detail["sku"]
					quantity = detail["quantity"]
					operation = Kardex.OPERATION_SELL
					price = detail["price"]

					promotion_price = detail["promotion_price"]

					if promotion_price != 0:
						sell_price = promotion_price
					else:
						sell_price = detail["sell_price"]
						
					size = detail["size"]
					color = detail["color"]
					user = 'Sistema - Despacho'

					k = Kardex()
					find_kardex = k.FindKardex(sku, new_cellar_id, size)

					balance_price = 0

					if "success" in find_kardex:
						balance_price = k.balance_price

					res_product_find = cellar.FindProductKardex(sku, new_cellar_id, size)

					buy=0
					sell=0

					if "success" in res_product_find:

						product_find = res_product_find["success"]

						for p in product_find:
							if p["operation_type"] == Kardex.OPERATION_BUY or p["operation_type"] == Kardex.OPERATION_MOV_IN:
								buy+=p["total"]	

							if p["operation_type"] == Kardex.OPERATION_SELL or p["operation_type"] == Kardex.OPERATION_MOV_OUT:
								sell+=p["total"]

					units=buy-sell		

					if int(units) >= int(quantity): 

						kardex = Kardex()

						kardex.product_sku = sku
						kardex.cellar_identifier = new_cellar_id
						kardex.date = str(datetime.datetime.now().isoformat())

						kardex.operation_type = operation
						kardex.units = quantity
						kardex.price = price
						kardex.size = size
						kardex.sell_price = sell_price

						kardex.color= color
						kardex.user = user

						response_kardex = kardex.Insert()

						if "error" in response_kardex:
							self.write(json_util.dumps(response_kardex))
							return
								

					else:
						self.write(json_util.dumps({"error":"Stock insuficiente para realizar el movimiento"}))
						return


				shipping = Shipping()
				res = shipping.SaveTrackingCode(order_id,tracking_code,provider_id)
				self.write(json_util.dumps(res))