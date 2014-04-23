#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler
from model.cellar import Cellar

class CellarHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		data = Cellar().List(1, 10)
		self.render("cellar/home.html", side_menu=self.side_menu, data=data, dn=self.get_argument("dn", ""))