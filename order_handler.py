#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler
from model.order import Order
from model.product import Product

from datetime import datetime

from bson import json_util

ACCIONES_ELIMINAR = 1
ACCIONES_ACEPTAR = 2
ACCIONES_DESPACHADO = 3
ACCIONES_PENDIENTE = 4

ESTADO_PENDIENTE = 0
ESTADO_ACEPTADO = 1
ESTADO_DESPACHADO = 2

class OrderHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.PEDIDOS_LISTA)

        order = Order()
        pedidos = order.List()
        self.render("order/home.html",side_menu=self.side_menu, pedidos=pedidos, dn=self.get_argument("dn", ""))

class AddOrderHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        order = Order()
        self.render("order/save.html",dn="",mode="add", order=order)

    @tornado.web.authenticated
    def post(self):

        # instantiate order
        order = Order()

        order.id                = self.get_argument("id", "")
        order.date              = datetime.now()
        order.salesman          = self.get_argument("salesman", "")
        order.customer          = self.get_argument("customer", "")
        order.subtotal          = self.get_argument("subtotal", "")
        order.discount          = self.get_argument("discount", "")
        order.tax               = self.get_argument("tax", "")
        order.total             = self.get_argument("total", "")
        order.address           = self.get_argument("address", "")
        order.town              = self.get_argument("town", "")
        order.city              = self.get_argument("city", "")
        order.country           = self.get_argument("country","")
        order.type              = self.get_argument("type","")
        order.source            = self.get_argument("source","")
        order.items_quantity    = self.get_argument("items_quantity","")
        order.product_quantity  = self.get_argument("product_quantity","")
        order.state             = self.get_argument("state","")

        #saving the current order
        oid = order.Save()

        self.write(oid)

class OrderActionsHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):

        order=Order()

        valores = self.get_argument("values","")
        accion = self.get_argument("action","")

        if accion == "":
            self.write("Debe seleccionar una acción")
            return 

        accion = int(accion)

        if valores == "":
            self.write("Debe seleccionar al menos un pedido")
            return

        if accion == ACCIONES_ACEPTAR:
            
            response = order.ChangeStateOrders(valores,ESTADO_ACEPTADO)
            
            self.write(json_util.dumps(response))

        elif accion == ACCIONES_ELIMINAR:

            response = order.Remove(valores)

            self.write(json_util.dumps(response))

        elif accion == ACCIONES_DESPACHADO:

            response = order.ChangeStateOrders(valores,ESTADO_DESPACHADO)

            self.write(json_util.dumps(response))

        elif accion == ACCIONES_PENDIENTE:

            response = order.ChangeStateOrders(valores,ESTADO_PENDIENTE)

            self.write(json_util.dumps(response))

    def check_xsrf_cookie(self):
        pass