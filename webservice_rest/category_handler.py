#!/usr/bin/env python

from model10.category import Category

from base_handler import BaseHandler
from bson import json_util

class AddCategoryHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		# isntantitate category
		category = Category()

		category.id 	= self.TryGetParam("id", "")
		category.name 			= self.TryGetParam("name", "")
		
		# saving current category
		oid = json_util.dumps(category.Save())

		self.write(oid)


class RemoveCategoryHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		name = self.get_argument("name", "")

		category = Category()

		if idd != "":
			category.InitById(idd)
		else:
			category.InitByName(name)

		self.write(json_util.dumps(category.Remove()))


class GetCategoryHandler(BaseHandler):
	def get(self):
		
		message = {}
		try:
			# validate access token
			if not self.ValidateToken():
				return

			idd = self.get_argument("id", "")
			name = self.get_argument("name", "")

			category = Category()

			if idd != "":
				message = category.InitById(idd)
			else:
				message = category.InitByName(name)

			self.write(json_util.dumps(category.Print()))
		except:
			self.write(json_util.dumps(message))

class LisCategoryHandler(BaseHandler):
	def get(self):
		
		#validate access token
		if not self.ValidateToken():
			return
		
		current_page 	= "1"
		items_per_page 	= "10"
		category 			= Category()

		try:
			current_page 	= int(self.TryGetParam("page", "1"))
			items_per_page 	= int(self.TryGetParam("items", "10"))
		except Exception, e:
			print str(e)
		
		self.write(json_util.dumps(category.GetList(current_page, items_per_page)))