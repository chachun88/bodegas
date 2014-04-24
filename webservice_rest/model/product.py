#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel

class Product(BaseModel):

	def __init__(self):
		self._sku			= ""
		self._name 			= ""
		self._description 	= ""
		self._brand 		= ""
		self._manufacturer 	= ""
		self._size			= ""
		self._color 		= ""
		self._material		= ""
		self._bullet_point_1= ""
		self._bullet_point_2= ""
		self._bullet_point_3= ""
		self._price 		= ""
		self._currency 		= ""
		self._image 		= ""
		self._image_2 		= ""
		self._image_3 		= ""

	def Save(self, collection):

		# validate codigo_proveedor and codigo_interno
		data = collection.find({"sku" : self.sku})
		if data.count() >= 1:

			collection.update(
				{"_id" : data[0]["_id"]},
				{"$set" : {
					"sku" 				: self.sku,
					"name"  			: self.name,
					"upc"				: self.upc,
					"description" 		: self.description,
					"brand"				: self.brand,
					"manufacturer" 		: self.manufacturer,
					"size" 				: self.size,
					"color" 			: self.color,
					"material" 			: self.material,
					"bullet_point_1"	: self.bullet_point_1,
					"bullet_point_2" 	: self.bullet_point_2,
					"bullet_point_3"	: self.bullet_point_3,
					"price"				: self.price,
					"currency" 			: self.currency,
					"image"				: self.image,
					"image_2" 			: self.image_2,
					"image_3" 			: self.image_3
				}})

			return str(data[0]["_id"])

		#save the object and return the id
		object_id = collection.insert(
			{
				"sku" 				: self.sku,
				"name"  			: self.name,
				"upc"				: self.upc,
				"description" 		: self.description,
				"brand"				: self.brand,
				"manufacturer" 		: self.manufacturer,
				"size" 				: self.size,
				"color" 			: self.color,
				"material" 			: self.material,
				"bullet_point_1"	: self.bullet_point_1,
				"bullet_point_2" 	: self.bullet_point_2,
				"bullet_point_3"	: self.bullet_point_3,
				"price"				: self.price,
				"currency" 			: self.currency,
				"image"				: self.image,
				"image_2" 			: self.image_2,
				"image_3" 			: self.image_3
			})

		return str(object_id)

	def Search(self, query):
		return self.collection.find({"name":"/"+query+"/i"})

	@property
	def sku(self):
	    return self._sku
	@sku.setter
	def sku(self, value):
	    self._sku = value
	
	@property
	def name(self):
	    return self._name
	@name.setter
	def name(self, value):
	    self._name = value
	
	@property
	def upc(self):
	    return self._upc
	@upc.setter
	def upc(self, value):
	    self._upc = value
	
	@property
	def description(self):
	    return self._description
	@description.setter
	def description(self, value):
	    self._description = value
	
	@property
	def brand(self):
	    return self._brand
	@brand.setter
	def brand(self, value):
	    self._brand = value
	
	@property
	def manufacturer(self):
	    return self._manufacturer
	@manufacturer.setter
	def manufacturer(self, value):
	    self._manufacturer = value
	
	@property
	def size(self):
	    return self._size
	@size.setter
	def size(self, value):
	    self._size = value
	
	@property
	def color(self):
	    return self._color
	@color.setter
	def color(self, value):
	    self._color = value
	
	@property
	def material(self):
	    return self._material
	@material.setter
	def material(self, value):
	    self._material = value
	
	@property
	def bullet_point_1(self):
	    return self._bullet_point_1
	@bullet_point_1.setter
	def bullet_point_1(self, value):
	    self._bullet_point_1 = value
	
	@property
	def bullet_point_2(self):
	    return self._bullet_point_2
	@bullet_point_2.setter
	def bullet_point_2(self, value):
	    self._bullet_point_2 = value
	
	@property
	def bullet_point_3(self):
	    return self._bullet_point_3
	@bullet_point_3.setter
	def bullet_point_3(self, value):
	    self._bullet_point_3 = value
	
	@property
	def price(self):
	    return self._price
	@price.setter
	def price(self, value):
	    self._price = value
	
	@property
	def currency(self):
	    return self._currency
	@currency.setter
	def currency(self, value):
	    self._currency = value
	
	@property
	def image(self):
	    return self._image
	@image.setter
	def image(self, value):
	    self._image = value
	
	@property
	def image_2(self):
	    return self._image_2
	@image_2.setter
	def image_2(self, value):
	    self._image_2 = value
	
	@property
	def image_3(self):
	    return self._image_3
	@image_3.setter
	def image_3(self, value):
	    self._image_3 = value
