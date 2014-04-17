#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel

class OrderDetail(BaseModel):

	def __init__(self):
		self._header	= ""
		self._product 	= ""
		self._quantity	= ""
		self._discount = ""
		self._net 		= ""
		self._total 	= ""

	def Save(self, collection):
		#save the object and return the id
		object_id = collection.insert(
			{
			"header" 		: self.header,
			"product" 		: self.product,
			"quantity"  	: self.quantity,
			"discount" 	: self.discount,
			"net" 			: self.net,
			"total" 		: self.total
			})

		return str(object_id)

	def GetList(self, identifier, collection):
		data	= "[]"
		
		try:
			data	= str(json_util.dumps(collection.find({
				"header" : identifier
				})))
		except Exception, e:
			print str(e)

		return data


	@property
	def header(self):
	    return self._header
	@header.setter
	def header(self, value):
	    self._header = value
	
	@property
	def product(self):
	    return self._product
	@product.setter
	def product(self, value):
	    self._product = value
		
	@property
	def quantity(self):
	    return self._quantity
	@quantity.setter
	def quantity(self, value):
	    self._quantity = value
	
	@property
	def discount(self):
	    return self._discount
	@discount.setter
	def discount(self, value):
	    self._discount = value
	
	@property
	def total(self):
	    return self._total
	@total.setter
	def total(self, value):
	    self._total = value
	
	@property
	def net(self):
	    return self._net
	@net.setter
	def net(self, value):
	    self._net = value
	