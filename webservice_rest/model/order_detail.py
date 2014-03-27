#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel

class OrderDetail(BaseModel):

	def __init__(self):
		self._cabecera	= ""
		self._producto 	= ""
		self._cantidad	= ""
		self._descuento = ""
		self._neto 		= ""
		self._total 	= ""

	def Save(self, collection):
		#save the object and return the id
		object_id = collection.insert(
			{
			"cabecera" 		: self.cabecera,
			"producto" 		: self.producto,
			"cantidad"  	: self.cantidad,
			"descuento" 	: self.descuento,
			"neto" 			: self.neto,
			"total" 		: self.total
			})

		return str(object_id)

	def GetList(self, identifier, collection):
		data	= "[]"
		
		try:
			data	= str(json_util.dumps(collection.find({
				"cabecera" : identifier
				})))
		except Exception, e:
			print str(e)

		return data


	@property
	def cabecera(self):
	    return self._cabecera
	@cabecera.setter
	def cabecera(self, value):
	    self._cabecera = value
	
	@property
	def producto(self):
	    return self._producto
	@producto.setter
	def producto(self, value):
	    self._producto = value
		
	@property
	def cantidad(self):
	    return self._cantidad
	@cantidad.setter
	def cantidad(self, value):
	    self._cantidad = value
	
	@property
	def descuento(self):
	    return self._descuento
	@descuento.setter
	def descuento(self, value):
	    self._descuento = value
	
	@property
	def total(self):
	    return self._total
	@total.setter
	def total(self, value):
	    self._total = value
	
	@property
	def neto(self):
	    return self._neto
	@neto.setter
	def neto(self, value):
	    self._neto = value
	