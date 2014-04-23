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

class CellarAddHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_AGREGAR) #change menu active item
		self.render("cellar/add.html", side_menu=self.side_menu)

	def post(self):

		name = self.get_argument("name", "bodega sin nombre")
		description = self.get_argument("description", "")

		cellar = Cellar()
		cellar.name = name
		cellar.description = description

		cellar.Save()

		#self.write("llega")

		self.redirect("/cellar?dn=t")