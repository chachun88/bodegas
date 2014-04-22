#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from bson.objectid import ObjectId

class Cellar(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._description = ''
		self.collection = db.cellar

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

	def GetTotalUnits(self):
		return ''

	def GetTotalPrice(self):
		return ''

	#@return json
	def Print(self):
		try:
			me = {"_id":ObjectId(self.identifier),
				"name" : self.name,
				"description": self.description}

			return me
		except:
			return self.ShowError("failed to print cellar")

	## validates and save cellar, it could be validated by name
	def Save(self):
		try:

			## validate if already exists a cellar with this name
			data_name = self.collection.find({"name": self.name})
			if data_name.count() >= 1:
				self.identifier = str(self.collection.update(
					{"_id":data_name[0]["_id"]},
					{"$set": {
						"name" : self.name,
						"description" : self.description
					}}))

				self.InitById(str(data_name[0]["_id"]))

				return self.ShowSuccessMessage(data_name[0]["_id"])

			##validate if the identifier exists
			if self.identifier == "":
				self.identifier = str(self.collection.insert({
					"name": self.name,
					"description": self.description
					}))

				self.InitById(self.identifier)

				return self.ShowSuccessMessage(self.identifier)

			data = self.collection.find({"_id":ObjectId(self.identifier)})

			if data.count() >= 1:
				self.identifier = str(self.collection.update(
					{"_id":data[0]["_id"]},
					{"$set": {
						"name" : self.name,
						"description" : self.description
					}}))
				self.InitById(self.identifier)

			return self.ShowSuccessMessage(str(object_id))
		except Exception, e:
			print str(e)
			return self.ShowError("failed to save cellar " + self.name)

	### WARNING: this method is not opmitimized
	#@return direct database collection
	@staticmethod
	def GetAllCellars():
		data = db.cellar.find()
		return data

	def InitById(self, idd):
		try:
			datas = self.collection.find({"_id": ObjectId(idd)})

			if datas >= 1:
				data = datas[0]
				self.identifier = str(data["_id"])
				self.name = data["name"]
				self.description = data["description"]

				return self.ShowSuccessMessage("cellar initialized")
			else:
				raise
		except:
			return self.ShowError("item not found")

	def ListProducts(self, page, items):
		pass

	def Rename(self, new_name):
		try:

			if new_name == "":
				raise

			self.collection.update({"_id":ObjectId(self.identifier)},
				{"$set":{
					"name":new_name
				}})
			self.name = new_name
			self.ShowSuccessMessage("name changed correctly")
		except:
			self.ShowError("error changing name")