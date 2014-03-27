#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler

class CellarHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item
		self.render("cellar/home.html", side_menu=self.side_menu)