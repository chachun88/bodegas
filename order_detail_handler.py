#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler
from model.order_detail import OrderDetail
from model.order import Order
from model.product import Product

from bson import json_util

class ListOrderDetailHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):

		order_id = self.get_argument("order_id","")

		od_list = []

		order = Order()
		response = order.InitWithId(order_id)

		order_detail = OrderDetail()
		
		product = Product()

		if "error" in response:
			self.render("order_detail/list.html",dn=response["error"],order_detail=od_list,order=order)

		if order_id == "":
			self.render("order_detail/list.html",dn="Pedido solicitado no existe",order_detail=od_list,order=order)
		else:
			try:
				response = order_detail.ListByOrderId(order_id)
				if "success" in response:
					od_list = response["success"]
					self.render("order_detail/list.html",dn="",order_detail=od_list,order=order)
				else:
					self.render("order_detail/list.html",dn=response["error"],order_detail=od_list,order=order)
			except Exception, e:
				self.render("order_detail/list.html",dn="bpf",error=str(e),order_detail=od_list,order=order)

			


class AddOrderDetailHandler(BaseHandler):
	
	@tornado.web.authenticated
	def get(self):
		order_detail = OrderDetail()
		self.render("order_detail/save.html",dn="",mode="add", order_detail=order_detail)

	@tornado.web.authenticated
	def post(self):

		order_id = self.get_argument("order_id","")
		product_id = self.get_argument("product_id","")
		quantity = self.get_argument("quantity","")
		total = self.get_argument("total","")

		order_detail = OrderDetail()

		if order_id == "" or product_id == "" or quantity == "" or total == "":
			self.render("order_detail/save.html",dn="Error al insertar detalle de pedido", order_detail=order_detail, mode="add")

		
		order_detail.order_id = order_id
		order_detail.product_id = product_id
		order_detail.quantity = quantity
		order_detail.total = total
		order_detail.Save()

		self.render("order_detail/save.html",dn="Detalle insertado correctamente",order_detail=order_detail, mode="add")		

class EditOrderDetailHandler(BaseHandler):
	
	@tornado.web.authenticated
	def get(self):
		self.render("order_detail/save.html",dn="",mode="edit",order_detail=order_detail)