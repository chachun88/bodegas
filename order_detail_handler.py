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

from bson import json_util

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
			self.render("order_detail/save.html",dn="Error al insertar detalle de pedido", order_detail=order_detail)

		
		order_detail.order_id = order_id
		order_detail.product_id = product_id
		order_detail.quantity = quantity
		order_detail.total = total
		order_detail.Save()

		self.render("order_detail/save.html",dn="Detalle insertado correctamente",order_detail=order_detail)		

class EditOrderDetailHandler(BaseHandler):
	
	@tornado.web.authenticated
	def get(self):
		self.render("order_detail/save.html",dn="",mode="edit",order_detail=order_detail)