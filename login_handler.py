#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basehandler import BaseHandler
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from model.user import User

class LoginHandler(BaseHandler):

	def get(self):
		self.clear_cookie("user")
		self.render("login.html", next=self.get_argument("next", "/"), error=self.get_argument("e", ""))

	def post(self):
		username = self.get_argument("user", "")
		password = self.get_argument("password", "")

		auth = False


		## validate user and password
		usr = User()
		usr.InitWithEmail(username)

		self.write(username)
		self.write(password)
		
		if username == usr.email and password == usr.password:
			auth = True

		if auth:
			self.set_current_user(username)
			self.redirect(self.get_argument("next", u"/"))
		else:
			error_msg = tornado.escape.url_escape("t")
			self.redirect(u"/auth/login?e=" + error_msg)
