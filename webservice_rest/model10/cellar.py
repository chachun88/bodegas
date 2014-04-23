#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from bson.objectid import ObjectId

from kardex import Kardex

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

		data = db.kardex.find({"cellar_identifier":self.identifier})

		data = db.kardex.aggregate([
			{"$match":
				{"cellar_identifier":self.identifier}
			},{
			"$group":
			{"_id":{ "product_identifier":"$product_identifier"}}
			}])

		kardex = Kardex()

		total_units = 0

		for x in data["result"]:
			product = x["_id"]["product_identifier"]
			kardex.FindKardex(product, self.identifier)

			total_units = kardex.balance_units
		
		return int(total_units)

	def GetTotalPrice(self):
		data = db.kardex.find({"cellar_identifier":self.identifier})

		data = db.kardex.aggregate([
			{"$match":
				{"cellar_identifier":self.identifier}
			},{
			"$group":
			{"_id":{ "product_identifier":"$product_identifier"}}
			}])

		kardex = Kardex()

		total_price = 0

		for x in data["result"]:
			product = x["_id"]["product_identifier"]
			kardex.FindKardex(product, self.identifier)

			total_price = kardex.balance_total
		
		return int(total_price)

	#@return json
	def Print(self):
		try:
			me = {"_id":ObjectId(self.identifier),
				"name" : self.name,
				"description": self.description,
				"total_price": self.GetTotalPrice(),
				"total_units": self.GetTotalUnits()}

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

	def GetList(self, page, items):
		#validate inputs
		page = int(page)
		items = int(items)
		data = self.collection.find().skip((page-1)*items).limit(items)

		data_rtn = [] ## return this data

		for d in data:

			cellar = Cellar()
			cellar.identifier = str(d["_id"])
			cellar.name = d["name"]
			cellar.description = d["description"]

			data_rtn.append(cellar.Print())
		return data_rtn

	### WARNING: this method is not opmitimized
	#@return direct database collection
	@staticmethod
	def GetAllCellars():
		data = db.cellar.find()

		data_rtn = [] ## return this data

		for d in data:

			cellar = Cellar()
			cellar.identifier = str(d["_id"])
			cellar.name = d["name"]
			cellar.description = d["description"]

			data_rtn.append(cellar.Print())
		return data_rtn

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
