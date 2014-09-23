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

class UserAddHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.USUARIOS_AGREGAR)

		usr = User()
		cellar = Cellar()

		self.render("user/add.html", side_menu=self.side_menu, user=usr, cellars=cellar.List(1,100))

	@tornado.web.authenticated
	def post(self):

		usr = User()

		usr.name 		= self.get_argument("name", "").encode("utf-8")
		usr.surname 	= self.get_argument("surname", "").encode("utf-8")
		usr.email 		= self.get_argument("email", "").encode("utf-8")
		usr.password 	= self.get_argument("password", "").encode("utf-8")
		usr.permissions = self.get_argument("permissions", "").encode("utf-8")
		usr.identifier	= self.get_argument("id", "").encode("utf-8")
		usr.cellars     = self.get_argument("cellars","").encode("utf-8")

		if usr.permissions == "":
			self.redirect("/user?dn=t3")
		else:
			response = json_util.loads(usr.Save())
			if "success" in response:
				self.redirect("/user?dn=t")
			else:
				self.write(response["error"])


class UserEditHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.USUARIOS_AGREGAR)
		
		usr = User()
		response = usr.InitWithId(self.get_argument("id", ""))

		if "success" in response:
			cellar = Cellar()

			self.render("user/add.html", side_menu=self.side_menu, user=usr, cellars=cellar.List(1,100))
		else:
			self.write(response["error"])

		