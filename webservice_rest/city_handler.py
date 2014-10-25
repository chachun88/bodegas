#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util

from base_handler import BaseHandler
from model10.city import City

class SaveHandler(BaseHandler):

	def post(self):

		if not self.ValidateToken(): 
			return

		identifier = self.get_argument("identifier","")
		name = self.get_argument("name","")

		city = City()
		city.id = identifier
		city.name = name
		
		self.write(json_util.dumps(city.Save()))

class ListHandler(BaseHandler):

	def post(self):

		if not self.ValidateToken():
			return

		city = City()
		self.write(json_util.dumps(city.List()))

