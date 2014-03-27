#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import pymongo

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from basehandler import BaseHandler
from globals import port, debugMode, domainName, carpeta_img, userMode, Menu

from basehandler import BaseHandler

class ProductAddHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA) #change menu active item

		self.render("product/add.html", side_menu=self.side_menu)