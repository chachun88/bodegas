#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel


class Order(BaseModel):

	def __init__():
		self._vendedor		= ""
		self._cliente		= ""
		self._subtotal		= ""
		self._descuento		= ""
		self._iva			= ""
		self._total 		= ""
		self._direccion		= ""
		self._comuna		= ""
		self._ciudad		= ""

	def Save(self, collection):
		
		# validate contrains
		object_id = collection.insert({
			"vendedor" : self.vendedor,
			"cliente" : self.cliente,
			"subtotal" : self.subtotal,
			"descuento" : self.descuento,
			"iva" : self.iva,
			"total" : self.total,
			"direccion" : self.direccion,
			"comuna" : self.comuna,
			"ciudad" : self.ciudad 
			})

		return str(object_id)

	def Edit():
		# validate contrains
		collection.update(
				{"_id" : self.identifier},
				{"$set" : {
					"codigo_proveedor" : self.codigo_proveedor,
					"codigo_interno" : self.codigo_interno,
					"nombre"  : self.nombre,
					"precio" : self.precio,
					"stock" : self.stock,
					"descuento" : self.descuento,
					"estado" : self.estado,
					"marca" : self.marca,
					"familia" : self.familia,
					"descripcion" : self.descripcion	
				}})

		return str(object_id)

	@property
	def vendedor(self):
	    return self._vendedor
	@vendedor.setter
	def vendedor(self, value):
	    self._vendedor = value
		
	@property
	def cliente(self):
	    return self._cliente
	@cliente.setter
	def cliente(self, value):
	    self._cliente = value
	
	@property
	def subtotal(self):
	    return self._subtotal
	@subtotal.setter
	def subtotal(self, value):
	    self._subtotal = value
	

	@property
	def descuento(self):
	    return self._descuento
	@descuento.setter
	def descuento(self, value):
	    self._descuento = value
	
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
	def direccion(self):
	    return self._direccion
	@direccion.setter
	def direccion(self, value):
	    self._direccion = value
	
	@property
	def comuna(self):
	    return self._comuna
	@comuna.setter
	def comuna(self, value):
	    self._comuna = value
	
	@property
	def ciudad(self):
	    return self._ciudad
	@ciudad.setter
	def ciudad(self, value):
	    self._ciudad = value


	