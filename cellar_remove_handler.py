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
	def get(self):

		idd = self.get_argument("id", "")

		cellar = Cellar()
		cellar.InitWithId(idd)

		json_string = cellar.Remove()
		json_data = json_util.loads( cellar.Remove() )

		if ( "error" in json_data ):
			self.write( json_data )
		else:
			self.write("{ \"message\" : \"Bodega eliminada correctamente.\"}")