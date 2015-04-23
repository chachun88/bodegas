#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from globals import Menu
from model.user import User
from model.cellar import Cellar

from bson import json_util

import hashlib


class UserAddHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.USUARIOS_AGREGAR)

        usr = User()
        cellar = Cellar()
        user_id = self.get_argument("id", "")
        dn = self.get_argument("dn", "")

        if user_id != "":

            response = usr.InitWithId(user_id)

            if "success" in response:
                self.render("user/add.html", 
                    side_menu=self.side_menu, 
                    user=usr, 
                    cellars=cellar.List(1,100), 
                    dn=dn,
                    warnings="")
            else:
                self.write(response["error"])

        else:

            self.render("user/add.html", 
                side_menu=self.side_menu, 
                user=usr, 
                cellars=cellar.List(1,100), 
                dn=dn,
                warnings="")

    @tornado.web.authenticated
    def post(self):

        usr = User()

        user_id = self.get_argument("id", "")

        if user_id != "":

            response = usr.InitWithId(user_id)

            if "error" in response:
                self.redirect("/user/add?dn=&warnings=" + response["error"])

        form_password = self.get_argument("password", "").encode("utf-8")
        usr.name  = self.get_argument("name", "").encode("utf-8")
        usr.surname = self.get_argument("surname", "").encode("utf-8")
        usr.email = self.get_argument("email", "").encode("utf-8")

        if usr.password != form_password:

            m = hashlib.md5()
            m.update(form_password)
            password = m.hexdigest()
            usr.password    = password

        usr.type_id = self.get_argument("type_id", "")
        usr.identifier  = self.get_argument("id", "").encode("utf-8")
        usr.cellars     = self.get_argument("cellars","").encode("utf-8")

        response = json_util.loads(usr.Save())

        if "success" in response:
            self.redirect("/user/add?dn=t&warnings=")
        else:
            self.redirect("/user/add?dn=warnings=" + response["error"])
