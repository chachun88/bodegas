#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util

class Cellar(BaseModel):

	""" docstring for Cellar """
	def __init__(self):
		self._name = ""
		self._description = ""
		self._identifier = ""
		pass

	def Save(self):
		url = self.wsurl() + "/cellar/add"
		url += "?token=" + self.token()
		url += "&name=" + self.name
		url += "&description=" + self.description

		return urllib.urlopen(url).read()

	def Remove(self):
		url = self.wsurl() + "/cellar/remove"
		url += "?token=" + self.token()
		url += "&id=" + self.identifier

		print url

		return urllib.urlopen(url).read()

	def ListProducts(self):

		url = self.wsurl() + "/cellar/products/list"

		url += "?token=" + self.token()
		url += "&id=" + self.identifier
		url += "&page=1"
		url += "&items=100"

		json_string = urllib.urlopen(url).read()
		return json_util.loads(json_string)

	def ListKardex(self, day, fromm, until):

		url = self.wsurl() + "/cellar/products/kardex"

		url += "?token=" + self.token()
		url += "&page=1"
		url += "&items=1"
		url += "&day="+ day
		url += "&from="+ fromm
		url += "&until="+ until

		json_string = urllib.urlopen(url).read()
		return json_util.loads(json_string)	

	def InitWithId(self, idd):
		url = self.wsurl() + "/cellar/find"
		url += "?token=" + self.token()
		url += "&id=" + idd

		json_string = urllib.urlopen(url).read()
		json_data = json_util.loads(json_string)

		print "{}".format(json_string)

		self.identifier = str(json_data["_id"])
		self.name = json_data["name"]
		self.description = json_data["description"]

	def InitWithName(self, name):
		url = self.wsurl() + "/cellar/find"
		url += "?token=" + self.token()
		url += "&name=" + name

		json_string = urllib.urlopen(url).read()
		json_data = json_util.loads(json_string)

		self.identifier = str(json_data["_id"])
		self.name = json_data["name"]
		self.description = json_data["description"]		

	def List(self, page, items):
		url = self.wsurl() + "/cellar/list"
		url += "?token=" + self.token()
		url += "&page={}".format(page)
		url += "&items={}".format(items)

		json_string = urllib.urlopen(url).read()
		return json_util.loads(json_string)
	
	def AddProducts(self, product_sku, quantity, price, size, color, operation, user):
		
		col=""
		
		try:
			col = col.encode('utf-8')
		except:
			col = color

		url = self.wsurl() + "/cellar/products/add?token=" + self.token()
		url += "&cellar_id=" + self.identifier
		url += "&product_sku=" + product_sku 
		url += "&operation=buy"
		url += "&quantity=" + quantity
		url += "&price=" + price
		url += "&size=" + size
		url += "&color=" + col
		url += "&user=" + user

		json_string = urllib.urlopen(url).read()

		return json_util.loads(json_string)

	def RemoveProducts(self, product_sku, quantity, price, size, color, operation, user):
		url = self.wsurl() + "/cellar/products/remove?token=" + self.token()

		url += "&cellar_id=" + self.identifier
		url += "&product_sku=" + product_sku
		url += "&operation=sell"
		url += "&quantity=" + quantity
		url += "&price=" + price
		url += "&size=" + size
		url += "&color=" + color
		url += "&user=" + user

		json_string = urllib.urlopen(url).read()

		print json_string

		return json_util.loads(json_string)

	def CellarExist( self, cellar_name ):
		url = self.wsurl() + "/cellar/exists?token=" + self.token()

		url += "&cellar_name" + cellar_name

		json_string = urllib.urlopen( url ).read()
		return json_util.loads( json_string )[ "exists" ]
 
	@property
	def name(self):
	    return self._name
	@name.setter
	def name(self, value):
	    self._name = value
	
	@property
	def description(self):
	    return self._description
	@description.setter
	def description(self, value):
	    self._description = value
	
	@property
	def identifier(self):
	    return self._identifier
	@identifier.setter
	def identifier(self, value):
	    self._identifier = value
	