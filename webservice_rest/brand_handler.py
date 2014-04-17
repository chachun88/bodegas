#!/usr/bin/env python

from model10.brand import Brand

from base_handler import BaseHandler
from bson import json_util

class AddBrandHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		# isntantitate brand
		brand = Brand()

		brand.identifier 	= self.TryGetParam("id", "")
		brand.name 			= self.TryGetParam("name", "")
		
		# saving current brand
		oid = json_util.dumps(brand.Save())

		self.write(oid)


class RemoveBrandHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		name = self.get_argument("name", "")

		brand = Brand()

		if idd != "":
			brand.InitById(idd)
		else:
			brand.InitByName(name)

		self.write(json_util.dumps(brand.Remove()))


class GetBrandHandler(BaseHandler):
	def get(self):
		
		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		name = self.get_argument("name", "")

		brand = Brand()

		if idd != "":
			brand.InitById(idd)
		else:
			brand.InitByName(name)

		self.write(json_util.dumps(brand.Print()))

class LisBrandHandler(BaseHandler):
	def get(self):
		
		#validate access token
		if not self.ValidateToken():
			return
		
		current_page 	= "1"
		items_per_page 	= "10"
		brand 			= Brand()

		try:
			current_page 	= int(self.TryGetParam("page", "1"))
			items_per_page 	= int(self.TryGetParam("items", "10"))
		except Exception, e:
			print str(e)
		
		self.write(json_util.dumps(brand.GetList(current_page, items_per_page)))