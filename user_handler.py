#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from model.user import User

from globals import Menu


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.USUARIOS_LISTAR)

        usr = User()

        # detect if is comming from the add user form
        dn = self.get_argument("dn", "f")  # by default f for false
        self.render("user/home.html", 
                    side_menu=self.side_menu, 
                    user_list=usr.get_users_list(), 
                    dn=dn, 
                    current_user_email=self.get_current_user())


class UserRemoveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        usr = User()
        usr.InitWithId(self.get_argument("id", ""))
        usr.Remove()

        self.redirect("/user?dn=t2")
