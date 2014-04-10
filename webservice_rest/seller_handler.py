#!/usr/bin/env python

from model.salesman import Salesman

from base_handler import BaseHandler

class AddSellerHandler(BaseHandler):
	def get(self):
				
		# validate access token
		if not self.ValidateToken():
			return

		# isntantitate product
		salesman = Salesman()

		salesman.identifier = self.TryGetParam("id", "")
		salesman.name 		= self.TryGetParam("name", "")
		salesman.password 	= self.TryGetParam("password", "")
		salesman.email		= self.TryGetParam("email", "")

		# saving current seller
		oid = salesman.Save(self.db.salesman)

		self.write(oid)


class RemoveSellerHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return
		
		# instantiate Salesman
		salesman = Salesman()

		salesman.RemoveById(self.TryGetParam("id", ""), self.db.salesman)


class GetSalesmanHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		idd = self.TryGetParam("id", "")
		email = self.TryGetParam("email", "")

		if idd == "":
			salesman = Salesman()
			self.write(salesman.FindByEmail(email, self.db.salesman))
		else:
			salesman = Salesman()
			self.write(salesman.FindById(idd, self.db.salesman))


class ListSalesmanHandler(BaseHandler):
	def get(self):

		#validate access token
		if not self.ValidateToken():
			return
		
		current_page 	= "1"
		items_per_page 	= "10"
		salesman 		= Salesman()

		try:
			current_page 	= int(self.TryGetParam("page", "1"))
			items_per_page 	= int(self.TryGetParam("items", "10"))
		except Exception, e:
			print str(e)
		
		self.write(salesman.GetList(current_page, items_per_page, self.db.salesman))