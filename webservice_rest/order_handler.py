#!/usr/bin/env python

from model10.order import Order
from bson import json_util

from base_handler import BaseHandler
from datetime import datetime


class AddOrderHandler(BaseHandler):
    

    def get(self):
        # validate access token
        if not self.ValidateToken():
            return

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


class EditOrderHandler(BaseHandler):
    def get(self):
        # validate access token
        if not self.ValidateToken():
            return

        # instantiate order
        order = Order()

        order.identifier        = self.get_argument("id", "")
        order.salesman          = self.get_argument("salesman_id", "")
        order.customer          = self.get_argument("customer", "")
        order.subtotal          = self.get_argument("subtotal", "")
        order.discount          = self.get_argument("discount", "")
        order.iva               = self.get_argument("iva", "")
        order.total             = self.get_argument("total", "")
        order.address           = self.get_argument("address", "")
        order.town              = self.get_argument("town", "")
        order.city              = self.get_argument("city", "")

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

        id = self.get_argument("id","")

        order = Order()
        orden = order.GetOrderById(id)
        self.write(orden)


class ListOrderHandler(BaseHandler):
    def get(self):

        #validate constrains
        if not self.ValidateToken():
            return

        order = Order()

        try:
            current_page    = int(self.get_argument("page", "1"))
            items_per_page  = int(self.get_argument("items", "20"))
        except Exception, e:
            print str(e)
        
        self.write(json_util.dumps(order.GetList(current_page, items_per_page)))