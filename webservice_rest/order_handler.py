#!/usr/bin/env python

from model.order import Order

from base_handler import BaseHandler


class AddOrderHandler(BaseHandler):
	

	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		# instantiate order
		order = Order()

		order.identifier		= self.get_argument("id", "") #optional
		order.salesman 			= self.get_argument("salesman_id", "")
		order.customer			= self.get_argument("customer", "")
		order.subtotal 			= self.get_argument("subtotal", "")
		order.discount 			= self.get_argument("discount", "")
		order.iva 				= self.get_argument("iva", "")
		order.total 			= self.get_argument("total", "")
		order.address 			= self.get_argument("address", "")
		order.town				= self.get_argument("town", "")
		order.city 				= self.get_argument("city", "")

		#saving the current order
		oid = order.Save(self.db.orders)

		self.write(oid)


class EditOrderHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		# instantiate order
		order = Order()

		order.identifier		= self.get_argument("id", "")
		order.salesman 			= self.get_argument("salesman_id", "")
		order.customer			= self.get_argument("customer", "")
		order.subtotal 			= self.get_argument("subtotal", "")
		order.discount 			= self.get_argument("discount", "")
		order.iva 				= self.get_argument("iva", "")
		order.total 			= self.get_argument("total", "")
		order.address 			= self.get_argument("address", "")
		order.town				= self.get_argument("town", "")
		order.city 				= self.get_argument("city", "")

		#saving the current order
		oid = order.Edit(self.db.orders)

		self.write(oid)


class RemoveOrderHandler(BaseHandler):
	def get(self):
		#validate constrains
		if not self.ValidateToken():
			return

		order = Order()
		order.RemoveById(self.TryGetParam("id", ""), self.db.orders)


class GetOrderHandler(BaseHandler):
	def get(self):
		
		#validate constrains
		if not self.ValidateToken():
			return

		order = Order()
		self.write(order.FindById(self.TryGetParam("id"), ""), self.db.orders)


class ListOrderHandler(BaseHandler):
	def get(self):

		#validate constrains
		if not self.ValidateToken():
			return
		
		current_page 	= "1"
		items_per_page 	= "10"
		order 			= Order()

		try:
			current_page 	= int(self.TryGetParam("page", "1"))
			items_per_page 	= int(self.TryGetParam("items", "10"))
		except Exception, e:
			print str(e)
		
		self.write(order.GetList(current_page, items_per_page, self.db.products))														