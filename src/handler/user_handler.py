#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from ..model10.user import User

from ..globals import Menu


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.USUARIOS_LISTAR)

        pjax = bool(self.get_argument("_pjax", False))

        usr = User()

        # detect if is comming from the add user form
        dn = self.get_argument("dn", "f")  # by default f for false

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'
        self.render("user{}/home.html".format(pjax_str), 
                    side_menu=self.side_menu, 
                    user_list=usr.GetList(), 
                    dn=dn, 
                    current_user_email=self.get_current_user())


class UserRemoveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        usr = User()
        usr.id = self.get_argument("id", "")
        res = usr.Remove()

        print res

        if "success" in res:
            self.redirect("/user?dn=t2")
        else:
            self.redirect("/user?dn=t4")
