#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler
from model.customer import Customer

from datetime import datetime

from bson import json_util

ACCIONES_PENDIENTE = 1
ACCIONES_ACEPTAR = 2

ESTADO_PENDIENTE = 1
ESTADO_ACEPTADO = 2

class OrderHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.CLIENTES_LISTAR)

        customer = Customer()
        clientes = customer.List()
        self.render("customer/list.html",side_menu=self.side_menu, clientes=clientes, dn=self.get_argument("dn", ""))

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
            try:
                order.ChangeStateOrders(valores,ESTADO_ACEPTADO)
                self.write("ok")
            except Exception,e:
                self.write(str(e))

        elif accion == ACCIONES_ELIMINAR:
            try:
                order.Remove(valores)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        elif accion == ACCIONES_DESPACHADO:
            try:
                order.ChangeStateOrders(valores,ESTADO_DESPACHADO)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        elif accion == ACCIONES_PENDIENTE:
            try:
                order.ChangeStateOrders(valores,ESTADO_PENDIENTE)
                self.write("ok")
            except Exception,e:
                self.write(str(e))

    def check_xsrf_cookie(self):
        pass