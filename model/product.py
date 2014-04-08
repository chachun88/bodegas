#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import urllib2

from basehandler import BaseHandler
from bson import json_util

from model.base_model import BaseModel

class Product(BaseModel):

#	def get_product_list(self):
#		return [{"name":"p1"},{"name":"p2"},{"name":"p3"}]

	def __init__(self):
		self._name=""
		self._price=""
		self._description=""
		self._quantity=""
		self._brand=""
		self._sku=""
		self._category=""
		self._identifier=""

	####################
	### Class fields ###
	####################		

	@property
	def name(self):
	    return self._name
	@name.setter
	def name(self, value):
	    self._name = value

	@property
	def price(self):
	    return self._price
	@price.setter
	def price(self, value):
	    self._price = value

	@property
	def description(self):
	    return self._description
	@description.setter
	def description(self, value):
	    self._description = value

	@property
	def quantity(self):
	    return self._quantity
	@quantity.setter
	def quantity(self, value):
	    self._quantity = value
	
	@property
	def brand(self):
	    return self._brand
	@brand.setter
	def brand(self, value):
	    self._brand = value

	@property
	def sku(self):
	    return self._sku
	@sku.setter
	def sku(self, value):
	    self._sku = value

	@property
	def category(self):
	    return self._category
	@category.setter
	def category(self, value):
	    self._category = value

	@property
	def identifier(self):
	    return self._identifier
	@identifier.setter
	def identifier(self, value):
	    self._identifier = value
	
	
	#################
	#### Methods ####
	#################

	def Remove(self):
		if self.identifier!="":
			url=self.wsurl() + "salesman/delete"
			url+="?token" + self.token()
			url+="&id" + self.identifier

			urllib.urlopen(url)

	def Save(self):
		url = self.wsurl()+"salesman/add?token=" + self.token()

		url += "&nombre=" + self.name
		url += "&precio=" + self.price
		url += "&descripcion=" + self.description
		url += "&cantidad=" + self.quantity
		url += "&marca=" + self.brand
		url += "&sku=" + self.sku
		url += "&categoria=" + self.category
		url += "&id=" + self.identifier

		return urllib.urlopen(url).read()

	def get_product_list(self):
			
		url = self.wsurl()+"salesman/list?token=" + self.token() + "&items=100"

		content = urllib2.urlopen(url).read()

		# parse content to array data
		data = json_util.loads(content)

		self.identifier = data

		return data



	
	
	
	
	