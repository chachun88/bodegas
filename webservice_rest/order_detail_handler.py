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

		order_detail.cabecera	= self.TryGetParam("cabecera", "")
		order_detail.producto	= self.TryGetParam("producto", "")
		order_detail.cantidad 	= self.TryGetParam("cantidad", "")
		order_detail.descuento 	= self.TryGetParam("descuento","")
		order_detail.neto 		= self.TryGetParam("neto", "")
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
		