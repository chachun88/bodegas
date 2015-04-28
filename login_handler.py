#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basehandler import BaseHandler
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from bson import json_util

import hashlib

from lp_email_tool import lpEmailTool

from model.user import User

class LoginHandler(BaseHandler):

	def get(self):
		self.clear_cookie("user_bodega")
		self.render("login.html", next=self.get_argument("next", "/"), error=self.get_argument("e", ""))

	def post(self):
		username = self.get_argument("user", "")
		password = self.get_argument("password", "")

		auth = False


		## validate user and password
		usr = User()
		response = usr.InitWithEmail(username)

		if "error" in response:
			self.redirect(u"/auth/login?e=" + response["error"])
			

		# print username
		# print password

		m = hashlib.md5()

		m.update(password)

		password = m.hexdigest()
		
		if username == usr.email and password == usr.password:
			auth = True

		if auth:
			self.set_secure_cookie("user_bodega",json_util.dumps(response["success"]))
			self.redirect(self.get_argument("next", u"/"))
		else:
			error_msg = tornado.escape.url_escape("t")
			self.redirect(u"/auth/login?e=" + error_msg)

class LoginPassHandler(BaseHandler):

	def get(self):

		email = self.get_argument("email", "")
		print email
		auth = False

		## validate user and password
		usr = User()
		usr.InitWithEmail(email)

		self.write(usr.password)

		## send email
		theEmail = lpEmailTool()

		theEmail.ffrom = "estefany@loadingplay.com"
		theEmail.password = "nunununu"
		theEmail.tto = email
		theEmail.subject = "un correo de prueba"
		theEmail.content = "Su contrasena es: "  + usr.password
		theEmail.content_type = lpEmailTool.PLAIN_TEXT

		theEmail.SendEmail()






