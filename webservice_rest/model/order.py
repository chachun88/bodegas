#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel


class Order(BaseModel):

	def __init__():
		self._salesman		= ""
		self._customer		= ""
		self._subtotal		= ""
		self._discount		= ""
		self._iva			= ""
		self._total 		= ""
		self._address		= ""
		self._town			= ""
		self._city			= ""

	def Save(self, collection):
		
		# validate contrains
		object_id = collection.insert({
			"salesman" : self.salesman,
			"customer" : self.customer,
			"subtotal" : self.subtotal,
			"discount" : self.discount,
			"iva" : self.iva,
			"total" : self.total,
			"address" : self.address,
			"town" : self.town,
			"city" : self.city 
			})

		return str(object_id)

	def Edit():
		# validate contrains

		# collection.update(
		# 		{"_id" : self.identifier},
		# 		{"$set" : {
		# 			"codigo_proveedor" : self.codigo_proveedor,
		# 			"codigo_interno" : self.codigo_interno,
		# 			"nombre"  : self.nombre,
		# 			"precio" : self.precio,
		# 			"stock" : self.stock,
		# 			"discount" : self.discount,
		# 			"estado" : self.estado,
		# 			"marca" : self.marca,
		# 			"familia" : self.familia,
		# 			"descripcion" : self.descripcion	
		# 		}})


		# return str(object_id)

		return self.identifier

	@property
	def salesman(self):
	    return self._salesman
	@salesman.setter
	def salesman(self, value):
	    self._salesman = value
		
	@property
	def customer(self):
	    return self._customer
	@customer.setter
	def customer(self, value):
	    self._customer = value
	
	@property
	def subtotal(self):
	    return self._subtotal
	@subtotal.setter
	def subtotal(self, value):
	    self._subtotal = value

	@property
	def discount(self):
	    return self._discount
	@discount.setter
	def discount(self, value):
	    self._discount = value
	
	@property
	def iva(self):
	    return self._iva
	@iva.setter
	def iva(self, value):
	    self._iva = value
	
	@property
	def total(self):
	    return self._total
	@total.setter
	def total(self, value):
	    self._total = value
	
	@property
	def address(self):
	    return self._address
	@address.setter
	def address(self, value):
	    self._address = value
	
	@property
	def town(self):
	    return self._town
	@town.setter
	def town(self, value):
	    self._town = value
	
	@property
	def city(self):
	    return self._city
	@city.setter
	def city(self, value):
	    self._city = value


	