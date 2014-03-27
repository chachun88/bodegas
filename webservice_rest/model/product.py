#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel

class Product(BaseModel):

	def __init__(self):
		self._codigo_proveedor  = ""
		self._codigo_interno	= ""
		self._nombre			= ""
		self._precio			= ""
		self._stock				= ""
		self._descuento			= ""
		self._estado			= ""
		self._marca				= ""
		self._familia			= ""
		self._descripcion		= ""

	def Save(self, collection):

		# validate codigo_proveedor and codigo_interno
		data = collection.find({"codigo_interno" : self.codigo_interno})
		if data.count() >= 1:

			collection.update(
				{"_id" : data[0]["_id"]},
				{"$set" : {
					"codigo_proveedor" 	: self.codigo_proveedor,
					"codigo_interno" 	: self.codigo_interno,
					"nombre"  			: self.nombre,
					"precio" 			: self.precio,
					"stock" 			: self.stock,
					"descuento" 		: self.descuento,
					"estado" 			: self.estado,
					"marca" 			: self.marca,
					"familia" 			: self.familia,
					"descripcion" 		: self.descripcion	
				}})

			return str(data[0]["_id"])

		#save the object and return the id
		object_id = collection.insert(
			{
			"codigo_proveedor" 	: self.codigo_proveedor,
			"codigo_interno" 	: self.codigo_interno,
			"nombre"  			: self.nombre,
			"precio" 			: self.precio,
			"stock" 			: self.stock,
			"descuento" 		: self.descuento,
			"estado" 			: self.estado,
			"marca" 			: self.marca,
			"familia" 			: self.familia,
			"descripcion" 		: self.descripcion
			})

		return str(object_id)

	@property
	def codigo_proveedor(self):
	    return self._codigo_proveedor
	@codigo_proveedor.setter
	def codigo_proveedor(self, value):
	    self._codigo_proveedor = value

	@property
	def codigo_interno(self):
	    return self._codigo_interno
	@codigo_interno.setter
	def codigo_interno(self, value):
	    self._codigo_interno = value	

	@property
	def nombre(self):
	    return self._nombre
	@nombre.setter
	def nombre(self, value):
	    self._nombre = value
	
	@property
	def precio(self):
	    return self._precio
	@precio.setter
	def precio(self, value):
	    self._precio = value

	@property
	def stock(self):
	    return self._stock
	@stock.setter
	def stock(self, value):
	    self._stock = value
	
	@property
	def descuento(self):
	    return self._descuento
	@descuento.setter
	def descuento(self, value):
	    self._descuento = value
	
	@property
	def estado(self):
	    return self._estado
	@estado.setter
	def estado(self, value):
	    self._estado = value

	@property
	def marca(self):
	    return self._marca
	@marca.setter
	def marca(self, value):
	    self._marca = value
	
	@property
	def familia(self):
	    return self._familia
	@familia.setter
	def familia(self, value):
	    self._familia = value
	
	@property
	def descripcion(self):
	    return self._descripcion
	@descripcion.setter
	def descripcion(self, value):
	    self._descripcion = value