#!/usr/bin/env python

from model10.salesman import Salesman

from base_handler import BaseHandler
from bson import json_util

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
		oid = salesman.Save()

		self.write(json_util.dumps(oid))


class RemoveSellerHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		email = self.get_argument("email", "")

		# instantiate Salesman
		salesman = Salesman()

		if idd != "":
			salesman.InitById(idd)
		else:
			salesman.InitByEmail(email)

		self.write(json_util.dumps(salesman.Remove()))


class GetSalesmanHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		idd = self.TryGetParam("id", "")
		email = self.TryGetParam("email", "")

		salesman = Salesman()

		if idd == "":
			salesman.InitByEmail(email)
		else:
			salesman.InitById(idd)

		self.write(json_util.dumps(salesman.Print()))


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
		
		self.write(json_util.dumps(salesman.GetList(current_page, items_per_page)))