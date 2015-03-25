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
from model.city import City

from datetime import datetime

from bson import json_util

ACCIONES_ACEPTAR = 1
ACCIONES_PENDIENTE = 2
ACCIONES_ELIMINAR = 3

ESTADO_PENDIENTE = 1
ESTADO_ACEPTADO = 2

class CustomerViewContactHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        user_id = self.get_argument("user_id","")

        contact = Contact()

        if user_id == "":
            self.write("Debe ingresar el id de cliente")
        else:
            response = contact.ListByCustomerId(user_id)
            if "success" in response:
                self.render("customer/view_contact.html",contactos = response["success"], dn="")
            else:
                self.write(response["error"])


class CustomerHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.CLIENTES_LISTAR)

        page = int(self.get_argument("page", 1))
        items = int(self.get_argument("items", 20))

        customer = Customer()
        clientes = customer.List(page, items)

        res_total_pages = customer.getTotalPages(page, items)

        if "success" in res_total_pages:
            total_pages = res_total_pages["success"]

        self.render("customer/list.html",
                    side_menu=self.side_menu,
                    clientes=clientes, 
                    dn=self.get_argument("dn", ""),
                    page=page, 
                    total_pages=total_pages)


class CustomerSaveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        customer = Customer()
        user_id = self.get_argument("id","")

        response = customer.GetTypes()

        if "success" in response:
            types = response["success"]

        if user_id == "":
            self.render("customer/save.html",dn="",mode="add", customer=customer,types=types)
        else:
            response = customer.InitById(user_id)
            if response == "ok":
                self.render("customer/save.html",dn="",mode="edit", customer=customer,types=types)
            else:
                self.write(response)

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

        response = customer.Save()

        if "success" in response:
            self.redirect("/customer")
        else:
            self.write(response["error"])

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
            self.write("Debe seleccionar al menos un cliente")
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

            response_obj = customer.Remove(valores)
            
            if "success" in response_obj:
                self.write("ok")
            else:
                self.write(response_obj["error"])
        

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
            self.write("Debe seleccionar al menos un contacto")
            return

        if accion == ACCIONES_ACEPTAR:

            try:
                response = contact.ChangeState(valores,ESTADO_ACEPTADO)
                if "success" in response:
                    self.write("ok")
                else:
                    self.write(response["error"])
            except Exception,e:
                self.write(str(e))

        elif accion == ACCIONES_PENDIENTE:

            try:
                response = contact.ChangeState(valores,ESTADO_PENDIENTE)
                if "success" in response:
                    self.write("ok")
                else:
                    self.write(response["error"])
            except Exception,e:
                self.write(str(e))

        elif accion == ACCIONES_ELIMINAR:

            try:
                response = contact.Remove(valores)
                if "success" in response:
                    self.write("ok")
                else:
                    self.write(response["error"])
            except Exception,e:
                self.write(str(e))
        

    def check_xsrf_cookie(self):
        pass

class CustomerAddContactHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.get_argument("user_id","")
        contact = Contact()
        contact.user_id = user_id
        
        types = {}

        response = contact.GetTypes()

        if "success" in response:
            types = response["success"]

        cities = {}

        city = City()
        res_city = city.List()

        if "success" in res_city:
            cities = res_city["success"]

        self.render("customer/add_contact.html",contact=contact,mode="add",dn="",types=types, cities=cities)

    @tornado.web.authenticated
    def post(self):
        contact = Contact()
        contact.user_id = self.get_argument("user_id","")
        contact.name = self.get_argument("name","").encode("utf-8")
        contact.email = self.get_argument("email","").encode("utf-8")
        contact.address = self.get_argument("address","").encode("utf-8")
        contact.telephone = self.get_argument("telephone","").encode("utf-8")
        contact.type = self.get_argument("type","")
        contact.rut = self.get_argument("rut","")
        contact.city = self.get_argument("city","")
        contact.town = self.get_argument("town","")
        contact.zip_code = self.get_argument("zip_code","")
        contact.additional_info = self.get_argument("additional_info","")
        contact.lastname = self.get_argument("lastname","")

        response = contact.Save()

        if "success" in response:
            self.redirect("/customer")
        else:
            self.write(response["error"])

class EditContactHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        contact_id = self.get_argument("id","")
        contact = Contact()
        contact.InitById(contact_id)

        city = City()
        res_city = city.List()

        cities = {}

        if "success" in res_city:
            cities = res_city["success"]

        types = {}

        response = contact.GetTypes()

        if "success" in response:
            types = response["success"]

        self.render("customer/edit_contact.html",contact=contact,mode="edit",dn="",types=types,cities=cities)

    @tornado.web.authenticated
    def post(self):
        contact = Contact()
        contact.user_id = self.get_argument("user_id","")
        contact.name = self.get_argument("name","").encode("utf-8")
        contact.email = self.get_argument("email","").encode("utf-8")
        contact.address = self.get_argument("address","").encode("utf-8")
        contact.telephone = self.get_argument("telephone","").encode("utf-8")
        contact.type = self.get_argument("type","")
        contact.id = self.get_argument("id","")
        contact.rut = self.get_argument("rut","")
        contact.city = self.get_argument("city","")
        contact.town = self.get_argument("town","")
        contact.zip_code = self.get_argument("zip_code","")
        contact.additional_info = self.get_argument("additional_info","")
        contact.lastname = self.get_argument("lastname","")

        response = contact.GetTypes()

        if "success" in response:
            types = response["success"]

        response = contact.Edit()

        if "success" in response:
            self.redirect("/customer/view_contact?user_id={}".format(contact.user_id))
        else:
            self.write(response["error"])
            