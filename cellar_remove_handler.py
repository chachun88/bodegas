#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from model.cellar import Cellar

from bson import json_util

class CellarRemoveHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):

		idd = self.get_argument("id", "")

		cellar = Cellar()
		cellar.InitWithId(idd)

		if cellar.name != "Bodega Central":

			json_string = cellar.Remove()
			json_data = json_util.loads( json_string )

			if ( "error" in json_data ):
				self.write( json_data )
			else:
				self.write("{ \"message\" : \"Bodega eliminada correctamente.\"}")

		else:

			self.write("{ \"error\" : \"Bodega central no puede ser eliminada.\"}")