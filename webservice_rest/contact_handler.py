#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model10.contact import Contact
from bson import json_util

from base_handler import BaseHandler


class SaveHandler(BaseHandler):

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        contact = Contact()
        contact.name = self.get_argument("name","")
        contact.type = self.get_argument("type","")
        contact.telephone = self.get_argument("telephone","")
        contact.email = self.get_argument("email","")
        contact.customer_id = self.get_argument("customer_id","")

        oid = str(contact.Save())

        self.write(oid)

class RemoveHandler(BaseHandler):
    def post(self):
        #validate constrains
        if not self.ValidateToken():
            return

        customer = Customer()
        customer.Remove(self.get_argument("ids", ""))

class ChangeStateHandler(BaseHandler):

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        ids = self.get_argument("ids","")
        state = self.get_argument("state","")

        if ids == "":
            self.write("Debe seleccionar al menos un contacto")
            return

        customer = Customer()

class ListByCustomerIdHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            return

        customer_id = self.get_argument("customer_id","")

        if customer_id != "":
            contact = Contact()
            str_res = json_util.dumps(contact.ListByCustomerId(customer_id))
            self.write(str_res)
        else:
            self.write("Debe ingresar id de cliente")