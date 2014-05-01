#!/usr/bin/env python

from model10.color import Color

from base_handler import BaseHandler
from bson import json_util

class AddColorHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		# isntantitate color
		color = Color()

		color.identifier 	= self.TryGetParam("id", "")
		color.name 			= self.TryGetParam("name", "")
		color.idd			= self.TryGetParam("idd", "")
		
		# saving current color
		oid = json_util.dumps(color.Save())

		self.write(oid)


class RemoveColorHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		identifier = self.get_argument("id", "")
		name = self.get_argument("name", "")



		color = Color()

		if identifier != "":
			color.InitById(identifier)
		else:
			color.InitByName(name)

		self.write(json_util.dumps(color.Remove()))


class GetColorHandler(BaseHandler):
	def get(self):
		
		message = {}
		try:
			# validate access token
			if not self.ValidateToken():
				return

			identifier = self.get_argument("id", "")
			name = self.get_argument("name", "")

			color = Color()

			if identifier != "":
				message = color.InitById(identifier)
			else:
				message = color.InitByName(name)

			self.write(json_util.dumps(color.Print()))
		except:
			self.write(json_util.dumps(message))

class LisColorHandler(BaseHandler):
	def get(self):
		
		#validate access token
		if not self.ValidateToken():
			return
		
		current_page 	= "1"
		items_per_page 	= "10"
		color 			= Color()

		try:
			current_page 	= int(self.TryGetParam("page", "1"))
			items_per_page 	= int(self.TryGetParam("items", "10"))
		except Exception, e:
			print str(e)
		
		self.write(json_util.dumps(color.GetList(current_page, items_per_page)))