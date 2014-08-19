#!/usr/bin/env python

from model10.order_detail import OrderDetail
from base_handler import BaseHandler

class ListDetailByOrderIdHandler(BaseHandler):

	def get(self):
		#validate
		if not self.ValidateToken():
			return

		page = self.get_argument("page",1)
		limit = self.get_argument("items",20)
		order_id = self.get_argument("order_id","")

		order_detail = OrderDetail()
		self.write(order_detail.ListByOrderId(order_id, page, limit))


class AddOrderDetailHandler(BaseHandler):
	def get(self):
		
		#validate access token
		if not self.ValidateToken():
			return

		#instantiate order detail
		order_detail = OrderDetail()

		order_detail.order_id	= self.get_argument("order_id", "")
		order_detail.quantity 	= self.get_argument("quantity", "")
		order_detail.product_id = self.get_argument("product_id","")
		order_detail.total 		= self.get_argument("total", "")

		oid = order_detail.Save()

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

		_id = int(self.get_argument("id", ""))

		order_detail = OrderDetail()
		self.write(order_detail.GetDetail(_id))


class ListOrderDetailHandler(BaseHandler):
	def get(self):
		#validate
		if not self.ValidateToken():
			return

		order_detail = OrderDetail()
		self.write(order_detail.GetList(self.TryGetParam("id", ""), self.db.order_details))
		