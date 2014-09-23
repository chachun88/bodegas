#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

		salesman.id = self.get_argument("id", "")
		salesman.name 		= self.get_argument("name", "")
		salesman.password 	= self.get_argument("password", "")
		salesman.email		= self.get_argument("email", "")
		salesman.permissions = self.get_argument("permissions", "").split(",")
		salesman.cellars     = self.get_argument("cellars","").split(",")
		salesman.lastname    = self.get_argument("lastname","")

		# saving current seller
		response = salesman.Save()

		self.write(json_util.dumps(response))


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
			salesman.id = idd
		else:
			salesman.email = email

		self.write(json_util.dumps(salesman.Remove()))


class GetSalesmanHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		email = self.get_argument("email", "")

		salesman = Salesman()

		res = {}

		if idd == "":
			res = salesman.InitByEmail(email)
		else:
			res = salesman.InitById(idd)

		self.write(json_util.dumps(res, indent=2))


class ListSalesmanHandler(BaseHandler):
	def get(self):

		#validate access token
		if not self.ValidateToken():
			return
		
		current_page 	= "1"
		items_per_page 	= "10"
		salesman 		= Salesman()

		try:
			current_page 	= int(self.get_argument("page", "1"))
			items_per_page 	= int(self.get_argument("items", "10"))
		except Exception, e:
			print str(e)
		
		self.write(json_util.dumps(salesman.GetList(current_page, items_per_page)))