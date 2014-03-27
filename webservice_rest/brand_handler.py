#!/usr/bin/env python

from model.brand import Brand

from base_handler import BaseHandler

class AddBrandHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		# isntantitate brand
		brand = Brand()

		brand.identifier 	= self.TryGetParam("id", "")
		brand.nombre 		= self.TryGetParam("nombre", "")
		
		# saving current brand
		oid = brand.Save(self.db.brands)

		self.write(oid)


class RemoveBrandHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		brand = Brand()
		brand.RemoveById(self.TryGetParam("id", ""), self.db.brands)

class GetBrandHandler(BaseHandler):
	def get(self):
		
		# validate access token
		if not self.ValidateToken():
			return

		brand = Brand()
		self.write(brand.FindById(self.TryGetParam("id", ""), self.db.brands))

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
		
		self.write(brand.GetList(current_page, items_per_page, self.db.brands))