#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from bson.objectid import ObjectId

class Brand(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''

		self.collection = db.brand

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	def Print(self):
		return {"name":self.name,
				"_id":ObjectId(self.identifier)}

	def InitByName(self, name):
		try:
			brands = self.collection.find({"name":name})

			if brands.count() >= 1: 
				self.name = brands[0]["name"]
				self.identifier = str(brands[0]["_id"])
			return self.ShowSuccessMessage("brand correctly initialized")
		except:
			return self.ShowError("brand can not be initialized")

	def InitById(self, idd):
		try:
			brands = self.collection.find({"_id":ObjectId(idd)})

			if brands.count() >= 1: 
				self.name = brands[0]["name"]
				self.identifier = str(brands[0]["_id"])
			return self.ShowSuccessMessage("brand correctly initialized")
		except:
			return self.ShowError("brand can not be initialized")

	def Save(self):
		try:
			data = self.collection.find({"name":self.name})
			if data.count() >= 1:
				self.collection.update({
					"name":self.name
					},{
					"$set":{
						"name" : self.name,
						}
					})
				self.identifier = str(data[0]["_id"])

			else:
				self.collection.save({
					"name":self.name
					})

				data = self.collection.find({"name":self.name})
				self.identifier = str(data[0]["_id"])

			return self.ShowSuccessMessage("brans saved correctly")
		except:
			return self.ShowError("error saving brand")


	def GetAllBrands(self):
		return self.collection.find()

	def Exist(self, name):
		if self.collection.find({"name":name}).count() >= 1:
			return True
		return False