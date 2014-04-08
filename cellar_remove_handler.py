#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from model.cellar import Cellar

class CellarRemoveHandler(BaseHandler):
	def get(self):

		idd = self.get_argument("id", "")

		cellar = Cellar()
		cellar.InitWithId(idd)

		cellar.Remove()
		self.write("Bodega eliminada correctamente.")