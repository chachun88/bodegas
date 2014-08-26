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
        contact.address = self.get_argument("address","")
        contact.id = self.get_argument("id","")

        oid = str(contact.Save())

        self.write(oid)

class EditHandler(BaseHandler):

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
        contact.address = self.get_argument("address","")
        contact.id = self.get_argument("id","")

        oid = str(contact.Edit())

        self.write(oid)

class RemoveHandler(BaseHandler):
    def post(self):
        #validate constrains
        if not self.ValidateToken():
            return

        contact = Contact()
        contact.Remove(self.get_argument("ids", ""))

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

class InitByIdHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            return

        contact_id = self.get_argument("id","")
        contact = Contact()
        str_res = json_util.dumps(contact.InitById(contact_id))
        self.write(str_res)
