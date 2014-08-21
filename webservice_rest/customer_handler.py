#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model10.customer import Customer
from model10.contact import Contact
from bson import json_util

from base_handler import BaseHandler


class SaveHandler(BaseHandler):
    

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        # instantiate order
        customer = Customer()
        contact = Contact()

        customer.name = self.get_argument("customer_name")
        customer.type = self.get_argument("customer_type", "")
        customer.rut = self.get_argument("rut", "")
        customer.lastname = self.get_argument("lastname","")
        customer.bussiness = self.get_argument("bussiness","")
        customer.registration_date = self.get_argument("registration_date","")
        customer.approval_date = self.get_argument("approval_date","")
        customer.status = self.get_argument("status",1)
        customer.first_view = self.get_argument("first_view","")
        customer.last_view = self.get_argument("last_view","")
        customer.contact = contact
        customer.username = self.get_argument("username","")
        customer.password = self.get_argument("password","")

        #saving the current customer
        oid = customer.Save()

        contact.name = self.get_argument("contact_name","")
        contact.type = self.get_argument("contact_type","")
        contact.telephone = self.get_argument("telephone","")
        contact.email = self.get_argument("email","")
        contact.customer_id = oid

        contact.Save()

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
        order.DeleteOrders(self.get_argument("id", ""))


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