#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from bson.objectid import ObjectId
from brand import Brand
from category import Category

class Product(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._sku = ''
		self._description = ''
		self._brand = ''
		self._manufacturer = ''
		self._size = ''
		self._color = ''
		self._material = ''
		self._bullet_point_1 = ''
		self._bullet_point_2 = ''
		self._bullet_point_3 = ''
		self._currency = '' 
		self._image = ''
		self._image_2 = ''
		self._image_3 = ''
		self._category = ''
		self._upc = ''

		self.collection = db.product

	@property
	def upc(self):
	    return self._upc
	@upc.setter
	def upc(self, value):
	    self._upc = value

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	@property
	def sku(self):
		return self._sku
	@sku.setter
	def sku(self, value):
		self._sku = value

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

	@property
	def category(self):
		return self._category
	@category.setter
	def category(self, value):
		self._category = value

	def GetCellars(self):
		return ''

	def Print(self):
		try:
			rtn_data = {
				"_id":ObjectId(self.identifier),
				"name":self.name,
				"description":self.description,
				"sku":self.sku,
				"brand":self.brand,
				"manufacturer":self.manufacturer,
				"size":self.size,
				"color":self.color,
				"material":self.material,
				"bullet_point_1":self.bullet_point_1,
				"bullet_point_2":self.bullet_point_2,
				"bullet_point_3":self.bullet_point_3,
				"image":self.image,
				"image_2":self.image_2,
				"image_3":self.image_3,
				"category":self.category,
				"upc":self.upc
			}

			return rtn_data
		except Exception, e:
			return self.ShowError("id: " + self.identifier + " not found")

	def Save(self):

		try:
			#if Category().Exist(self.category) == False and Brand().Exist(self.brand) == False:
			#	raise
			
			sku_count = self.collection.find({"sku":self.sku}).count()

			## solve when sku already exists
			if sku_count >= 1:
				self.collection.update({
						"sku":self.sku
						},{
						"$set":{
							"name":self.name,
							"description":self.description,
							"brand":self.brand,
							"manufacturer":self.manufacturer,
							"size":self.size,
							"color":self.color,
							"material":self.material,
							"bullet_point_1":self.bullet_point_1,
							"bullet_point_2":self.bullet_point_2,
							"bullet_point_3":self.bullet_point_3,
							"image":self.image,
							"image_2":self.image_2,
							"image_3":self.image_3,
							"category":self.category
							}
						})
				self.identifier = str(self.collection.find({"sku":self.sku})[0]["_id"])
			##solve when id is not empty
			elif self.identifier.strip() != "":
				self.collection.update({
						"_id":ObjectId(self.identifier)
					},{
					"$set":{
						"name":self.name,
						"description":self.description,
						"sku":self.sku,
						"brand":self.brand,
						"manufacturer":self.manufacturer,
						"size":self.size,
						"color":self.color,
						"material":self.material,
						"bullet_point_1":self.bullet_point_1,
						"bullet_point_2":self.bullet_point_2,
						"bullet_point_3":self.bullet_point_3,
						"image":self.image,
						"image_2":self.image_2,
						"image_3":self.image_3,
						"category":self.category
					}})
			##solve when the product does not exists
			else:
				self.identifier = str(self.collection.save({
						"name":self.name,
						"description":self.description,
						"sku":self.sku,
						"brand":self.brand,
						"manufacturer":self.manufacturer,
						"size":self.size,
						"color":self.color,
						"material":self.material,
						"bullet_point_1":self.bullet_point_1,
						"bullet_point_2":self.bullet_point_2,
						"bullet_point_3":self.bullet_point_3,
						"image":self.image,
						"image_2":self.image_2,
						"image_3":self.image_3,
						"category":self.category
					}))

			return self.ShowSuccessMessage("product correctly saved")
		except Exception, e:
			return self.ShowError("product could not be saved")

	def InitBySku(self, sku):
		data = self.collection.find({"sku":sku})

		if data.count() >= 1:
			self.identifier = str(data[0]["_id"])
			self.name = data[0]["name"]
			self.description = data[0]["description"]
			self.brand = data[0]["brand"]
			self.manufacturer = data[0]["manufacturer"]
			self.size = data[0]["size"]
			self.color = data[0]["color"]
			self.material = data[0]["color"]
			self.bullet_point_1 = data[0]["bullet_point_1"]
			self.bullet_point_2 = data[0]["bullet_point_2"]
			self.bullet_point_3 = data[0]["bullet_point_3"]
			self.image = data[0]["image"]
			self.image_2 = data[0]["image_2"]
			self.image_3 = data[0]["image_3"]
			self.category = data[0]["category"]
			self.sku = data[0]["sku"]

			return self.ShowSuccessMessage("product initialized")
		return self.ShowError("product can not be initialized")

	def InitById(self, identifier):
		data = self.collection.find({"_id":ObjectId(identifier)})

		if data.count() >= 1:
			self.identifier = str(data[0]["_id"])
			self.name = data[0]["name"]
			self.description = data[0]["description"]
			self.brand = data[0]["brand"]
			self.manufacturer = data[0]["manufacturer"]
			self.size = data[0]["size"]
			self.color = data[0]["color"]
			self.material = data[0]["color"]
			self.bullet_point_1 = data[0]["bullet_point_1"]
			self.bullet_point_2 = data[0]["bullet_point_2"]
			self.bullet_point_3 = data[0]["bullet_point_3"]
			self.image = data[0]["image"]
			self.image_2 = data[0]["image_2"]
			self.image_3 = data[0]["image_3"]
			self.category = data[0]["category"]
			self.sku = data[0]["sku"]

			return self.ShowSuccessMessage("product initialized")
		return self.ShowError("product can not be initialized")

	def Exist(self, name):
		if self.collection.find({"name":name}).count() >= 1:
			return True
		return False
