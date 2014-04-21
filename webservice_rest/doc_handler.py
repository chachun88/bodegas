#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from base_handler import BaseHandler

class DocHandler(BaseHandler):
	def get(self):
		self.render("base.html")