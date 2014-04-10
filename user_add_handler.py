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

class UserAddHandler(BaseHandler):

	def get(self):
		self.set_active(Menu.USUARIOS_AGREGAR)

		usr = User()
		self.render("user/add.html", side_menu=self.side_menu, user=usr)

	def post(self):

		usr = User()
		
		usr.name 		= self.get_argument("name", "")
		usr.surname 	= self.get_argument("surname", "")
		usr.email 		= self.get_argument("email", "")
		usr.password 	= self.get_argument("password", "")
		usr.permissions = self.get_argument("permissions", "")
		usr.identifier	= self.get_argument("id", "")

		usr.Save()
		self.redirect("/user?dn=t")


class UserEditHandler(BaseHandler):

	def get(self):
		self.set_active(Menu.USUARIOS_AGREGAR)
		
		usr = User()
		usr.InitWithId(self.get_argument("id", ""))

		self.render("user/add.html", side_menu=self.side_menu, user=usr)

		