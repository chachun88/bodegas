#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from globals import Menu

class ReportHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.INFORMES_POR_BODEGA)
		self.render("report/home.html", side_menu=self.side_menu)