#!/usr/bin/env python

from model.order_detail import OrderDetail
from base_handler import BaseHandler

class OrderDetailHandler(BaseHandler):
	def get(self):
		
		#validate access token
		if not self.ValidateToken():
			return

		#instantiate order detail
		order_detail = OrderDetail()

		order_detail.header		= self.TryGetParam("header", "")
		order_detail.product	= self.TryGetParam("product", "")
		order_detail.quantity 	= self.TryGetParam("quantity", "")
		order_detail.discount 	= self.TryGetParam("discount","")
		order_detail.net 		= self.TryGetParam("net", "")
		order_detail.total 		= self.TryGetParam("total", "")

		oid = order_detail.Save(self.db.order_details)

		self.write(oid)


class RemoveOrderDetailHandler(BaseHandler):
	def get(self):
		#validate contrains
		if not self.ValidateToken():
			return

		order_detail = OrderDetail()
		order_detail.RemoveById(self.TryGetParam("id", ""), self.db.order_details)


class GetOrderDetailHandler(BaseHandler):
	def get(self):
		#validate contrains
		if not self.ValidateToken():
			return

		order_detail = OrderDetail()
		order_detail.GetList(self.TryGetParam("id", ""), self.db.order_details)


class ListOrderDetailHandler(BaseHandler):
	def get(self):
		#validate
		if not self.ValidateToken():
			return

		order_detail = OrderDetail()
		self.write(order_detail.GetList(self.TryGetParam("id", ""), self.db.order_details))
		