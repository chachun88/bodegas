#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from globals import Menu

class UserAddHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.USUARIOS_AGREGAR)
		self.render("user/add.html", side_menu=self.side_menu)