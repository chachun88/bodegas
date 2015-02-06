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
        contact.type_id = self.get_argument("type_id","")
        contact.telephone = self.get_argument("telephone","")
        contact.email = self.get_argument("email","")
        contact.user_id = self.get_argument("user_id","")
        contact.address = self.get_argument("address","")
        contact.id = self.get_argument("id","")

        contact.type = self.get_argument("type","")
        contact.lastname = self.get_argument("lastname","")
        contact.city = self.get_argument("city","")
        contact.zip_code = self.get_argument("zip_code","")
        contact.additional_info = self.get_argument("additional_info","")
        contact.town = self.get_argument("town","")
        contact.rut = self.get_argument("rut","")

        self.write(json_util.dumps(contact.Save()))

class EditHandler(BaseHandler):

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        contact = Contact()
        contact.name = self.get_argument("name","")
        contact.type_id = self.get_argument("type_id","")
        contact.telephone = self.get_argument("telephone","")
        contact.email = self.get_argument("email","")
        contact.user_id = self.get_argument("user_id","")
        contact.address = self.get_argument("address","")
        contact.id = self.get_argument("id","")

        contact.type = self.get_argument("type","")
        contact.lastname = self.get_argument("lastname","")
        contact.city = self.get_argument("city","")
        contact.zip_code = self.get_argument("zip_code","")
        contact.additional_info = self.get_argument("additional_info","")
        contact.town = self.get_argument("town","")
        contact.rut = self.get_argument("rut","")

        self.write(json_util.dumps(contact.Edit()))

class RemoveHandler(BaseHandler):
    def post(self):
        #validate constrains
        if not self.ValidateToken():
            return

        contact = Contact()
        self.write(json_util.dumps(contact.Remove(self.get_argument("ids", ""))))

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

        user_id = self.get_argument("user_id","")

        if user_id != "":
            contact = Contact()
            self.write(json_util.dumps(contact.ListByCustomerId(user_id)))
        else:
            self.write(json_util.dumps({"error":"Debe ingresar id de cliente"}))

class InitByIdHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            return

        contact_id = self.get_argument("id","")
        contact = Contact()
        str_res = json_util.dumps(contact.InitById(contact_id))
        self.write(str_res)

class GetTypesHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            return

        contact = Contact()
        self.write(json_util.dumps(contact.GetTypes()))

