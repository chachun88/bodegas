#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model10.customer import Customer
from model10.contact import Contact
from bson import json_util

from base_handler import BaseHandler

class InitByIdHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            return

        customer_id = self.get_argument("id","")

        customer = Customer()
        self.write(json_util.dumps(customer.InitById(customer_id)))

class SaveHandler(BaseHandler):
    

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        # instantiate order
        customer = Customer()
        # contact = Contact()

        customer.name = self.get_argument("name","")
        customer.type = self.get_argument("type", "")
        customer.rut = self.get_argument("rut", "")
        customer.lastname = self.get_argument("lastname","")
        customer.bussiness = self.get_argument("bussiness","")
        customer.registration_date = self.get_argument("registration_date","")
        customer.approval_date = self.get_argument("approval_date","")
        customer.status = self.get_argument("status",1)
        customer.first_view = self.get_argument("first_view","")
        customer.last_view = self.get_argument("last_view","")
        customer.id = self.get_argument("id","")
        customer.username = self.get_argument("username","")
        customer.password = self.get_argument("password","")
        customer.email = self.get_argument("email","")

        #saving the current customer
        if customer.id == "":
            self.write(json_util.dumps(customer.Save()))
        else:
            self.write(json_util.dumps(customer.Edit()))

        # contact.name = self.get_argument("contact_name","")
        # contact.type = self.get_argument("contact_type","")
        # contact.telephone = self.get_argument("telephone","")
        # contact.email = self.get_argument("email","")
        # contact.customer_id = oid

        # contact.Save()

        # self.write(oid)


class EditHandler(BaseHandler):
    def get(self):
        # validate access token
        if not self.ValidateToken():
            return

        # instantiate order
        customer = Customer()

        customer.id = self.get_argument("id")

        customer.InitById(customer.id)
        customer.name = self.get_argument("name")
        customer.type = self.get_argument("type", "")
        customer.rut = self.get_argument("rut", "")
        customer.lastname = self.get_argument("lastname","")
        customer.bussiness = self.get_argument("bussiness","")
        customer.registration_date = self.get_argument("registration_date","")
        customer.approval_date = self.get_argument("approval_date","")
        customer.status = self.get_argument("status",1)
        customer.first_view = self.get_argument("first_view","")
        customer.last_view = self.get_argument("last_view","")
        customer.username = self.get_argument("username","")
        customer.password = self.get_argument("password","")
        customer.email = self.get_argument("email","")

        #saving the current customer
        oid = customer.Edit()

        self.write(oid)


class RemoveHandler(BaseHandler):
    def post(self):
        #validate constrains
        if not self.ValidateToken():
            return

        customer = Customer()
        response = customer.Remove(self.get_argument("ids", ""))

        self.write(json_util.dumps(response))


class GetOrderHandler(BaseHandler):
    def get(self):
        
        #validate constrains
        if not self.ValidateToken():
            return

        id = self.get_argument("id","")

        order = Order()
        orden = order.GetOrderById(id)
        self.write(orden)


class ListHandler(BaseHandler):
    def post(self):

        #validate constrains
        if not self.ValidateToken():
            return

        customer = Customer()

        try:
            current_page    = int(self.get_argument("page", "1"))
            items_per_page  = int(self.get_argument("items", "20"))
        except Exception, e:
            print str(e)
        
        self.write(json_util.dumps(customer.List(current_page, items_per_page)))

    def get(self):
        self.post()

class ChangeStateHandler(BaseHandler):

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        ids = self.get_argument("ids","")
        state = self.get_argument("state","")

        if ids == "":
            self.write("Debe seleccionar al menos un cliente")
            return

        customer = Customer()
        self.write(json_util.dumps(customer.ChangeState(ids,state)))

class GetTypesHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            return

        customer = Customer()
        self.write(json_util.dumps(customer.GetTypes()))


class GetTotalPagesHandler(BaseHandler):
    """ get total pages with items """

    def post(self):

        items = self.get_argument("items", 20)
        page = self.get_argument("page", 1)

        customer = Customer()
        total = customer.getTotalPages(page, items)

        self.write(json_util.dumps(total))