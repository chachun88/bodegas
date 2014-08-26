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
from model.contact import Contact

from datetime import datetime

from bson import json_util

ACCIONES_ACEPTAR = 1
ACCIONES_PENDIENTE = 2
ACCIONES_ELIMINAR = 3

ESTADO_PENDIENTE = 1
ESTADO_ACEPTADO = 2

class CustomerViewContactHandler(BaseHandler):

    def get(self):

        customer_id = self.get_argument("customer_id","")

        contact = Contact()

        if customer_id == "":
            self.write("Debe ingresar el id de cliente")
        else:
            self.render("customer/view_contact.html",contactos = json_util.loads(contact.ListByCustomerId(customer_id)), dn="")


class CustomerAddContactHandler(BaseHandler):

    def get(self):
        customer_id = self.get_argument("customer_id","")
        contact = Contact()
        contact.customer_id = customer_id
        self.render("customer/add_contact.html",contact=contact,mode="add",dn="")

    def post(self):
        contact = Contact()
        contact.customer_id = self.get_argument("customer_id","")
        contact.name = self.get_argument("name","")
        contact.email = self.get_argument("email","")
        contact.address = self.get_argument("address","")
        contact.telephone = self.get_argument("telephone","")
        contact.type = self.get_argument("type","")

        if contact.Save().isdigit():
            self.redirect("/customer")

class CustomerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.CLIENTES_LISTAR)

        customer = Customer()
        clientes = customer.List()
        self.render("customer/list.html",side_menu=self.side_menu, clientes=clientes, dn=self.get_argument("dn", ""))

class CustomerSaveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        customer = Customer()
        customer_id = self.get_argument("id","")
        if customer_id == "":
            self.render("customer/save.html",dn="",mode="add", customer=customer)
        else:
            customer.InitById(customer_id)
            self.render("customer/save.html",dn="",mode="edit", customer=customer)

    @tornado.web.authenticated
    def post(self):

        # instantiate order
        customer = Customer()

        customer.id = self.get_argument("id","")
        customer.name = self.get_argument("name","").encode("utf-8")
        customer.type = self.get_argument("type", "")

        

        customer.rut = self.get_argument("rut", "")
        customer.lastname = self.get_argument("lastname","").encode("utf-8")
        customer.bussiness = self.get_argument("bussiness","").encode("utf-8")
        customer.registration_date = self.get_argument("registration_date","")
        customer.approval_date = self.get_argument("approval_date","")
        customer.status = self.get_argument("status",1)
        customer.first_view = self.get_argument("first_view","")
        customer.last_view = self.get_argument("last_view","")
        customer.username = self.get_argument("username","")
        customer.password = self.get_argument("password","")
        customer.contact = Contact()

        oid = customer.Save()

        if oid:
            self.redirect("/customer")

class CustomerActionsHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):

        customer=Customer()

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
                customer.ChangeState(valores,ESTADO_ACEPTADO)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        elif accion == ACCIONES_PENDIENTE:
            try:
                customer.ChangeState(valores,ESTADO_PENDIENTE)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        elif accion == ACCIONES_ELIMINAR:
            try:
                customer.Remove(valores)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        

    def check_xsrf_cookie(self):
        pass

class ContactActionsHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):

        contact=Contact()

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
                contact.ChangeState(valores,ESTADO_ACEPTADO)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        elif accion == ACCIONES_PENDIENTE:
            try:
                contact.ChangeState(valores,ESTADO_PENDIENTE)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        elif accion == ACCIONES_ELIMINAR:
            try:
                contact.Remove(valores)
                self.write("ok")
            except Exception,e:
                self.write(str(e))
        

    def check_xsrf_cookie(self):
        pass

class EditContactHandler(BaseHandler):

    def get(self):
        contact_id = self.get_argument("id","")
        contact = Contact()
        contact.InitById(contact_id)
        self.render("customer/edit_contact.html",contact=contact,mode="edit",dn="")

    def post(self):
        contact = Contact()
        contact.customer_id = self.get_argument("customer_id","")
        contact.name = self.get_argument("name","").encode("utf-8")
        contact.email = self.get_argument("email","")
        contact.address = self.get_argument("address","").encode("utf-8")
        contact.telephone = self.get_argument("telephone","")
        contact.type = self.get_argument("type","")
        contact.id = self.get_argument("id","")

        if contact.Edit().isdigit():
            self.render("customer/edit_contact.html",contact=contact,mode="edit",dn="")